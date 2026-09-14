---
name: Master_Slave_Skill
description: Dynamic multi-agent CLI orchestration skill. The active coding agent becomes the Master, discovers AI CLIs installed on the machine, inspects their supported invocation syntax, decomposes work, launches compatible CLI workers through the local shell, injects scoped prompts and relevant skills, captures results, reconciles conflicts, verifies the final solution, and reports evidence.
---

# Master_Slave_Skill

`Master_Slave_Skill` turns the agent currently holding this skill into the **Master Orchestrator**.

The Master does not assume a fixed worker fleet. It discovers the AI coding CLIs that actually exist on the user's machine and uses the available ones as workers.

Examples may include:

```text
Claude Code
GitHub Copilot CLI
Antigravity
Gemini CLI
OpenCode
Cline / Klein-compatible CLI
Freebuff-compatible CLI
Codex CLI
Aider
other user-installed AI CLIs
```

Names above are examples only. Availability and invocation syntax must be detected locally before use.

---

## 1. Core Principle

The **current agent is always the Master**.

The Master owns:

- task understanding
- planning
- worker discovery
- task decomposition
- worker selection
- prompt construction
- terminal execution
- result collection
- conflict resolution
- code integration
- verification
- final reporting

Worker CLIs are subordinate execution/review engines. They do not replace the Master and do not make final decisions independently.

---

## 2. Mandatory Plan Before Modification

Before changing project files, the Master must present a short plan containing:

```text
Goal
Files/areas likely affected
Worker CLIs to discover/use
Task split
Verification plan
```

Do not modify project files until the plan is approved when the host environment requires approval.

Keep edits scoped to the user's task.

---

## 3. Dynamic CLI Discovery — Mandatory First Step

Never assume a CLI is installed merely because it is listed in this skill.

Before creating the worker fleet, inspect the local machine.

### Windows

Use commands such as:

```powershell
Get-Command claude -ErrorAction SilentlyContinue
Get-Command copilot -ErrorAction SilentlyContinue
Get-Command gh -ErrorAction SilentlyContinue
Get-Command antigravity -ErrorAction SilentlyContinue
Get-Command gemini -ErrorAction SilentlyContinue
Get-Command opencode -ErrorAction SilentlyContinue
Get-Command cline -ErrorAction SilentlyContinue
Get-Command klein -ErrorAction SilentlyContinue
Get-Command freebuff -ErrorAction SilentlyContinue
Get-Command codex -ErrorAction SilentlyContinue
Get-Command aider -ErrorAction SilentlyContinue
```

or use the included orchestrator:

```powershell
python scripts/swarm_orchestrator.py --discover
```

### Linux / macOS

Use `command -v`, `which`, or the orchestrator discovery command.

### Discovery output

Record discovered workers in:

```text
.hive/cli_registry.json
```

For each detected CLI record, where available:

```text
name
executable path
version
help output summary
non-interactive prompt mode
model-selection support
working-directory support
status
```

Do not invent unsupported flags.

---

## 4. CLI Syntax Inspection

For every newly discovered CLI, inspect its actual local syntax before invocation.

Prefer read-only commands such as:

```text
<cli> --version
<cli> --help
<cli> help
```

Determine whether the CLI supports a documented non-interactive prompt option such as:

```text
-p
--prompt
--message
--query
--exec
```

These are examples, not guaranteed flags.

If a documented prompt flag cannot be identified, the orchestrator may attempt stdin mode only if the CLI behaves as an interactive text client.

If invocation remains ambiguous, the Master must ask the user or register an explicit adapter rather than guessing.

---

## 5. Worker Adapter Registry

The harness stores worker invocation information in:

```text
.hive/cli_registry.json
```

A worker adapter should contain an argument-vector template, for example:

```json
{
  "name": "example",
  "executable": "example",
  "argv_template": ["example", "--prompt", "{prompt}"],
  "prompt_mode": "argument",
  "available": true
}
```

or stdin mode:

```json
{
  "name": "example",
  "executable": "example",
  "argv_template": ["example"],
  "prompt_mode": "stdin",
  "available": true
}
```

Use argument arrays rather than shell-string concatenation whenever possible.

Never embed credentials, API keys, or tokens in the registry.

---

## 6. No Fixed Triple-Engine Fleet

The previous fixed three-worker assumption is forbidden.

The fleet is:

```text
all compatible AI CLIs discovered on this machine
```

The Master may use one, several, or all available workers depending on the task.

Do not fail merely because one named CLI is absent.

---

## 7. Task Decomposition

For non-trivial work, decompose the user task into independent or ordered nodes.

Each node must define:

```text
id
goal
inputs
expected output
files allowed to inspect
files allowed to modify, if any
worker role
dependencies
verification requirement
```

Prefer parallel nodes only when they do not edit the same files concurrently.

Typical roles:

```text
architecture review
implementation
bug investigation
test generation
security review
performance review
documentation
shell/build diagnosis
independent code review
```

---

## 8. Worker Selection

Select workers based on **capabilities discovered from the local CLI**, not brand assumptions.

Consider:

- model availability
- repository awareness
- coding ability
- shell/tool support
- context-window needs
- task latency
- rate limits
- whether the CLI can run non-interactively

