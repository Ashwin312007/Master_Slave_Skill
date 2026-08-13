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

def check_cli_tool(command_name):
    """Checks if a command-line tool exists in PATH."""
    path = shutil.which(command_name)
    return path is not None

def check_environment():
    """Validates CLI tools and OpenCode model configuration."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("==================================================")
    print("[+] Master_Slave_Skill: Swarm Environment Status")
    print("==================================================")
    
    tools = {
        "Antigravity CLI": "antigravity",
        "Claude Code CLI": "claude",
        "GitHub Copilot CLI": "copilot",
        "GitHub CLI (gh)": "gh",
        "Python 3": sys.executable
    }
    
    status_summary = {}
    for name, cmd in tools.items():
        if cmd == sys.executable:
            status_summary[name] = True
            print(f"  [✓] {name}: {sys.executable}")
        else:
            exists = check_cli_tool(cmd)
            status_summary[name] = exists
            icon = "✓" if exists else "✗"
            print(f"  [{icon}] {name}: {'Available' if exists else 'Not found in PATH'}")
    
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
    """Generates a sample execution DAG for a task."""
    init_hive()
    dag = {
        "task": task_description,
        "nodes": [
            {
                "id": "node-1",
                "title": "Architecture & Schema Design",
                "engine": "antigravity",
                "tier": "pro",
                "dependencies": []
            },
            {
                "id": "node-2",
                "title": "Component & Feature Implementation",
                "engine": "claude",
                "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
                "dependencies": ["node-1"]
            },
            {
                "id": "node-3",
                "title": "Shell Scripts & Command Validation",
                "engine": "copilot",
                "dependencies": ["node-1"]
            }
        ]
    }
    
    with open(DAG_FILE, "w", encoding="utf-8") as f:
        json.dump(dag, f, indent=2)
    
    print(f"\n[✓] Generated Task DAG at {DAG_FILE}")
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
