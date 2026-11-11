# Failures

What went wrong on Vectoralis I and must not happen twice, the agent's failures and the author's alike. Read it before starting work and before logging a new entry. A failure is logged the same turn it is found.

**Contents:** How an entry is written · Traps ahead · Entries

---

## How an entry is written

- **A failure** is something that went wrong and was caught after the fact. A guard that refuses a write is the system working, and is not logged.
- **Facts only.** No apology, no blame. The author's failures are written exactly like the agent's.
- **Three boxes** → the instance fixed → the cause named → the guard in place. An entry closes when all three are ✅.
- **The same failure twice** gets a guard a machine enforces.

```text
### ⬜ 2026-11-11 · Claude · What failed, in a few words

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

### ✅ 2026-11-11 · Claude · An edit was lost in a file the author was typing in · closed 2026-11-11

**What failed.** The question round was patched while the author was answering in it. The author's save landed over the patch, and two stale lines stayed in the file.

**Cause.** A file handed to the author was still treated as the agent's to edit.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → the stale lines were named to the author and ignored when the answers were read.
- The guard → a file handed over for answers is the author's until they say done. A change goes in the chat, a rule now in `CLAUDE.md`.

### ✅ 2026-11-11 · Claude · A working rule was written into the outline as a rule of the product · closed 2026-11-11

**What failed.** A rule the author meant for how the work runs was recorded in `vectoralis-i.md` and committed. The author corrected it in the next message.

**Cause.** The ruling was recorded at once, without asking where it belongs.

**Fix.** ✅ the instance · ✅ the cause · ✅ the guard

- The instance → the line was removed and the unpushed commit amended, so no commit holds it.
- The guard → what the product contains goes to the outline. How the work runs goes to `CLAUDE.md`, or stays out of the repository. When it is unclear which, ask.
