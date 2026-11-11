---
name: record
description: Move a box, write a decision or an exception, or lock finished work, in harness/.
---

# Record

A record moves the moment its work is checked, before the next unit starts. A crash, a limit or a closed laptop then loses nothing.

| What happened | Where it goes | How |
|---|---|---|
| A unit was built or checked | `harness/tracker.md` | its box → ✅ |
| A step was finished | `harness/todo.md` | its box → ✅, and `## Now` when what is next changed |
| A call was made | `harness/decisions.md`, Decisions | one line: the date, the call in bold, why |
| The person granted an exception | `harness/decisions.md`, Exceptions | the date, the rule it bends, why, its exact scope |
| Work is finished for good | `harness/locks.md` | one line: the path in backticks, the date, the reason. On the person's word |

## The rules

- ✅ is done and checked. ⬜ is not done. Nothing else goes in a cell or a box.
- A box ticked on a claim is the worst thing a tracker can hold. Tick after the check, never before.
- A tick refers to the file as it was then. Change a ticked file and `vectoralis check` flags its row: check it again and run `vectoralis affirm` with its path, or untick the box.
- The last column of the tracker and every box under `## Yours` are the person's. Ask them to type `tick` and a few words of the line. A guard refuses otherwise.
- A lesson is the person's. They start a message with `lesson:`, and you write it in their words and add nothing.
- A subagent never writes a record. It reports, and you write.
- An exception that excuses a path from a guard also goes into `skip` in `harness/settings.json`, which is the person's to open.

**What to write where:** the table above. One fact has one home.
