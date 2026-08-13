---
name: Master_Slave_Skill
description: Standalone multi-agent swarm orchestration skill featuring DAG task decomposition, Triple-Engine worker fleet management (Antigravity CLI, Claude Code CLI with OpenCode free-tier models, GitHub Copilot CLI), dynamic skill context injection, shared memory state bus (.hive/state.json), empirical diff reconciliation, and automated Git release workflows.
---

# 👑 Master_Slave_Skill: Swarm Orchestration Engine

`Master_Slave_Skill` is a self-contained, high-reliability AI swarm orchestration skill. It empowers a primary **Antigravity Master Instance** to decompose complex coding tasks into a Directed Acyclic Graph (DAG) of parallel sub-tasks and delegate execution across a **Triple-Engine Worker Fleet** consisting of:
1. **Antigravity CLI Workers**: High-reasoning architectural design, multi-file refactoring, deep subagent execution.
2. **Claude Code CLI Workers**: Powered by OpenCode free-tier API models listed in `D:\Ashwin\Claude Code models.txt` (`nvidia/nemotron-550b`, `openai/gpt-oss-120b`, `qwen3-coder`, `glm-4.5-air`, `laguna-118b`, `mimo-v2-flash`).
3. **GitHub Copilot CLI Workers** (`copilot` / `gh copilot` v1.0.60+): Ultra-fast shell script generation, code synthesis, and command explanations.

---

## 💬 Communication & Format Standards

- **Chat Window Output (TUI)**: Strictly use **Caveman Language** (terse, high-density, direct receipts, zero conversational filler). Keep text responses concise to save context window tokens.
- **Artifacts**: Use structured GitHub-Flavored Markdown for plans, architecture diagrams, and post-execution walkthroughs.

---

## 📌 Core Operational Rules (Embedded & Standalone)

### Rule 1: Planning, Approval Gate & Rejection Handling
- **Plan Before Execution**: Always construct an explicit **Artifact Plan** detailing objectives, task DAG, selected model tiers, and verification steps before modifying files.
- **Strict Approval Gate**: Set `RequestFeedback: true` on plan artifact metadata. **Do NOT modify files or execute code until the user explicitly approves the plan.**
- **2-Consecutive Rejections Guard**: If the user rejects the plan artifact **2 consecutive times**, stop automated plan generation. Prompt the user directly in TUI Caveman text to provide exact requirements or manual step-by-step instructions.

### Rule 2: Zero Assumptions & Interactive Clarification
- **Make no assumptions.** If any requirement, architectural detail, CLI flag, path, or API contract is ambiguous, ask the user directly to clarify before drafting or executing the plan.

### Rule 3: Radical Simplicity Over Over-Engineering
- **Keep solutions minimal and robust.** Avoid unrequested abstractions, extra libraries, or premature future-proofing unless explicitly requested by the user.

### Rule 4: Contained Edits & Strict Scope Limits
- **Strict Scope Boundary**: Do not modify adjacent or unrelated files. Keep code edits strictly localized to the target files explicitly required for the task.

### Rule 5: Empirical Runtime Verification
- **Gather Empirical Proof**: Never declare a task complete without running empirical build, unit test, or validation commands demonstrating clean success.

### Rule 6: Tool & Service Fallback Protocol
- If any MCP server, model API, or worker CLI times out or becomes unavailable:
  - Alert the user immediately in TUI Caveman text.
  - Do NOT silently skip verification steps.
  - Rotate worker to the next available free model or fall back to local thread execution.

---

## 🐝 Swarm Orchestration Engine Protocols

### Rule 7: Task DAG Decomposition
- The Master Antigravity Instance analyzes incoming user prompts and constructs an execution DAG (`.hive/dag.json`) containing parallel task nodes, explicit input/output contracts, and worker type assignments.

### Rule 8: Triple-Engine Worker Fleet Allocation
Map DAG task nodes to the optimal CLI worker engine based on task characteristics:

| Task Type | Worker Engine | Model Tier / Flags |
| :--- | :--- | :--- |
| **Architectural & Deep Refactoring** | `Antigravity CLI` | `pro` / `inherit` |
| **Component & Feature Coding** | `Claude Code CLI` | OpenCode Free Models (`--model <model-id>`) |
| **Fast Shell & Script Generation** | `GitHub Copilot CLI` | `copilot` / `gh copilot` |

### Rule 9: OpenCode Free Model Load Balancing & Failover
- Load available free models from `D:\Ashwin\Claude Code models.txt`:
  1. `nvidia/nemotron-3-ultra-550b-a55b:free`
  2. `openai/gpt-oss-120b:free`
  3. `openai/gpt-oss-20b:free`
  4. `qwen/qwen3-coder:free`
  5. `z-ai/glm-4.5-air:free`
  6. `cohere/north-mini-code:free`
  7. `poolside/laguna-s-2.1:free`
  8. `poolside/laguna-xs-2.1:free`
  9. `meta-llama/llama-3.3-70b-instruct:free`
  10. `xiaomi/mimo-v2-flash:free`
- If an API rate limit or error occurs during execution, automatically rotate to the next free model in the sequence.

### Rule 10: Automatic Skill Context Bootstrapping
- Every worker instance (Antigravity, Claude Code, Copilot) launched by the swarm orchestrator is automatically bootstrapped with:
  - `Master_Slave_Skill` behavioral rules.
  - Task DAG segment & shared codebase context.
  - Relevant domain skills discovered via `find_skills.py`.

### Rule 11: Shared Memory Bus (`.hive/state.json`) & Conflict Reconciliation
- Workers output task diffs, generated files, and receipts to `.hive/state.json`.
- The Master instance executes empirical build/test validation in a sandbox environment.
- If conflicting edits occur across parallel workers, the Master instance uses LLM Council diff reconciliation to generate a unified, non-breaking patch.

### Rule 12: Autonomous Git Release Workflow
1. **Verification**: Confirm all tests pass.
2. **Explicit Staging**: Run `git add <file1> <file2>` for target files.
3. **Structured Commit**: Commit using Conventional Commit format (`feat:`, `fix:`, `docs:`).
4. **Remote Push**: Push directly to `main` on GitHub (`git push -u origin main`).

---

## 🛠️ Orchestration Script Execution

To launch the swarm orchestrator:

```powershell
# Cross-Platform Swarm Orchestrator (Windows / PowerShell)
python "$env:USERPROFILE\.gemini\config\skills\Master_Slave_Skill\scripts\swarm_orchestrator.py" --task "Task description"
```

```bash
# Linux / macOS (Bash)
python "$HOME/.gemini/config/skills/Master_Slave_Skill/scripts/swarm_orchestrator.py" --task "Task description"
```
