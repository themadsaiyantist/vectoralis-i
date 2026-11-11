# Cost

What each piece costs, in tokens and in attention, so you add only what earns its place. Read this before you add a piece, and when a session feels slow or expensive.

**Contents:** Two kinds of cost · What is always loaded · What loads on use · What a run costs · Attention · In Claude Code · In Codex · What can go wrong

---

## Two kinds of cost

- **Tokens** → what the agent reads. Some of it is loaded before you type and paid in every turn. The rest loads when a task calls for it.
- **Attention** → what you do, and how often. A piece that needs you every turn is expensive, however few tokens it reads.

The cheapest piece is a guard: it reads nothing until it speaks.

---

## What is always loaded

| Piece | Light | Heavy |
|---|---|---|
| The guards | 0 | 0 |
| The skill descriptions | 0 | about 340 |
| The subagent descriptions | 0 | about 80 |
| `harness/rules.md`, the core | 0 | about 740 |
| The briefing | 0 | about 190 |
| **Total** | **0** | **about 1,360** |
| **The cap** | **300** | **2,000** |

- `run`: `vectoralis budget` on a fresh heavy project, 2026-11-11. It counts characters and divides by 2.7, and says it is an estimate.
- **Measured, not only estimated.** The first request of a live session carried 1,444 tokens more with the two plugins than without, on a project one setup old, and 1,746 more on this repository. Light alone added 0. The estimate came within 2% of both. `run`: Claude Code 2.1.322, Sonnet 5.5, 2026-11-11.
- **Four characters to a token read a third too low here.** The first version of the estimate used that rule of thumb and printed 870 where the session carried 1,444. Records are dense with paths, backticks and symbols. Measure once before you trust a rule of thumb.
- The briefing grows with your handoff. This repository's is about 520 today, which puts its total near 1,690.
- In Codex the two `setup` descriptions are listed as well, about 45 tokens: the field that hides them is Claude Code's.
- Over the cap, `vectoralis check` fails. The cap is a test, not a hope.
- Light's one skill is called by you alone, so its description is never loaded.

---

## What loads on use

A skill's body loads when the task calls it, and stays for the session.

| Skill | About, in tokens | Skill | About, in tokens |
|---|---|---|---|
| `brief` | 360 | `failure` | 770 |
| `plan` | 630 | `handoff` | 530 |
| `check` | 530 | `agents` | 570 |
| `record` | 650 | `pr` | 450 |
| `report` | 350 | `setup` | 530 |

`run`: the size of each `SKILL.md`, in characters divided by 2.7, the rate the live sessions measured, 2026-11-11.

- A record costs what it weighs, when it is read. A tracker of 80 rows is read once per session, not per turn.
- A subagent starts its own context. It keeps yours small, and fills its own.

---

## What a run costs

Three real runs of light, on a small Python project:

| The task | Turns | Time | Cost |
|---|---|---|---|
| Add a command, with a test, and commit | 7 | 22 s | $0.07 |
| A change that breaks three tests, stopped by the `tests` guard | 6 | 15 s | $0.06 |
| A token in a file, refused by the `secrets` guard | 4 | 19 s | $0.06 |

`run`: Claude Code 2.1.322, Sonnet 5.5, headless, 2026-11-11. The cost is the session's own `total_cost_usd`. [Light](light.md) has the runs.

Which model and what effort for which job → [Models](models.md).

---

## Attention

| Piece | What you do | How often |
|---|---|---|
| The three light guards | nothing | until one speaks |
| The plan | answer one round of questions | once per piece of heavy work |
| The tracker | tick your own column | once per unit |
| A lesson | dictate it | when you teach one |
| A lock | type `unlock` | when finished work must change |
| A guard of the project's own | read ten lines, type `promote` | once per guard |
| The failure log | read it | when you want to know why |

---

## In Claude Code

- `/context` shows what is loaded now, piece by piece.
- `vectoralis budget` shows what this harness adds to it.

## In Codex

- `vectoralis budget` works the same way. It reads files, not the session.
- A Codex skill is read by its `name` and `description`. The body loads on use, as in Claude Code.

[Context](context.md) has both in full.

---

## What can go wrong

- **An instructions file that grows.** It is paid in every turn of every session. Move a procedure into a skill.
- **A piece added "to be safe".** Each one costs attention. Add it when its signal is true.
- **An MCP server for what a command does.** A server adds to the context before you use it: its tool names and instructions in Claude Code, its tools in Codex unless you limit them. A command costs nothing until it runs. [MCP](mcp.md)
- **A number nobody measured.** Run `vectoralis budget` before you believe a cost, this page's included.

Verified on Claude Code 2.1.322, 2026-11-11. Every number on this page is `run`.
