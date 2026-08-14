---
name: Master_Slave_Skill
description: Standalone multi-agent swarm orchestration skill featuring DAG task decomposition, Triple-Engine worker fleet management (Antigravity Cloud CLI, Claude Code CLI with OpenCode free-tier models, GitHub Copilot CLI), unified terminal subversion execution, mandatory task-based Claude model selection first protocol, shared memory state bus (.hive/state.json), empirical diff reconciliation, inner CLI autonomous prompt auto-approval, and automated Git release workflows committing directly to main.
---

# 👑 Master_Slave_Skill: Swarm Orchestration Engine

`Master_Slave_Skill` is a self-contained, high-reliability AI swarm orchestration skill. It empowers a primary **Antigravity Master Instance** to decompose complex coding tasks into a Directed Acyclic Graph (DAG) of parallel sub-tasks and delegate execution across a **Triple-Engine Worker Fleet** consisting of:
1. **Antigravity Cloud CLI Workers**: High-reasoning architectural design, multi-file refactoring, deep subagent execution with task-tailored Claude models.
2. **Claude Code CLI Workers**: Powered by OpenCode free-tier API models listed in `D:\Ashwin\Claude Code models.txt` (`nvidia/nemotron-550b`, `openai/gpt-oss-120b`, `qwen3-coder`, `glm-4.5-air`, `laguna-118b`, `mimo-v2-flash`).
3. **GitHub Copilot CLI Workers** (`copilot` / `gh copilot` v1.0.60+): Ultra-fast shell script generation, code synthesis, and command explanations with configurable Claude models.

---

## 💬 Communication & Format Standards

- **Chat Window Output (TUI)**: Strictly use **Caveman Language** (terse, high-density, direct receipts, zero conversational filler). Keep text responses concise to save context window tokens.
- **Artifacts**: Use structured GitHub-Flavored Markdown for plans, architecture diagrams, and post-execution walkthroughs.

---

## 📌 Core Operational Rules (Embedded & Standalone)

### Rule 1: Planning, Approval Gate & Autonomous Inner CLI Auto-Approval
- **Plan Before Execution**: Construct an explicit **Artifact Plan** detailing objectives, task DAG, selected model tiers, and verification steps before modifying files.
- **Autonomous Inner CLI Prompt Auto-Approval**: For all inner CLI tools, sub-shells, package managers, git commands, and worker sessions (Antigravity Cloud CLI, Claude Code CLI, GitHub Copilot CLI), **automatically approve all interactive prompts, permission questions, and confirmation dialogs** (using flags like `--yes`, `-y`, `--dangerously-skip-permissions`, `--non-interactive`, or auto-responding `yes`/`y` to stdin prompts) without pausing or asking for manual user permission.
- **2-Consecutive Rejections Guard**: If the user rejects the plan artifact **2 consecutive times**, stop automated plan generation. Prompt the user directly in TUI Caveman text to provide exact requirements or manual step-by-step instructions.

### Rule 2: Zero Assumptions & Interactive Clarification
- **Make no assumptions.** If any requirement, architectural detail, CLI flag, path, or API contract is ambiguous, ask the user directly to clarify before drafting or executing the plan.

### Rule 3: Zero Bare-Minimum Output & Elite Production Craft
- **No Half-Baked MVPs or Placeholder Code**: Never deliver minimal viable prototypes, unstyled HTML/CSS, shallow script skeletons, or basic placeholder implementations. Every output—whether a full-stack web application, a backend microservice, or an automation script—must be fully realized, resilient, and production-ready.
- **Deep Design & Engineering Rigor**:
  - **User Interfaces & Web Apps**: Deliver premium visual aesthetics, curated typography, fluid responsiveness, interactive micro-animations, comprehensive state management, and edge-case error boundaries.
  - **Systems & Backend Architectures**: Implement robust error handling, structured logging, strict type validation, and clean, scalable modular design.
- **Mandatory Self-Reflection & Enhancement Pass**:
  - Before writing code or marking a task DAG node as complete, every worker instance MUST execute a mandatory self-review:
    - *Is this solution bare minimum or merely functional?*
    - *How can the interaction design, performance, reliability, or code architecture be further elevated?*
  - Iterate and refine the implementation until it achieves uncompromising software craft.

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
| **Architectural & Deep Refactoring** | `Antigravity Cloud CLI` | `claude-3-7-sonnet` / `claude-3-opus` / `pro` |
| **Component & Feature Coding** | `Claude Code CLI` | OpenCode Free Models (`--model <model-id>`) |
| **Fast Shell & Script Generation** | `GitHub Copilot CLI` | `claude-3-5-sonnet` / `claude-3-5-haiku` (`copilot --model`) |

