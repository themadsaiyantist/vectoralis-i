# Start

What a harness is, and which of the two you need. One minute.

**Contents:** What a harness is · Light or heavy · The five signals · What you get · What it is not

---

## What a harness is

- An agent is a model with tools. A **harness** is everything around it: the instructions it reads, the guards that stop it, the records it keeps.
- The model writes the code. The harness decides whether you can trust the result.
- It has two halves. **Guidance** comes before the work: what to do, and how. **Sensors** come after: did it happen, and is it true.
- Most setups have the first half only. An instruction asks. A guard checks.

---

## Light or heavy

| | Light | Heavy |
|---|---|---|
| The work | a bug fix, a small feature, one sitting | days of work, many files, anything other people rely on |
| The steps | describe → plan in one line → edit → run the tests → commit | briefing → plan → build → check → re-check → record → report |
| What is installed | three guards, one settings file | light, plus the records and the guards that keep them true |
| Always loaded | 0 tokens | about 930 tokens, capped at 2,000 |
| What you do | nothing, until a guard speaks | tick your own boxes, answer one round of questions |
| Read next | [Light](light.md) | [Heavy](heavy.md) |

The token counts are `run`: `vectoralis budget` on this repository, 2026-11-11. It counts characters and divides by four.

---

## The five signals

Start light. Move to heavy the moment one of these is true:

- the work will not fit in one session
- someone else will read, review or depend on it
- it is hard to undo: deleting, money, law, publishing
- the same mistake has happened twice
- more than one agent works at once

The switch is one install. Nothing you did under light is lost.

---

## What you get

- **Guards that prove themselves.** Each one ships with payloads: at least one that must be stopped, at least one that must pass. `vectoralis guards` runs them all in seconds. [Guards](guards.md)
- **Records that stay true.** A box moves when its work is checked. A file that changes after its tick is flagged until it is checked again. [Checks](checks.md)
- **One harness, two agents.** The same guards and the same records in Claude Code and in Codex, from one package. [Codex](codex.md)
- **What is yours stays yours.** Three things no agent can do here: tick your box, write your lesson, open your lock. [Tracker](tracker.md)

---

## What it is not

- **Not a sandbox.** A guard is a guardrail, not a wall. It stops the mistakes a machine can be sure of. [Safety](safety.md)
- **Not a replacement** for the agent's own features. To-dos, plan mode and memory are theirs. This adds memory of failures, enforcement, and records.
- **Not a skills dump.** [The kit](../kit/README.md) names the few that matter for each kind of work.
- **Not theory.** What a page shows was run, or read in the maker's own docs, and the page says which.

Next → [Install](install.md).
