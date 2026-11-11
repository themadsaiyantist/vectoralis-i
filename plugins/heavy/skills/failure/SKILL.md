---
name: failure
description: Log something that went wrong in harness/failures.md, and draft a guard the second time.
---

# Failure

A failure is something that went wrong and was caught after the fact: a defect that reached a file, a check that was skipped, a claim nothing backs, a rule broken, an instruction missed. A guard refusing a write is the system working, and is not logged.

## The steps

1. Log it the same turn → `vectoralis fail "what failed, in a few words" --class a-short-slug`.
   - The person's failure is written exactly like yours, with `--who` and their name. Facts only, no apology, no blame.
2. Fill the entry: what failed, then the cause. The cause is why it happened, not what happened.
3. Fix the instance → the first box.
4. Sweep for siblings by meaning → fix each one, and say how many.
5. Name the cause → the second box.
6. Put a guard in place → the third box.
   - A machine can check it → a guard file, below.
   - It needs judgment → one line in `harness/rules.md`.
7. The entry closes when its three boxes are ✅: the heading's ⬜ becomes ✅, and `· closed` with the date is added.

## The second time

`vectoralis fail` says when a class has failed before. Then draft a guard, `harness/guards/<class>.json`:

```json
{
  "id": "debug-print",
  "why": "failures.md, class debug-print, twice",
  "on": "write",
  "path": "src/**/*.py",
  "pattern": "^\\s*print\\(",
  "mode": "warn",
  "message": "A debug print is about to ship. Remove it or use the logger.",
  "payloads": [
    { "name": "catches a print", "path": "src/a.py", "text": "print(x)", "expect": "hit" },
    { "name": "passes the logger", "path": "src/a.py", "text": "log.info(x)", "expect": "pass" }
  ]
}
```

- It starts at `warn`. Cut the two payloads from the two real failures.
- Run `vectoralis guards`. A guard whose payloads misbehave does not run.
- Show the person the file. They make it block by typing `promote` and its name.

**What to write where:** the entry → `harness/failures.md`. The guard → `harness/guards/`. A lesson the person dictates → `harness/lessons.md`.
