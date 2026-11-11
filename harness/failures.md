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

### ✅ 2026-11-11 · Claude · The staleness check flagged an open to-do line that names a file not built yet · closed 2026-11-11

**Class.** `false-flag`

**What failed.** One commit after the first false flag was fixed, `vectoralis check` flagged a new to-do line because it named a page that is still to be written. The commit went out with the check not clean, because the command that ran it only showed its last line and did not stop on its exit code.

**Cause.** The first fix covered the tracker and not the to-do list, though both hold work that is ahead. The sweep for siblings was skipped. And a check whose exit code nobody reads is not a check.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → an open box may name a file that is not built yet. A done box may not.
- Every sibling → the tracker and the to-do list are the two records that hold work ahead, and both are now covered. The rules and the decisions name only what exists.
- The guard → this is the second failure of the class, so it gets one a machine enforces: a test holds both cases for both records, and the commit step now runs the check on its own line, so a flag stops the commit.
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
