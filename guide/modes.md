# Modes

Plan mode in action, and the permission modes of both agents, bypass included. Read this before you let an agent work without asking.

**Contents:** The choices · Plan mode in action · Before bypass · The work and the mode · In Claude Code · In Codex · With the harness · What can go wrong

---

## The choices

A mode decides **when the agent stops to ask**. What a command can reach once it runs is the sandbox's job. Claude Code has one dial with six positions:

| Mode | Runs without asking | Fits |
|---|---|---|
| `default`, shown as Manual | reads | sensitive work, code you do not know |
| `acceptEdits` | reads, file edits, plain file commands such as `mkdir` and `mv` | changes you review in your editor |
| `plan` | reads, and exploring commands a classifier approves | looking before changing |
| `auto` | everything. A second model reviews what is not a read or an edit in your folder | long tasks. A terminal session starts here |
| `dontAsk` | reads, and what you allowed in advance. The rest is refused | CI and scripts |
| `bypassPermissions` | everything | containers and virtual machines only |

Codex has two dials. `sandbox_mode` is what the agent can touch: `read-only`, `workspace-write` or `danger-full-access`. `approval_policy` is when it asks: `on-request` or `never`, and `never` works with every sandbox. Who approves never widens the sandbox.

| You want | You type | What happens |
|---|---|---|
| Auto, the default | `codex --sandbox workspace-write --ask-for-approval on-request` | edits and runs commands in the workspace. Asks to leave it or to use the network |
| To change nothing | `codex --sandbox read-only --ask-for-approval on-request` | reads. Asks before anything more |
| Fewer stops, the same sandbox | `codex --approve-for-me` | a reviewer agent answers the eligible requests |
| A run in a script | `codex exec "<task>"` | read-only, unless you add `--sandbox workspace-write` |
| No sandbox, no questions | `codex --yolo` | everything runs. Its docs: not recommended |

