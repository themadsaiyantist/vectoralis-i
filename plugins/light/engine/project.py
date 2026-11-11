"""The project the engine is working in: its root, its settings, its paths.

Reads `harness/settings.json`. Writes nothing.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, Optional

LIGHT = ("secrets", "format", "tests")
HEAVY = ("destructive", "locks", "yours", "records", "push", "sweep", "nudge")
DEFAULT_MODES = {
    "secrets": "block", "format": "warn", "tests": "block", "destructive": "block", "locks": "block",
    "yours": "block", "records": "block", "push": "block", "sweep": "block", "nudge": "warn",
}


def git(root, *args, timeout=10, stdin=None):
    """The output of one git command in `root`, or an empty string when it fails."""
    try:
        done = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, timeout=timeout, input=stdin
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return done.stdout if done.returncode == 0 else ""


def find_root(cwd=None):
    """The project root: the agent's project folder, else the git top level, else the working folder."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and Path(env).is_dir():
        return Path(env).resolve()
    start = Path(cwd or os.getcwd())
    if not start.is_dir():
        start = Path(os.getcwd())
    top = git(start, "rev-parse", "--show-toplevel").strip()
    return Path(top).resolve() if top else start.resolve()


def glob_regex(glob):
    """A glob as a regular expression: `**` crosses folders, `*` and `?` stay inside one."""
    out, i = [], 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif glob.startswith("**", i):
            out.append(".*")
            i += 2
        elif glob[i] == "*":
            out.append("[^/]*")
            i += 1
        elif glob[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def matches(glob, rel):
    """Whether a project path falls under a glob. A bare folder covers everything in it."""
    glob = glob.strip().rstrip("/")
    if not glob or rel is None:
        return False
    return bool(glob_regex(glob).match(rel)) or rel == glob or rel.startswith(glob + "/")


class Project:
    """One project: where it is, which profile it runs, how each guard is set."""

    def __init__(self, cwd=None):
        self.root = find_root(cwd)
        self.harness = self.root / "harness"
        self.settings: Dict = {}
        self.broken = False
        path = self.harness / "settings.json"
        self.ready = path.is_file()
        if self.ready:
            try:
                loaded = json.loads(path.read_text(encoding="utf-8"))
                self.settings = loaded if isinstance(loaded, dict) else {}
            except (OSError, ValueError):
                self.broken = True
        self.profile = "heavy" if self.settings.get("profile") == "heavy" else "light"
        self._tops: Dict[str, Optional[Path]] = {}

    def rel(self, path) -> Optional[str]:
        """A path as the project names it, also when the file sits in a worktree of the same repository."""
        target = Path(path)
        if not target.is_absolute():
            target = self.root / target
        target = Path(os.path.normpath(str(target)))
        for base in (self.root, self._top_of(target)):
            if base is None:
                continue
            try:
                return target.relative_to(base).as_posix()
            except ValueError:
                continue
        return None

    def _top_of(self, target):
        folder = target if target.is_dir() else target.parent
        while not folder.exists() and folder != folder.parent:
            folder = folder.parent
        key = str(folder)
        if key not in self._tops:
            top = git(folder, "rev-parse", "--show-toplevel").strip()
            self._tops[key] = Path(top).resolve() if top else None
        return self._tops[key]

    def mode(self, guard) -> str:
        """block, warn or off."""
        if guard == "tests" and not str(self.settings.get("test") or "").strip():
            return "off"
        if guard == "format" and not str(self.settings.get("format") or "").strip():
            return "off"
        if guard in HEAVY and self.profile != "heavy":
            return "off"
        chosen = (self.settings.get("guards") or {}).get(guard)
        return chosen if chosen in ("block", "warn", "off") else DEFAULT_MODES.get(guard, "warn")

    def skipped(self, guard, rel) -> bool:
        """Whether a path is excused from one guard."""
        globs = (self.settings.get("skip") or {}).get(guard) or []
        return any(matches(str(g), rel) for g in globs)

    def read(self, name) -> str:
        """The text of one record, or an empty string."""
        try:
            return (self.harness / name).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return ""
