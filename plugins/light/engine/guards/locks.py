"""Finished work is not written to.

Blocks a write to a path that `harness/locks.md` locks, unless the person typed `unlock` for it this turn.
"""
from __future__ import annotations

import re

from . import Finding
from .destructive import git_words, segments
from .. import grants, records
from ..project import matches

NAME = "locks"
RULE = "finished work is not written to (guard `locks`, harness/locks.md)"
REDIRECT = re.compile(r"(?<![0-9&>])>{1,2}\s*([^\s|;&<>]+)")
ALL_ARGS = ("rm", "mv", "tee", "truncate", "touch", "shred", "unlink")
LAST_ARG = ("cp", "install", "ln", "rsync")


def locked_by(proj, rel, state):
    """The lock that covers a path and that the person did not open, or None."""
    for lock in records.locks(proj.read("locks.md")):
        if matches(lock, rel) and not grants.unlocked(state.get("grants"), rel, lock):
            return lock
    return None


def write_targets(command):
    """The paths a shell line writes to, as far as its words show."""
    out = list(REDIRECT.findall(command or ""))
    for words in segments(command):
        name = words[0].rsplit("/", 1)[-1]
        args = [w for w in words[1:] if not w.startswith("-")]
        if name in ALL_ARGS:
            out += args
        elif name in LAST_ARG and args:
            out.append(args[-1])
        elif name in ("sed", "perl") and any(re.match(r"^-[a-zA-Z]*i", w) for w in words[1:]):
            out += args[1:]
        elif name == "git":
            sub, rest = git_words(words)
            if sub in ("checkout", "restore", "rm", "mv"):
                out += [w for w in rest if not w.startswith("-")]
    return [t for t in out if t and not any(c in t for c in "$*?")]


def check(call, proj, state):
    out, seen = [], set()
    paths = [w.path for w in call.writes]
    if call.event == "shell":
        paths += [str((proj.root / t)) if not t.startswith("/") else t for t in write_targets(call.command)]
    for path in paths:
        rel = proj.rel(path)
        if rel is None or rel in seen or proj.skipped(NAME, rel):
            continue
        seen.add(rel)
        lock = locked_by(proj, rel, state)
        if lock:
            out.append(Finding(NAME, "block", f"`{rel}` is locked by `{lock}`.", RULE,
                               f"ask the person. They open it by typing `unlock {rel}`."))
    return out
