"""The end-of-turn sweep: a file changed around the write guards is judged here.

A shell command can write what no write guard saw. The sweep compares the turn's baseline with now.
"""
from __future__ import annotations

from pathlib import Path

from . import Finding, secrets
from .. import grants, records
from ..project import matches
from ..state import changed, snapshot
from .yours import BY_HAND

NAME = "sweep"
RULE = "a write made around the write guards is held to the same rules (guard `sweep`)"


def moved(proj, state):
    """The paths this turn changed, and the snapshot they were read from."""
    now = snapshot(proj.root)
    return changed(proj.root, state.get("base"), now), now


def check(call, proj, state):
    base = state.get("base")
    if call.stop_active or not base:
        return []
    paths, now = moved(proj, state)
    given = state.get("grants") or {}
    out = []
    if not base.get("git", True):
        if not state.get("no_git_said"):
            state["no_git_said"] = True
            out.append(Finding(NAME, "notice", "Vectoralis could not sweep this turn: the project is not a git repository, "
                                               "so a write made through the shell is not checked here."))
        return out
    if base.get("skipped") or now.get("skipped"):
        return [Finding(NAME, "notice", "Vectoralis could not sweep this turn: more than 500 files changed at once.")]
    for rel in sorted(paths - set(state.get("touched") or [])):
        if proj.skipped(NAME, rel):
            continue
        mine = rel in BY_HAND or rel.startswith("harness/guards/")
        allowed = grants.unlocked(given, rel) or (rel == "harness/settings.json" and state.get("init")) \
            or (rel == "harness/lessons.md" and given.get("lesson"))
        if mine and not allowed:
            out.append(Finding(NAME, "block", f"`{rel}` changed this turn outside the edit tool, and it is the person's.", RULE,
                               "put it back as it was. Then make the change with the edit tool, or ask them to open the file."))
            continue
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
    for key in records.removed_open(before, after):
        if not (grants.unlocked(given, "harness/todo.md") or grants.unlocked(given, "harness/tracker.md")):
            out.append(Finding(NAME, "block", f"An open box of the person's was removed this turn (\"{records.unit_of(key)}\").", RULE,
                               "put the line back as it was."))
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
