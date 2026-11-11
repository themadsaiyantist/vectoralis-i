"""What the engine prints into the agent's context: the core and the briefing at session start, and the compaction prompt."""
from __future__ import annotations

from . import records
from .project import git

CORE_MAX = 6000


def status_text(proj, flags=None) -> str:
    """The briefing: where things stand, in a dozen lines. `flags` are the stale flags, found here when not given."""
    from . import checks

    todo, tracker = proj.read("todo.md"), proj.read("tracker.md")
    boxes = records.todo_boxes(todo)
    mine = [b for b in boxes if not b["yours"] and not b["done"]]
    yours = [b for b in boxes if b["yours"] and not b["done"]]
    marks = [m for row in records.tracker_rows(tracker) for m in row["marks"].values()]
    done, total = marks.count(records.DONE), marks.count(records.DONE) + marks.count(records.OPEN)
    fails = [f for f in records.failures(proj.read("failures.md")) if f["open"]]
    locks = records.locks(proj.read("locks.md"))
    if flags is None:
        flags = checks.stale(proj, seconds=0.15)
    branch = git(proj.root, "rev-parse", "--abbrev-ref", "HEAD").strip() or "no branch"
    dirty = len([line for line in git(proj.root, "status", "--porcelain").splitlines() if line.strip()])
    lines = [f"VECTORALIS BRIEFING · heavy · branch {branch} · {dirty} file(s) changed"]
    now = [line for line in records.section_text(todo, "Now").splitlines() if line.strip()][:10]
    if now:
        lines += ["Now:"] + ["  " + line for line in now]
    if total:
        lines.append(f"Tracker: {done} of {total} boxes done")
    if mine:
        lines += ["Next for the agent:"] + ["  - " + b["text"] for b in mine[:3]]
    lines.append(f"Open for the person: {len(yours)}" + (f" · first: {yours[0]['text']}" if yours else ""))
    lines.append("Open failures: " + (f"{len(fails)} · " + " · ".join(f["title"] for f in fails[:3]) if fails else "none"))
    lines.append("Locks: " + (", ".join(f"`{lock}`" for lock in locks[:5]) if locks else "none"))
    lines.append("Stale: " + (f"{len(flags)} · " + " · ".join(flags[:3]) if flags else "nothing"))
    lines.append("The person's alone: a box in their column, a lesson, a lock. They type `tick`, `lesson:` or `unlock`.")
    return "\n".join(lines)


def session_text(proj) -> str:
    """The always-loaded core, then the briefing."""
    core = proj.read("rules.md").strip()[:CORE_MAX]
    return ((core + "\n\n") if core else "") + status_text(proj) + "\n"


def compact_text(proj, state) -> str:
    """What a compaction must keep, written from the records and the session's state."""
    written = (state.get("written") or state.get("touched") or [])[:30]
    given = state.get("grants") or {}
    open_grants = [f"{verb} {target}" for verb in ("unlock", "tick", "promote") for target in given.get(verb, [])]
    lines = [
        "Keep these in the summary, in this order:",
        "1. The task in hand and its goal, in the person's own words.",
        "2. The boxes moved this session, and the next open box in harness/todo.md and harness/tracker.md.",
        "3. Every decision made, and every call made without asking.",
        "4. The files written this session" + (": " + ", ".join(written) if written else "."),
        "5. Every failure logged, and everything that was not verified.",
        "6. What the person allowed this turn" + (": " + ", ".join(open_grants) if open_grants else ": nothing") + ".",
        "Drop any tool output that a file already holds. The rules and the briefing are printed again after the compaction, and the records stay on disk in harness/.",
    ]
    return "\n".join(lines) + "\n"
