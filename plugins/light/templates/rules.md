# Rules

How the work runs in this project. The harness loads this file at the start of every session, so it stays short.

**Contents:** The seven steps · The records · The person's alone · When to ask · What done means

---

## The seven steps

briefing → plan → build → check → re-check → record → report

1. **Briefing** → read `## Now` in `harness/todo.md`, then the next open box.
2. **Plan** → every question in one round, before the first edit, the pick first.
3. **Build** → one unit at a time.
4. **Check** → run what the change claims: the tests, then the thing itself.
5. **Re-check** → a second pass of a different kind: read the diff, look for the same defect elsewhere.
6. **Record** → move the box the moment the check passes, before the next unit starts.
7. **Report** → what changed, what ran and what it printed, what was not verified, every call made without asking.

---

## The records

| Record | What goes there |
|---|---|
| `harness/tracker.md` | the build state, ✅ and ⬜ only |
| `harness/todo.md` | what is left: yours, the agent's, and `## Now` |
| `harness/failures.md` | what went wrong, with its cause and its guard |
| `harness/lessons.md` | what the person taught, in their words |
| `harness/decisions.md` | decisions and exceptions, dated, with the reason |
| `harness/locks.md` | finished work nothing may write to |

---

## The person's alone

- A box in the last column of the tracker, and a box under `## Yours` → they type `tick` and a few words of the line.
- A lesson → they start their message with `lesson:`.
- A lock → they type `unlock` and the path.
- A guard's mode and the settings → they type `promote` and the guard, or `unlock harness/settings.json`.

---

## When to ask

- The call is hard to undo, faces outward, or changes a rule.
- Two readings of the instruction lead to different work.
- Otherwise make the call, and name it in the report.

---

## What done means

- The tests pass.
- The box is moved.
- The report says what was not verified.
