# Locks

Finished work stays finished: a list of paths nothing may write to until you open one by name. Read this when a later task has broken something that already worked, or when a part of the project is live and must not move.

**Contents:** When to add it · The steps · The file · The guard · What it costs · In Claude Code · In Codex · What can go wrong

---

## When to add it

- A change for one task broke a part that was done and checked.
- A part is live, published, signed or paid for, so a slip is hard to undo.
- You want the agent free everywhere except in a few folders.

---

## The steps

1. A unit is finished for good → say so: `the refund webhook is live, lock src/payments`.
2. The agent adds one line to `harness/locks.md`: the path or the pattern in backticks, then the date and the reason.
3. From then on a write there is blocked, from an edit and from the shell.
4. Finished work must change → type `unlock` and the path. The grant lasts until your next message, and the lock closes by itself.
5. To remove a lock for good → `unlock` its pattern and ask for the line to go.

---

## The file

`harness/locks.md`, one line per lock. From a scratch project:

```markdown
- `src/payments/**` → locked 2026-11-11, the refund webhook is live
```

- `**` crosses folders, `*` stays inside one, and a bare folder covers everything in it (`run`: the unit test of the patterns).
- This repository's own [locks](../harness/locks.md) file is still empty: nothing in it is finished for good yet.

| You type | It opens, until your next message |
|---|---|
| `unlock src/payments/refund.py` | that file |
| `unlock src/payments` | everything under the folder |
| `unlock src/payments/**` | everything that lock covers |
| `unlock all` | every lock |

Each row is `run`. So are three that open nothing: `unlock src/cart.py` for a write to `src/payments/refund.py`, `please unlock it` with no path, and a machine's notice that says `unlock all`.

---

## The guard

**`locks`** blocks the write before it happens: an edit, and a shell command whose words show the target. `rm`, a redirect, `sed -i` and `git checkout` were each stopped, and a `grep` of the same file passed (`run`).

```text
BLOCKED by Vectoralis. Nothing was written.
- `src/payments/refund.py` is locked by `src/payments/**`.
  Rule: finished work is not written to (guard `locks`, harness/locks.md).
  Do instead: ask the person. They open it by typing `unlock src/payments/refund.py`.
```

**`sweep`** catches the write no words showed. A one-line script changed the file, and when the agent stopped it was sent back (`run`):

```text
NOT DONE YET, says Vectoralis.
- `src/payments/refund.py` changed this turn and it is locked by `src/payments/**`.
  Rule: a write made around the write guards is held to the same rules (guard `sweep`).
  Do instead: put it back as it was, then ask the person to type `unlock src/payments/refund.py`.
```

**`yours`** keeps the list itself. The agent may add a lock and reword a reason. Removing a line or changing its pattern is blocked, and a line removed through the shell is caught by the sweep (`run`).

---

## What it costs

- **Tokens** → one line of the briefing names the first five locks (`run`: `vectoralis status`). Nothing else is loaded.
- **Attention** → you type `unlock` when finished work must change. That is the cost and the point: the change becomes a decision.
- **Time** → the sweep compares the turn's start with its end, once, when the agent stops.

---

## In Claude Code

- Say what to lock. The agent writes the line with the `record` skill, by itself or when you type `/heavy:record`.
- Open one with a plain message: `unlock src/payments/refund.py and round the refund to cents`.
- A hook fires inside a subagent too, so a subagent's write meets the same lock. A write carrying a subagent's id was blocked the same way (`run`).

## In Codex

- `$heavy:record`, and the same `unlock` words.
- An edit arrives as one `apply_patch`. Fed to the engine in that shape, a patch to the locked file got the same block (`run`).
- At `Stop`, Codex turns the sweep's text into a new prompt and goes on. Not yet run in a Codex session. [Codex](codex.md)

`read`: [Claude Code hooks](https://code.claude.com/docs/en/hooks), [Claude Code skills](https://code.claude.com/docs/en/skills), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [the `$plugin:skill` form](https://learn.chatgpt.com/docs/security/plugin/changelog), 2026-11-11.

---

## What can go wrong

- **Your own controls, and the shell.** A `sed` on `harness/settings.json`, an `echo` into `harness/lessons.md` and an `rm` of a guard file are each blocked before they run, and a change made some other way is caught by the sweep when the agent stops (`run`: the guards' payloads). These files are changed with the edit tool, where the guard can read the change.
- **The sweep cannot always look.** Outside a git repository, or with more than 500 changed files in the tree, it has no baseline. It says so in one line and does not block (`run`: the guard's payload). The `locks` guard still blocks the edit. Commit or ignore build output.
- **A lock on nothing.** A renamed folder leaves its pattern behind. `vectoralis check` flags a lock that covers no file (`run`).
- **A lock too wide, or `unlock all` as a habit.** `src/**` stops the work, and `unlock all` opens everything for a message. Lock the finished unit, and name the path you open.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `run`: every output and every line marked so, printed by this repository's CLI and engine on scratch projects. `read`: that a hook fires in a subagent, how Codex trusts a hook and what it does with a `Stop` hook's answer, in the docs linked above.
