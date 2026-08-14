# 👑 Master_Slave_Skill: Swarm Orchestration Engine

> Standalone, Multi-Agent Swarm Orchestration Engine for AI Coding CLIs.

## 📖 Overview

`Master_Slave_Skill` is an advanced multi-agent orchestration skill designed to coordinate a fleet of worker CLI tools (**Antigravity CLI**, **Claude Code CLI**, and **GitHub Copilot CLI**) to execute complex programming tasks in parallel.

---

## ✨ Core Capabilities

- **🐝 Multi-Agent Swarm Architecture**: Decomposes complex coding prompts into a Directed Acyclic Graph (DAG) of parallel sub-tasks.
- **⚡ Triple-Engine Worker Fleet**:
  - **Antigravity Cloud CLI**: Complex architectural design, refactoring, and multi-file logic using task-matched Claude models.
  - **Claude Code CLI**: Fast component generation using 10+ free OpenCode models listed in `D:\Ashwin\Claude Code models.txt`.
  - **GitHub Copilot CLI** (`copilot` / `gh copilot` v1.0.60+): Instant shell script generation, command line tasks, and synthesis with configurable Claude models.
- **💻 Unified Terminal Subversion**: Runs CLI workers inside isolated terminal subversions for process stability and unified state tracking.
- **🎯 Task-Based Model Selection First Protocol**: Mandatory protocol upon logging into any terminal session and launching CLIs to immediately select the optimal model (e.g. `claude-3-7-sonnet`, `claude-3-5-sonnet`, `claude-3-5-haiku`, `claude-3-opus`) based on task requirements BEFORE running prompts.
- **🔄 OpenCode Free-Tier Load Balancer**: Dynamically load-balances across free models specified in `D:\Ashwin\Claude Code models.txt` (`nvidia/nemotron-550b`, `openai/gpt-oss-120b`, `qwen3-coder`, `glm-4.5-air`, `laguna-118b`, `mimo-v2-flash`), with automatic rate-limit failover.
- **💉 Automated Skill Context Injection**: Injects domain skills and task context directly into inner worker terminal sessions.
- **🧠 Shared Memory Bus (`.hive/state.json`)**: Real-time cross-worker state management and diff reconciliation.
- **🚀 Autonomous Git Synchronization**: Atomic conventional commits and automated push to `main`.

---

## 🏗️ Repository Layout

```
Master_Slave_Skill/
├── SKILL.md                     # Comprehensive standalone skill specification
├── README.md                    # Developer documentation & CLI manual
└── scripts/
    └── swarm_orchestrator.py   # Python Swarm Orchestration Engine
```

---

## 🚀 Usage

### Check Environment & Dependencies
```bash
python scripts/swarm_orchestrator.py --check-environment
```

### Launch Swarm Orchestration
```bash
python scripts/swarm_orchestrator.py --task "Build a full-stack REST API with authentication and tests"
```

---

## 📄 License

[MIT License](LICENSE)
