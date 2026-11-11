"""The tests pass before the agent says done.

Runs the project's test command at the end of a turn, only when something changed since the last green run.
"""
from __future__ import annotations

import hashlib
import re
import subprocess

from . import Finding
from ..project import git

NAME = "tests"
SIGNS = re.compile(r"FAILED|FAIL:|ERROR|Error:|error:|AssertionError|Traceback|✗|not ok")


def fingerprint(root):
    """The commit plus every uncommitted change, as one short value. None outside a git repository."""
    head = git(root, "rev-parse", "HEAD").strip()
    if not head and not git(root, "rev-parse", "--git-dir").strip():
        return None
    text = head + git(root, "status", "--porcelain") + git(root, "diff", "HEAD")
    return hashlib.sha1(text.encode("utf-8", "replace")).hexdigest()


def check(call, proj, state):
    if call.stop_active or not (state.get("changed") or state.get("shell")):
        return []
    command = str(proj.settings.get("test") or "").strip()
    seconds = int(proj.settings.get("test_timeout") or 120)
    mark = fingerprint(proj.root)
    if mark and state.get("green") == mark:
        return []
    try:
        done = subprocess.run(command, shell=True, cwd=str(proj.root), capture_output=True, text=True, timeout=seconds)
    except subprocess.TimeoutExpired:
        return [Finding(NAME, "notice", f"The tests ran out of time ({seconds} s), so they were not checked.")]
    except OSError as error:
        return [Finding(NAME, "notice", f"The test command could not run ({error}).")]
    if done.returncode == 0:
        state["green"] = mark
        return []
    lines = [line for line in (done.stdout + "\n" + done.stderr).splitlines() if line.strip()]
    tail = [line for line in lines if SIGNS.search(line)][:12] or lines[-12:]
    return [Finding(
        NAME, "block", "The tests fail, so the work is not done.\n" + "\n".join("    " + line for line in tail),
        "the tests pass before the agent says done (guard `tests`, the `test` command in harness/settings.json)",
        "fix what fails and run them again. If a failure is not yours to fix, say which one and why.",
    )]
