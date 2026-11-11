# Failures

What went wrong on Vectoralis I and must not happen twice, the agent's failures and the author's alike. Read it before starting work and before logging a new entry. A failure is logged the same turn it is found.

**Contents:** How an entry is written · Traps ahead · Entries

---

## How an entry is written

- **A failure** is something that went wrong and was caught after the fact. A guard that refuses a write is the system working, and is not logged.
- **Facts only.** No apology, no blame. The author's failures are written exactly like the agent's.
- **Three boxes** → the instance fixed → the cause named → the guard in place. An entry closes when all three are ✅.
- **The class** is a short slug. The second entry of one class gets a guard a machine enforces.

```text
### ⬜ 2026-11-11 · Claude · What failed, in a few words

**Class.** `a-short-slug`

**What failed.** The facts, in one or two sentences.

**Cause.** Why it happened, not what happened.

**Fix.** ⬜ the instance · ⬜ the cause · ⬜ the guard
```

---

## Traps ahead

The hardest things in this work, each with what keeps us out of it.

| The trap | What keeps us out |
|---|---|
| A guard blocks good work | every guard ships with one payload that must block and one that must pass |
| A record falls behind the work | a box moves the moment its work is checked |
| Too much is loaded every session | hard caps: light 300 tokens, heavy 2,000 |
| A claim nothing backs | every fact carries its source or its run, and the date |
| A fact about an agent goes stale | every page closes with the versions and the date it was verified on |
| Everything is run when reading would do | check the docs first, run only what cannot be read |
| The scope grows without a record | a new part goes into the outline first, in the author's words |
| The kit turns into a directory | one pick and at most four more of each kind |
| A resource is paid, dead or not legal to share | free and legal first, a paid one marked with its price |
| Unannounced work leaks through git | the history is cleaned before the first push |

---

## Entries

Newest first.

### ✅ 2026-11-11 · Claude · A second reader found a hole the guard fix had opened, and older ways past the guard · closed 2026-11-11

**Class.** `claim-without-proof`

**What failed.** The fix for the sample rows was checked by its author and pushed. A reader who had not written it then went through the same code, five times as the fix grew. It found a hole the fix had opened: a moved row counted as kept when its box had not survived the move. It found a false block left behind: a section could not be renamed once the person had ticked a row in it. And it found ways past the guard that were older than the fix: a cell left blank, a column added after the person's, an Owner cell rewritten, a row hidden in a comment, a line of cells put above a header, a twin box standing in for the real one. Every pass also found a fault that the round before had opened, each one smaller than the last.

**Cause.** The proof was written by the hand that wrote the code, from the cases that hand had thought of. It is the cause of the two older entries of this class, a third time over. The author's own second read found one sibling. The second reader found the rest.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → a box is compared by where it sits: its row, its owner and the last column of its table, with twins lined up like with like and a moved row matched once. The reader takes a record the way a page shows it: the header above the row of dashes, the cell under the last header, a comment block up to its closer. 93 cases run through both guards and 15 through real commits, and all behave.
- The guard → what a machine holds: 52 new payloads and the tests beside them, most of which fail on the engine as it was. What it cannot hold is one line in `CLAUDE.md`: a change to a guard gets a second reader who did not write it, before it is called checked. What stays a limit is written in the guide: a record rewritten into another shape of Markdown, and a commit made under another person's name on the same machine.

### ✅ 2026-11-11 · Claude · Every commit was attributed to another GitHub account than the author's · closed 2026-11-11

**Class.** `wrong-identity`

**What failed.** All 37 commits made on this machine showed on GitHub under an account that is not `themadsaiyantist`. The author found it and said so. The pushes had gone out under the right account, so nothing looked wrong from here.

**Cause.** GitHub attributes a commit by its email, not by who pushes it. The machine's git identity carries an email that belongs to the other account, and it was never read before the first commit.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → this repository has its own git identity, `themadsaiyantist` with that account's no-reply address. The author and the committer of every commit were rewritten to it and pushed once, on the author's word. Trees, dates and messages were compared commit by commit first, and the old history is kept in a bundle outside the repository. One trace stays: pull request 1 lists its commit under the other account, and GitHub does not let that be rewritten.
- The guard → one line in `CLAUDE.md`: read `git config user.email` before the first commit in a repository, and after the first push ask GitHub who it thinks wrote it.

