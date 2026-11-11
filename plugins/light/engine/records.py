"""Read the records in `harness/`: the tracker, the to-do list, the locks, the failure log.

Every reader skips fenced code and HTML comments. An example inside a record is never taken for the real thing,
and a line that a comment hides is not there.
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

DONE, OPEN = "✅", "⬜"
BOX = re.compile(r"^\s*- (" + DONE + "|" + OPEN + r") (.*)$")
LOCK = re.compile(r"^\s*- `([^`]+)`")
FAILURE = re.compile(r"^### (" + DONE + "|" + OPEN + r") (\d{4}-\d{2}-\d{2}) · ([^·]+) · (.+?)\s*$")
CLASS = re.compile(r"^\*\*Class\.\*\*\s*`([^`]+)`")
BOUND = re.compile(r"^`([^`]+)`")
COMMENT = re.compile(r"<!--.*?-->")
# A comment block opens where a line, a list item or a quote begins with the opener.
BLOCK = re.compile(r"^ {0,3}(?:(?:[-*+]|\d{1,9}[.)])[ \t]+|>[ \t]?)*<!--")
# Between the parts of a box's key and of its value. No heading and no cell can hold it.
SEP = "\x1f"
# The sample boxes `vectoralis init` writes in the person's column. Until someone rewrites one, it is nobody's.
# Held here and not read from the templates, so a project that holds the templates cannot widen the list.
SAMPLES = frozenset({"the first unit of work", "the first thing only you can do"})
# What a guard says when a box stayed in its row and its owner or its column changed under it.
PLACE = {
    "owner": "The owner of \"{unit}\" would change, and with it whose box that is.",
    "column": "The person's column of \"{unit}\" would stop being the last one.",
}
PLACE_DONE = {
    "owner": "The owner of \"{unit}\" changed this turn, and with it whose box that is.",
    "column": "The person's column of \"{unit}\" stopped being the last one this turn.",
}


def _inline(line) -> Tuple[str, bool]:
    """One line without the comments that open and close on it, and whether one was cut.

    A marker inside a code span is text, and a span is a run of backticks closed by a run of the same length.
    An opener in the middle of a line with no closer on that line is text too. One that begins a line, a list item
    or a quote is a block, and `_read` takes it before this is called.
    """
    out, i, cut = [], 0, False
    while i < len(line):
        if line[i] == "`":
            run = len(line) - i - len(line[i:].lstrip("`"))
            j, close = i + run, -1
            while j < len(line):
                if line[j] == "`":
                    size = len(line) - j - len(line[j:].lstrip("`"))
                    if size == run:
                        close = j
                        break
                    j += size
                else:
                    j += 1
            stop = close + run if close >= 0 else i + run
            out.append(line[i:stop])
            i = stop
            continue
        if line.startswith("<!--", i):
            close = line.find("-->", i + 2)
            if close >= 0:
                i, cut = close + 3, True
                continue
        out.append(line[i])
        i += 1
    return "".join(out), cut


def _read(text) -> Tuple[List[Tuple[int, str]], List[int]]:
    """The plain lines of a record, and the lines where a comment opens and never closes.

    A record is read as a page shows it. A line, a list item or a quote that starts with a comment opener starts a
    block that runs to the line that closes it, or to the end of the file when nothing does. The closer may share
    the opener's dashes, as in the shortest comment there is. Fenced code is skipped.
    """
    raw = (text or "").replace(SEP, "").split("\n")
    out, unclosed, fence, block = [], [], "", 0
    for number, line in enumerate(raw, 1):
        if block:
            if "-->" in line:
                block = 0
            continue
        mark = line.lstrip()[:3]
        if fence:
            if mark == fence:
                fence = ""
            continue
        if mark in ("```", "~~~"):
            fence = mark
            continue
        opened = BLOCK.match(line)
        if opened:
            if "-->" not in line[opened.end() - 2:]:
                block = number
            continue
        cut = False
        if "<!--" in line:
            line, cut = _inline(line)
        if cut and not line.strip():
            continue
        out.append((number, line))
    if block:
        unclosed.append(block)
    return out, unclosed


def plain_lines(text) -> List[Tuple[int, str]]:
    """The lines of a record that are in neither a code fence nor an HTML comment, with their numbers from 1."""
    return _read(text)[0]


def unclosed_comments(text) -> List[int]:
    """The line where a comment block opens and never closes. A page hides everything after it, and so does the reader."""
    return _read(text)[1]


def headings(text) -> List[str]:
    return [line[3:].strip() for _, line in plain_lines(text) if line.startswith("## ")]


def _cells(line) -> List[str]:
    """The cells of one table line, split on the pipes that are not escaped."""
    cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())]
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return cells


def tracker_rows(text) -> List[Dict]:
    """Every row of every table: its section, its unit, each stage's mark, and the person's column.

    A table is read as a page shows it. Its header is the line right above the first row of dashes, and a row of
    dashes further down is a row like any other. The person's cell is the one under the last header: a cell that
    no header stands over is not shown, and a row cut short of that column holds no box.
    """
    rows, section, header, above = [], "", None, None
    for number, line in plain_lines(text):
        if line.startswith("## "):
            section, header, above = line[3:].strip(), None, None
            continue
        if not line.lstrip().startswith("|"):
            header, above = None, None
            continue
        cells = _cells(line)
        if header is None:
            if above is not None and cells and all(c and set(c) <= set("-: ") and "-" in c for c in cells):
                header, above = above, None
            else:
                above = cells
            continue
        marks = dict(zip(header[1:], cells[1:]))
        bound = BOUND.match(cells[0]) if cells else None
        last = header[-1] if len(header) > 1 else ""
        twice = header.count(last)
        rows.append({
            "section": section, "unit": cells[0] if cells else "", "marks": marks, "line": number,
            "yours_stage": last,
            "yours_column": last if twice < 2 else f"{last} x{twice}",
            "yours": cells[len(header) - 1] if len(header) > 1 and len(cells) >= len(header) else "",
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


def _parts(key) -> List[str]:
    """The record, the section, the words and the count of one box. A key from an older engine used pipes."""
    parts = key.split(SEP) if SEP in key else key.split("|", 2)
    return (parts + ["", "", "", ""])[:4]


def unit_of(key) -> Optional[str]:
    return _parts(key)[2] or None


def mark_of(value) -> str:
    """The box itself: done, open, or anything else where no box is left."""
    return (value or "").rsplit(SEP, 1)[-1].strip()


def _holder(value) -> Optional[Tuple[str, str]]:
    """Whose the box is and where it sits: the row's Owner cell, and the last column of its table.

    None for a value written before the two were kept, which is then compared by its mark alone.
    """
    parts = (value or "").split(SEP)
    return (parts[0].strip().lower(), parts[1]) if len(parts) == 3 else None


def _words(key, value) -> Tuple:
    return (_parts(key)[2], _holder(value))


def _current(marks: Dict[str, str]) -> Dict[str, str]:
    """The same boxes with every key in today's form, so a reading kept from an older engine still compares."""
    return {(key if SEP in key else SEP.join(_parts(key))): value for key, value in (marks or {}).items()}


