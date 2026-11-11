# The To-do List

Everything left on the work, in order, in two lists that never mix: yours and the agent's. `## Now` sits on top and is the handoff. Read this when steps that wait on you get lost in the chat, or when a new session has to ask where things stand.

**Contents:** When to add it · The steps · The file · The guard · What it costs · In Claude Code · In Codex · What can go wrong

---

## When to add it

- The work will not fit in one session, and the next one has to start cold.
- Steps wait on you, a decision, a login, an approval, and nothing shows them in one place.
- A step of yours was marked done, and you never did it.

---

## The steps

1. Set up heavy → `/heavy:setup` in Claude Code, `$heavy:setup` in Codex. `vectoralis init heavy` writes `harness/todo.md` with three sections: `## Now`, `## Yours`, `## The agent's`.
2. Fill it with the agent: one line per step, ✅ or ⬜, a sequence written with →.
3. The agent ticks its own box the moment the step is checked, and adds a step the moment it is known.
4. You tick yours by typing `tick` and a few words of the line.
5. Before a session ends, the agent rewrites `## Now`: where it stands, what is next, what is open, the one trap to mind. [Handoff](handoff.md)
6. The next session starts on it. The briefing prints `## Now`, the agent's next three open boxes, and how many wait on you.

---

## The file

`harness/todo.md`. A few lines of this repository's own [to-do list](../harness/todo.md), as they stood on 2026-11-11:

```markdown
## Yours

- ✅ Say start
- ⬜ Say release → the repository goes public

## The agent's

- ✅ Light → three guards, one settings file
- ⬜ The kit → 19 situations
```

- A section is yours when its heading starts with `Your`: `## Yours`, or `## Yours, vegeta` in a [team](team.md). Every other section is the agent's.
- A done box may not name a file that is gone. An open box may name one that is not built yet.

What a session start prints from the list: the first eight lines of `vectoralis status`, `run` in a scratch project.

```text
VECTORALIS BRIEFING · heavy · branch main · 5 file(s) changed
Now:
  **Next →** the refund webhook → then the receipt email.
Tracker: 2 of 6 boxes done
Next for the agent:
  - Build the refund webhook
  - Write the receipt email
Open for the person: 2 · first: Approve the refund copy
```

---

## The guard

**`yours`** blocks the agent from ticking a box in your section. What it answered, `run`:

```text
BLOCKED by Vectoralis. Nothing was written.
- The box of "Approve the refund copy" is the person's to tick.
  Rule: this is the person's alone (guard `yours`).
  Do instead: ask them. They give it by typing `tick` and a few words of that line.
```

- `tick approve the refund copy` opens that one box, until your next message.
- The agent may add an open box to your list. That is how a step that waits on you reaches you.
- A new box that arrives already ticked is blocked like a tick (`run`).

---

## What it costs

- **Tokens** → `## Now` and the next boxes ride in the briefing, which is always loaded: about 190 tokens in a fresh project, about 240 once a scratch project had a handoff, two open failures and a lock. `run`: `vectoralis budget`, an estimate checked against live sessions.
- **Attention** → you tick your own boxes, and you read `## Now` when you come back.

---

## In Claude Code

- `/heavy:brief` turns the briefing into the session's goal, and `/heavy:handoff` rewrites `## Now`. The agent also picks both from the task.
- Your tick is a plain message: `tick approve the refund copy`.
- The briefing arrives by itself. Claude Code adds what a `SessionStart` hook prints to the context.

## In Codex

- `$heavy:brief` and `$heavy:handoff`. Your tick is the same words.
- The same hook prints the briefing, once you trust the hooks in `/hooks`. Codex adds a `SessionStart` hook's plain output as developer context.
- None of this was run in a Codex session yet. [Codex](codex.md)

`read`: [Claude Code hooks](https://code.claude.com/docs/en/hooks), [Claude Code skills](https://code.claude.com/docs/en/skills), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [the `$plugin:skill` form](https://learn.chatgpt.com/docs/security/plugin/changelog), 2026-11-11.

---

## What can go wrong

- **A section the guard does not know.** `## Vegeta` is not yours to the guard, and the agent's tick there passed (`run`). Start the heading with `Yours`.
- **A box deleted, not ticked.** The agent cannot remove an open box of yours either: the edit is blocked, and a removal through the shell is caught by the sweep (`run`: the guards' payloads).
- **`## Now` grows.** The briefing prints its first ten lines and drops the rest (`run`). Rewrite it, never append to it.
- **A tick through the shell.** `sed` goes around `yours`. The `sweep` guard finds the ticked box when the agent stops, and sends it back (`run`). [Locks](locks.md)
- **A done box that names a dead file.** `vectoralis check` flags the line until the path or the box is fixed (`run`). [Checks](checks.md)

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `run`: every output and every line marked so, printed by this repository's CLI and engine on a scratch project. `read`: what each agent does with a skill and with a session-start hook, in the docs linked above.
