"""Work changed and no record moved. Said once, when the agent says it is done."""
from __future__ import annotations

import re

from . import Finding
from .sweep import moved

NAME = "nudge"
DONE = re.compile(r"(?i)\b(done|finished|complete[d]?|implemented|fixed|shipped|all set|ready)\b")


def check(call, proj, state):
    if call.stop_active or not state.get("base") or (state.get("turn") and state.get("nudged") == state.get("turn")):
        return []
    if call.last_message and not DONE.search(call.last_message):
        return []
    paths, _ = moved(proj, state)
    paths |= set(state.get("touched") or [])
    work = [p for p in paths if not p.startswith("harness/")]
    if not work or any(p.startswith("harness/") for p in paths):
        return []
    state["nudged"] = state.get("turn")
    return [Finding(
        NAME, "warn", f"{len(work)} file(s) changed this turn and no record moved.",
        "a box moves the moment its work is checked (guard `nudge`)",
        "move the box in harness/tracker.md or harness/todo.md, or say in one line why none applies.",
    )]
