---
name: pr
description: Open a pull request and watch it to green, fixing what breaks.
---

# Pull request

Watched to green. A pull request you opened is yours until its last check passes.

1. Work on a branch, never on the default branch → `git switch -c short-name`.
2. Commit, then push the branch → `git push -u origin short-name`.
3. Open it → `gh pr create --fill`. Say what changed, what ran, and what was not verified.
4. Watch it to its last check → `gh pr checks --watch`. Do not leave it for the person to report back.
5. A red check → read its log with `gh run view --log-failed` → find the cause → fix it → push → watch again. The same turn, before new work.
6. What you cannot fix alone, a secret, a click, an outside service → tell the person at once, with the exact step.
7. Green → say so. The merge is the person's, unless `merge` is `agent` in `harness/settings.json`. Then `gh pr merge --squash`, once every check is green and never before.
8. A pull request that taught something → one line in `harness/decisions.md`: the break, its cause, the practice now.

**What to write where:** the box → `harness/tracker.md`, once it is merged. The lesson of a break → `harness/decisions.md`.
