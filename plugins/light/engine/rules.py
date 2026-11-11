"""The project's own guards, `harness/guards/<id>.json`: each one data, each one with its proof.

A guard without one payload that hits and one that passes, both behaving, does not run.
"""
from __future__ import annotations

import json
import re
from typing import Dict, List, Tuple

from .guards import Finding
from .project import matches


def load(proj) -> Tuple[List[Dict], List[str]]:
    """Every project guard that proved itself, and one line for each that did not."""
    good, bad = [], []
    folder = proj.harness / "guards"
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        try:
            rule = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            bad.append(f"harness/guards/{path.name} is not valid JSON")
            continue
        problem = proof(rule)
        if problem:
            bad.append(f"harness/guards/{path.name}: {problem}")
        else:
            rule.setdefault("id", path.stem)
            good.append(rule)
    return good, bad


def hits(rule, path, text) -> bool:
    if rule.get("on", "write") == "write" and rule.get("path") and not matches(str(rule["path"]), path or ""):
        return False
    return bool(re.search(str(rule.get("pattern", "")), text or "", re.M))


def proof(rule):
    """None when the guard's payloads behave, else what is wrong."""
    if not isinstance(rule, dict) or not rule.get("pattern") or not rule.get("message"):
        return "it needs a pattern and a message"
    if rule.get("on", "write") not in ("write", "shell") or rule.get("mode", "warn") not in ("warn", "block", "off"):
        return "`on` is write or shell, `mode` is warn, block or off"
    try:
        re.compile(str(rule["pattern"]))
    except re.error as error:
        return f"the pattern does not compile ({error})"
    seen = set()
    for case in rule.get("payloads") or []:
        want = case.get("expect")
        got = "hit" if hits(rule, case.get("path", ""), case.get("text", "")) else "pass"
        if want != got:
            return f"payload \"{case.get('name', '?')}\" expected {want} and got {got}"
        seen.add(want)
    return None if seen >= {"hit", "pass"} else "it needs one payload that hits and one that passes"


def check(call, proj, event) -> List[Finding]:
    out = []
    for rule in load(proj)[0]:
        mode = rule.get("mode", "warn")
        if mode == "off" or rule.get("on", "write") != event:
            continue
        texts = [(proj.rel(w.path) or "", w.added) for w in call.writes] if event == "write" else [("", call.command)]
        for path, text in texts:
            if hits(rule, path, text):
                where = f"`{path}`: " if path else ""
                out.append(Finding(rule["id"], mode, where + str(rule["message"]),
                                   f"the project's own guard `{rule['id']}` (harness/guards/{rule['id']}.json)",
                                   str(rule.get("instead", ""))))
    return out
