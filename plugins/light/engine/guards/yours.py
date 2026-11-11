"""Three things stay the person's alone: ticking a box in their column, writing a lesson, opening a lock.

The same holds for the settings and the project's guards. The person gives each by typing it, and nothing else does.
"""
from __future__ import annotations

import json

from . import Finding
from .. import grants, records
from ..project import DEFAULT_MODES

NAME = "yours"
RULE = "this is the person's alone (guard `yours`)"
PROTECTED = ("guards", "skip", "merge", "profile", "test", "format", "test_timeout")
RANK = {"off": 0, "warn": 1, "block": 2}


def _json(text):
    try:
        data = json.loads(text or "")
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def check(call, proj, state):
    given = state.get("grants") or {}
    out = []

    def block(what, instead):
        out.append(Finding(NAME, "block", what, RULE, instead))

    for write in call.writes:
        rel = proj.rel(write.path)
        if rel is None or not rel.startswith("harness/"):
            continue
        name = rel[len("harness/"):]
        now = proj.read(name)
        if name in ("tracker.md", "todo.md") and write.after is not None:
            other = proj.read("todo.md" if name == "tracker.md" else "tracker.md")
            pair = (now, other) if name == "tracker.md" else (other, now)
            after = (write.after, other) if name == "tracker.md" else (other, write.after)
            for key in records.newly_ticked(records.yours_marks(*pair), records.yours_marks(*after)):
                unit = records.unit_of(key) or ""
                if not grants.ticked(given, unit):
                    block(f"The box of \"{unit}\" is the person's to tick.",
                          "ask them. They give it by typing `tick` and a few words of that line.")
        elif name == "lessons.md" and not given.get("lesson"):
            block("A lesson is written only when the person dictates it.",
                  "ask them. They start their message with `lesson:`.")
        elif name == "locks.md":
            gone = set(records.locks(now)) - set(records.locks(write.after if write.after is not None else ""))
            for lock in sorted(gone):
                if not (grants.unlocked(given, lock, lock) or grants.unlocked(given, rel)):
                    block(f"The lock on `{lock}` is the person's to open.",
                          f"ask them. They open it by typing `unlock {lock}`.")
        elif name == "settings.json" and proj.ready and not grants.unlocked(given, rel):
            before, after = _json(now) or {}, _json(write.after)
            if after is None:
                block("The edit would leave `harness/settings.json` unreadable.", "write the whole file as valid JSON.")
                continue
            changed = [k for k in PROTECTED if before.get(k) != after.get(k)]
            if changed == ["guards"]:
                old, new = before.get("guards") or {}, after.get("guards") or {}
                raised = [g for g in new if RANK.get(new[g], 1) > RANK.get(old.get(g, DEFAULT_MODES.get(g, "warn")), 1)]
                lowered = [g for g in set(old) | set(new)
                           if RANK.get(new.get(g, DEFAULT_MODES.get(g, "warn")), 1)
                           < RANK.get(old.get(g, DEFAULT_MODES.get(g, "warn")), 1)]
                if not lowered and all(grants.promoted(given, g) for g in raised):
                    continue
            if changed:
                block("The settings are the person's: " + ", ".join(f"`{k}`" for k in changed) + " would change.",
                      "ask them. They open the file by typing `unlock harness/settings.json`, "
                      "or promote one guard by typing `promote` and its name.")
        elif name.startswith("guards/") and name.endswith(".json"):
            before, after = _json(now), _json(write.after)
            guard = name[len("guards/"):-len(".json")]
            fresh = before is None and not (proj.harness / name).exists()
            mode = (after or {}).get("mode", "warn")
            if fresh and mode != "block":
                continue
            if grants.unlocked(given, rel):
                continue
            same = before is not None and after is not None and \
                {k: v for k, v in before.items() if k != "mode"} == {k: v for k, v in after.items() if k != "mode"}
            if (fresh or same) and mode == "block" and grants.promoted(given, guard):
                continue
            block(f"The guard `{guard}` is the person's to promote or change.",
                  f"ask them. They type `promote {guard}`, or `unlock {rel}` to let you edit it.")
    return out
