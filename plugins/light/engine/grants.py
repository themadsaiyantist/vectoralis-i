"""What only the person can give, read from the words they typed.

`unlock <path>`, `tick <unit>`, `lesson: <text>` and `promote <guard>`.
A grant lasts until the person's next message.
"""
from __future__ import annotations

import re
from typing import Dict, Optional

from .project import matches

NOTICE = re.compile(r"<task-notification>|\[SYSTEM NOTIFICATION|<cross-session-message|<system-reminder>", re.I)
VERB = re.compile(
    r"\b(?:(unlock|promote)\b[ \t]+(\S+)"
    r"|(tick)\b[ \t]+(.+?)(?=$|\n|[,.;!?](?:\s|$)|\s+and\s+(?:unlock|tick|promote)\b))",
    re.I | re.M,
)
LESSON = re.compile(r"^\s*lesson\s*:", re.I | re.M)
REFUSAL = re.compile(r"\b(not|never|no|dont|don't|do not|won't|n't)\W*$", re.I)


def is_notice(prompt) -> bool:
    """Whether a message is a machine's notice and not the person's own words."""
    return bool(NOTICE.search(prompt or ""))


def parse(prompt) -> Optional[Dict]:
    """The grants in one message, or None when the message is not the person's."""
    if is_notice(prompt):
        return None
    out = {"unlock": [], "tick": [], "promote": [], "lesson": bool(LESSON.search(prompt or ""))}
    for found in VERB.finditer(prompt or ""):
        if REFUSAL.search(prompt[max(0, found.start() - 12):found.start()]):
            continue
        verb = (found.group(1) or found.group(3)).lower()
        target = (found.group(2) or found.group(4)).strip().strip("`'\"").rstrip(".,!?:;").strip().strip("`'\"")
        if target:
            out[verb].append(target)
    return out


def unlocked(grants, rel, lock="") -> bool:
    """Whether the person opened this path, by naming it, a folder above it, its lock or `all`."""
    for target in (grants or {}).get("unlock", []):
        clean = target.strip().rstrip("/")
        if clean.lower() in ("all", "everything") or clean == lock or matches(clean, rel):
            return True
    return False


def ticked(grants, unit) -> bool:
    """Whether the person asked for this unit's box, by any words the unit's row holds."""
    plain = re.sub(r"[`*_]", "", unit or "").lower()
    for target in (grants or {}).get("tick", []):
        clean = re.sub(r"[`*_]", "", target).lower().strip()
        if clean in ("all", "everything") or (clean and clean in plain):
            return True
    return False


def promoted(grants, guard) -> bool:
    return any(t.strip().lower() in (guard.lower(), "all") for t in (grants or {}).get("promote", []))
