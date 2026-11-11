"""The staleness check and the budget: is every record still backed by the repository, and is the core still small.

Keeps one generated file in the project, `harness/.checked.json`: which version of each bound file its ticks refer to.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import time
from pathlib import Path
from typing import Dict, List

from . import records, rules
from .project import git, matches

CAPS = {"light": 300, "heavy": 2000}
# Characters to one token, and the list syntax around one skill or subagent. Measured, not assumed: three live
# Claude Code sessions on Sonnet 5.5, 2026-11-11, where this estimate came within 2% of what the model was sent.
# Four characters to a token, the usual rule of thumb, read a third too low on this kind of text.
CHARS_PER_TOKEN, LISTING = 2.7, 10
CHECKED = "harness/.checked.json"
MAX_FILES = 3000
RECORDS = ("rules.md", "tracker.md", "todo.md", "failures.md", "lessons.md", "decisions.md", "locks.md")
PATHLIKE = re.compile(r"`([^`\s]+/[^`\s]*)`")


def blob(path) -> str:
    """The content of a file, or of every file under a folder, as one short value."""
    path = Path(path)
    if path.is_dir():
        total = hashlib.sha1()
        files = sorted(f for f in path.rglob("*") if f.is_file() and "__pycache__" not in f.parts)
        for found in files[:MAX_FILES]:
            total.update(found.relative_to(path).as_posix().encode("utf-8"))
            total.update(hashlib.sha1(found.read_bytes()).digest())
        return total.hexdigest()
    return hashlib.sha1(path.read_bytes()).hexdigest()


def ticked_rows(proj) -> Dict[str, Dict]:
    """Every tracker row that is bound to a path and has a stage ticked, by its path."""
    out = {}
    for row in records.tracker_rows(proj.read("tracker.md")):
        path = row["path"]
        if not path or any(c in path for c in "*?"):
            continue
        stages = [mark for name, mark in row["marks"].items() if name != row["yours_stage"]]
        if records.DONE in stages:
            out[path.rstrip("/")] = row
    return out


def load_checked(proj) -> Dict[str, str]:
    """Which version of each bound file its ticks refer to."""
    try:
        data = json.loads((proj.root / CHECKED).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def checked_broken(proj) -> bool:
    """Whether the version file is there and cannot be read, as after a merge that left its markers in."""
    target = proj.root / CHECKED
    if not target.is_file():
        return False
    try:
        return not isinstance(json.loads(target.read_text(encoding="utf-8")), dict)
    except (OSError, ValueError):
        return True


def save_checked(proj, data) -> None:
    target = proj.root / CHECKED
    if data:
        target.write_text(json.dumps(dict(sorted(data.items())), indent=2) + "\n", encoding="utf-8")
    elif target.exists():
        target.unlink()


def sync(proj) -> List[str]:
    """Record the version of every newly ticked file, and forget the ones no longer ticked. Returns what was recorded."""
    if checked_broken(proj):
        return []
    rows, data = ticked_rows(proj), load_checked(proj)
    fresh = [path for path in rows if path not in data and (proj.root / path).exists()]
    kept = {path: mark for path, mark in data.items() if path in rows}
    for path in fresh:
        kept[path] = blob(proj.root / path)
    if kept != data:
        save_checked(proj, kept)
    return fresh


def affirm(proj, paths) -> List[str]:
    """Say that these ticked files were checked again as they are now. Returns the ones recorded."""
    rows, data = ticked_rows(proj), load_checked(proj)
    done = []
    for path in paths:
        key = (proj.rel(path) or str(path)).rstrip("/")
        if key in rows and (proj.root / key).exists():
            data[key] = blob(proj.root / key)
            done.append(key)
    if done:
        save_checked(proj, data)
    return done


def _names(text) -> List[str]:
    return [re.sub(r"[^a-z0-9]+", "", re.sub(r"^\d+\.?\s*", "", n.lower())) for n in text]


def stale(proj, seconds=None) -> List[str]:
    """Every flag: a record that says something the repository no longer backs.

    A ticked row is stale when its file no longer is what it was when the row was ticked.
    With `seconds`, that comparison stops when the time is up.
    """
    start, flags = time.monotonic(), []
    checked = load_checked(proj)
    if checked_broken(proj):
        flags.append("harness/.checked.json cannot be read. Fix it by hand, or delete it and run the check again: "
                     "every tick is then recorded against the files as they are now")
    for row in records.tracker_rows(proj.read("tracker.md")):
        for stage, mark in row["marks"].items():
            if stage.lower() != "owner" and mark not in (records.DONE, records.OPEN, ""):
                flags.append(f"tracker: the cell of \"{row['unit']}\" under {stage} holds `{mark}`. "
                             f"A cell holds {records.DONE}, {records.OPEN} or nothing")
    for path in ticked_rows(proj):
        target = proj.root / path
        if not target.exists():
            flags.append(f"tracker: `{path}` is ticked and the file is gone")
        elif seconds is not None and time.monotonic() - start > seconds:
            break
        elif path in checked and checked[path] != blob(target):
            flags.append(f"tracker: `{path}` changed after its row was ticked")
    planned = {row["path"].rstrip("/") for row in records.tracker_rows(proj.read("tracker.md"))
               if row["path"] and records.DONE not in row["marks"].values()}
    for name in ("rules.md", "todo.md", "decisions.md"):
        for _, line in records.plain_lines(proj.read(name)):
            if records.OPEN in line:
                continue  # an open box may name a file that is not built yet
            for token in PATHLIKE.findall(line):
                if token.rstrip("/") in planned:
                    continue  # the tracker lists it as work ahead
                looks = re.search(r"\.\w{1,5}$", token) or token.endswith("/")
                if not looks or token.startswith(("http", "/", "~", "-", "$", ".")) or any(c in token for c in "*?<>{}$|=@:"):
                    continue
                if not (proj.root / token.rstrip("/")).exists():
                    flags.append(f"{name}: `{token}` names nothing")
    locks = records.locks(proj.read("locks.md"))
    if locks:
        files = (git(proj.root, "ls-files") + git(proj.root, "ls-files", "-o", "--exclude-standard")).splitlines()
        flags += [f"locks: `{lock}` covers no file" for lock in locks if not any(matches(lock, f) for f in files)]
    for name in RECORDS:
        text = proj.read(name)
        line = next((l for _, l in records.plain_lines(text) if l.startswith("**Contents:**")), None)
        if line and _names(line.replace("**Contents:**", "").split("·")) != _names(records.headings(text)):
            flags.append(f"{name}: the Contents line is out of step with the headings")
    flags += rules.load(proj)[1]
    spent = budget(proj)
    if spent["total"] > spent["cap"]:
        flags.append(f"budget: about {spent['total']} tokens are always loaded, the cap is {spent['cap']}")
    return flags


def frontmatter(text) -> Dict[str, str]:
    """The `key: value` lines between the first two `---` of a skill or a subagent file."""
    out, lines = {}, text.split("\n")
    if not lines or lines[0].strip() != "---":
        return out
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip().strip("\"'")
    return out


def plugin_roots(profile) -> List[Path]:
    """Where light lives, and heavy beside it when the project runs heavy."""
    light = Path(__file__).resolve().parents[1]
    roots = [light]
    if profile == "heavy":
        for found in (light.parent / "heavy", light.parents[1] / "heavy" / light.name):
            if (found / "skills").is_dir():
                roots.append(found)
                break
    return roots


def budget(proj) -> Dict:
    """What is always loaded, in characters and in estimated tokens, against the cap."""
    from . import briefing

    items = []
    for root in plugin_roots(proj.profile):
        for path in sorted(root.glob("skills/*/SKILL.md")) + sorted(root.glob("agents/*.md")):
            meta = frontmatter(path.read_text(encoding="utf-8"))
            if str(meta.get("disable-model-invocation", "")).lower() == "true":
                continue
            name = path.parent.name if path.name == "SKILL.md" else path.stem
            text = (meta.get("description", "") + " " + meta.get("when_to_use", "")).strip()
            label = f"{root.name}:{name}"
            items.append((label, len(label) + len(text) + LISTING))
    if proj.profile == "heavy":
        items.append(("harness/rules.md", len(proj.read("rules.md").strip())))
        items.append(("the briefing", len(briefing.status_text(proj, flags=[]))))
    rows = [(name, chars, math.ceil(chars / CHARS_PER_TOKEN)) for name, chars in items]
    return {"rows": rows, "total": sum(r[2] for r in rows), "cap": CAPS[proj.profile]}
