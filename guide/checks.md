# Checks

Done is a claim until something proves it. Check, re-check, and the staleness check that keeps a tick honest. Read this before you trust a ✅.

**Contents:** Check · Re-check · The staleness check · The report · In Claude Code · In Codex · What it costs · What can go wrong

---

## Check

The first pass. Run what the change claims to do.

1. The thing itself, once. Read what it printed.
2. The tests. The `tests` guard runs them again when the agent stops.
3. The project's own checkers that cover what changed.

---

## Re-check

A second pass of a **different kind**, because reading the same way finds what the first read found.

1. Read the final diff, every hunk, as the reviewer will read it.
2. Sweep for siblings: the same defect by its meaning, not by its text. One wrong line usually has brothers.
3. Re-run what found the problem, and watch it come back clean.
4. Trace every number in the report to a run in this session.
5. For work that matters, hand it to a second pair of eyes that cannot write: the `reviewer` subagent. Its findings are claims too.

---

## The staleness check

A record is stale when it says something the repository no longer backs.

```text
$ vectoralis check
STALE: tracker: `tools/check_writing.py` changed after its row was ticked
1 flag(s).
```

| The flag | What it means |
|---|---|
| a file changed after its row was ticked | the ✅ refers to an older version |
| a ticked file is gone | the row claims work that is not there |
| a path names nothing | a rule, a decision or a finished step points at a file that does not exist |
| a lock covers no file | the pattern is wrong, or the work moved |
| the Contents line is out of step | a section was added, removed or renamed |
| a guard without its proof | a payload is missing or misbehaves |
| over the cap | too much is always loaded |

**How a tick knows its version.** The harness keeps `harness/.checked.json`: for every row bound to a file, a short hash of the file as it was at the tick. It compares content, never dates, so it is right before a commit and after one.

- The file changed and you checked it again → `vectoralis affirm <path>`.
- The file changed and you did not → untick the box.
- A row that is not built yet is never stale. A tracker lists the work ahead.

The output is `run` on this repository, 2026-11-11. That flag stopped a real commit, see [Heavy](heavy.md).

---

## The report

The last step, and the place where honesty costs least.

1. What changed.
2. What ran, and what it printed.
3. **What was not verified**, by name.
4. Every call made without asking.
5. What is next.

"Should work" is not a result. It ran, or it was not run.

---

## In Claude Code

- `/heavy:check` runs both passes. `/heavy:report` writes the report.
- The `reviewer` subagent re-checks with no write access.
- Run every check before a commit as one command that stops at the first failure. This repository's is [`tools/check.sh`](../tools/check.sh), and it is its pre-commit hook.

## In Codex

- `$heavy:check` and `$heavy:report` run the same steps.
- The `reviewer` subagent is a gap: a Codex plugin cannot carry one. A second session with a read-only sandbox does the same job. [Codex](codex.md)

---

## What it costs

- **Tokens** → the `check` skill is about 530 when it loads, and its description about 36 before that.
- **Attention** → none for the check. For the re-check, you read the report's third line.
- **Time** → a second pass. It is cheaper than the bug.

---

## What can go wrong

- **A check whose result nobody reads.** This repository committed twice while its own check showed a flag. The fix was a pre-commit hook, not a promise. [`harness/failures.md`](../harness/failures.md)
- **A re-check of the same kind.** Reading the code twice is one check.
- **A test that agrees with the bug.** The first false flag here had a test that expected it. Test the case that must not flag, too.
- **A tick on a claim.** A subagent's "done", a green run of the wrong tests. Check, then tick.

Verified 2026-11-11. The outputs are `run`. The steps are the `check` and `report` skills of this repository.