### Rule 8A: Unified Terminal Subversion & Mandatory Task-Based Model Selection First Protocol
1. **Unified Terminal Subversion Execution**:
   - Maintain worker terminal execution within a single, isolated terminal subversion / sub-session to ensure consistent environment variables, credentials, and context tracking across worker tools.
2. **Terminal Login & Worker CLI Launch**:
   - Log into the terminal session and launch the required worker CLI tool: **Antigravity Cloud CLI** (`antigravity` / `antigravity cloud`), **GitHub Copilot CLI** (`copilot` / `gh copilot`), or **Claude Code CLI** (`claude`).
3. **Mandatory Task-Based Model Selection First Rule**:
   - **CRITICAL STEP**: Upon logging into any terminal and initiating a CLI worker session, the **VERY FIRST ACTION** before entering or executing any task prompt is to evaluate task requirements and **explicitly select the model to use based on the task**.
   - **Claude Models in Antigravity Cloud & GitHub Copilot CLI**:
     - Both Antigravity Cloud CLI and GitHub Copilot CLI support running **Claude Models** (`claude-3-7-sonnet`, `claude-3-5-sonnet`, `claude-3-5-haiku`, `claude-3-opus`).
     - **Selection Matrix**:
       - *Complex Architecture & Multi-File Refactoring*: Select `claude-3-7-sonnet` or `claude-3-opus`.
       - *Standard Component Coding & Logic*: Select `claude-3-5-sonnet`.
       - *Fast Scripting, One-Liners & Command Synthesis*: Select `claude-3-5-haiku` or task-tailored Copilot model.
     - **CLI Model Selection Flags & Commands**:
       - **Antigravity Cloud CLI**: `antigravity --model <claude-model-id>` or `/model <claude-model-id>` inside session.
       - **GitHub Copilot CLI**: `copilot --model <claude-model-id>` or `gh copilot --model <claude-model-id>`.
       - **Claude Code CLI**: `claude --model <model-id>` (selected from `D:\Ashwin\Claude Code models.txt`).

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

### Rule 10: Multi-Terminal Fleet Execution & Mandatory Dynamic Skill Context Injection
- **Concurrent Multi-Terminal Worker Swarm**:
  - The orchestrator can spawn and execute across **multiple parallel terminal instances** of Antigravity Cloud CLI, Claude Code CLI, and GitHub Copilot CLI simultaneously.
- **Mandatory Dynamic Skill Bootstrapping**:
  - **NEVER RUN BARE WORKERS**: Every single worker terminal instance launched in the fleet MUST be dynamically bootstrapped with relevant domain skills before starting code generation.
  - Skill injection pipeline:
    1. Scan task node domain requirements (e.g., `frontend-developer`, `ui-ux-designer`, `tailwind-design-system`, `backend-architect`, `api-design-principles`, `security-auditor`).
    2. Inject `SKILL.md` instructions and referenced templates directly into the worker's initial prompt context.
    3. Inject `Master_Slave_Skill` core operational rules and Task DAG node contracts.
- **Continuous Skill-Driven Reflection & Quality Elevation**:
  - Every worker in every terminal session must continuously evaluate its work against injected skill domain standards:
    - *How can this code, architecture, or UI be improved using the injected skill best practices?*
    - *Are all micro-interactions, responsive states, type definitions, and error boundaries fully realized?*
  - Re-evaluate and refine until the code achieves elite production quality with zero bare-minimum compromises.

### Rule 11: Shared Memory Bus (`.hive/state.json`) & Conflict Reconciliation
- Workers output task diffs, generated files, and receipts to `.hive/state.json`.
- The Master instance executes empirical build/test validation in a sandbox environment.
- If conflicting edits occur across parallel workers, the Master instance uses LLM Council diff reconciliation to generate a unified, non-breaking patch.

### Rule 12: Autonomous Git Release Workflow & Mandatory Commit to Main
1. **Verification**: Confirm all build/test DAG nodes pass verification.
2. **Automated Staging of All Files**: Automatically stage **all** changes, modified files, and untracked files (`git add -A` or `git add .`).
3. **Structured Commit to Main**: Automatically commit all staged changes directly to the `main` branch using Conventional Commit format (`feat:`, `fix:`, `chore:`, `docs:`) without prompting for manual user approval (`git commit -m "..."`).
4. **Remote Push**: Push directly to `main` on GitHub/remote repository (`git push -u origin main`).

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
