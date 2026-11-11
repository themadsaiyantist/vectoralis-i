# Guards

Hooks used as guards: a rule a machine enforces. Read this when an instruction keeps being forgotten, or before you write a guard of your own.

**Contents:** What a guard is · The ten · Block or warn · The proof · A guard of your own · Switching one off · In Claude Code · In Codex · What can go wrong

---

## What a guard is

- A **hook** is a command the agent runs at a fixed moment: before a write, before a shell command, after an edit, when it stops.
- A **guard** is a hook that checks one rule and answers in one of four ways.

| The answer | When |
|---|---|
| Pass, in silence | nothing to say |
| Warn | the guard is not sure, or it is new |
| Block | a machine can be sure |
| Step aside, and say so | the guard itself broke. It never blocks on its own failure |

A block always says three things: what was stopped → the rule → what to do instead.

**A rule that is fixed and checkable by a machine becomes a guard. A rule that needs judgment stays an instruction.**

---

## The ten

| Guard | Profile | Blocks | Warns |
|---|---|---|---|
| `secrets` | light | a key in a known format written to a file, a command that prints a secrets file | a quoted value that only looks like a key |
| `format` | light | never | says when the formatter rewrote the file |
| `tests` | light | "done" while the tests fail | tells you when they pass, and when the suite ran out of time |
| `destructive` | heavy | `git reset --hard`, `git clean -f`, a forced push, `rm -rf` on the root, the home or `.` | `rm -r`, `git checkout --`, `git branch -D` |
| `locks` | heavy | a write to a locked path | |
| `yours` | heavy | your box ticked or removed, a lesson written, a lock opened, a guard promoted or switched off, by the agent with no grant, through an edit or through the shell | |
| `records` | heavy | a subagent writing a record | |
| `push` | heavy | a push to the default branch, a merge, while the merge is yours | |
| `sweep` | heavy | a file changed around the write guards that breaks `secrets`, `locks` or `yours` | says when it could not look |
| `nudge` | heavy | | work changed and no record moved, said once when the agent says done |

---

## Block or warn

- A guard blocks only what a machine can be sure of. A GitHub token has a format. "This looks risky" does not.
- A guard that blocks good work gets switched off, and then it protects nothing. So a new guard starts at `warn`.
- `sweep` runs at the end of a turn. A shell command can write what no write guard saw, so the sweep compares the turn's start with its end.

---

## The proof

Every guard ships with payloads: at least one that must be stopped, at least one that must pass.

```text
$ vectoralis guards
guard                 here    default  proof
secrets               block   block    15 of 15 payloads behave
format                off     warn     6 of 6 payloads behave
tests                 block   block    6 of 6 payloads behave
destructive           block   block    21 of 21 payloads behave
locks                 block   block    11 of 11 payloads behave
yours                 block   block    28 of 28 payloads behave
records               block   block    3 of 3 payloads behave
push                  block   block    6 of 6 payloads behave
sweep                 block   block    15 of 15 payloads behave
nudge                 warn    warn     4 of 4 payloads behave
rule-of-thumb-tokens  warn    project  its payloads behave
115 payloads, the slowest answer took 20 ms
```

`run` on this repository, 2026-11-11. The last row is this repository's own guard, drafted after a third failure of one class. A payload is plain JSON, in [`plugins/light/engine/guards/payloads/`](../plugins/light/engine/guards/payloads/).

---

## A guard of your own

One file, `harness/guards/<id>.json`. It runs in light and in heavy. It is data, so reading it takes a minute.

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

- `on` is `write` or `shell`. On `shell` the pattern is read against the command.
- **A guard without its proof does not run.** It needs one payload that hits and one that passes, both behaving.
- **It starts at `warn`.** In heavy you make it block by typing `promote debug-print`, and the agent cannot. In light nothing guards the file: set `"mode": "block"` yourself.
- [The kit](../kit/README.md) has a proven recipe for each kind of work.

---

## Switching one off

In `harness/settings.json`:

```json
"guards": { "tests": "warn", "nudge": "off" },
"skip": { "format": ["legacy/**"] }
```

- Each guard takes `block`, `warn` or `off`. `skip` excuses a path from one guard.
- In heavy, the settings are yours. The agent needs `unlock harness/settings.json` from you to change them.
- Write the reason in [`harness/decisions.md`](decisions.md), under Exceptions.

---

## In Claude Code

- The guards arrive with the plugin, in one `hooks/hooks.json`. They run in a headless `claude -p` session too.
- A guard sees a subagent's call, so `records` can tell the main session from a subagent.

## In Codex

- The same file. Codex runs a hook only after you trust it in `/hooks`, and asks again when it changes.
- An edit arrives as one patch. The guards read each file in it.
- Codex has no "ask" answer, so a guard here blocks or warns and never asks.

`read`: [Claude Code hooks](https://code.claude.com/docs/en/hooks.md), [Codex hooks](https://learn.chatgpt.com/docs/hooks), 2026-11-11.

---

## What can go wrong

- **A guard that blocks good work.** Promote only after it has warned for a while and every warning was right.
- **A guard nobody tested.** Without a payload that must pass, you find the false alarm in the middle of real work.
- **Routing around a block.** When a write is refused, the fix is the cause. Writing the same text through the shell is the same mistake, and the sweep finds it.
- **A guard is not a sandbox.** It stops honest mistakes. [Safety](safety.md)

Verified on Claude Code 2.1.322, 2026-11-11. The table is `run`. The Codex lines are `read`.
