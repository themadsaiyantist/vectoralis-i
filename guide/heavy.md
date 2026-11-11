# Heavy

Work that runs for days, touches many files, or that other people rely on. Seven steps, and records that stay true between sessions. Read this when one of [the five signals](start.md) is true.

**Contents:** The seven steps · What heavy adds · Set it up · One real session · What it costs · In Claude Code · In Codex · Samples to study · What can go wrong

---

## The seven steps

briefing → plan → build → check → re-check → record → report

| Step | What happens | Its page |
|---|---|---|
| Briefing | the session starts having read where things stand | [To-dos](todos.md) |
| Plan | every question asked in one round, before the first edit | [Plan](plan.md) |
| Build | one unit at a time | [Agents](agents.md) |
| Check | run what the change claims to do | [Checks](checks.md) |
| Re-check | a second pass of a different kind | [Checks](checks.md) |
| Record | the box moves the moment the check passes | [Tracker](tracker.md) |
| Report | what changed, what ran, what was not verified | [Checks](checks.md) |

**Record comes before the next build.** A crash, a limit or a closed laptop between two steps then loses nothing.

---

## What heavy adds

One folder in your project, `harness/`:

```text
harness/
├── settings.json   the profile, the test command, which guards are on
├── rules.md        how the work runs here, the small core that is always loaded
├── tracker.md      the build state, ✅ and ⬜ only
├── todo.md         two lists: yours, the agent's
├── failures.md     the failure log
├── lessons.md      what you taught after a failure, in your words
├── decisions.md    decisions and exceptions, dated, with the reason
├── locks.md        finished work nothing may write to
└── guards/         this project's own guards, each with its test payloads
```

And seven more guards on top of light's three. [Guards](guards.md) has the table.

**Three things stay yours alone.** You give each by typing it, and it lasts until your next message.

| You type | It allows |
|---|---|
| `tick` and a few words of the line | a box in your column |
| `lesson:` and the lesson | one entry in `harness/lessons.md` |
| `unlock` and the path | a write to locked work |

---

## Set it up

[Install](install.md) the `heavy` plugin → `/heavy:setup` in Claude Code, `$heavy:setup` in Codex. It adds the records and never overwrites a file that exists. Then fill the first rows of the tracker with the agent.

---

## One real session

This repository is built under its own heavy harness. Its records are in [`harness/`](../harness/), as they were written. This is what one session looked like.

**Briefing.** What the session start printed:

```text
VECTORALIS BRIEFING · heavy · branch main · 5 file(s) changed
Now:
  **Next →** the guide's pages → the kit → one real run of light on `runlog`.
Tracker: 32 of 240 boxes done
Next for the agent:
  - Fold the answers of `b.md` into the outline → delete `b.md`
  - Codex → the same package, and the table of gaps. Built for both, not yet run in Codex
Open for the person: 4 · first: Answer `b.md` → seven short calls, while the build runs
Open failures: none
Locks: none
Stale: 1 · tracker: `plugins/light/engine/guards` changed after its row was ticked
```

**Plan.** Twenty-five questions went to the author in one file, each with a pick. The answers came back as letters, and each went to its home the same turn.

**Build, check.** The engine, then its proof: 33 unit tests and 81 guard payloads.

**Re-check.** The repository ran its own check on itself, and the check stopped a commit:

```text
STALE: tracker: `tools/check_writing.py` changed after its row was ticked
1 flag(s).
```

The file had changed after its box was ticked. It was checked again, then recorded:

```text
$ vectoralis affirm tools/check_writing.py
Recorded: `tools/check_writing.py` was checked again as it is now.
```

**Record.** The boxes moved in [`harness/tracker.md`](../harness/tracker.md). Ten calls went into [`harness/decisions.md`](../harness/decisions.md), each with its reason. Five things that went wrong went into [`harness/failures.md`](../harness/failures.md), each with its cause and its guard.

**Report.** What changed, what ran and what it printed, what was not verified.

Every output above is `run` on this repository, 2026-11-11.

---

## What it costs

- **Tokens** → about 930 always loaded: the skill descriptions about 240, `rules.md` about 500, the briefing about 190. The cap is 2,000, and `vectoralis check` fails over it. [Cost](cost.md)
- **Attention** → you answer one round of questions before the build, and you tick your own boxes.
- **Time** → one more test run at the end of a turn that changed something.

---

## In Claude Code

- The session start prints the core and the briefing by itself.
- The skills are picked by the agent from the task, or called by name: `/heavy:plan`, `/heavy:check`, `/heavy:record`, `/heavy:handoff`.
- Before a compaction, the harness prints what the summary must keep. [Handoff](handoff.md)

## In Codex

- The same records, the same guards, the same skills, called with `$heavy:plan` and the rest.
- Two gaps: the `reviewer` and `builder` subagents are Claude Code only, and the compaction prompt is not confirmed in Codex. [Codex](codex.md)

---

## Samples to study

Two public projects worth reading beside this one. Both are `referenced`, not run here.

| Sample | What it does well | What to add when you use it |
|---|---|---|
| [superpowers](https://github.com/obra/superpowers) | a full path of skills from the first idea to the review | a guard for each rule you cannot afford to break. A skill asks, it does not stop |
| [spec-kit](https://github.com/github/spec-kit) | the spec comes first, and the plan and the tasks are cut from it | a check that the spec and the work still agree a week later |

---

## What can go wrong

- **The records fall behind.** A box that is not moved the moment its work is checked is never moved. The `nudge` guard says so once, when the agent says done.
- **A box ticked on a claim.** The worst thing a tracker can hold. Tick after the check.
- **Heavy on light work.** A one-line fix does not need a tracker row. Stay light until a signal is true.
- **The core grows.** `harness/rules.md` is read in every session. Keep it under 60 lines.

Verified on Claude Code 2.1.322, 2026-11-11. The outputs are `run`. The Codex lines are `read`.
