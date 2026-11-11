# Plan

The brief and the plan. Every question is asked once, before the first edit. Read this before any work with more than one part.

**Contents:** Why before the first edit · The brief · The plan · The question round · In Claude Code · In Codex · With the harness · What can go wrong

---

## Why before the first edit

- A question asked in the middle of a build stops the build, and you are not always there to answer.
- A wrong guess found at the end costs the whole run. Found in the plan, it costs one line.
- An agent that knows what done looks like can check itself. One that does not will tell you it is done.

---

## The brief

Four lines. Write them before the agent writes anything.

1. **The goal** → what you want, in your own words.
2. **Done** → a check a machine can run: a test, a command and what it must print.
3. **The edges** → what is in scope, and what must not change.
4. **What you already know** → the dead ends, the decision already made, the file to start from.

---

## The plan

- **Light** → one line, asked for in the task: "say your plan in one line first".
- **Heavy** → units, then questions.
  1. Split the work into units. A unit is one thing you can build and check on its own.
  2. One row per unit in the tracker, one line per step in the to-do list. The rows and the lines are the plan. There is no plan document to rot.
  3. List every call the agent cannot make alone: taste, hard to undo, a conflict, an unclear request.
  4. Look for the answer in the repository first. A call already made is followed, not asked again.

---

## The question round

Everything left is asked in one round.

- **The crucial few** → in the chat or the question dialog, each with its options, the pick first.
- **A longer round** → one file at the project root. A is the agent's pick. B is the strongest case against it. An `Answer:` line sits under each question, and a letter is enough.

```markdown
**2.4 The tracker's shape.**

- A. One row per unit of work, one column per stage. The last column is yours.
- B. A flat checklist. Simpler, but built and checked become one box.

Answer: a, and improve and refine if needed
```

- **"All A" is a valid answer.** The pick is there so you can skim.
- **The file is yours until you say done.** The agent does not edit it while you type. A change goes in the chat.
- **Each answer goes to its home the same turn**, dated: a decision or an exception to `harness/decisions.md`. Then the file is deleted.
- Work that does not depend on an answer goes on. Work that does waits.

The example is real: one of 25 questions asked before this repository was built, with the answer as it was typed.

---

## In Claude Code

- **Plan mode** keeps the agent to reading until you approve its plan. [Modes](modes.md)
- `/heavy:plan` runs the steps above. The agent also picks the skill by itself when the work has more than one part.

## In Codex

- `$heavy:plan` runs the same steps.
- The question file works the same way: it is a plain Markdown file.

---

## With the harness

| | Light | Heavy |
|---|---|---|
| The plan | one line, in the chat | the tracker rows and the to-do lines |
| The questions | in the chat | one round, in the dialog or in a file |
| The answers | in the chat | `harness/decisions.md`, dated |

---

## What can go wrong

- **A question that the repository already answers.** It costs the person a turn and teaches them to skim. Read `harness/decisions.md` first.
- **Questions that trickle in.** Three rounds of two are worse than one round of six. Hold them until the list is whole.
- **No pick.** A question with no recommendation hands the work back. Always say which one, and why.
- **An answer that stays in the chat.** It is gone at the next session. Write it down the same turn.

Verified 2026-11-11. The steps are the `plan` skill of this repository, [`plugins/heavy/skills/plan/SKILL.md`](../plugins/heavy/skills/plan/SKILL.md).