def aligned(before: Dict[str, str], after: Dict[str, str]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Two readings ready to compare: every key in today's form, and twins lined up like with like.

    Boxes with the same words in one section are told apart by a count, and a count follows the order they stand
    in. So before two readings are compared, each twin of the first is paired with one of the second: the same
    value first, then the same mark, then whatever is left. A twin with no partner is a box that came or went.
    """
    before, after = _current(before), _current(after)
    groups: Dict[Tuple, List[List[str]]] = {}
    for side, marks in enumerate((before, after)):
        for key in marks:
            groups.setdefault(tuple(_parts(key)[:3]), [[], []])[side].append(key)
    out = dict(after)
    for group, (olds, news) in groups.items():
        if len(olds) < 2 and len(news) < 2:
            continue
        for key in news:
            del out[key]
        free, pairs = list(news), {}
        for same in (lambda a, b: a == b, lambda a, b: mark_of(a) == mark_of(b), lambda a, b: True):
            for old in olds:
                if old in pairs:
                    continue
                match = next((new for new in free if same(before[old], after[new])), None)
                if match is not None:
                    free.remove(match)
                    pairs[old] = match
        for old, new in pairs.items():
            out[old] = after[new]
        for number, new in enumerate(free, 1):
            out[SEP.join(group + (f"new{number}",))] = after[new]
    return before, out


def place_of(key, value) -> Tuple[str, str, str, str]:
    """A box by where it stands and whose it is: its record, its section, its words, its owner in lower case."""
    record, section, words = _parts(key)[:3]
    return (record, section, words, owner_of(key, value).lower())


def owner_of(key, value) -> str:
    """Whose a box is, in a team layout: the row's Owner cell, or the name in the heading of its to-do section."""
    record, section = _parts(key)[:2]
    if record == "todo":
        return re.sub(r"(?i)^yours?\b[\s,:]*", "", section).strip()
    parts = (value or "").split(SEP)
    return parts[0].strip() if len(parts) == 3 else ""


def yours_marks(tracker_text, todo_text) -> Dict[str, str]:
    """Every box that is the person's, keyed by where it sits, so two readings can be compared.

    The value holds the row's owner and the last column of its table beside the mark. So a box whose owner was
    rewritten, or whose column stopped being the last one, reads as changed. Two boxes with the same words in one
    section are two boxes, counted in the order they stand, so one cannot stand in for the other.
    """
    out: Dict[str, str] = {}
    seen: Dict[Tuple, int] = {}

    def key_for(record, section, words):
        seen[(record, section, words)] = seen.get((record, section, words), 0) + 1
        count = seen[(record, section, words)]
        return SEP.join((record, section, words, "" if count == 1 else str(count)))

    for row in tracker_rows(tracker_text):
        owner = next((value for column, value in row["marks"].items() if column.lower() == "owner"), "").strip()
        out[key_for("tracker", row["section"], row["unit"])] = SEP.join((owner, row["yours_column"], row["yours"]))
    for box in todo_boxes(todo_text):
        if box["yours"]:
            out[key_for("todo", box["section"], box["text"])] = SEP.join(("", "", DONE if box["done"] else OPEN))
    return out


def _moves(before: Dict[str, str], after: Dict[str, str]) -> Dict[str, str]:
    """The tracker rows that left one place and arrived in another, the old key to the new one.

    A row moved when its words, its owner and its column are unchanged and a box arrived with it. Each arrival
    stands in for one row only. A row that was done takes a done arrival first, then an open row takes what is left.
    In the to-do list the section says whose the box is, so nothing there counts as a move.
    """
    def boxed(marks, key):
        return _parts(key)[0] == "tracker" and mark_of(marks[key]) in (OPEN, DONE)

    left = [key for key in before if key not in after and boxed(before, key)]
    free = [key for key in after if key not in before and boxed(after, key)]
    pairs: Dict[str, str] = {}

    def take(old, done) -> bool:
        for new in free:
            if _words(old, before[old]) == _words(new, after[new]) and (mark_of(after[new]) == DONE) == done:
                free.remove(new)
                pairs[old] = new
                return True
        return False

    for old in left:
        if mark_of(before[old]) == DONE:
            take(old, True)
    for old in left:
        if mark_of(before[old]) == OPEN and not take(old, False):
            take(old, True)
    return pairs


def newly_ticked(before: Dict[str, str], after: Dict[str, str]) -> List[str]:
    """The person's boxes that read done now and did not before. A done row that only moved is not a new tick."""
    before, after = aligned(before, after)
    came_from = {new: old for old, new in _moves(before, after).items()}
    out = []
    for key, value in after.items():
        if mark_of(value) != DONE:
            continue
        old = key if key in before else came_from.get(key)
        if old is not None and mark_of(before[old]) == DONE:
            continue
        out.append(key)
    return out


def ticked_places(before: Dict[str, str], after: Dict[str, str]) -> List[Tuple[str, Tuple[str, str, str, str]]]:
    """The newly ticked boxes, each with the place it stood in before the change.

    A box that stayed, or is new, stands where it stands. A row that moved is known by the place it left, so a tick
    can be told apart from the move or the rename that happened beside it.
    """
    before, after = aligned(before, after)
    came_from = {new: old for old, new in _moves(before, after).items()}
    out = []
    for key in newly_ticked(before, after):
        old = key if key in before else came_from.get(key)
        out.append((key, place_of(old, before[old]) if old is not None else place_of(key, after[key])))
    return out


def removed_open(before: Dict[str, str], after: Dict[str, str]) -> List[str]:
    """The person's boxes that were open and are gone.

    A box is still there when a box, open or done, sits in its row. A cell left blank takes it away, and so does a
    row that is deleted, reworded or hidden. Two things are not a removal. A sample box that `vectoralis init`
    wrote is nobody's until someone rewrites it. And a tracker row that only moved keeps its box.
    """
    before, after = aligned(before, after)
    moved = _moves(before, after)
    gone = []
    for key, value in before.items():
        if mark_of(value) != OPEN or unit_of(key) in SAMPLES:
            continue
        now = after.get(key)
        if now is None:
            if key not in moved:
                gone.append(key)
        elif mark_of(now) not in (OPEN, DONE):
            gone.append(key)
    return gone


def changed_place(before: Dict[str, str], after: Dict[str, str]) -> List[Tuple[str, str]]:
    """The person's boxes that stayed in their row while their owner or their column changed: the key, and which.

    An Owner cell rewritten hands the box to someone else. A column added after the person's, or a second one with
    its name, takes their column out of the last place. Either is the person's to allow, with `unlock`.
    """
    before, after = aligned(before, after)
    out = []
    for key, value in before.items():
        now = after.get(key)
        if now is None or mark_of(value) not in (OPEN, DONE) or mark_of(now) not in (OPEN, DONE):
            continue
        old, new = _holder(value), _holder(now)
        if old is None or new is None or old == new or unit_of(key) in SAMPLES:
            continue
        out.append((key, "owner" if old[0] != new[0] else "column"))
    return out
