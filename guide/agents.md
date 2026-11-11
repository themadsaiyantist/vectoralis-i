# Agents

Parallel work without two hands on one file: subagents, worktrees and workflows. Read this before you send a second agent into the same repository.

**Contents:** When · The brief · One owner per file · The two subagents · Workflows · The guard · One real run · What it costs · In Claude Code · In Codex · What can go wrong

---

## When

- The work splits into units that do not depend on each other, and each costs more than a few tool calls.
- A search would flood the session with files it never needs.

**Not** for one file. Not for steps that depend on each other. Not when the session already holds the context an agent would have to rebuild. An agent starts cold.

---

## The brief

An agent knows only what the brief says. Give it all of this:

1. The goal, and what done looks like.
2. The files it owns.
3. The commit it starts from. Commit first.
4. The rules that bind it, in the person's own words where the person gave them.
5. What to report: what changed, what ran and what it printed, what it could not verify.
6. That it never writes a record, never pushes, never asks the person.

---

## One owner per file

- Two agents never edit one file.
- Edits that could collide run in separate worktrees: each agent gets its own copy of the repository on its own branch.
- **A worktree starts from the remote's default branch**, not from your checkout. So a builder does not see your unpushed commits, unless one line in `.claude/settings.json` says otherwise: `"worktree": {"baseRef": "head"}`. `/heavy:setup` offers it. Either way it gets what is committed, never an edit that is not. Commit first.
- A worktree's branch is merged only after its check passed, and only when it started from your commit. Otherwise take its files, never its branch.
- **An agent's "done" is a claim.** The session that sent it re-checks every file it touched before a box moves.

---

## The two subagents

| Subagent | What it does | Limits |
|---|---|---|
| `reviewer` | the re-check, read with fresh eyes | cannot write or edit |
| `builder` | builds one unit it owns, in its own worktree | reports, never writes a record |

They ship with the `heavy` plugin, in [`plugins/heavy/agents/`](../plugins/heavy/agents/).

---

## Workflows

- A workflow is a script that sends several agents out in a fixed order: review, then verify each finding.
- Use one when the same fan-out runs again and again. For a one-off, send the agents by hand.
- It spends several times the tokens of one session. Ask for it by name. Never let it start by itself.

---

## The guard

`records` → a subagent that writes anything under `harness/` is blocked:

```text
BLOCKED by Vectoralis. Nothing was written.
- A subagent does not write a record (`harness/tracker.md`).
  Rule: only the main session writes a record (guard `records`).
  Do instead: report it in your last message. The main session writes it.
```

`run`: the guard's payload, on this repository, 2026-11-11.

---

## One real run

Two builders and the reviewer, on a scratch project whose remote was two commits behind the work in hand.

- **The brief named the commit.** The session ran `git rev-parse --short HEAD` and wrote the answer into both briefs.
- **Each builder checked where it stood**, and said so in its report:

```text
The worktree began at `2d7b983`, not `505dcdd`. `2d7b983` was an ancestor of `505dcdd`, so I moved
forward with `git merge --ff-only 505dcdd` instead of `git reset --hard`, and no work was discarded.
```

- **Each built its two files** and nothing else, ran the whole suite in its worktree, and committed on its own branch.
- **The session treated both reports as claims.** It sent the reviewer, which read both branches and found two defects in one unit. Both were fixed before the merge.
- **Then the records** → two rows ticked Built and Checked, by the session. No builder wrote under `harness/`.

A later run showed the net under the instruction. The session's own brief told the builders to get to its commit with `git reset --hard`. The `destructive` guard blocked that, and each builder went by a fast-forward, as its own steps say.

The run before these two is why a builder checks. The same two builders started on the remote's default branch, 79 files away from the work in hand. One tried `git reset --hard` to get there, and the `destructive` guard blocked it. The session refused to trust either report: it took only the four files the builders owned, and ran the tests itself.

`run`: Claude Code 2.1.322, Sonnet 5.5, headless, permission prompts off, 2026-11-11. Three minutes and 26 seconds, 69 cents.

---

## What it costs

- **Tokens** → each subagent's description is about 40, always loaded. Each agent you send starts its own context and fills it.
- **Attention** → you read one report per agent, and the main session re-checks.
- **The rule of thumb** → an agent pays for itself when its work would otherwise fill your session with files you never needed.

---

## In Claude Code

- The agent sends subagents itself. `/heavy:agents` loads the brief's steps.
- A subagent file sets its tools, its model and its isolation: `isolation: worktree` gives it its own copy.
- That copy starts from the remote's default branch. `"worktree": {"baseRef": "head"}` in `.claude/settings.json` starts it from your last commit.
- A hook sees a subagent's call, which is how `records` tells it from the main session.

`read`: [subagents](https://code.claude.com/docs/en/sub-agents.md) and [worktrees](https://code.claude.com/docs/en/worktrees.md), 2026-11-11. Agent teams are still experimental there, so this guide leaves them out.

## In Codex

- A Codex plugin cannot carry a subagent. Yours live in `.codex/agents/*.toml`, with `name`, `description` and `developer_instructions`.
- There is no worktree isolation for a subagent. Make the worktree yourself: `git worktree add ../unit-a -b unit-a`.
- A subagent cannot loosen the sandbox or the approval policy of its session.

`read`: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), 2026-11-11.

---

## What can go wrong

- **A cold brief.** The agent solves a nearby problem. Say what done looks like.
- **Two agents, one file.** One of them loses its work. Name the owner.
- **A claim taken as a fact.** The report said the tests pass. Run them.
- **A worktree on another base.** The builder's tests pass on code you do not have. Name the commit in the brief, and take files, never a branch, from a builder that started elsewhere.
- **A flood of agents.** Six agents on a task one could do spends six contexts. Send the second only when the first is not enough.

Verified 2026-11-11. The block and the real run are `run`. The agents' own features are `read`.
