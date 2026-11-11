# Proof

One person and an agent, three months. This page is what that built, and which piece of this guide carried each part. Every number was counted from the author's own repositories on 2026-11-11, and the table says how.

**Contents:** What was built · The numbers · What carried it · This repository · What it means for you

---

## What was built

- **A machine learning bootcamp**, from the first terminal command to a monitored model in production → 7 modules, 39 sections, 130 lessons, every code block run before it was printed.
- **The platform that serves it** → a web application with accounts, progress and exams, and the service that grades them.
- **A free course on coding agents** → 15 lessons, written in five days.
- **The products around them.**
- **This repository** → built under the harness it describes.

---

## The numbers

| The number | What it counts | How it was counted |
|---|---|---|
| 130 lessons, about 1.2 million words | the bootcamp's content | the words of the lesson files |
| 708 boxes ticked, none open | the tracker: every lesson written, run and passed by the author | the ✅ and ⬜ in the trackers |
| 351 commits | from 8 August to 11 November 2026 | the repository's history |
| 26 pull requests merged | each one green before the merge | the merged pull requests |
| 34 failures on record, 29 closed | each with its cause and its guard | the entries of the failure log |
| 5 hook scripts, 2,050 lines | bad writes refused before they landed | the lines of the hooks |
| 49 test files | the platform's tests | the tracked test files |
| 15 lessons in 5 days, on 199 recorded runs | the course, every output a real run | the commits and the kept runs |

---

## What carried it

| The piece | What it made possible |
|---|---|
| [The tracker](tracker.md) | 130 lessons across hundreds of sessions, and none lost or done twice. No session had to remember the one before |
| [Check, re-check](checks.md) | every number in a lesson came from a run, not from a guess |
| [The failure log](failures.md) | a mistake was paid for once. 29 of them now have a guard |
| [Guards](guards.md) | the rules held on the days attention did not |
| [The plan](plan.md) | decisions were made once, in one round, and written down |
| [Agents](agents.md) | whole sections were checked side by side, each by its own agent |
| [Pull requests](pull-requests.md) | 26 went in, and none was left red |
| [Locks](locks.md) | finished modules stayed finished while the next ones were built |

---

## This repository

It was started on 11 November 2026 and it runs on its own harness.

- **54 unit tests and 236 guard payloads**, green on three versions of Python.
- **Its own check stopped its own commit**, twice, and each time the check was right. [`harness/failures.md`](../harness/failures.md) has both.
- **A live session opened, watched and merged its own pull request**, and stopped at the one call that was not its to make. [Pull requests](pull-requests.md)
- **Running it found what reading had missed.** The first live sessions of the skills turned up four defects. Each one was fixed and proven the same day. [Heavy](heavy.md)
- **A second reader found what the author had missed.** The fix to one guard went to a reader who had not written it, five times. Each pass found less than the one before, and the last finding is closed and held by a test. [`harness/failures.md`](../harness/failures.md) has it.
- **Its tracker, its decisions and its failures are public**, as they were written, the mistakes included. [`harness/`](../harness/)

`run`: `sh tools/check.sh` and the live sessions, on this repository, 2026-11-11.

---

## What it means for you

- **None of this needed a team.** It needed records that stay true, and guards that hold when attention runs out.
- **The size was never the hard part.** A project of 130 lessons is a tracker with 708 boxes. Each box is one sitting.
- **It starts small.** Three guards, today, on the project you already have. [Install](install.md)
- **Then one signal turns true**, and you switch. [Start](start.md)

Tick the first box.