### ✅ 2026-11-11 · Claude · The fix for the sample rows let a to-do box move from one person's list to another's · closed 2026-11-11

**Class.** `fix-too-wide`

**What failed.** The first fix for the sample rows matched a box that left one place with one that arrived, by its words, in both records. In the to-do list that let an open box move from one person's list to another's without a word from either. It was on `main` for under an hour, and no live session met the case.

**Cause.** The fix was written for the tracker, where a section is an area of work, and applied to both records without asking what a section means in each. In the to-do list the section is the owner.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → the match by words holds for the tracker alone. In the to-do list a box that changed section is gone from its owner, and the guard blocks.
- The guard → a payload that moves one person's box into another's list and must block, and a unit test on the function. It was found by reading the fix again a different way before the last pass, which is the re-check the `check` skill asks for.

### ✅ 2026-11-11 · Claude · The builder and the agents skill assumed a worktree starts from the work in hand · closed 2026-11-11

**Class.** `unread-docs`

**What failed.** The `builder` subagent works in its own worktree, and the `agents` skill merges its branch after the check. Both took for granted that a worktree starts from the session's checkout. It starts from the remote's default branch. In the first live run both builders built on a base 79 files away from the work in hand, and their passing tests proved nothing about it. The session caught it by checking the reports, and took their files instead of their branches.

**Cause.** The page of Claude Code's docs on worktrees was not read when the subagent was written. Only the page on subagents was. The working rule says check the docs first, and one page short is not checked.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → the brief names the commit. The builder checks where it stands, goes there with a fast-forward, or builds nothing and says so. The setup skill offers the one setting that starts a worktree from the work in hand. A second live run started two commits behind, moved forward, and was merged after its check.
- The guard → the box that caught it. A skill or a subagent is ticked Checked only after a live session used it, and that box stayed open until one did. For every piece that leans on the agent, the docs page of the feature it leans on is read before the piece is called built.

### ✅ 2026-11-11 · Claude · The always-loaded cost on the pages was an estimate marked run, and a third too low · closed 2026-11-11

**Class.** `claim-without-proof`

**What failed.** The guide said heavy loads about 870 tokens before the first message, and a dozen pages gave a number for each piece, every one marked `run`. All of them came from `vectoralis budget`, which counted characters and divided by four. The spec said the guide's numbers come from a real session's context reading, and listed that reading as still to prove. The first reading showed 1,444 on a project one setup old and 1,746 on this repository. The pages were a third too low.

**Cause.** A stand-in was marked as the thing. `run` was written because a command had run, not because a session had been read. The rule of thumb was never checked once against the model it stands for.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → the estimate divides by 2.7 and counts each name with its list syntax. Three live sessions set the rate, and it reads within 2% of them. Every page that carried an old number carries the new one, and says where it comes from.
- The guard → the third failure of the class, so two things a machine holds. A unit test pins the estimate to the sessions that were measured. And this repository's first own guard, `harness/guards/rule-of-thumb-tokens.json`, warns when a guide page states the rule of thumb again. What a machine cannot hold stays a step: a `run` mark is written for a run of the thing itself.

### ✅ 2026-11-11 · Claude · The setup skill could not fill the first rows: the yours guard blocked the sample rows and a renamed section · closed 2026-11-11

**Class.** `false-flag`

**What failed.** `/heavy:setup` ran in a live session for the first time. Its fifth step fills the first rows of the tracker and the to-do list. The `yours` guard blocked it twice. Replacing the sample row that `vectoralis init` writes read as removing an open box of the person's. Renaming the sample section read as removing every open box in it. The agent stopped and said so both times, and the project was left with sample rows only the person could delete.

