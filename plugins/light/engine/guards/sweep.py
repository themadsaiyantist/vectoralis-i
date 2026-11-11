"""The end-of-turn sweep: a file changed around the write guards is judged here.

A shell command can write what no write guard saw. The sweep compares the turn's baseline with now.
"""
from __future__ import annotations

from pathlib import Path

from . import Finding, secrets
from .. import grants, records
from ..project import git, matches
from ..state import changed, snapshot
from .yours import BY_HAND

NAME = "sweep"
MAX_COMMITS = 400
RULE = "a write made around the write guards is held to the same rules (guard `sweep`)"


def moved(proj, state):
    """The paths this turn changed, and the snapshot they were read from."""
    now = snapshot(proj.root)
    return changed(proj.root, state.get("base"), now), now


def arrived(proj, base, now):
    """The boxes a teammate ticked in a commit of their own, which reached this checkout during the turn.

    A pull or a merge brings a teammate's tick with it. That tick was made in their session, under their rules, so
    it is not this turn's doing. Two things must hold. A commit that is not a merge, and whose committer is not the
    person at this machine, made the tick: an agent's own commit carries the machine's name as its committer,
    whatever author it claims. And the tick still stands between the two committed records, the one the turn began
    on and the one it ended on. Each such tick excuses one box, counted by where the box stood before the change,
    so a row that the turn also moved, or a section it renamed, is still known.
    """
    old, new = (base or {}).get("head"), (now or {}).get("head")
    if not old or not new or old == new or not proj.person:
        return {}
    names = ("harness/tracker.md", "harness/todo.md")

    def ticked(first, second):
        before, after = (records.yours_marks(*(git(proj.root, "show", f"{commit}:{name}") for name in names))
                         for commit in (first, second))
        return [place for _, place in records.ticked_places(before, after)]

    log = git(proj.root, "log", "--no-merges", "--format=%H%x1f%cn", f"{old}..{new}", "--", *names).splitlines()
    if len(log) > MAX_COMMITS:
        return {}
    made = set()
    for line in log:
        commit, _, committer = line.partition("\x1f")
        if commit and committer.strip().lower() != proj.person.lower():
            made.update(ticked(commit + "^", commit))
    standing: dict = {}
    for place in ticked(old, new):
        if place in made:
            standing[place] = standing.get(place, 0) + 1
    return standing


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
    before, after = records.aligned(state.get("yours") or {}, records.yours_marks(proj.read("tracker.md"), proj.read("todo.md")))
    open_file = grants.unlocked(given, "harness/todo.md") or grants.unlocked(given, "harness/tracker.md")
    for key in records.removed_open(before, after):
        if not open_file:
            out.append(Finding(NAME, "block", f"An open box of the person's was removed this turn (\"{records.unit_of(key)}\").", RULE,
                               "put the line back as it was."))
    for key, what in records.changed_place(before, after) if before else []:
        if not open_file:
            out.append(Finding(NAME, "block", records.PLACE_DONE[what].format(unit=records.unit_of(key)), RULE,
                               "put it back as it was, or ask the person to type `unlock harness/tracker.md`."))
    theirs = arrived(proj, base, now) if before else {}
    for key, place in records.ticked_places(before, after):
        unit = records.unit_of(key) or ""
        owner = records.owner_of(key, before.get(key) or after[key])
        other = bool(proj.settings.get("team") and owner and proj.person and owner.lower() != proj.person.lower())
        if not before:
            continue
        if other and theirs.get(place, 0) > 0:
            theirs[place] -= 1
            continue
        if other:
            out.append(Finding(NAME, "block", f"The box of \"{unit}\" was ticked this turn, and it is {owner}'s.", RULE,
                               "set it back to open, and tell them it is ready. Only their own session ticks it."))
        elif not grants.ticked(given, unit):
            out.append(Finding(NAME, "block", f"The box of \"{unit}\" was ticked this turn, and it is the person's.", RULE,
                               "set it back to open, then ask the person to type `tick` and a few words of that line."))
    for lock in sorted(set(state.get("locks") or []) - set(records.locks(proj.read("locks.md")))):
        if not grants.unlocked(given, lock, lock):
            out.append(Finding(NAME, "block", f"The lock on `{lock}` was removed this turn, and it is the person's.", RULE,
                               f"put the line back, then ask the person to type `unlock {lock}`."))
    return out
