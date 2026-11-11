# The Failure Log

What went wrong, why it happened and what now stops it: one entry per failure, three boxes, and a guard drafted the second time a class fails. Read this when the same mistake has happened twice, or before you write your first guard.

**Contents:** When to add it · The steps · The file · The guard · What it costs · In Claude Code · In Codex · What can go wrong

---

## When to add it

- The same mistake happened twice. That is also one of [the five signals](start.md) to go heavy.
- A fix was a promise to be careful, and nothing a machine runs.
- You explained the same correction in two sessions.

---

## The steps

1. Log it the same turn → `vectoralis fail "what failed, in a few words" --class a-short-slug`. `--who` names whose it is. Yours are written exactly like the agent's.
2. Fill in what failed, then the cause: why it happened, not what happened.
3. Fix the instance → the first box. Then sweep for its siblings, by meaning and not by text, and fix each one.
4. Name the cause → the second box.
5. Put a guard in place → the third box. A machine can check it → a guard file. It needs judgment → one line in `harness/rules.md`.
6. Three ✅ → the heading's ⬜ becomes ✅, with `· closed` and the date.
7. The second failure of a class → the agent drafts `harness/guards/<class>.json` at `warn` → you read it → you type `promote` and its name.

---

## The file

`harness/failures.md`, newest first. **A failure** is something that went wrong and was caught after the fact. A guard that refuses a write is the system working, and is not logged. The second failure of a class, and the entry the command wrote, `run` in a scratch project:

```text
$ vectoralis fail "A debug print shipped in the refund webhook" --class debug-print --who goku
Logged in harness/failures.md: A debug print shipped in the refund webhook
This class has failed before (1 time(s), first on 2026-11-11).
Draft a guard: harness/guards/debug-print.json, in warn mode, with one payload that hits and one that passes.
```

```markdown
### ⬜ 2026-11-11 · goku · A debug print shipped in the refund webhook

**Class.** `debug-print`

**What failed.**

**Cause.**

**Fix.** ⬜ the instance · ⬜ the cause · ⬜ the guard
```

- **The class** is a short slug. The command turns `Debug Print!` into `debug-print` and counts the entries that share it, open or closed.
- **The real one** → this repository's [failure log](../harness/failures.md). Its class `false-flag` failed a second time, and that entry says: "this is the second failure of the class, so it gets one a machine enforces". What it got is a test. A guard is whatever a machine runs. This repository has no guard file yet.

---

## The guard

Nothing forces a failure into the log. The briefing keeps an open one in view: every session start prints `Open failures: 2` and their titles, and the `brief` skill puts an open failure before new work.

The guard this page is about is the one the log produces. [Guards](guards.md) has the file. At `warn` it tells the agent and lets the write through (`run`):

```text
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "Vectoralis, guard `debug-print`: `src/cart.py`: A debug print is about to ship. Remove it or use the logger. The rule: the project's own guard `debug-print` (harness/guards/debug-print.json)."}}
```

You read the file and type `promote debug-print`. From then on the same write is stopped (`run`):

```text
BLOCKED by Vectoralis. Nothing was written.
- `src/cart.py`: A debug print is about to ship. Remove it or use the logger.
  Rule: the project's own guard `debug-print` (harness/guards/debug-print.json).
```

- **`yours`** blocks the agent's own write that would set the guard to `block`, change its pattern or set it back to `warn` (`run`). The block names the way out: `promote debug-print`, or `unlock harness/guards/debug-print.json`.
- **A guard without its proof does not run.** With one payload missing, `vectoralis guards` printed `NOT RUNNING`, and `vectoralis check` flagged it (`run`).

---

## What it costs

- **Tokens** → always loaded: the `failure` skill's description, 24 tokens, and one line of the briefing. `run`: `vectoralis budget`, an estimate of characters divided by four. The skill's body loads when a failure is logged. [Cost](cost.md)
- **Attention** → you read one guard file and type `promote`, once per guard. You read the log when you want to know why.

---

## In Claude Code

- `/heavy:failure`, or say what went wrong and the agent picks the skill from its description.
- The agent runs `vectoralis fail` and `vectoralis guards` by name.
- You promote with a plain message: `promote debug-print`.

## In Codex

- `$heavy:failure`, and the same `promote debug-print`.
- Codex's plugin docs name no folder that lands on the path. Call the CLI by its path: `~/.codex/plugins/cache/vectoralis/light/*/bin/vectoralis fail`.
- A guard on `write` reads the added lines of each file in a patch. Fed a patch in Codex's shape, the promoted guard blocked it (`run`). Not yet run in a Codex session. [Codex](codex.md)

`read`: [Claude Code skills](https://code.claude.com/docs/en/skills), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [the `$plugin:skill` form](https://learn.chatgpt.com/docs/security/plugin/changelog), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [where Codex keeps a plugin](https://developers.openai.com/plugins/build/plugins), 2026-11-11.

---

## What can go wrong

- **A guard for the instance, not the cause.** Here `false-flag` failed a third time after it had its test. The third entry says why: "Each earlier fix handled one place". Name the cause before you tick the third box.
- **A habit written down as a guard.** Here two commits went out while the check showed a flag. The entry says: "The guard was a habit, written down as if it were a mechanism." The fix was a pre-commit hook. [Checks](checks.md)
- **A pattern that hits good work.** That is why a new guard only warns, and why it carries a payload that must pass. Promote it after every warning was right.
- **A guard file changed through the shell.** `rm harness/guards/debug-print.json` is blocked before it runs, and a change the guard could not see is caught by the sweep when the agent stops (`run`: the guards' payloads). A guard file is changed with the edit tool, where the guard can read the change.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `run`: every output and every line marked so, printed by this repository's CLI and engine on a scratch project. `read`: how each agent calls a skill, finds the CLI and trusts a hook, in the docs linked above. The quotes are from this repository's failure log.
