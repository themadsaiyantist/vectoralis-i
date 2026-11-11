# Agents

Parallel work without two hands on one file: subagents, worktrees and workflows. Read this before you send a second agent into the same repository.

**Contents:** When · The brief · One owner per file · The two subagents · Workflows · The guard · What it costs · In Claude Code · In Codex · What can go wrong

---

## When

- The work splits into units that do not depend on each other, and each costs more than a few tool calls.
- A search would flood the session with files it never needs.

**Not** for one file. Not for steps that depend on each other. Not when the session already holds the context an agent would have to rebuild. An agent starts cold.

---

## The brief

An agent knows only what the brief says. Give it all of this:

1. The goal, and what done looks like.
2. The files it owns.
3. The rules that bind it, in the person's own words where the person gave them.
4. What to report: what changed, what ran and what it printed, what it could not verify.
5. That it never writes a record, never pushes, never asks the person.

---

## One owner per file

- Two agents never edit one file.
- Edits that could collide run in separate worktrees: each agent gets its own copy of the repository on its own branch.
- A worktree's branch is merged only after its check passed.
- **An agent's "done" is a claim.** The session that sent it re-checks every file it touched before a box moves.

---

## The two subagents

| Subagent | What it does | Limits |
|---|---|---|
| `reviewer` | the re-check, read with fresh eyes | cannot write or edit |
| `builder` | builds one unit it owns, in its own worktree | reports, never writes a record |

They ship with the `heavy` plugin, in [`plugins/heavy/agents/`](../plugins/heavy/agents/).

---

## Workflows

- A workflow is a script that sends several agents out in a fixed order: review, then verify each finding.
- Use one when the same fan-out runs again and again. For a one-off, send the agents by hand.
- It spends several times the tokens of one session. Ask for it by name. Never let it start by itself.

---

## The guard

`records` → a subagent that writes anything under `harness/` is blocked:

```text
BLOCKED by Vectoralis. Nothing was written.
- A subagent does not write a record (`harness/tracker.md`).
  Rule: only the main session writes a record (guard `records`).
  Do instead: report it in your last message. The main session writes it.
```

`run`: the guard's payload, on this repository, 2026-11-11.

---

## What it costs

- **Tokens** → each subagent's description is about 25, always loaded. Each agent you send starts its own context and fills it.
- **Attention** → you read one report per agent, and the main session re-checks.
- **The rule of thumb** → an agent pays for itself when its work would otherwise fill your session with files you never needed.

---

## In Claude Code

- The agent sends subagents itself. `/heavy:agents` loads the brief's steps.
- A subagent file sets its tools, its model and its isolation: `isolation: worktree` gives it its own copy.
- A hook sees a subagent's call, which is how `records` tells it from the main session.

`read`: [subagents](https://code.claude.com/docs/en/sub-agents.md), 2026-11-11. Agent teams are still experimental there, so this guide leaves them out.

## In Codex

- A Codex plugin cannot carry a subagent. Yours live in `.codex/agents/*.toml`, with `name`, `description` and `developer_instructions`.
- There is no worktree isolation for a subagent. Make the worktree yourself: `git worktree add ../unit-a -b unit-a`.
- A subagent cannot loosen the sandbox or the approval policy of its session.

`read`: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), 2026-11-11.

---

## What can go wrong

- **A cold brief.** The agent solves a nearby problem. Say what done looks like.
- **Two agents, one file.** One of them loses its work. Name the owner.
- **A claim taken as a fact.** The report said the tests pass. Run them.
- **A flood of agents.** Six agents on a task one could do spends six contexts. Send the second only when the first is not enough.

Verified 2026-11-11. The block is `run`. The agents' own features are `read`.
