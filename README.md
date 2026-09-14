# Master_Slave_Skill

> Dynamic local multi-agent orchestration for AI coding CLIs.

## What Changed

The active coding agent is the **Master**. Instead of assuming only three fixed tools, it discovers the AI CLIs actually installed on the machine, inspects their local invocation syntax, routes work to compatible workers, launches them through the shell, captures their outputs, and synthesizes the final result.

The fleet can include tools such as:

```text
Claude Code
GitHub Copilot CLI
Antigravity
Gemini CLI
OpenCode
Cline / Klein-compatible CLIs
Freebuff-compatible CLIs
Codex CLI
Aider
other installed AI CLIs
```

The names above are discovery candidates, not guaranteed dependencies.

---

## Why This Version Is Different

The original script could check whether a few CLIs existed and generate a fixed DAG, but it did not actually execute workers.

The current harness adds:

- dynamic CLI discovery from `PATH`
- local `--version` / `--help` inspection
- non-interactive prompt-mode detection when documented
- configurable worker adapters
- dynamic worker registry in `.hive/cli_registry.json`
- actual subprocess execution of worker CLIs
- parallel read-only worker reviews
- captured stdout, stderr, exit code, prompt, timestamps, and command argv
- run receipts under `.hive/runs/`
- failover-friendly worker selection
- master-side synthesis and final verification rules
- no dependency on historical hard-coded model names
- safer permission handling instead of blindly bypassing every confirmation

---

## Architecture

```text
User task
   ↓
Master coding agent
   ↓
Discover local AI CLIs
   ↓
Inspect CLI help/version
   ↓
Build .hive/cli_registry.json
   ↓
Decompose task
   ↓
┌────────────┬────────────┬────────────┬────────────┐
│ Worker CLI │ Worker CLI │ Worker CLI │ Worker CLI │
└────────────┴────────────┴────────────┴────────────┘
   ↓             ↓             ↓             ↓
Captured worker receipts / recommendations
   ↓
Master evaluates + reconciles
   ↓
Master integrates changes
   ↓
Build / test / runtime verification
   ↓
Final result
```

---

## Repository Layout

```text
Master_Slave_Skill/
├── SKILL.md
├── README.md
├── .gitignore
└── scripts/
    └── swarm_orchestrator.py
```

Runtime state is stored locally and ignored by Git:

```text
.hive/
├── cli_registry.json
├── dag.json
├── state.json
└── runs/
    └── <run-id>/
```

---

## Usage

### 1. Discover installed AI CLIs

```bash
python scripts/swarm_orchestrator.py --discover
```

Add another executable name to discovery:

```bash
python scripts/swarm_orchestrator.py --discover --extra-cli my-ai-cli
```

### 2. Inspect the worker registry

```bash
python scripts/swarm_orchestrator.py --list-workers
```

Workers whose syntax can be inferred from their local help output are marked `ready`.

Workers whose invocation cannot be safely inferred are marked `needs_adapter` rather than guessed.

### 3. Generate a task DAG

```bash
python scripts/swarm_orchestrator.py --task "Review this project and propose the safest fix"
```

### 4. Run the worker harness

```bash
python scripts/swarm_orchestrator.py --task "Review this project and identify bugs" --run
```

Use every runnable discovered worker:

```bash
python scripts/swarm_orchestrator.py --task "Review this project independently" --run --all-workers
```

Change the target working directory:

```bash
python scripts/swarm_orchestrator.py --task "Review this repository" --run --cwd "D:\\Projects\\Robot"
```

---

## Custom CLI Adapters

Some CLIs do not expose a prompt flag that can be reliably inferred from `--help`.

Create a local adapter JSON:

```json
{
  "name": "my-cli",
  "executable": "my-cli",
  "argv_template": ["my-cli", "--prompt", "{prompt}"],
  "prompt_mode": "argument"
}
```

Then register it:

```bash
python scripts/swarm_orchestrator.py --register-worker worker.json
```

For a CLI that receives prompts from stdin:

```json
{
  "name": "my-cli",
  "executable": "my-cli",
  "argv_template": ["my-cli"],
  "prompt_mode": "stdin"
}
```

Adapters contain invocation syntax only. Do not store API keys or credentials in them.

---

## Master / Worker Rules

The Master remains responsible for:

- deciding which workers are useful
- scoping every prompt
- preventing overlapping concurrent file edits
- evaluating worker answers
- resolving contradictions
- integrating only required changes
- running final verification itself

The recommended default is:

```text
multiple read-only worker reviews
→ one controlled implementation path
→ Master verification
```

This avoids several autonomous CLIs racing to edit the same files.

---

## Security and Permissions

The harness does **not** blindly enable dangerous permission-bypass flags.

Routine non-interactive operation is allowed when already authorized, but destructive actions, force pushes, credential exposure, and unrelated system changes remain under Master control.

---

## Requirements

- Python 3.10+
- AI CLI tools already installed and authenticated by the user
- worker executables accessible through `PATH`, or explicit adapter paths

No Python third-party dependencies are required.

---

## License

See the repository license if present.
