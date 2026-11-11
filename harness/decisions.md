# Decisions

Every call that was made on Vectoralis I, and every exception to a rule, each one dated, with the reason. What the product contains is in `vectoralis-i.md`. This file holds how it is built, and why that way.

**Contents:** Decisions · Exceptions

---

## Decisions

Newest first. One line: the date, the call in bold, then why.

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
