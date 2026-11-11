# Lessons

What you taught the agent after a failure, kept in your own words. An entry is written only when you type `lesson:`, and a guard holds the agent to that. Read this when you have corrected the same thing twice and want it kept the way you said it.

**Contents:** When to add it · The steps · The file · The guard · What it costs · In Claude Code · In Codex · What can go wrong

---

## When to add it

- You showed the agent an easier way, and the next session did not know it.
- A failure's cause was a judgment, and no pattern can check it.
- The agent's summary of what you said lost the point.

---

## The steps

1. Something goes wrong → it is logged first. [Failures](failures.md)
2. You teach → start a message, or a line of it, with `lesson:` and say it your way.
3. The agent writes one entry in `harness/lessons.md`, in your words, and adds nothing of its own.
4. Read the entry. The grant ends with your next message, so a correction needs `lesson:` again.
5. A lesson that must hold in every session → one line in `harness/rules.md`, which is always loaded. A lesson a machine can check → a guard. [Guards](guards.md)

---

## The file

`harness/lessons.md`, newest first. The shape `vectoralis init heavy` gives an entry:

```markdown
### 2026-01-01 · What it is about

**The failure.** What went wrong, and its entry in the failure log.

**The easier way.** What the person showed, in their words.

**Next time.** When this comes up, do that.
```

- **The failure** points at the log, so the lesson keeps its reason.
- **The easier way** is the part that is yours, word for word.
- This repository's own [lessons](../harness/lessons.md) hold no entry yet. Its failures are logged and closed, and the author has dictated no lesson, so the file is empty.

---

## The guard

**`yours`** blocks every write to the file unless your last message opened it. What it answered, `run`:

```text
BLOCKED by Vectoralis. Nothing was written.
- A lesson is written only when the person dictates it.
  Rule: this is the person's alone (guard `yours`).
  Do instead: ask them. They start their message with `lesson:`.
```

| Your message | The agent's write to the file |
|---|---|
| `lesson: use the logger, it is already imported everywhere` | passes |
| two lines, the second one starting with `lesson:` | passes |
| `write that down as a lesson please` | blocked |
| `here is a lesson: use the logger` | blocked, the word does not start a line |
| `thanks`, right after a lesson | blocked again |

- Each row is `run`: a message and a write, fed to this repository's engine.
- **`records`** blocks a subagent from writing the file, grant or no grant (`run`).
- The guard checks that you dictated. It cannot check what was written, so reading the entry stays yours.

---

## What it costs

- **Tokens** → nothing is always loaded, and nothing loads the file for you. The briefing has a line for the to-do list, the tracker, the failure log and the locks, and none for the lessons (`run`: `vectoralis status`).
- **Attention** → you dictate the lesson, and you read the entry once.

---

## In Claude Code

- Type it as a plain message: `lesson: use the logger, it is already imported everywhere`. There is no skill to call.
- To have the lessons read in every session, add one line to your `CLAUDE.md`. This repository's own does it for the failure log: "Read it before starting work."
- Vectoralis never edits that file. The line is yours to add.

## In Codex

- The same message, the same file. Both agents hand a hook your text in the `prompt` field, and the engine reads the grant from there.
- The line that sends the agent to the lessons goes in `AGENTS.md`.
- The guard runs once you trust the hooks in `/hooks`. Fed a patch in Codex's shape, a lesson nobody dictated got the same block (`run`). Not yet run in a Codex session. [Codex](codex.md)
- A gap: `records` knows a subagent by the `agent_id` Claude Code sends. Codex's docs list no such field for a tool hook.

`read`: [Claude Code hooks](https://code.claude.com/docs/en/hooks), [Codex hooks](https://learn.chatgpt.com/docs/hooks), 2026-11-11.

---

## What can go wrong

- **A lesson nobody reads.** No hook loads the file. Without the line in your instructions file, the agent opens it only when it thinks to.
- **The agent paraphrases.** The guard cannot tell your words from a summary. Read the entry while the message is fresh.
- **A lesson for what a machine can check.** A rule about a pattern belongs in a guard, which never forgets. Keep lessons for judgment.
- **A write through the shell.** An `echo` into the file is blocked before it runs, and the sweep catches what the guard could not see (`run`: the guards' payloads). A lesson is written with the edit tool, after you type `lesson:`.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `run`: every output and every line marked so, printed by this repository's engine on a scratch project. `read`: what a hook receives when you send a message, and how Codex trusts a hook, in the docs linked above.
