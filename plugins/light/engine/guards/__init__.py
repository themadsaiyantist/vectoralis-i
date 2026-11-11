"""The guards: each one a small module with one `check`, each beside its payloads.

A guard answers with findings. A finding blocks, warns or leaves a notice for the person.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Finding:
    guard: str
    level: str          # block, warn or notice
    what: str           # what was stopped, or what was seen
    rule: str = ""      # the rule, and the file it lives in
    instead: str = ""   # what to do instead


def run(event, call, proj, state) -> List[Finding]:
    """Every finding of every guard that answers this event, in the mode the project set for each."""
    from . import destructive, fmt, locks, nudge, push, records, secrets, sweep, tests, yours
    from .. import rules

    order = {
        "write": (secrets, locks, yours, records),
        "shell": (secrets, destructive, locks, push),
        "wrote": (fmt,),
        "stop": (tests, sweep, nudge),
    }.get(event, ())
    guards = list(order)
    if event == "shell" and call.writes:
        guards += [g for g in (yours, records) if g not in guards]
    out: List[Finding] = []
    for guard in guards:
        mode = proj.mode(guard.NAME)
        if mode == "off":
            continue
        for finding in guard.check(call, proj, state):
            if mode == "warn" and finding.level == "block":
                finding.level = "warn"
            out.append(finding)
    if event in ("write", "shell") and proj.profile == "heavy":
        out.extend(rules.check(call, proj, event))
    return out
