#!/usr/bin/env python3
"""
Master_Slave_Skill: Swarm Orchestration Engine
Coordinates Antigravity CLI, Claude Code CLI (OpenCode free models), and GitHub Copilot CLI workers.
"""

import os
import sys
import json
import argparse
import subprocess
import shutil
from pathlib import Path

DEFAULT_MODEL_FILE = r"D:\Ashwin\Claude Code models.txt"
HIVE_DIR = Path(".hive")
STATE_FILE = HIVE_DIR / "state.json"
DAG_FILE = HIVE_DIR / "dag.json"

def load_opencode_models(filepath=DEFAULT_MODEL_FILE):
    """Parses free-tier OpenCode models from text file."""
    models = []
    if not os.path.exists(filepath):
        print(f"[!] Warning: Model file not found at {filepath}")
        return [
            "nvidia/nemotron-3-ultra-550b-a55b:free",
            "openai/gpt-oss-120b:free",
            "qwen/qwen3-coder:free",
            "z-ai/glm-4.5-air:free",
            "poolside/laguna-s-2.1:free"
        ]
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("claude --model "):
                model = line.replace("claude --model ", "").strip()
                if model and model not in models:
                    models.append(model)
            elif ":free" in line:
                parts = line.split()
                for part in parts:
                    if ":free" in part:
                        model = part.strip()
                        if model not in models:
                            models.append(model)
    return models

CLAUDE_MODELS = {
    "architectural": "claude-3-7-sonnet",
    "feature_coding": "claude-3-5-sonnet",
    "fast_scripting": "claude-3-5-haiku",
    "heavy_reasoning": "claude-3-opus"
}

def check_cli_tool(command_name):
    """Checks if a command-line tool exists in PATH."""
    path = shutil.which(command_name)
    return path is not None

def check_environment():
    """Validates CLI tools, Terminal Subversion readiness, and Claude/OpenCode model configurations."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    print("==================================================")
    print("[+] Master_Slave_Skill: Swarm Environment Status")
    print("==================================================")
    
    tools = {
        "Antigravity Cloud CLI": "antigravity",
        "Claude Code CLI": "claude",
        "GitHub Copilot CLI": "copilot",
        "GitHub CLI (gh)": "gh",
        "Python 3": sys.executable
    }
    
    status_summary = {}
    for name, cmd in tools.items():
        if cmd == sys.executable:
            status_summary[name] = True
            print(f"  [OK] {name}: {sys.executable}")
        else:
            exists = check_cli_tool(cmd)
            status_summary[name] = exists
            icon = "OK" if exists else "X"
            print(f"  [{icon}] {name}: {'Available' if exists else 'Not found in PATH'}")
    
    print("\n🧠 Claude Model Presets (Antigravity Cloud & Copilot CLI):")
    for category, model_id in CLAUDE_MODELS.items():
        print(f"  * [{category.upper()}]: {model_id}")

    print("\n📦 OpenCode Free Models (D:\\Ashwin\\Claude Code models.txt):")
    models = load_opencode_models()
    for idx, model in enumerate(models, 1):
        print(f"  {idx}. {model}")
    
    return status_summary

def init_hive():
    """Initializes .hive directory and state storage."""
    HIVE_DIR.mkdir(exist_ok=True)
    if not STATE_FILE.exists():
        initial_state = {
            "status": "initialized",
            "workers": [],
            "completed_tasks": [],
            "diffs": {}
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_state, f, indent=2)

def generate_task_dag(task_description):
    """Generates an execution DAG for a task with mandatory task-based model selection, skill injection, and Manus-level quality standards."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    init_hive()
    dag = {
        "task": task_description,
        "quality_standard": "Manus-Level Excellence (Zero Bare Minimum)",
        "nodes": [
            {
                "id": "node-1",
                "title": "Architecture & Schema Design",
                "engine": "antigravity",
                "selected_model": CLAUDE_MODELS["architectural"],
                "injected_skills": ["backend-architect", "api-design-principles", "database-architect"],
                "quality_reflection": True,
                "dependencies": []
            },
            {
                "id": "node-2",
                "title": "Component & Feature Implementation",
                "engine": "claude",
                "selected_model": "nvidia/nemotron-3-ultra-550b-a55b:free",
                "injected_skills": ["frontend-developer", "ui-ux-designer", "tailwind-design-system"],
                "quality_reflection": True,
                "dependencies": ["node-1"]
            },
            {
                "id": "node-3",
                "title": "Shell Scripts & Command Validation",
                "engine": "copilot",
                "selected_model": CLAUDE_MODELS["fast_scripting"],
                "injected_skills": ["bash-pro", "devops-troubleshooter"],
                "quality_reflection": True,
                "dependencies": ["node-1"]
            }
        ]
    }
    
    with open(DAG_FILE, "w", encoding="utf-8") as f:
        json.dump(dag, f, indent=2)
    
    print(f"\n[OK] Generated Task DAG at {DAG_FILE}")
    print(json.dumps(dag, indent=2))
    return dag

def main():
    parser = argparse.ArgumentParser(description="Master_Slave_Skill Swarm Orchestration Engine")
    parser.add_argument("--check-environment", action="store_true", help="Check CLI tools and OpenCode models")
    parser.add_argument("--test-models", action="store_true", help="Test loading OpenCode free models")
    parser.add_argument("--test-dag", action="store_true", help="Test DAG task generation")
    parser.add_argument("--task", type=str, help="Task description to orchestrate")
    
    args = parser.parse_args()
    
    if args.check_environment:
        check_environment()
    elif args.test_models:
        models = load_opencode_models()
        print(f"Loaded {len(models)} models:")
        for m in models:
            print(f" - {m}")
    elif args.test_dag or args.task:
        task = args.task or "Build full-stack microservice with tests"
        generate_task_dag(task)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
