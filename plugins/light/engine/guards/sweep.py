"""The end-of-turn sweep: a file changed around the write guards is judged here.

A shell command can write what no write guard saw. The sweep compares the turn's baseline with now.
"""
from __future__ import annotations

from pathlib import Path

from . import Finding, secrets
from .. import grants, records
from ..project import matches
from ..state import changed, snapshot

NAME = "sweep"
RULE = "a write made around the write guards is held to the same rules (guard `sweep`)"


def moved(proj, state):
    """The paths this turn changed, and the snapshot they were read from."""
    now = snapshot(proj.root)
    return changed(proj.root, state.get("base"), now), now


def check(call, proj, state):
    if call.stop_active or not state.get("base"):
        return []
    paths, _ = moved(proj, state)
    given = state.get("grants") or {}
    out = []
    for rel in sorted(paths - set(state.get("touched") or [])):
        for lock in records.locks(proj.read("locks.md")):
            if matches(lock, rel) and not grants.unlocked(given, rel, lock):
                out.append(Finding(NAME, "block", f"`{rel}` changed this turn and it is locked by `{lock}`.", RULE,
                                   f"put it back as it was, then ask the person to type `unlock {rel}`."))
                break
        path = Path(proj.root) / rel
        if path.is_file() and path.stat().st_size < 1_000_000 and not proj.skipped("secrets", rel):
            try:
                name = secrets.known(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                name = None
            if name:
                out.append(Finding(NAME, "block", f"`{rel}` now holds {name}.", RULE,
                                   "take the value out and read it from the environment."))
    before = state.get("yours") or {}
    after = records.yours_marks(proj.read("tracker.md"), proj.read("todo.md"))
    for key in records.newly_ticked(before, after):
        unit = records.unit_of(key) or ""
        if before and not grants.ticked(given, unit):
            out.append(Finding(NAME, "block", f"The box of \"{unit}\" was ticked this turn, and it is the person's.", RULE,
                               "set it back to open, then ask the person to type `tick` and a few words of that line."))
    for lock in sorted(set(state.get("locks") or []) - set(records.locks(proj.read("locks.md")))):
        if not grants.unlocked(given, lock, lock):
            out.append(Finding(NAME, "block", f"The lock on `{lock}` was removed this turn, and it is the person's.", RULE,
                               f"put the line back, then ask the person to type `unlock {lock}`."))
    return out
