# Decisions

Every call that was made on Vectoralis I, and every exception to a rule, each one dated, with the reason. What the product contains is in `vectoralis-i.md`. This file holds how it is built, and why that way.

**Contents:** Decisions · Exceptions

---

## Decisions

Newest first. One line: the date, the call in bold, then why.

- 2026-11-11 · **A change to a guard gets a second reader who did not write it, before it is called checked.** Why: the author's own second read of the guard fix found one sibling. A reader who had not written it found seven things, one of them a hole the fix had opened.
- 2026-11-11 · **A box is where it sits: its row, its owner, and the last column of its table.** Why: a mark alone let a box go while its row stayed. A cell left blank, a column added after the person's, an Owner cell rewritten, a row hidden in a comment: each one now reads as the box taken away. A row that moves with all three unchanged keeps its box.
- 2026-11-11 · **In the tracker a section is an area of work. In the to-do list it is the owner.** Why: a tracker row keeps its box when its section is renamed. A to-do box does not change lists without its owner's word, so the guard matches a moved box by its words in the tracker alone.
- 2026-11-11 · **A builder is told its commit, and goes there or builds nothing.** Why: a worktree starts from the remote's default branch, and a result on another base proves nothing. A fast-forward is the only move it makes alone. `git reset --hard` stays blocked.
- 2026-11-11 · **The skills were proven in headless sessions: on a scratch project, and on a copy of this repository with the plugins loaded from their own folders.** Why: a session cannot load a plugin into itself, and a copy keeps a second writer out of the working tree. What the copy pushed came in through pull request 1.
- 2026-11-11 · **The budget counts 2.7 characters to a token, and ten more for each name in a list.** Why: three live sessions measured it. Light added 0, the descriptions 419, and two heavy projects 1,444 and 1,746, where four characters to a token read a third too low. The estimate lands within 2% of them. Another model counts differently, so the tool still says it is an estimate.
- 2026-11-11 · **A sample box that `init` wrote is nobody's, and a box that only moved was not removed.** Why: the first live run of `/heavy:setup` was blocked by the `yours` guard on both. The person's box is its words. Reworded or gone, the guard still blocks.
- 2026-11-11 · **CI follows `ubuntu-latest`.** Why: the live session asked it in `c.md`, the pick first, as the rules say. It is a minor call. The pick leaves the workflow as it is, and a red run says so the day a new image breaks it. Made without asking and named in the report. The file is folded into this line and deleted, and commit `bd3008e` keeps it.
- 2026-11-11 · **A workflow change is proven by its pull request, and its Built box stays unticked until the run is green.** Why: the commit step refuses a changed ticked file, and affirming before the run would claim a check that has not happened. `ci.yml` moved to `checkout@v7` and `setup-python@v7` (pull request 1, green on 3.9, 3.12 and 3.13, no Node.js 20 warning), after the release notes showed no break for push and pull_request runs.
- 2026-11-11 · **The people worth following are one table at the foot of the communities page, a row per topic, with no date per person.** Why: a fourth column does not fit the community tables, and the page's own form, a name → what it is good for, carries over. One line at the foot says when everyone was checked, as it does for the communities. Twenty-six dates would read as stale within a month.
- 2026-11-11 · **A hook runs only a command the person approved on this machine.** Why: `test` and `format` sit in a file a cloned repository can set, and a hook runs outside the agent's permission prompts. The approval lives in the home folder, so a repository cannot approve itself. It is the one file this harness keeps outside the project.
- 2026-11-11 · **Planned has one meaning: the tracker lists it and no box is ticked.** Why: three false flags came from three separate patches. The staleness check and the link check now ask the tracker.
- 2026-11-11 · **A tick refers to a recorded version of its file, not to a date.** Why: the first design compared git times. A file changed and checked again in one commit would have stayed flagged for good, because its row reads the same before and after. Content compared with content is right before a commit and after one.
- 2026-11-11 · **A row not built yet is never stale.** Why: a tracker lists the work ahead, and a check that flags it trains everyone to ignore the check. Found by running the check on this repository, `harness/failures.md`.
- 2026-11-11 · **A kit pick is marked `read` until it is tried.** Why: the author's word, run only what cannot be read. The mark keeps the page honest.
- 2026-11-11 · **The handoff is `## Now` in the to-do list, not a file of its own.** Why: one fact has one home, and the session start already prints it.
- 2026-11-11 · **The nudge speaks only when the agent says done.** Why: a build that runs over several turns leaves the tracker alone on purpose, and a guard that interrupts it is noise.
- 2026-11-11 · **A guard that breaks steps aside.** Why: a crash is not something a machine can be sure of. It says so in one line and never blocks.
- 2026-11-11 · **A grant is typed by the person, and lasts one message.** Why: the agent cannot forge the person's words, and a grant that outlives the request is a lock left open.
- 2026-11-11 · **One hooks file for both agents, in shell form.** Why: Codex reads `command` alone, and it sets `CLAUDE_PLUGIN_ROOT` as Claude Code does.
- 2026-11-11 · **One engine, in light. Heavy carries no code.** Why: a plugin cannot reach another plugin's files, and a second copy would drift.
- 2026-11-11 · **`merge` is `agent` in this repository.** Why: the author's word, push without asking, while the repository is private.

---

## Exceptions

Newest first. Each one names the rule it bends, why, and its exact scope. It never widens on its own.

None.
