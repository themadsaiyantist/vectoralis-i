"""A command that cannot be undone is the person's to run.

Blocks the ones a machine can be sure of. Warns on the ones that depend on what the paths hold.
"""
from __future__ import annotations

import re
import shlex

from . import Finding

NAME = "destructive"
RULE = "a command that cannot be undone is the person's to run (guard `destructive`)"
ASK = "ask the person. They can run it themselves."
SPLIT = re.compile(r"\s*(?:&&|\|\||;|\||\n)\s*")
WHOLE = {"/", "~", "~/", "$HOME", "${HOME}", ".", "./", "..", "../", "*", "/*", "./*", "~/*"}


def segments(command):
    """Each simple command of a line, as words, with leading assignments and wrappers dropped."""
    out = []
    for piece in SPLIT.split(command or ""):
        try:
            words = shlex.split(piece)
        except ValueError:
            words = piece.split()
        while words and (re.match(r"^\w+=", words[0]) or words[0] in ("sudo", "command", "time", "nohup", "exec")):
            words = words[1:]
        if words:
            out.append(words)
    return out


def git_words(words):
    """The subcommand of a git call and what follows it, past `-C path` and `-c key=value`."""
    rest = words[1:]
    while rest and rest[0].startswith("-"):
        rest = rest[2:] if rest[0] in ("-C", "-c", "--git-dir", "--work-tree") else rest[1:]
    return (rest[0], rest[1:]) if rest else ("", [])


def check(call, proj, state):
    out = []

    def add(level, what):
        out.append(Finding(NAME, level, what, RULE, ASK))

    for words in segments(call.command):
        name = words[0].rsplit("/", 1)[-1]
        if name == "git":
            sub, rest = git_words(words)
            if sub == "reset" and "--hard" in rest:
                add("block", "`git reset --hard` throws away every uncommitted change.")
            elif sub == "clean" and any(w == "--force" or (re.match(r"^-[a-zA-Z]+$", w) and "f" in w) for w in rest):
                add("block", "`git clean -f` deletes files git does not track.")
            elif sub == "push" and any(w in ("--force", "-f") or w.startswith(("--force-with-lease", "+")) for w in rest):
                add("block", "A forced push rewrites the history other people hold.")
            elif (sub == "checkout" and ("--" in rest or "." in rest)) or (sub == "restore" and "--staged" not in rest):
                add("warn", "The command discards uncommitted changes in the paths it names.")
            elif sub == "branch" and "-D" in rest:
                add("warn", "`git branch -D` deletes a branch even when it is not merged.")
            elif sub == "stash" and rest[:1] and rest[0] in ("drop", "clear"):
                add("warn", "The command deletes stashed work.")
        elif name == "rm":
            flags = "".join(w.lstrip("-") for w in words[1:] if re.match(r"^-[a-zA-Z]+$", w))
            deep = "r" in flags or "R" in flags or "--recursive" in words
            targets = [w for w in words[1:] if not w.startswith("-")]
            if deep and any(t in WHOLE or t.rstrip("/") == str(proj.root) for t in targets):
                add("block", "`rm -r` on " + ", ".join(f"`{t}`" for t in targets) + " deletes everything under it.")
            elif deep:
                add("warn", "`rm -r` deletes " + ", ".join(f"`{t}`" for t in targets) + " and everything in it.")
        elif name.startswith("mkfs") or (name == "dd" and any(w.startswith("of=/dev/") for w in words)):
            add("block", "The command overwrites a disk.")
    return out
