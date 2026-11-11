# Light

A bug fix, a small feature, one sitting. Five steps, three guards, one settings file. Read this page, then give the agent its first task.

**Contents:** The five steps · The three guards · Set it up · One real run · When a guard speaks · What it costs · In Claude Code · In Codex · What can go wrong · When to switch

---

## The five steps

describe → plan in one line → edit → run the tests → commit

1. **Describe** → what you want, and how you will know it is done.
2. **Plan in one line** → ask for it. One line is enough to catch a wrong turn before it costs anything.
3. **Edit** → the agent makes the change, with a test.
4. **Run the tests** → the agent runs them. The `tests` guard runs them again when it stops.
5. **Commit** → one change, one commit.

---

## The three guards

| Guard | What it does | When |
|---|---|---|
| `secrets` | stops a key being written to a file, and a command that prints one | before the write, before the command |
| `format` | runs your formatter, and says when it rewrote the file | after every edit |
| `tests` | stops "done" while the tests fail | when the agent stops |

Nothing else is added. No tracker, no log, no subagent.

---

## Set it up

[Install](install.md) the `light` plugin → `/light:setup` in Claude Code, `$light:setup` in Codex. It writes one file, `harness/settings.json`:

```json
{
  "profile": "light",
  "test": ".venv/bin/python -m pytest -q",
  "test_timeout": 120,
  "format": "",
  "guards": {},
  "skip": {},
  "merge": "yours",
  "team": false
}
```

- It finds the test command and the formatter from the files your project already has. An empty one switches that guard off.
- A hook runs those two commands, so they are approved on your machine: by the setup when it found them itself, by `vectoralis trust` when the repository arrived with its own.
- Where no instructions file exists, it offers a starter: a twelve-line `AGENTS.md` with your commands, and a one-line `CLAUDE.md` that points at it. It never edits one you wrote.

---

## One real run

The project is [`runlog`](https://github.com/themadsaiyantist/runlog), a small command-line tool with ten tests. The task, as typed:

```text
Add a `count` command to this tool: it prints how many runs are in the file, and takes
--data like the other commands. Say your plan in one line first. Add a test for it.
When the tests pass, commit.
```

What happened:

- **The plan, in one line** → "find the existing CLI commands, add a `count` command that loads the file via `--data` and prints the number of runs, add a test, run the tests, then commit."
- **The edit** → `runlog/cli.py`, and a new `tests/test_count.py`.
- **The tests** → 12 passed.
- **The commit** → `feat: a count command`.
- **The guard, when the agent stopped** → one line for the person:

```text
Stop says: Vectoralis ran the tests after this turn's changes, and they pass (`.venv/bin/python -m pytest -q`).
```

Seven turns, 22 seconds, about 7 cents. `run`: Claude Code 2.1.322, Sonnet 5.5, 2026-11-11.

---

## When a guard speaks

**A token in a file.** The task asked for a GitHub token as a constant in `scripts/upload.py`. The write never happened. The agent was told:

```text
BLOCKED by Vectoralis. Nothing was written.
- `scripts/upload.py` would hold a GitHub token.
  Rule: no secret is written to a file or printed (guard `secrets`).
  Do instead: read the value from the environment, and keep it out of the repository.
```

It wrote the script to read `GITHUB_TOKEN` from the environment, and told the person to rotate the token they had pasted.

**Done, with failing tests.** The task changed what `best` returns and said to leave the tests alone. When the agent stopped, it was sent back:

```text
NOT DONE YET, says Vectoralis.
- The tests fail, so the work is not done.
    FAILED tests/test_best.py::test_best_run_has_the_highest_accuracy
    FAILED tests/test_best.py::test_best_command_prints_the_best_run
    FAILED tests/test_report.py::test_summary_names_the_count_and_the_best
  Rule: the tests pass before the agent says done (guard `tests`, the `test` command in harness/settings.json).
  Do instead: fix what fails and run them again. If a failure is not yours to fix, say which one and why.
```

It did not call the work done. It named the three tests, said why each fails, and asked which should change: the tests or the request.

Both are `run`, the same day, shortened to the lines that matter. Every block says three things: what was stopped → the rule → what to do instead.

---

## What it costs

- **Tokens** → 0 always loaded. A guard costs context only when it speaks.
- **Attention** → none until a guard speaks. One line when the tests pass.
- **Time** → the test suite runs once more at the end of a turn that changed something. It does not run when nothing changed.

---

## In Claude Code

- Start → `/light:setup`, once.
- Then work as you do. The guards run by themselves, also in a headless `claude -p` run.

## In Codex

- Start → `/hooks` to trust the hooks, then `$light:setup`, once.
- A Codex edit arrives as a patch. The guards read it the same way.

---

## What can go wrong

- **The agent guesses your commands.** In the first try of the run above there was no instructions file. The agent reached for `python`, which was not on the path, and could not run the tests. The starter file fixed it. Twelve lines.
- **The tests already fail before you start** → every turn ends in a block. Fix them first, or set `"tests": "warn"` under `guards` for now.
- **A slow suite** → raise `test_timeout`. Past it, the guard leaves a notice and does not block.
- **A repository that arrives with its own settings** → its test command does not run until you have read it and typed `vectoralis trust`. The guard tells you so.
- **An edit made through the shell** → the `secrets` guard reads a write and a command, not what a script does inside. Heavy adds a sweep at the end of the turn. [Guards](guards.md)

---

## When to switch

The moment one of [the five signals](start.md) is true → [Heavy](heavy.md).

Verified on Claude Code 2.1.322, 2026-11-11: every output above is `run`. The Codex lines are `read` in [its hooks docs](https://learn.chatgpt.com/docs/hooks).
