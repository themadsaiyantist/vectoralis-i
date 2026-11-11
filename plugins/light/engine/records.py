"""Read the records in `harness/`: the tracker, the to-do list, the locks, the failure log.

Every reader skips fenced code, so an example inside a record is never taken for the real thing.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

DONE, OPEN = "✅", "⬜"
BOX = re.compile(r"^\s*- (" + DONE + "|" + OPEN + r") (.*)$")
LOCK = re.compile(r"^\s*- `([^`]+)`")
FAILURE = re.compile(r"^### (" + DONE + "|" + OPEN + r") (\d{4}-\d{2}-\d{2}) · ([^·]+) · (.+?)\s*$")
CLASS = re.compile(r"^\*\*Class\.\*\*\s*`([^`]+)`")
BOUND = re.compile(r"^`([^`]+)`")
TEMPLATES = Path(__file__).resolve().parents[1] / "templates"


def plain_lines(text) -> List[Tuple[int, str]]:
    """The lines of a record that are not inside a code fence, with their numbers from 1."""
    out, fenced = [], False
    for number, line in enumerate((text or "").split("\n"), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append((number, line))
    return out


def headings(text) -> List[str]:
    return [line[3:].strip() for _, line in plain_lines(text) if line.startswith("## ")]


def tracker_rows(text) -> List[Dict]:
    """Every row of every table: its section, its unit, each stage's mark, and the person's column."""
    rows, section, header = [], "", None
    for number, line in plain_lines(text):
        if line.startswith("## "):
            section, header = line[3:].strip(), None
            continue
        if not line.lstrip().startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        marks = dict(zip(header[1:], cells[1:]))
        bound = BOUND.match(cells[0])
        rows.append({
            "section": section, "unit": cells[0], "marks": marks, "line": number,
            "yours_stage": header[-1] if len(header) > 1 else "",
            "yours": cells[-1] if len(cells) > 1 else "",
            "path": bound.group(1) if bound else None,
        })
    return rows


def todo_boxes(text) -> List[Dict]:
    """Every box of the to-do list, with its section and whether that section is the person's."""
    out, section = [], ""
    for number, line in plain_lines(text):
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        found = BOX.match(line)
        if found:
            out.append({
                "section": section, "done": found.group(1) == DONE, "text": found.group(2).strip(),
                "yours": section.lower().startswith("your"), "line": number,
            })
    return out


def section_text(text, name) -> str:
    """The body of one `##` section, without its heading."""
    out, inside = [], False
    for _, line in plain_lines(text):
        if line.startswith("## "):
            inside = line[3:].strip().lower() == name.lower()
            continue
        if inside and line.strip() != "---":
            out.append(line)
    return "\n".join(out).strip()


def locks(text) -> List[str]:
    return [found.group(1) for _, line in plain_lines(text) for found in [LOCK.match(line)] if found]


def failures(text) -> List[Dict]:
    """Every entry of the failure log: open or closed, its date, who, its title and its class."""
    out: List[Dict] = []
    for number, line in plain_lines(text):
        found = FAILURE.match(line)
        if found:
            title = re.sub(r"\s*· closed.*$", "", found.group(4))
            out.append({
                "open": found.group(1) == OPEN, "date": found.group(2), "who": found.group(3).strip(),
                "title": title, "class": None, "line": number,
            })
            continue
        tagged = CLASS.match(line)
        if tagged and out and out[-1]["class"] is None:
            out[-1]["class"] = tagged.group(1)
    return out


def yours_marks(tracker_text, todo_text) -> Dict[str, str]:
    """Every box that is the person's, keyed by where it sits, so two readings can be compared."""
    out = {}
    for row in tracker_rows(tracker_text):
        out["tracker|" + row["section"] + "|" + row["unit"]] = row["yours"]
    for box in todo_boxes(todo_text):
        if box["yours"]:
            out["todo|" + box["section"] + "|" + box["text"]] = DONE if box["done"] else OPEN
    return out


def newly_ticked(before: Dict[str, str], after: Dict[str, str]) -> List[str]:
    """The person's boxes that read done now and did not before."""
    return [key for key, mark in after.items() if mark == DONE and before.get(key) != DONE]


def removed_open(before: Dict[str, str], after: Dict[str, str]) -> List[str]:
    """The person's boxes that were open and are gone. A box that only moved, its words unchanged, is still there.

    A renamed section moves every box in it. So a box that left one place is matched with one that arrived, by the
    record it is in and by its words, before it is called removed.
    """
    def words(key):
        kind, _, unit = (key.split("|", 2) + ["", ""])[:3]
        return kind, unit

    arrived: Dict[Tuple[str, str], int] = {}
    for key in after:
        if key not in before:
            arrived[words(key)] = arrived.get(words(key), 0) + 1
    gone = []
    for key, mark in before.items():
        if mark != OPEN or key in after:
            continue
        if arrived.get(words(key), 0) > 0:
            arrived[words(key)] -= 1
            continue
        gone.append(key)
    return gone


def owners(tracker_text, todo_text) -> Dict[str, str]:
    """Whose each of the person's boxes is, in a team layout: the row's Owner cell, or the name in the section's heading."""
    out = {}
    for row in tracker_rows(tracker_text):
        name = next((value for column, value in row["marks"].items() if column.lower() == "owner"), "")
        out["tracker|" + row["section"] + "|" + row["unit"]] = name.strip()
    for box in todo_boxes(todo_text):
        if box["yours"]:
            name = re.sub(r"(?i)^yours?\b[\s,:]*", "", box["section"]).strip()
            out["todo|" + box["section"] + "|" + box["text"]] = name
    return out


def unit_of(key) -> Optional[str]:
    return key.split("|", 2)[2] if key.count("|") >= 2 else None


def samples() -> Set[str]:
    """The sample boxes `vectoralis init` writes in the person's column. Until someone rewrites one, it is nobody's."""
    out: Set[str] = set()
    for tracker, todo in (("tracker.md", "todo.md"), ("tracker.team.md", "todo.team.md")):
        try:
            marks = yours_marks((TEMPLATES / tracker).read_text(encoding="utf-8"),
                                (TEMPLATES / todo).read_text(encoding="utf-8"))
        except OSError:
            continue
        out |= {unit_of(key) or "" for key in marks}
    return out - {""}
