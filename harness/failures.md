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
