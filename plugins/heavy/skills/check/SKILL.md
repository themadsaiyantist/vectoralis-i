---
name: check
description: Check finished work, then re-check it a different way, before any box moves.
---

# Check, then re-check

Done is a claim until something proves it. Two passes of two different kinds, because reading the same way finds what the first read found.

## Check

1. Run what the change claims to do. Not the tests alone: the thing itself, once. Read what it printed.
2. Run the tests. The `tests` guard runs them again when you stop, so run them first.
3. Run the project's own checkers that cover what changed.

## Re-check

1. Read the final diff, every hunk, as the person who will review it reads it.
2. Sweep for siblings: the same defect by its meaning, not by its text, forward and back through the repository. One wrong line usually has brothers.
3. Re-run what found the problem, and watch it come back clean.
4. Trace every number you are about to report to a run in this session.
5. For work that matters, hand the re-check to the `reviewer` subagent: fresh eyes, no write access. Its findings are claims too. Check each one before you act on it.

## Then

- Passed both → move the box, with the `record` skill.
- Found something → fix it, log it with the `failure` skill if it had reached a file, and start the check again.
- Could not verify something → say so by name in the report. "Should work" is not a result.

**What to write where:** nothing here. The box moves in `record`.
