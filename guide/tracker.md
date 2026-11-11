# The Tracker

The build state of a project as tables: one row per unit of work, one column per stage, ✅ or ⬜ in every cell and nothing else. Read this when the work has more units than one session can hold, or when a ✅ has been wrong once.

**Contents:** When to add it · The steps · The file · The guard · What it costs · In Claude Code · In Codex · What can go wrong

---

## When to add it

- The work will not fit in one session, so "where are we" has to live in a file.
- You asked "is that done?" and the answer was a paragraph.
- Someone else relies on the work, and needs to see what was checked and what was only built.

---

## The steps

1. Set up heavy → `/heavy:setup` in Claude Code, `$heavy:setup` in Codex. It runs `vectoralis init heavy`, which writes `harness/tracker.md` with one empty row.
2. Name the stages. The default is `Built`, `Checked`, `Yours`. The names are the project's, and the last column is always yours, whatever it is called.
3. Write one row per unit. Open the unit with its path in backticks, a file or a folder, and the row is bound to it.
4. The agent ticks a stage the moment its check passes, and the harness records which version of the file that tick refers to.
5. You tick your column by typing `tick` and a few words of the row.
6. The file changes later → `vectoralis check` flags the row → check it again and run `vectoralis affirm <path>`, or untick the box. [Checks](checks.md)

---

## The file

`harness/tracker.md`, one table under each `##` heading. Three rows of this repository's own [tracker](../harness/tracker.md), as they stood on 2026-11-11, before the skills had run in a live session:

```markdown
| Unit | Built | Checked | Yours |
|---|---|---|---|
| `plugins/light/engine/checks.py` the staleness check and the budget | ✅ | ✅ | ⬜ |
| `plugins/heavy/skills/` ten skills, used in a live session | ✅ | ⬜ | ⬜ |
| Codex: the hooks and the skills, in a live Codex session | ⬜ | ⬜ | ⬜ |
```

- ✅ is done and checked. ⬜ is not done. A blank cell does not apply, and is not counted.
- The first row is bound to a file, the second to a folder. The third names no path, so nothing watches it.
- A row with no box ticked is work ahead, and is never stale.
- **A tick refers to a version.** `harness/.checked.json` holds, for each bound row with a stage ticked, a hash of the file as it was at the tick. Content is compared, never dates, so it is right before a commit and after one. A file that changed after its tick, then was checked again, `run` in a scratch project:

```text
$ vectoralis check
STALE: tracker: `src/cart.py` changed after its row was ticked
1 flag(s).
$ vectoralis affirm src/cart.py
Recorded: `src/cart.py` was checked again as it is now.
```

---

## The guard

**`yours`** blocks the agent from ticking the last column. What it answered, `run`:

```text
BLOCKED by Vectoralis. Nothing was written.
- The box of "`src/cart.py` cart total" is the person's to tick.
  Rule: this is the person's alone (guard `yours`).
  Do instead: ask them. They give it by typing `tick` and a few words of that line.
```

- `tick cart total` opens that one box until your next message, and so does `tick src/cart.py`. `do not tick cart total yet` opens nothing.
- The words must stand in the row as you type them. `tick the endpoint for orders` opens nothing when the row says "the orders endpoint".
- **Your box cannot be taken away either.** An open row deleted, your cell left blank, the row hidden in a comment, a column added after yours: each one is blocked, through an edit and through the shell (`run`: the guard's payloads).
- **A row may move.** Rename a section, or move a row to another one, and its box goes with it, open or ticked. The sample row that `vectoralis init` wrote is nobody's, and is there to be replaced.

**`nudge`** speaks when work changed, no record moved and the agent says it is done. Once a turn, and it sends the agent back (`run`). The other guards → [Guards](guards.md).

```text
NOT DONE YET, says Vectoralis.
- 1 file(s) changed this turn and no record moved.
  Rule: a box moves the moment its work is checked (guard `nudge`).
  Do instead: move the box in harness/tracker.md or harness/todo.md, or say in one line why none applies.
```

---

## What it costs

- **Tokens** → always loaded: one line of the briefing, `Tracker: 2 of 6 boxes done`, and the `record` skill's description, about 39 tokens. `run`: `vectoralis budget`, an estimate checked against live sessions. The file itself is read when the agent opens it, and costs what it weighs. [Cost](cost.md)
- **Attention** → you tick your column, once per unit, and you read a stale flag when one appears.

---

## In Claude Code

- `/heavy:setup` once. After that the agent moves boxes with the `record` skill, by itself or when you type `/heavy:record`.
- Your tick is a plain message: `tick cart total`.
- The agent runs `vectoralis check` and `vectoralis affirm src/cart.py` by name. A plugin's `bin/` folder is on the path of its shell.

## In Codex

- `$heavy:setup` once, then `$heavy:record`. Your tick is the same words.
- Codex's plugin docs name no folder that lands on the path. Call the CLI by its path: `~/.codex/plugins/cache/vectoralis/light/*/bin/vectoralis check`.
- The guards run once you trust the hooks in `/hooks`. An edit arrives as one `apply_patch`. Fed to the engine in that shape, the same tick got the same block (`run`). Not yet run in a Codex session. [Codex](codex.md)

`read`: [Claude Code skills](https://code.claude.com/docs/en/skills), [plugin components](https://code.claude.com/docs/en/plugins/components), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [the `$plugin:skill` form](https://learn.chatgpt.com/docs/security/plugin/changelog), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [where Codex keeps a plugin](https://developers.openai.com/plugins/build/plugins), 2026-11-11.

---

## What can go wrong

- **`.checked.json` deleted, or left with merge markers.** With markers in it, `vectoralis check` says the file cannot be read and exits 1 (`run`). Deleted, it is rebuilt from the files as they are now, and every stale flag is gone. Commit it with the tracker, never delete it, and in a merge keep the lines of both sides.
- **A row that is not bound.** A unit with no path, or with a wildcard such as `src/**/*.py`, is not watched (`run`). Bind it to a file or a folder.
- **A cell that holds something else.** `WIP` in a cell is flagged by `vectoralis check`: a cell holds ✅, ⬜ or nothing (`run`). Make two rows, one done and one not.
- **A tick through the shell.** `sed` on the tracker goes around `yours`. The `sweep` guard finds the ticked box when the agent stops, and sends it back (`run`). [Locks](locks.md)

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `run`: every output and every line marked so, printed by this repository's CLI and engine on a scratch project. `read`: how each agent calls a skill, finds the CLI and trusts a hook, in the docs linked above.
