---
name: handoff
description: Write the handoff before a session ends, a clear or a compaction.
---

# Handoff

Three ways to carry a long session over. Pick by what must survive.

| The way | What survives | Use it when |
|---|---|---|
| Handoff, then a new session | exactly what the records say | the task changes, or the context is full of dead ends |
| Compact with a prompt | a summary shaped by your instructions | the same task goes on, and the thread matters |
| Auto compact | a summary shaped by the harness | nothing was done in time. The harness prints what to keep, right before |

## Write the handoff

Rewrite `## Now` in `harness/todo.md`, ten lines at most:

1. **Where it stands** → the box in hand, and how far it got.
2. **Next →** the very next step, exact enough to start cold.
3. **Open** → what waits on the person, what was not verified, any failure still open.
4. **Mind** → the one trap the next session would walk into.

Then check the records are true: every box that moved is moved, every call is in `harness/decisions.md`. A new session reads the files, not this conversation.

## Then

- A new session → the session start prints `## Now` again.
- A compaction with a prompt → say what to keep: the task, the boxes moved, the calls made, what was not verified.
- Before either, the records come first. A summary can drop a fact. A file cannot.

**What to write where:** only `## Now` in `harness/todo.md`.
