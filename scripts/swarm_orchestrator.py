#!/usr/bin/env python3
"""Dynamic local CLI swarm harness for Master_Slave_Skill."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

HIVE_DIR = Path(".hive")
REGISTRY_FILE = HIVE_DIR / "cli_registry.json"
STATE_FILE = HIVE_DIR / "state.json"
DAG_FILE = HIVE_DIR / "dag.json"
RUNS_DIR = HIVE_DIR / "runs"

CANDIDATE_COMMANDS = [
    "claude",
    "copilot",
    "antigravity",
    "gemini",
    "opencode",
    "cline",
    "klein",
    "freebuff",
    "codex",
    "aider",
]

PROMPT_FLAG_PATTERNS = [
    (re.compile(r"(^|\s)-p([,\s=]|$)", re.I), "-p"),
    (re.compile(r"--prompt\b", re.I), "--prompt"),
    (re.compile(r"--message\b", re.I), "--message"),
    (re.compile(r"--query\b", re.I), "--query"),
    (re.compile(r"--exec\b", re.I), "--exec"),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def init_hive() -> None:
    HIVE_DIR.mkdir(exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        write_json(STATE_FILE, {"status": "initialized", "updated_at": now_iso(), "runs": []})


def read_json(path: Path, default):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def run_probe(argv: list[str], timeout: int = 8) -> dict:
    try:
        result = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return {
            "ok": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except Exception as exc:
        return {"ok": False, "exit_code": None, "stdout": "", "stderr": str(exc)}


def detect_prompt_mode(help_text: str) -> tuple[str | None, list[str] | None]:
    for pattern, flag in PROMPT_FLAG_PATTERNS:
        if pattern.search(help_text):
            return "argument", ["{executable}", flag, "{prompt}"]
    return None, None


def discover_workers(extra_commands: list[str] | None = None) -> list[dict]:
    """Discover candidate AI CLIs and infer only documented prompt syntax."""
    init_hive()
    commands = []
    for command in CANDIDATE_COMMANDS + (extra_commands or []):
        if command and command not in commands:
            commands.append(command)

    previous = {w.get("name"): w for w in read_json(REGISTRY_FILE, {}).get("workers", [])}
    workers = []

    for command in commands:
        path = shutil.which(command)
        if not path:
            continue

        version = run_probe([path, "--version"])
        help_result = run_probe([path, "--help"])
        help_text = "\n".join(x for x in [help_result.get("stdout", ""), help_result.get("stderr", "")] if x)
        mode, template = detect_prompt_mode(help_text)

        existing = previous.get(command, {})
        if not template and existing.get("argv_template"):
            template = existing["argv_template"]
            mode = existing.get("prompt_mode")

        workers.append(
            {
                "name": command,
                "executable": path,
                "available": True,
                "version": version.get("stdout") or version.get("stderr") or None,
                "prompt_mode": mode,
                "argv_template": template,
                "syntax_status": "ready" if template else "needs_adapter",
                "discovered_at": now_iso(),
            }
        )

    registry = {"updated_at": now_iso(), "workers": workers}
    write_json(REGISTRY_FILE, registry)
    return workers


def load_workers(ready_only: bool = False) -> list[dict]:
    workers = read_json(REGISTRY_FILE, {}).get("workers", [])
    if ready_only:
        workers = [w for w in workers if w.get("available") and w.get("argv_template")]
    return workers


def register_worker(adapter_path: str) -> dict:
    """Merge one explicit JSON adapter into the local registry."""
    init_hive()
    adapter = read_json(Path(adapter_path), None)
    if not isinstance(adapter, dict):
        raise ValueError("Adapter must be a JSON object")
    for key in ("name", "argv_template"):
        if key not in adapter:
            raise ValueError(f"Adapter missing required field: {key}")
    if not isinstance(adapter["argv_template"], list) or not adapter["argv_template"]:
        raise ValueError("argv_template must be a non-empty JSON array")

    workers = load_workers()
    workers = [w for w in workers if w.get("name") != adapter["name"]]
    executable = adapter.get("executable") or adapter["argv_template"][0]
    resolved = shutil.which(executable) or executable
    adapter.update(
        {
            "executable": resolved,
            "available": bool(shutil.which(executable) or Path(str(executable)).exists()),
            "syntax_status": "ready",
            "registered_at": now_iso(),
        }
    )
    workers.append(adapter)
    write_json(REGISTRY_FILE, {"updated_at": now_iso(), "workers": workers})
    return adapter


def build_worker_prompt(master_task: str, worker_name: str, role: str = "independent reviewer") -> str:
    return f"""MASTER TASK
{master_task}

WORKER ROLE
{role}

INSTRUCTIONS
- Work only on the task above.
- Inspect the current working directory as needed.
- Do not make unrelated changes.
- If you are acting as a reviewer, do not modify files.
- Return concrete findings, recommended changes, and verification commands.
- State uncertainties instead of inventing facts.

EXPECTED OUTPUT
A concise implementation/review report that the Master agent can evaluate and integrate.