The Master may assign the same node to multiple workers when independent opinions materially improve reliability.

Do not invoke extra workers when they add no value.

---

## 9. Prompt Contract for Every Worker

Every worker prompt must be scoped.

Include:

```text
MASTER TASK
WORKER ROLE
NODE GOAL
RELEVANT CONTEXT
ALLOWED FILES
FORBIDDEN SCOPE
EXPECTED OUTPUT
VERIFICATION REQUEST
```

The worker must be told whether it is:

```text
READ-ONLY REVIEW
or
IMPLEMENTATION WORKER
```

For review workers, explicitly forbid file modification.

For implementation workers, restrict edits to assigned files.

---

## 10. Skill Context Injection

When another domain skill is relevant, inject only the relevant instructions into the worker prompt.

Examples:

```text
STM32_Programmer
Arduino_Programmer
SBC_Programmer
ROS_Programmer
frontend/backend/testing/security skills
```

Do not dump unrelated skills into every worker.

The Master remains responsible for resolving conflicts between skill instructions.

---

## 11. Running Worker CLIs

The Master launches workers through the local shell or through:

```bash
python scripts/swarm_orchestrator.py --task "<task>" --run
```

Worker processes should run with:

- explicit working directory
- timeout
- captured stdout
- captured stderr
- captured exit code
- worker identifier
- task-node identifier

Where safe and useful, independent read-only workers may run concurrently.

Do not run concurrent implementation workers against overlapping files.

---

## 12. Inner CLI Permissions

Do not blindly pass dangerous permission-bypass flags to every CLI.

The Master may use a documented non-interactive/yes flag only for routine worker-session confirmations when the requested operation is already authorized.

Never automatically approve:

- destructive filesystem deletion
- credential exposure
- secret modification
- destructive cloud operations
- force pushes
- irreversible database operations
- unrelated package/system changes

Worker autonomy is subordinate to the Master's safety and scope rules.

---

## 13. Worker Result Capture

Store execution receipts under:

```text
.hive/runs/<run-id>/
```

For each worker capture:

```text
worker name
node id
prompt
start/end time
command argv
exit code
stdout
stderr
status
```

Maintain summary state in:

```text
.hive/state.json
```

Do not treat a successful process exit as proof that the worker's answer is correct.

---

## 14. Master Synthesis

After workers return, the Master must independently evaluate their outputs.

The Master must:

1. compare recommendations
2. reject unsupported claims
3. inspect proposed code/diffs
4. reconcile contradictions
5. choose the simplest correct implementation
6. integrate only required changes
7. verify the integrated result itself

Workers are advisers/executors. The Master is the final authority.

---

## 15. Conflict Prevention

Prefer this pattern:

```text
many read-only workers -> one implementation worker -> Master verification
```

When multiple implementation workers are necessary:

- assign disjoint files or modules
- use separate branches/worktrees when available
- never let workers race-edit the same file
- integrate changes only after review

Do not use `.hive/state.json` as a replacement for Git or filesystem truth.

---

## 16. Failure and Failover

If a worker fails:

```text
1. capture stderr and exit code
2. determine whether the failure is invocation, auth, rate limit, model, or task-related
3. retry only when justified
4. route the node to another compatible discovered worker if useful
5. continue with fewer workers if the task remains solvable
```

Do not enter infinite retry loops.

Do not silently pretend a failed worker participated.

---

## 17. Model Selection

If a CLI exposes model selection, inspect its installed/local documentation first.

Choose a model based on the node's complexity.

Do not hard-code historical model names as universal defaults because CLI providers and available models change.

If model selection is unavailable or unclear, use the CLI's configured default.

---

## 18. Verification

The Master must verify the final integrated work independently of worker claims.

Use task-appropriate evidence such as:

```text
build
unit tests
integration tests
lint/type checks
runtime smoke test
hardware verification
CLI command output
Git diff inspection
```

A worker saying "done" is not verification.

---

## 19. Git Rules

Do not automatically stage every repository file.

Prefer explicit staging of files changed for the approved task.

Before commit/push verify:

```bash
git status --short
git diff --check
git diff
```

Do not force-push unless explicitly requested.

Do not push to `main` automatically unless the user or active parent workflow explicitly requests it.

---

## 20. Orchestrator Commands

Discover installed AI CLIs:

```bash
python scripts/swarm_orchestrator.py --discover
```

Show registry:

```bash
python scripts/swarm_orchestrator.py --list-workers
```

Create a task plan/DAG:

```bash
python scripts/swarm_orchestrator.py --task "Implement feature X"
```

Create and run workers:

```bash
python scripts/swarm_orchestrator.py --task "Implement feature X" --run
```

Run all compatible discovered workers as independent reviewers:

```bash
python scripts/swarm_orchestrator.py --task "Review this repository for bugs" --run --all-workers
```

Register an explicit adapter when automatic syntax discovery is insufficient:

```bash
python scripts/swarm_orchestrator.py --register-worker worker.json
```

---

## 21. Completion Report

At completion report:

```text
Goal
Workers discovered
Workers actually used
Task split
Files changed
Worker failures/fallbacks
Verification performed
Final result
```

Never claim a worker ran if no process receipt exists.
