# Pull Requests

Watched to green. A pull request the agent opened is the agent's until its last check passes. Read this when work leaves your machine.

**Contents:** When to add it · The steps · The file · The guard · What it costs · In Claude Code · In Codex · What can go wrong

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

## What it costs

- **Tokens** → the `pr` skill is about 310 when it loads. No MCP server: `gh` is a command, and a command costs no context.
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

Verified 2026-11-11. The block is `run`. The steps are the `pr` skill of this repository.
