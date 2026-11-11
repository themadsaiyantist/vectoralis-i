"""A subagent reports. Only the main session writes a record."""
from __future__ import annotations

from . import Finding

NAME = "records"


def check(call, proj, state):
    if not call.subagent:
        return []
    out = []
    for write in call.writes:
        rel = proj.rel(write.path)
        if rel and rel.startswith("harness/"):
            out.append(Finding(NAME, "block", f"A subagent does not write a record (`{rel}`).",
                               "only the main session writes a record (guard `records`)",
                               "report it in your last message. The main session writes it."))
    return out
