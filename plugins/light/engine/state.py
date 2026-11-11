"""The state of one session: the turn's baseline, the files touched, the grants, what was already said.

One small JSON file, in the session's scratchpad when the agent names one, in the system's temp folder otherwise.
This module writes nothing to the project.
"""
from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path
from typing import Dict, Set

from .project import git

MAX_DIRTY = 500


def state_path(call) -> Path:
    if call.scratchpad and Path(call.scratchpad).is_dir():
        return Path(call.scratchpad) / "vectoralis.json"
    folder = Path(tempfile.gettempdir()) / "vectoralis"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / (re.sub(r"[^A-Za-z0-9_-]", "_", call.session or "session") + ".json")


def load(call) -> Dict:
    try:
        data = json.loads(state_path(call).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def save(call, state) -> None:
    try:
        state_path(call).write_text(json.dumps(state), encoding="utf-8")
    except OSError:
        pass


def snapshot(root) -> Dict:
    """The commit and the content of every changed file, so a turn's writes can be told apart later."""
    head = git(root, "rev-parse", "HEAD").strip()
    status = git(root, "status", "--porcelain", "-z", "--untracked-files=all")
    paths, parts, i = [], status.split("\0"), 0
    while i < len(parts):
        entry = parts[i]
        if len(entry) > 3:
            paths.append(entry[3:])
            if entry[0] in "RC":
                i += 1
        i += 1
    inside = bool(head or git(root, "rev-parse", "--git-dir").strip())
    if len(paths) > MAX_DIRTY:
        return {"head": head, "dirty": {}, "skipped": True, "git": inside}
    real = [p for p in paths if (Path(root) / p).is_file()]
    hashes = git(root, "hash-object", "--stdin-paths", stdin="\n".join(real) + "\n").split() if real else []
    dirty = dict(zip(real, hashes)) if len(hashes) == len(real) else {}
    for gone in set(paths) - set(real):
        dirty[gone] = "gone"
    return {"head": head, "dirty": dirty, "skipped": False, "git": inside}


def changed(root, base, now) -> Set[str]:
    """The project paths whose content differs between two snapshots."""
    if not base or base.get("skipped") or now.get("skipped"):
        return set()
    before, after = base.get("dirty") or {}, now.get("dirty") or {}
    out = {path for path, digest in after.items() if before.get(path) != digest}
    if base.get("head") and now.get("head") and base["head"] != now["head"]:
        out.update(p for p in git(root, "diff", "--name-only", base["head"], now["head"]).splitlines() if p)
    return out
