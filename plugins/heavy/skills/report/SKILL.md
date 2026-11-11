---
name: report
description: Report at the end of a task. What changed, what ran, what was not verified.
---

# Report

The last step. Short, and honest about what is not known.

1. **What changed** → the files, and what each change does, in a few bullets.
2. **What ran, and what it printed** → the commands and their real output, a failing line in full.
3. **What was not verified** → by name. An unverified claim is said to be one.
4. **Every call made without asking** → one line each, so the person can veto it.
5. **What is next** → the next open box.

## The rules

- Lead with the result, not the story.
- If the tests fail, say so and show the output.
- If a step was skipped, say which one and why.
- No "should work". It ran, or it was not run.
- Then write the handoff with the `handoff` skill, so the report outlives the session.

**What to write where:** the report goes in the chat. `## Now` in `harness/todo.md` keeps what is next.