**Cause.** The guard's payloads were cut from its rule, not from the first minute of a new project. And the skill that leans on the guard had never been called in a live session, so the two had never met.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → a sample box that `init` wrote is nobody's until someone rewrites it, and a tracker row that only moved keeps its place by its words. A third live run of the skill finished clean: rows replaced, section renamed, `vectoralis check` clean, the harness committed.
- One sibling → the end-of-turn sweep judged a removed box by its own copy of the rule, and would have blocked the same work one turn later, when the person had run `init` first. Both guards now ask one function. That case ran live too, and ended clean.
- The guard → the fourth failure of the class. Nine payloads hold both sides: the sample row, the sample box and the renamed section pass, for the write guard and for the sweep, and a real box removed, a box ticked during a rename and a box moved out of its owner's list still block. Two tests walk from `init` to the first real rows, one through the write hook and one through a whole turn.

### ✅ 2026-11-11 · Claude · A script was edited while a background run was executing it, and the run started a second live session · closed 2026-11-11

**Class.** `edit-while-running`

**What failed.** A shell script that starts a headless session was edited while a background job was running it. A shell reads a script as it goes. When the first session ended, the shell read on from the middle of the new text and started the session a second time, with the same push rights on the copy of this repository. The second session found the work done and changed nothing. Its output replaced the transcript file of the first.

**Cause.** The script was treated as text at rest. A file that a running process still reads is part of that process.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → the first session's transcript was recovered from Claude Code's own store. The second session ran three read-only commands and wrote nothing, and `main` holds no commit of its own.
- The guard → one line in `CLAUDE.md`: a script a background job is running is not edited, a copy is.

### ✅ 2026-11-11 · Claude · A second review found the guards miss command forms the spec says they stop, and a hook ran commands nobody approved · closed 2026-11-11

**Class.** `claim-without-proof`

**What failed.** The subagent that wrote the safety page tried the guards as an attacker would. `bash -c 'git reset --hard'` and the same behind `env` passed. `rm -rf` on the home by its path only warned, where the spec says it blocks. `find . -delete` passed. `printenv` of a secret variable and a `grep` through `.env` passed. And the `test` and `format` commands of `harness/settings.json` ran inside a hook, with the person's access, with no approval, so a cloned repository could run anything.

**Cause.** The same as the entry below: the payloads proved the forms the author thought of, not the ones the spec's words cover. And the two commands were treated as the project's own, when the project may be someone else's.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → each form is now stopped, with a payload. A hook runs a command only after it was approved on this machine, and the approval lives in the home folder, where a repository cannot write it.
- The guard → the class failed twice, so it gets what a machine can hold: 106 payloads from 95, one for every form either review found. What a machine cannot hold stays a step: a page about a guard is written by someone who tried to get past it.

### ✅ 2026-11-11 · Claude · A review found thirteen gaps between what the spec says and what the engine does · closed 2026-11-11

**Class.** `claim-without-proof`

**What failed.** A subagent that wrote eight guide pages ran the real engine instead of trusting the spec, and found thirteen things wrong after the code was pushed. The worst: a shell command could switch a guard off in `harness/settings.json`, write a lesson or delete a project guard, and nothing spoke. The sweep went blind past 500 changed files without saying so, though the spec says it does. The spec said nobody's agent can tick another person's box, and nothing checked whose box it was. A version file with merge markers in it was rebuilt in silence and reported Clean. The engine's own block text, fed back as a prompt, parsed as a grant.

**Cause.** The spec was written first and the engine after it, and no one walked each sentence of the spec against a payload. The payloads proved what the code did, not what the spec promised.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → all thirteen are fixed. The person's files are closed to the shell and swept at the end of a turn. A row is ticked only in its owner's session. A broken version file is a flag. A guard's own answer is never read as the person's words.
- Every sibling → the eight pages that had documented the gaps were brought in line the same turn, and the spec's tables with them.
- The guard → each fix has a payload or a test that fails without it: 95 payloads and 37 tests, from 81 and 34. And a page is ticked only after someone ran the engine against what the page says.

### ✅ 2026-11-11 · Claude · The staleness check flagged a handoff line that names a page the tracker lists as not built · closed 2026-11-11

**Class.** `false-flag`