`read`: [Claude Code permission modes](https://code.claude.com/docs/en/permission-modes.md), [Codex approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security), [Codex in scripts](https://learn.chatgpt.com/docs/non-interactive-mode), 2026-11-11.

---

## Plan mode in action

One task in Claude Code, from the plan to the approval:

1. **Enter** → `/plan add a count command, with a test`, or `Shift+Tab` until the status bar shows `⏸ plan mode on`.
2. **It reads.** Files, exploring commands, and a Plan subagent for the wide reading, so the file contents stay out of your context. It edits nothing.
3. **It shows the plan and asks.** `Ctrl+G` opens the plan in your editor if you want to change it. Then one of three answers: `Yes, and use auto mode`, `Yes, manually approve edits`, or `No, keep planning`.
4. **Approved** → plan mode ends and the edits start. The plan is a file, so it survives a compaction. [Handoff](handoff.md)

In Codex → `/plan`, or `Shift+Tab`. It gathers context, asks its questions and proposes a plan. When nothing may change, add the read-only sandbox: `/permissions` → Read Only.

Both flows are `read`, not run here: [plan mode](https://code.claude.com/docs/en/permission-modes.md#analyze-before-you-edit-with-plan-mode), [the Plan subagent](https://code.claude.com/docs/en/sub-agents.md#built-in-subagents), [Codex best practices](https://learn.chatgpt.com/guides/best-practices), 2026-11-11.

---

## Before bypass

Bypass is fast. **It removes the question, not the risk.** A guard stops only what a machine can be sure of. So three things are in place first:

| What | Why | How you know |
|---|---|---|
| The guards of this harness | Claude Code asks a hook before it checks the mode, so a guard's block holds under bypass | `vectoralis guards` → every row says `behave` |
| A sandbox around the whole agent | it is the only wall left. Claude Code's own sandbox wraps shell commands, not its file tools, MCP servers or hooks | a container or a virtual machine, not as root |
| A clean git state | a rewind restores what the edit tools changed, not what a shell command changed | `git status` prints nothing, on a branch of its own |

- **In Codex** `--yolo` drops the sandbox too. Its docs call a hook a guardrail, not a complete enforcement boundary, and warn that a hostile project can take what the container holds, credentials included.
- **Most days the answer is not bypass.** `auto` in Claude Code and `--approve-for-me` in Codex remove most prompts and keep a check.

`run`: `vectoralis guards` on this repository, 167 payloads, all behaving, 2026-11-11. And under bypass, in a live headless session on a scratch project: `yours` blocked a shell command that would have written a guard file, and `destructive` blocked a `git reset --hard` that a subagent tried. More in [Safety](safety.md).

---

## The work and the mode

| The work | Claude Code | Codex |
|---|---|---|
| Read a codebase you do not know | `plan` | `read-only`, `on-request` |
| A one-line fix you watch | Manual, or `acceptEdits` | Auto |
| A feature in one sitting | `auto` | Auto, or `--approve-for-me` to stop less |
| Heavy work | `plan` → approve → `auto` | `/plan` → Auto |
| A script or CI | `dontAsk` with `--allowedTools` | `codex exec`, read-only or `workspace-write` |
| Unattended, in a container | `bypassPermissions` | `--yolo`, inside the container |
| Money, production, secrets | Manual | `read-only`, `on-request` |

## In Claude Code

- **Switch** → `Shift+Tab`. From `auto` it goes to Manual, then `acceptEdits`, then `plan`.
- **Start in one** → `claude --permission-mode plan`. Always → `permissions.defaultMode` in `~/.claude/settings.json`.
- **`dontAsk`** → `claude -p "run the test suite" --permission-mode dontAsk --allowedTools "Bash(npm test)" "Read"`.
- **Bypass**, at launch only → `claude --permission-mode bypassPermissions`. It refuses to start as root.
- **The shell in a sandbox** → `/sandbox`. A deny rule blocks in every mode, bypass included.

## In Codex

- **Switch** → `/permissions`. Always → `sandbox_mode` and `approval_policy` in `~/.codex/config.toml`.
- Plain `codex` suggests Auto in a folder under version control, and read-only elsewhere. In `workspace-write` the network stays off until you set `network_access = true` under `[sandbox_workspace_write]`.
- **The gap** → no allow, ask and deny rules. Codex's own command rules are labelled experimental in its docs, so this guide does not build on them.

## With the harness

| | Light | Heavy |
|---|---|---|
| In every mode | `secrets` and `tests` keep running. In Claude Code no mode switches a hook off | adds `destructive`, `locks`, `push`, `yours`, `records` and the `sweep` |
| Before the first edit | one line of plan, asked for in the task | the `plan` skill asks every question in one round. Plan mode does the reading. [Plan](plan.md) |
| Under bypass | a secret and failing tests are still stopped | the default branch, locked work and your own boxes stay out of reach. [Guards](guards.md) |

## What can go wrong

- **Bypass on your own machine.** One hostile line in a file the agent reads, and nothing asks → a container, or `auto`.
- **A plan mode that does not hold.** In a terminal session started with bypass available, Claude Code does not enforce plan mode, and an edit tried while planning runs → start plan sessions without the bypass flags.
- **`auto` or bypass in the project's settings.** Claude Code ignores both in `.claude/settings.json`, so a repository cannot switch your prompts off → the flag, or `~/.claude/settings.json`.
- **Yes without reading.** Its docs: after the tenth prompt you approve without reading → `auto` or the sandbox, not a faster finger.
- **A boundary said only in the chat.** "Do not push" can vanish in a compaction → a deny rule, or the `push` guard. [Handoff](handoff.md)

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `read`, beside the pages linked in each section: Claude Code's [sandboxing](https://code.claude.com/docs/en/sandboxing.md), [sandbox environments](https://code.claude.com/docs/en/sandbox-environments.md), [hooks and permission modes](https://code.claude.com/docs/en/hooks-guide.md#hooks-and-permission-modes), [checkpointing](https://code.claude.com/docs/en/checkpointing.md) and [best practices](https://code.claude.com/docs/en/best-practices.md), and Codex's [sandbox](https://learn.chatgpt.com/docs/sandboxing), [rules](https://learn.chatgpt.com/docs/agent-configuration/rules), [hooks](https://learn.chatgpt.com/docs/hooks) and [CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli). `run`: `vectoralis guards`. No agent session was run for this page.
