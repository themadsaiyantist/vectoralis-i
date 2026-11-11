"""Which commands the person approved on this machine.

`test` and `format` in `harness/settings.json` are run by a hook, outside the agent's permission prompts.
A cloned repository can set them. So a command runs only after it was approved here, by `vectoralis init`
when it found the command itself, or by `vectoralis trust`. The record lives in the home folder,
never in the repository, so a repository cannot approve itself.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

KINDS = ("test", "format")


def home() -> Path:
    return Path(os.environ.get("VECTORALIS_HOME") or Path.home() / ".vectoralis")


def _load() -> Dict:
    try:
        data = json.loads((home() / "trusted.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _digest(command) -> str:
    return hashlib.sha1(command.encode("utf-8", "replace")).hexdigest()


def command(proj, kind) -> str:
    return str(proj.settings.get(kind) or "").strip()


def trusted(proj, kind) -> bool:
    """Whether this project's command, exactly as it is written now, was approved on this machine."""
    line = command(proj, kind)
    return not line or _load().get(str(proj.root), {}).get(kind) == _digest(line)


def approve(proj) -> List[Tuple[str, str]]:
    """Approve the project's commands as they are written now. Returns each kind with its command."""
    data, found = _load(), [(kind, command(proj, kind)) for kind in KINDS if command(proj, kind)]
    if not found and str(proj.root) not in data:
        return found  # nothing to approve, so nothing is written to the home folder
    data[str(proj.root)] = {kind: _digest(line) for kind, line in found}
    folder = home()
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "trusted.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return found
