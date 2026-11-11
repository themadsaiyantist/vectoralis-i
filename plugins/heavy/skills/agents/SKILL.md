---
name: agents
description: Brief a subagent for parallel work. One owner per file, a worktree, then re-check its claim.
---

# Agents

Parallel work, without two hands on one file.

## When

- The work splits into units that do not depend on each other, and each costs more than a few tool calls.
- A search would flood this session with files it never needs.
- Not for one file. Not for steps that depend on each other. Not when you already hold the context the agent would have to rebuild. An agent starts cold.

## The brief

An agent knows only what the brief says. Give it all of this:

1. The goal, and what done looks like.
2. The files it owns. One owner per file. Two agents never edit one file.
3. The commit it starts from → `git rev-parse --short HEAD`.
4. The rules that bind it, in the person's own words where the person gave them.
5. What to report back: what changed, what ran and what it printed, what it could not verify.
6. That it never commits to the default branch, never asks the person, never writes in `harness/`.

## The run

- Edits that could collide → each agent in its own worktree. The `builder` subagent works in one.
- A worktree starts from the remote's default branch, not from your checkout. It starts from your work only when `.claude/settings.json` holds `"worktree": {"baseRef": "head"}`.
- A read-only second opinion → the `reviewer` subagent.
- Independent agents go out together, in one message.

## After

- An agent's "done" is a claim. Re-check every file it touched, with the `check` skill, before a box moves.
- You write the records. The agent reported, you verified.
- A worktree's branch is merged only after its check passed, and only when it started from your commit. Otherwise take its files, never its branch.

**What to write where:** the boxes → `harness/tracker.md`, by you, after the re-check.
