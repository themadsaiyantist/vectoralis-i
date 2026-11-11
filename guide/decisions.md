# Decisions and Exceptions

Every call that was made and every rule that was bent, each one dated, with the reason, in one file. Read this when the agent asks a question you already answered, or when a guard has to step aside for one path.

**Contents:** When to add it · The steps · The file · The guard · What it costs · In Claude Code · In Codex · What can go wrong

---

## When to add it

- The same question comes back in a new session.
- A choice was made in the chat, and a week later nobody knows why.
- A guard is right in general and wrong for one folder, and you are about to switch it off for everything.

---

## The steps

1. A call is made, by you or by the agent → one line under `## Decisions`: the date, the call in bold, then why.
2. Before the agent asks a question, it looks here. A call already made is followed, not asked again. [Plan](plan.md)
3. You grant an exception → one line under `## Exceptions`: the date, the rule it bends, why, its exact scope.
4. The exception excuses a path from a guard → the same path goes into `skip` in `harness/settings.json`. That file is yours, so you type `unlock harness/settings.json`.
5. An exception never widens on its own. A second path is a second line and a second grant.

---

## The file

`harness/decisions.md`, two lists, newest first. Two lines of this repository's own [decisions](../harness/decisions.md):

```markdown
- 2026-11-11 · **A grant is typed by the person, and lasts one message.** Why: the agent cannot forge the person's words, and a grant that outlives the request is a lock left open.
- 2026-11-11 · **`merge` is `agent` in this repository.** Why: the author's word, push without asking, while the repository is private.
```

Its `## Exceptions` list holds one word: `None.` An exception from a scratch project, and its line in the settings:

```markdown
- 2026-11-11 · **The `secrets` guard is excused in `tests/fixtures/`.** Bends: no secret is written to a file. Why: the scanner test needs keys in a known format, and every one is fake. Scope: that folder and nothing else.
```

```json
"skip": { "secrets": ["tests/fixtures/**"] }
```

- With that line, a fixture holding a fake key was written, and the same key in `src/config.py` was still blocked (`run`).
- `skip` excuses a path from a guard that reads files: `secrets`, `format`, `locks`, `yours`, `records` and `sweep`. A guard that reads a command or a whole turn has no path to excuse. [Guards](guards.md)

---

## The guard

No guard stands on the decisions file. The agent writes a decision the moment it is made, and that is the point. Three things stand around it:

- **`yours`** → the `skip` line lives in your settings, so the agent cannot excuse a path by itself. What it answered, `run`:

```text
BLOCKED by Vectoralis. Nothing was written.
- The settings are the person's: `skip` would change.
  Rule: this is the person's alone (guard `yours`).
  Do instead: ask them. They open the file by typing `unlock harness/settings.json`, or promote one guard by typing `promote` and its name.
```

- **`records`** → a subagent's write to the file is blocked (`run`). It reports, and the main session writes.
- **The staleness check** → a decision that names a file that is gone is flagged (`run`):

```text
$ vectoralis check
STALE: decisions.md: `src/basket.py` names nothing
1 flag(s).
```

---

## What it costs

- **Tokens** → nothing of the file is always loaded. Two skills send the agent to it, `plan` before it asks and `record` when a call is made: 22 tokens each for their descriptions. `run`: `vectoralis budget`, an estimate of characters divided by four.
- **Attention** → none for a decision. For an exception you read the scope and type one `unlock`.

---

## In Claude Code

- The agent writes a decision with the `record` skill, by itself or when you type `/heavy:record`.
- Grant an exception and open the settings in one message: `excuse tests/fixtures from secrets. unlock harness/settings.json`.
- The grant lasts until your next message. Read both lines before you send it.

## In Codex

- `$heavy:record`, and the same message for an exception.
- An edit to the settings arrives as a patch. Fed to the engine in Codex's shape, a changed setting got the same block (`run`).
- A gap: `records` knows a subagent by the `agent_id` Claude Code sends. Codex's docs list no such field for a tool hook.
- The guards run once you trust the hooks in `/hooks`. Not yet run in a Codex session. [Codex](codex.md)

`read`: [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude Code hooks](https://code.claude.com/docs/en/hooks), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [the `$plugin:skill` form](https://learn.chatgpt.com/docs/security/plugin/changelog), [Codex hooks](https://learn.chatgpt.com/docs/hooks), 2026-11-11.

---

## What can go wrong

- **An exception with no scope.** "Skip the formatter for now" becomes forever. Write the path and nothing wider, and the same path in `skip`.
- **A `skip` for a guard that reads no file.** `destructive`, `push`, `tests` and `nudge` judge a command or a turn, not a path, so a `skip` line for them changes nothing.
- **Two homes that disagree.** Nothing checks that every `skip` line has its entry here. Ask for both in the turn you type `unlock harness/settings.json`.
- **A decision nobody finds.** One line each, the call in bold. A paragraph is not read before a question is asked.
- **The settings changed through the shell.** A `sed` on `harness/settings.json` is blocked before it runs (`run`: the guard's payload). The settings are changed with the edit tool, after you type `unlock harness/settings.json`.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `run`: every output and every line marked so, printed by this repository's CLI and engine on a scratch project. `read`: how each agent calls a skill, what a tool hook receives and how Codex trusts a hook, in the docs linked above.
