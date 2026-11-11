"""The staleness check and the budget: is every record still backed by the repository, and is the core still small."""
from __future__ import annotations

import math
import re
import time
from pathlib import Path
from typing import Dict, List

from . import records, rules
from .project import git, matches

CAPS = {"light": 300, "heavy": 2000}
RECORDS = ("rules.md", "tracker.md", "todo.md", "failures.md", "lessons.md", "decisions.md", "locks.md")
PATHLIKE = re.compile(r"`([^`\s]+/[^`\s]*)`")


def _line_times(proj, rel) -> Dict[int, int]:
    """When each line of a file last changed, from one git blame."""
    times, per_commit, sha = {}, {}, ""
    for line in git(proj.root, "blame", "--porcelain", "--", rel, timeout=20).splitlines():
        head = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", line)
        if head:
            sha = head.group(1)
            times[int(head.group(2))] = sha
        elif line.startswith("committer-time "):
            per_commit[sha] = int(line.split()[1])
    return {number: per_commit.get(commit, 0) for number, commit in times.items()}


def _path_time(proj, rel) -> int:
    """When a path last changed: now-ish when it has uncommitted changes, else its last commit."""
    if git(proj.root, "status", "--porcelain", "--", rel).strip():
        target = proj.root / rel
        return int(target.stat().st_mtime) if target.exists() else 0
    stamp = git(proj.root, "log", "-1", "--format=%ct", "--", rel).strip()
    return int(stamp) if stamp.isdigit() else 0


def _names(text) -> List[str]:
    return [re.sub(r"[^a-z0-9]+", "", re.sub(r"^\d+\.?\s*", "", n.lower())) for n in text]


def stale(proj, seconds=None) -> List[str]:
    """Every flag: a record that says something the repository no longer backs.

    With `seconds`, the slow part (the tracker against git) stops when the time is up.
    """
    start, flags = time.monotonic(), []
    tracker = proj.read("tracker.md")
    line_times = None
    for row in records.tracker_rows(tracker):
        path = row["path"]
        if not path or any(c in path for c in "*?"):
            continue
        stages = [mark for name, mark in row["marks"].items() if name != row["yours_stage"]]
        if records.DONE not in stages:
            continue
        if not (proj.root / path).exists():
            flags.append(f"tracker: `{path}` is ticked and the file is gone")
            continue
        if seconds is not None and time.monotonic() - start > seconds:
            continue
        if line_times is None:
            line_times = _line_times(proj, "harness/tracker.md")
        ticked, changed = line_times.get(row["line"], 0), _path_time(proj, path)
        if ticked and changed and changed > ticked:
            flags.append(f"tracker: `{path}` changed after its row was ticked")
    for name in ("rules.md", "todo.md", "decisions.md"):
        for _, line in records.plain_lines(proj.read(name)):
            for token in PATHLIKE.findall(line):
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
    """What is always loaded, in characters and in tokens estimated at four characters each, against the cap."""
    from . import briefing

    items = []
    for root in plugin_roots(proj.profile):
        for path in sorted(root.glob("skills/*/SKILL.md")) + sorted(root.glob("agents/*.md")):
            meta = frontmatter(path.read_text(encoding="utf-8"))
            if str(meta.get("disable-model-invocation", "")).lower() == "true":
                continue
            name = path.parent.name if path.name == "SKILL.md" else path.stem
            text = (meta.get("description", "") + " " + meta.get("when_to_use", "")).strip()
            items.append((f"{root.name}:{name}", len(name) + len(text)))
    if proj.profile == "heavy":
        items.append(("harness/rules.md", len(proj.read("rules.md").strip())))
        items.append(("the briefing", len(briefing.status_text(proj, flags=[]))))
    rows = [(name, chars, math.ceil(chars / 4)) for name, chars in items]
    return {"rows": rows, "total": sum(r[2] for r in rows), "cap": CAPS[proj.profile]}