WORKER
{worker_name}
"""


def materialize_argv(worker: dict, prompt: str) -> tuple[list[str], str | None]:
    template = worker.get("argv_template")
    if not template:
        raise ValueError(f"Worker {worker.get('name')} has no registered invocation adapter")

    executable = worker.get("executable") or template[0]
    argv = []
    uses_prompt_arg = False
    for token in template:
        token = str(token)
        if token == "{executable}":
            argv.append(str(executable))
        elif token == "{prompt}":
            argv.append(prompt)
            uses_prompt_arg = True
        else:
            argv.append(token.replace("{executable}", str(executable)).replace("{prompt}", prompt))
            if "{prompt}" in token:
                uses_prompt_arg = True

    stdin_text = None if uses_prompt_arg else prompt if worker.get("prompt_mode") == "stdin" else None
    return argv, stdin_text


def run_worker(worker: dict, task: str, cwd: str, timeout: int, run_dir: Path, role: str) -> dict:
    prompt = build_worker_prompt(task, worker["name"], role=role)
    started = now_iso()
    receipt = {
        "worker": worker["name"],
        "role": role,
        "started_at": started,
        "cwd": str(Path(cwd).resolve()),
        "prompt": prompt,
        "status": "failed",
    }

    try:
        argv, stdin_text = materialize_argv(worker, prompt)
        receipt["argv"] = argv
        result = subprocess.run(
            argv,
            cwd=cwd,
            input=stdin_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        receipt.update(
            {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "status": "completed" if result.returncode == 0 else "failed",
            }
        )
    except subprocess.TimeoutExpired as exc:
        receipt.update(
            {
                "exit_code": None,
                "stdout": exc.stdout or "",
                "stderr": exc.stderr or "",
                "status": "timeout",
            }
        )
    except Exception as exc:
        receipt.update({"exit_code": None, "stdout": "", "stderr": str(exc), "status": "failed"})

    receipt["finished_at"] = now_iso()
    write_json(run_dir / f"{worker['name']}.json", receipt)
    return receipt


def generate_task_dag(task: str, workers: list[dict]) -> dict:
    """Create a generic plan using the actual ready worker fleet."""
    init_hive()
    nodes = []
    roles = ["architecture reviewer", "implementation reviewer", "test and verification reviewer", "security and edge-case reviewer"]
    for index, worker in enumerate(workers):
        nodes.append(
            {
                "id": f"node-{index + 1}",
                "worker": worker["name"],
                "role": roles[index % len(roles)],
                "mode": "read-only review",
                "dependencies": [],
            }
        )
    dag = {"task": task, "created_at": now_iso(), "nodes": nodes}
    write_json(DAG_FILE, dag)
    return dag


def run_swarm(task: str, cwd: str, timeout: int, all_workers: bool, max_workers: int) -> dict:
    init_hive()
    workers = load_workers(ready_only=True)
    if not workers:
        workers = [w for w in discover_workers() if w.get("argv_template")]
    if not workers:
        raise RuntimeError("No runnable worker adapters found. Run --discover, then register adapters for CLIs marked needs_adapter.")

    selected = workers if all_workers else workers[: min(len(workers), max_workers)]
    dag = generate_task_dag(task, selected)
    run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    receipts = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(max_workers, len(selected))) as pool:
        futures = []
        for node in dag["nodes"]:
            worker = next(w for w in selected if w["name"] == node["worker"])
            futures.append(pool.submit(run_worker, worker, task, cwd, timeout, run_dir, node["role"]))
        for future in concurrent.futures.as_completed(futures):
            receipts.append(future.result())

    summary = {
        "run_id": run_id,
        "task": task,
        "cwd": str(Path(cwd).resolve()),
        "workers_requested": [w["name"] for w in selected],
        "completed": [r["worker"] for r in receipts if r["status"] == "completed"],
        "failed": [r["worker"] for r in receipts if r["status"] != "completed"],
        "receipts": [str(run_dir / f"{r['worker']}.json") for r in receipts],
        "finished_at": now_iso(),
    }
    write_json(run_dir / "summary.json", summary)

    state = read_json(STATE_FILE, {"runs": []})
    state.setdefault("runs", []).append(summary)
    state["updated_at"] = now_iso()
    state["status"] = "completed"
    write_json(STATE_FILE, state)
    return summary


def print_workers(workers: list[dict]) -> None:
    if not workers:
        print("No workers discovered. Run --discover.")
        return
    for worker in workers:
        print(
            f"{worker.get('name')}: {worker.get('syntax_status', 'unknown')} | "
            f"{worker.get('executable')} | {worker.get('version') or 'version unknown'}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Dynamic local AI CLI swarm harness")
    parser.add_argument("--discover", action="store_true", help="Discover installed AI CLIs and update .hive/cli_registry.json")
    parser.add_argument("--extra-cli", action="append", default=[], help="Additional executable name to include during discovery")
    parser.add_argument("--list-workers", action="store_true", help="Show the local worker registry")
    parser.add_argument("--register-worker", type=str, help="Register/replace a worker using a JSON adapter file")
    parser.add_argument("--task", type=str, help="Master task to decompose or execute")
    parser.add_argument("--run", action="store_true", help="Execute compatible workers for --task")
    parser.add_argument("--all-workers", action="store_true", help="Use every runnable discovered worker")
    parser.add_argument("--cwd", default=".", help="Working directory given to worker processes")
    parser.add_argument("--timeout", type=int, default=600, help="Per-worker timeout in seconds")
    parser.add_argument("--max-workers", type=int, default=4, help="Maximum concurrent worker processes")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if args.discover:
        workers = discover_workers(args.extra_cli)
        print_workers(workers)
        return 0

    if args.register_worker:
        adapter = register_worker(args.register_worker)
        print(f"Registered {adapter['name']}")
        return 0

    if args.list_workers:
        print_workers(load_workers())
        return 0

    if args.task and args.run:
        summary = run_swarm(args.task, args.cwd, args.timeout, args.all_workers, args.max_workers)
        print(json.dumps(summary, indent=2))
        return 0

    if args.task:
        workers = load_workers(ready_only=True)
        dag = generate_task_dag(args.task, workers)
        print(json.dumps(dag, indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
