"""Read a hook payload from either agent and turn it into one shape, a Call.

This is the only module that knows which agent is calling.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

SHELL_TOOLS = ("Bash", "shell", "local_shell", "exec_command", "unified_exec")
PATCH_START = "*** Begin Patch"


@dataclass
class Write:
    """One file a call is about to change, or has changed."""

    path: str                     # absolute
    after: Optional[str] = None   # the whole file as the call leaves it, when that can be known
    added: str = ""               # only the new text
    deleted: bool = False


@dataclass
class Call:
    """One hook event, the same shape for Claude Code and for Codex."""

    event: str = ""
    agent: str = "claude"
    session: str = ""
    cwd: str = ""
    tool: str = ""
    writes: List[Write] = field(default_factory=list)
    command: str = ""
    prompt: str = ""
    subagent: bool = False
    stop_active: bool = False
    last_message: str = ""
    source: str = ""
    scratchpad: str = ""


def read_stdin() -> dict:
    """The payload on stdin, or an empty one when it cannot be read."""
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def build(event, data) -> Call:
    """A Call from an engine event name and a raw payload."""
    tool_input = data.get("tool_input") if isinstance(data.get("tool_input"), dict) else {}
    tool = str(data.get("tool_name") or "")
    codex = bool(os.environ.get("PLUGIN_ROOT")) and not os.environ.get("CLAUDE_PROJECT_DIR")
    call = Call(
        event=event,
        agent="codex" if codex or tool == "apply_patch" else "claude",
        session=str(data.get("session_id") or ""),
        cwd=str(data.get("cwd") or os.getcwd()),
        tool=tool,
        prompt=str(data.get("prompt") or ""),
        subagent=bool(data.get("agent_id")),
        stop_active=bool(data.get("stop_hook_active")),
        last_message=str(data.get("last_assistant_message") or ""),
        source=str(data.get("source") or data.get("trigger") or ""),
        scratchpad=str(data.get("scratchpad_dir") or ""),
    )
    command = tool_input.get("command")
    if isinstance(command, list):
        command = " ".join(str(part) for part in command)
    if event == "shell" or tool in SHELL_TOOLS:
        call.command = str(command or "")
    if event in ("write", "wrote"):
        call.writes = writes_of(tool, tool_input, call.cwd)
    elif PATCH_START in call.command:
        call.writes = patch_writes(call.command, call.cwd)
    return call


def _absolute(path, cwd) -> str:
    if not path:
        return ""
    target = Path(str(path))
    return str(target if target.is_absolute() else Path(cwd) / target)


def _current(path) -> Optional[str]:
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _replace(text, old, new, every) -> Optional[str]:
    if text is None or not old or old not in text:
        return None
    return text.replace(old, new) if every else text.replace(old, new, 1)


def writes_of(tool, tool_input, cwd) -> List[Write]:
    """Every file a write tool touches, with the text it adds and, when it can be known, the file after."""
    out: List[Write] = []
    if tool == "Write":
        text = str(tool_input.get("content", ""))
        out.append(Write(_absolute(tool_input.get("file_path"), cwd), text, text))
    elif tool == "Edit":
        path = _absolute(tool_input.get("file_path"), cwd)
        new = str(tool_input.get("new_string", ""))
        after = _replace(_current(path), str(tool_input.get("old_string", "")), new, tool_input.get("replace_all"))
        out.append(Write(path, after, new))
    elif tool == "MultiEdit":
        path = _absolute(tool_input.get("file_path"), cwd)
        text, added = _current(path), []
        for edit in tool_input.get("edits") or []:
            new = str(edit.get("new_string", ""))
            added.append(new)
            text = _replace(text, str(edit.get("old_string", "")), new, edit.get("replace_all"))
        out.append(Write(path, text, "\n".join(added)))
    elif tool == "NotebookEdit":
        path = _absolute(tool_input.get("notebook_path") or tool_input.get("file_path"), cwd)
        out.append(Write(path, None, str(tool_input.get("new_source", ""))))
    else:
        patch = next((v for v in tool_input.values() if isinstance(v, str) and PATCH_START in v), "")
        out.extend(patch_writes(patch, cwd))
    return [w for w in out if w.path]


def patch_writes(patch, cwd) -> List[Write]:
    """The files of one Codex patch: added, updated, moved or deleted."""
    out: List[Write] = []
    kind, path, body = "", "", []

    def close():
        if not path:
            return
        target = _absolute(path, cwd)
        added = "\n".join(line[1:] for line in body if line.startswith("+"))
        if kind == "Add":
            out.append(Write(target, added, added))
        elif kind == "Delete":
            out.append(Write(target, None, "", True))
        else:
            out.append(Write(target, _apply_hunks(_current(target), body), added))

    for line in patch.splitlines():
        head = line.strip()
        if head.startswith("*** ") and head.endswith(" Patch"):
            continue
        if head.startswith(("*** Add File:", "*** Update File:", "*** Delete File:")):
            close()
            kind, path, body = head.split()[1], head.split(":", 1)[1].strip(), []
        elif head.startswith("*** Move to:"):
            moved = head.split(":", 1)[1].strip()
            out.append(Write(_absolute(path, cwd), None, "", True))
            path = moved
        elif path:
            body.append(line)
    close()
    return out


def _apply_hunks(text, body) -> Optional[str]:
    """The file after a patch's hunks, or None when a hunk does not fit the file as it is."""
    if text is None:
        return None
    lines = text.split("\n")
    hunks, hunk = [], []
    for line in body:
        if line.startswith("@@"):
            if hunk:
                hunks.append(hunk)
            hunk = []
        elif line[:1] in (" ", "+", "-"):
            hunk.append(line)
    if hunk:
        hunks.append(hunk)
    start = 0
    for hunk in hunks:
        old = [line[1:] for line in hunk if line[:1] in (" ", "-")]
        new = [line[1:] for line in hunk if line[:1] in (" ", "+")]
        at = next((i for i in range(start, len(lines) - len(old) + 1) if lines[i:i + len(old)] == old), None)
        if at is None or not old:
            return None
        lines[at:at + len(old)] = new
        start = at + len(new)
    return "\n".join(lines)
