# Pull Requests

Watched to green. A pull request the agent opened is the agent's until its last check passes. Read this when work leaves your machine.

**Contents:** When to add it · The steps · The file · The guard · One real run · What it costs · In Claude Code · In Codex · What can go wrong

---

## When to add it

- Someone else will review the work, or a pipeline will test it.
- The default branch is what ships.

---

## The steps

1. Work on a branch, never on the default branch → `git switch -c short-name`.
2. Commit, then push the branch → `git push -u origin short-name`.
3. Open it → `gh pr create --fill`. Say what changed, what ran, what was not verified.
4. **Watch it to its last check** → `gh pr checks --watch`. It is not left for the person to report back.
5. A red check → `gh run view --log-failed` → the cause → the fix → push → watch again. The same turn, before new work.
6. What the agent cannot fix alone, a secret, a click, an outside service → it tells the person at once, with the exact step.
7. Green → it says so. The merge is yours.

---

## The file

`harness/settings.json` holds one line for it:

```json
"merge": "yours"
```

- `yours` → the agent never pushes to the default branch and never merges.
- `agent` → it may merge its own pull request, once every check is green and never before.
- A break that taught something goes into `harness/decisions.md`: the break, its cause, the practice now.

---

## The guard

`push` → while the merge is yours:

```text
BLOCKED by Vectoralis. The command did not run.
- A push to `main` is the person's.
  Rule: the default branch moves on the person's word (guard `push`, `merge` in harness/settings.json).
  Do instead: push your own branch and open a pull request.
```

`destructive` blocks a forced push in every setting. Both are `run`: the guards' payloads, 2026-11-11.

---

## One real run

Pull request 1 of this repository, opened, watched and merged by a live session. `merge` is `agent` here.

- **The change** → the CI workflow ran green, but warned that two of its actions sat on a deprecated runtime. The session read both sets of release notes, then moved them to their current major version.
- **The commit was refused first.** The workflow's row in the tracker was ticked, and the file had changed:

```text
STALE: tracker: `.github/workflows/ci.yml` changed after its row was ticked
1 flag(s).
```

- **It did not record a check that had not happened.** It unticked the box on its branch, pushed, opened the pull request and watched it: two runs, green on Python 3.9, 3.12 and 3.13.
- **It read the run's log** for the warning the change was meant to remove, and found none. Then it merged, and ticked the row on `main`.
- **What it taught** went into `harness/decisions.md`: a workflow is proven by its pull request, and its box stays open until the run is green.

`run`: Claude Code 2.1.322, Sonnet 5.5, headless, 2026-11-11. Five minutes and 42 seconds, from the briefing to the handoff.

---

## What it costs

- **Tokens** → the `pr` skill is about 450 when it loads. No MCP server: `gh` is a command, and a command costs no context.
- **Attention** → you merge. Nothing before that, unless a check needs something only you have.
- **Time** → the agent waits on the pipeline. That is the point.

---

## In Claude Code

- `/heavy:pr`, or just ask for a pull request. A background watch keeps the session free while the checks run.

## In Codex

- `$heavy:pr`. The commands are the same: they are `git` and `gh`.
- In a `workspace-write` sandbox the network is off by default, so a push needs your approval.

`read`: [Codex approvals and sandbox](https://learn.chatgpt.com/docs/agent-approvals-security), 2026-11-11.

---

## What can go wrong

- **A pull request left red.** Nobody looks, and the work is done on paper only. Watch it.
- **A merge on a pending check.** Pending is not green.
- **Fixing the check, not the cause.** A skipped test is not a passing test.
- **A branch open across another merge.** It was tested against code that is gone. Update it, and watch again.

Verified 2026-11-11. The block and the real run are `run`. The steps are the `pr` skill of this repository.