**What failed.** The third false flag of the check. The handoff said what comes next and named the page, which is not written yet. The check called the path dead. The pre-commit hook then refused the commit, which is the hook working and the check wrong.

**Cause.** Each earlier fix handled one place: first the tracker's rows, then the to-do list's open boxes. Nobody had written down what "planned" means, so each record got its own patch.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The cause → one definition, used by the staleness check and by the link check: a path the tracker lists with no box ticked is planned, and planned work is never stale.
- The guard → the test holds a handoff line that names a planned page, beside the two earlier cases.

### ✅ 2026-11-11 · Claude · A commit went out while the check still showed a flag, a second time · closed 2026-11-11

**Class.** `unread-check`

**What failed.** Two commits went out with `vectoralis check` reporting one flag. The first time the check's last line was printed and its exit code dropped. The entry above then said the commit step stops on a flag. It did not: the next commit ran the check on its own line, saw `1 flag(s)`, and committed anyway.

**Cause.** The guard was a habit, written down as if it were a mechanism. Nothing a machine ran stood between a failing check and the commit.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → the flagged file was checked again and affirmed.
- The guard → `tools/check.sh` runs every check and stops at the first failure. It is installed as the pre-commit hook here, and CI runs the same checks, so a commit cannot be made while one fails.

### ✅ 2026-11-11 · Claude · The staleness check flagged an open to-do line that names a file not built yet · closed 2026-11-11

**Class.** `false-flag`

**What failed.** One commit after the first false flag was fixed, `vectoralis check` flagged a new to-do line because it named a page that is still to be written. The commit went out with the check not clean, because the command that ran it only showed its last line and did not stop on its exit code.

**Cause.** The first fix covered the tracker and not the to-do list, though both hold work that is ahead. The sweep for siblings was skipped. And a check whose exit code nobody reads is not a check.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → an open box may name a file that is not built yet. A done box may not.
- Every sibling → the tracker and the to-do list are the two records that hold work ahead, and both are now covered. The rules and the decisions name only what exists.
- The guard → this is the second failure of the class, so it gets one a machine enforces: a test holds both cases for both records, and the commit step was meant to stop on a flag. It did not, see the entry above.
- What the fix turned up → the check then stopped the very commit that carried this fix, rightly: a ticked file had changed. That showed the rule under it was wrong too, `harness/decisions.md`, a tick refers to a recorded version.

### ✅ 2026-11-11 · Claude · The staleness check flagged every unit that was not built yet · closed 2026-11-11

**Class.** `false-flag`

**What failed.** `vectoralis check` reported a tracker row as stale when its file did not exist, even when no box of the row was ticked. A fresh tracker that lists the work ahead would have opened on a wall of flags. It was found the first time this repository ran its own check, after the code was pushed.

**Cause.** The check asked whether the file exists before it asked whether the row claims anything. Its test used a row with no box ticked, so the test agreed with the defect.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → a missing file is a flag only when a box of its row is ticked.
- The guard → the test now holds both cases: a ticked row whose file is gone must flag, a row not built yet must not.

### ✅ 2026-11-11 · Claude · An edit was lost in a file the author was typing in · closed 2026-11-11

**Class.** `handed-over-file`

**What failed.** The question round was patched while the author was answering in it. The author's save landed over the patch, and two stale lines stayed in the file.

**Cause.** A file handed to the author was still treated as the agent's to edit.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → the stale lines were named to the author and ignored when the answers were read.
- The guard → a file handed over for answers is the author's until they say done. A change goes in the chat, a rule now in `CLAUDE.md`.

### ✅ 2026-11-11 · Claude · A working rule was written into the outline as a rule of the product · closed 2026-11-11

**Class.** `wrong-home`

**What failed.** A rule the author meant for how the work runs was recorded in `vectoralis-i.md` and committed. The author corrected it in the next message.

**Cause.** The ruling was recorded at once, without asking where it belongs.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → the line was removed and the unpushed commit amended, so no commit holds it.
- The guard → what the product contains goes to the outline. How the work runs goes to `CLAUDE.md`, or stays out of the repository. When it is unclear which, ask.
