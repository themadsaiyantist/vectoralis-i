"""Answer one hook event: read the payload, run the guards, answer the agent.

Exit 0 passes. Exit 2 blocks, with the reason on stderr. Exit 1 means the engine itself broke and stepped aside.
"""
from __future__ import annotations

import json
import sys

from . import briefing, grants, guards, records
from . import state as states
from .payload import build, read_stdin
from .project import Project

HEAD = {
    "write": "BLOCKED by Vectoralis. Nothing was written.",
    "shell": "BLOCKED by Vectoralis. The command did not run.",
    "stop": "NOT DONE YET, says Vectoralis.",
}
HOOK = {"write": "PreToolUse", "shell": "PreToolUse", "wrote": "PostToolUse"}


def render(findings, event) -> str:
    """A block, as the agent reads it: what was stopped, the rule, what to do instead."""
    lines = [HEAD.get(event, "BLOCKED by Vectoralis.")]
    for finding in findings:
        lines.append(f"- {finding.what}")
        if finding.rule:
            lines.append(f"  Rule: {finding.rule}.")
        if finding.instead:
            lines.append(f"  Do instead: {finding.instead}")
    return "\n".join(lines) + "\n"


def note(finding) -> str:
    """A warning, as a plain fact the agent can weigh."""
    text = f"Vectoralis, guard `{finding.guard}`: {finding.what}"
    if finding.rule:
        text += f" The rule: {finding.rule}."
    if finding.instead:
        text += f" The usual fix: {finding.instead}"
    return text


def answer(event, findings) -> int:
    blocks = [f for f in findings if f.level == "block"]
    warns = [f for f in findings if f.level == "warn"]
    notices = [f for f in findings if f.level == "notice"]
    if blocks or (event == "stop" and warns):
        sys.stderr.write(render(blocks or warns, event))
        return 2
    out = {}
    if warns and event in HOOK:
        out["hookSpecificOutput"] = {"hookEventName": HOOK[event], "additionalContext": " ".join(note(f) for f in warns)}
    if notices:
        out["systemMessage"] = " ".join(f.what for f in notices)
    if out:
        sys.stdout.write(json.dumps(out) + "\n")
    return 0


def run(event) -> int:
    call = build(event, read_stdin())
    proj = Project(call.cwd)
    heavy = proj.profile == "heavy"
    if event == "session":
        if heavy:
            sys.stdout.write(briefing.session_text(proj))
        return 0
    state = states.load(call)
    if event == "compact":
        if heavy:
            sys.stdout.write(briefing.compact_text(proj, state))
        return 0
    if event == "prompt":
        given = grants.parse(call.prompt) if heavy else None
        if given is None:
            return 0
        state.update(
            grants=given, base=states.snapshot(proj.root), touched=[],
            yours=records.yours_marks(proj.read("tracker.md"), proj.read("todo.md")),
            locks=records.locks(proj.read("locks.md")), turn=int(state.get("turn") or 0) + 1,
        )
        states.save(call, state)
        return 0
    if event not in ("write", "shell", "wrote", "stop"):
        return 0
    findings = guards.run(event, call, proj, state)
    if event == "wrote":
        state["changed"] = True
        names = {proj.rel(w.path) for w in call.writes}
        state["touched"] = sorted(set(state.get("touched") or []) | {n for n in names if n})
    elif event == "shell":
        state["shell"] = True
    elif event == "stop" and not any(f.level == "block" for f in findings):
        state["changed"] = state["shell"] = False
    states.save(call, state)
    return answer(event, findings)


def main(argv) -> int:
    event = argv[0] if argv else ""
    try:
        return run(event)
    except Exception as error:  # a guard that breaks steps aside and says so, it never blocks on its own failure
        sys.stderr.write(f"vectoralis: the {event} hook broke and stepped aside ({type(error).__name__}: {error})\n")
        return 1
