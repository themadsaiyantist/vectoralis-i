# Reference

Every command, file, guard, setting and word of this harness, on one page. Look things up here. The other pages say why.

**Contents:** The commands · The files · The guards · The settings · The words only you type · The events · The skills · The limits

---

## The commands

`vectoralis`, from the `light` plugin.

| Command | What it does |
|---|---|
| `vectoralis init light` | writes `harness/settings.json`, finds the test and format commands |
| `vectoralis init heavy` | adds the records. `--team` adds an owner column and a to-do section per person |
| `vectoralis init <profile> --starter` | also writes a starter `AGENTS.md` and a one-line `CLAUDE.md`, only where neither exists |
| `vectoralis status` | the briefing, as a session start prints it |
| `vectoralis check` | staleness, the budget and every guard's proof. Exit 1 on any flag |
| `vectoralis affirm <path>` | says a ticked file was checked again as it is now |
| `vectoralis guards` | every guard, its mode, and whether its payloads behave |
| `vectoralis budget` | what is always loaded, against the cap |
| `vectoralis dashboard` | writes `harness/dashboard.html` and prints its path |
| `vectoralis fail "title" --class slug` | adds an entry to the failure log. `--who` names whose it is |
| `vectoralis version` | the version |

---

## The files

All in `harness/`. Light keeps the first one alone.

| File | What it holds | Who writes it |
|---|---|---|
| `settings.json` | the profile, the commands, the guards' modes | you. The agent needs `unlock` |
| `rules.md` | how the work runs here, always loaded | both |
| `tracker.md` | the build state | the agent, and you for your column |
| `todo.md` | `## Now`, yours, the agent's | the agent, and you for your list |
| `failures.md` | what went wrong, its cause, its guard | the agent |
| `lessons.md` | what you taught | the agent, only on `lesson:` |
| `decisions.md` | decisions and exceptions | the agent |
| `locks.md` | finished work | the agent adds. Only you remove |
| `guards/<id>.json` | the project's own guards | the agent drafts at `warn`. You promote |
| `.checked.json` | which version each tick refers to | the harness. Never by hand |
| `dashboard.html` | the dashboard | the harness. Never committed |

---

## The guards

| Guard | Profile | When it runs | Default |
|---|---|---|---|
| `secrets` | light | before a write, before a command | block |
| `format` | light | after an edit | warn |
| `tests` | light | when the agent stops | block |
| `destructive` | heavy | before a command | block |
| `locks` | heavy | before a write, before a command | block |
| `yours` | heavy | before a write | block |
| `records` | heavy | before a write | block |
| `push` | heavy | before a command | block |
| `sweep` | heavy | when the agent stops | block |
| `nudge` | heavy | when the agent stops | warn |

What each one stops → [Guards](guards.md).

---

## The settings

`harness/settings.json`.

| Key | Values | What it does |
|---|---|---|
| `profile` | `light`, `heavy` | which guards run |
| `test` | a command | what the `tests` guard runs. Empty switches it off |
| `test_timeout` | seconds, 120 by default | past it, the guard leaves a notice |
| `format` | a command, `{file}` for the path | what the `format` guard runs. Empty switches it off |
| `guards` | a guard → `block`, `warn`, `off` | overrides a default |
| `skip` | a guard → a list of paths | excuses paths from one guard |
| `merge` | `yours`, `agent` | who may push to the default branch and merge |
| `team` | `true`, `false` | the team layout of the records |

---

## The words only you type

Each lasts until your next message. The agent cannot give itself one.

| You type | It allows |
|---|---|
| `unlock <path>` | a write to that locked path, or to `harness/settings.json` |
| `tick <a few words of the line>` | a box in your column |
| `lesson: <the lesson>` | one entry in `harness/lessons.md` |
| `promote <guard>` | that guard goes from warn to block |

"Do not unlock" and "never tick" give nothing. A machine's notice is never read as your words.

---

## The events

| The moment | Claude Code | Codex | What runs |
|---|---|---|---|
| A session starts | `SessionStart` | `SessionStart` | heavy prints the core and the briefing |
| You send a message | `UserPromptSubmit` | `UserPromptSubmit` | heavy reads the grants and takes the turn's baseline |
| Before a write | `PreToolUse` | `PreToolUse` on `apply_patch` | `secrets`, `locks`, `yours`, `records` |
| Before a command | `PreToolUse` on `Bash` | `PreToolUse` on the shell | `secrets`, `destructive`, `locks`, `push` |
| After an edit | `PostToolUse` | `PostToolUse` | `format` |
| The agent stops | `Stop` | `Stop` | `tests`, `sweep`, `nudge` |
| Before a compaction | `PreCompact` | `PreCompact` | heavy prints what the summary must keep |

---

## The skills

| Skill | Plugin | Who calls it |
|---|---|---|
| `setup` | light, heavy | you |
| `brief`, `plan`, `check`, `record`, `report`, `failure`, `agents`, `pr` | heavy | the agent |
| `handoff` | heavy | either |

Claude Code → `/heavy:check`. Codex → `$heavy:check`.

---

## The limits

| What | The limit |
|---|---|
| Always loaded, light | 300 tokens |
| Always loaded, heavy | 2,000 tokens |
| `harness/rules.md` | 60 lines |
| A skill's body | 60 lines |
| A guard's answer | 200 ms, the `tests` guard aside |
| Python | 3.9 or later, the standard library alone |

Verified 2026-11-11 against the code of this repository, [`plugins/light/engine/`](../plugins/light/engine/).
