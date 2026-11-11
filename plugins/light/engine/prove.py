"""Prove the guards: run every guard's payloads in a temporary project and compare what happens with what must.

A payload file is `guards/payloads/<guard>.json`, a list of cases. `vectoralis guards` runs them all.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List

from . import grants, guards, records, trust
from .payload import Call, Write
from .project import Project
from .state import snapshot

RANK = {"pass": 0, "notice": 1, "warn": 2, "block": 3}
PAYLOADS = Path(__file__).resolve().parent / "guards" / "payloads"


def _text(parts) -> str:
    """A payload's text: a string, or pieces joined, so no real-looking key ever sits whole in a file."""
    if isinstance(parts, str):
        return parts
    return "".join(p if isinstance(p, str) else str(p["repeat"]) * int(p["times"]) for p in parts or [])


def _put(root, files):
    for name, text in (files or {}).items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if text is None:
            if path.exists():
                path.unlink()
        else:
            path.write_text(_text(text), encoding="utf-8")


def run_case(case) -> Dict:
    """One case: build the project, make the call, return what the guard answered."""
    with tempfile.TemporaryDirectory(prefix="vectoralis-") as folder:
        root = Path(folder).resolve()
        settings = {"profile": case.get("profile", "light"), "test": "", "format": ""}
        settings.update(case.get("settings") or {})
        _put(root, {"harness/settings.json": json.dumps(settings)})
        _put(root, case.get("files"))
        quiet = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
        if case.get("git"):
            identity = ["-c", "user.name=goku", "-c", "user.email=goku@example.com"]
            subprocess.run(["git", "init", "-q", "-b", "main", str(root)], **quiet)
            subprocess.run(["git", "-C", str(root), "add", "-A"], **quiet)
            subprocess.run(["git", "-C", str(root), *identity, "commit", "-q", "-m", "start"], **quiet)
            if case.get("person"):
                subprocess.run(["git", "-C", str(root), "config", "user.name", case["person"]], **quiet)
        kept = os.environ.pop("CLAUDE_PROJECT_DIR", None)
        kept_home = os.environ.get("VECTORALIS_HOME")
        os.environ["VECTORALIS_HOME"] = str(root.parent / (root.name + "-home"))
        try:
            proj = Project(str(root))
            if not case.get("unapproved"):
                trust.approve(proj)
            state = dict(case.get("state") or {})
            if "prompt" in case:
                state["grants"] = grants.parse(case["prompt"])
            if case.get("git"):
                state.setdefault("base", snapshot(root))
                state.setdefault("yours", records.yours_marks(proj.read("tracker.md"), proj.read("todo.md")))
                state.setdefault("locks", records.locks(proj.read("locks.md")))
            _put(root, case.get("then"))
            spec = case.get("call") or {}
            call = Call(event=case["event"], cwd=str(root), command=spec.get("command", ""),
                        subagent=bool(case.get("subagent")), last_message=case.get("last_message", ""))
            if "path" in spec:
                target = root / spec["path"]
                text = _text(spec.get("text", ""))
                if "old" in spec:
                    now = target.read_text(encoding="utf-8") if target.exists() else ""
                    call.writes = [Write(str(target), now.replace(_text(spec["old"]), text, 1), text)]
                else:
                    call.writes = [Write(str(target), text, text)]
            began = time.monotonic()
            found = [f for f in guards.run(case["event"], call, proj, state) if f.guard == case["guard"]]
            took = time.monotonic() - began
        finally:
            shutil.rmtree(os.environ["VECTORALIS_HOME"], ignore_errors=True)
            if kept_home is None:
                os.environ.pop("VECTORALIS_HOME", None)
            else:
                os.environ["VECTORALIS_HOME"] = kept_home
            if kept is not None:
                os.environ["CLAUDE_PROJECT_DIR"] = kept
    got = max((f.level for f in found), key=lambda level: RANK[level], default="pass")
    return {"name": case["name"], "guard": case["guard"], "event": case["event"], "expect": case["expect"],
            "got": got, "ok": got == case["expect"], "seconds": took}


def run_all() -> List[Dict]:
    """Every case of every built-in guard."""
    out = []
    for path in sorted(PAYLOADS.glob("*.json")):
        for case in json.loads(path.read_text(encoding="utf-8")):
            case.setdefault("guard", path.stem)
            out.append(run_case(case))
    return out


def unproven(results) -> List[str]:
    """The guards that lack a case that must act, or a case that must pass."""
    kinds: Dict[str, set] = {}
    for result in results:
        kinds.setdefault(result["guard"], set()).add("pass" if result["expect"] == "pass" else "act")
    names = {path.stem for path in PAYLOADS.glob("*.json")}
    return sorted(g for g in names if kinds.get(g, set()) != {"pass", "act"})
