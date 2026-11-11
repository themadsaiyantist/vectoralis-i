---
name: plan
description: Plan heavy work before the first edit. Every question in one round, the pick first.
---

# Plan

Every question is asked once, before the first edit. A question asked in the middle of the build stops the build.

## The steps

1. Split the work into units. A unit is one thing you can build and check on its own.
   - More than one big part → one row per unit in `harness/tracker.md`, one line per step in `harness/todo.md`.
2. List every call you cannot make alone:
   - taste → naming, voice, which of two good designs
   - hard to undo → deleting, moving, publishing, money
   - a conflict → two instructions disagree
   - unclear → the request reads two ways that lead to different work
3. Look for the answer first: `harness/decisions.md`, the project's instructions file, the code. A call already made is followed, not asked again.
4. Ask what is left, in one round:
   - the crucial few → in the chat or the question dialog, each with its options, your pick first
   - a longer round → one file at the project root, A as your pick and B as the strongest case against it, an `Answer:` line under each
5. A file handed over for answers is the person's until they say done. Do not edit it. A change goes in the chat.
6. Work that does not depend on an answer goes on. Work that does waits.
7. When the answers land → each goes to its home the same turn, dated. Then delete the question file.

## What a plan is not

- Not a document. The tracker rows and the to-do lines are the plan.
- Not a place for a minor call. Make it, and name it in the report.

**What to write where:** the units → `harness/tracker.md`. The steps → `harness/todo.md`. The answers → `harness/decisions.md`.
