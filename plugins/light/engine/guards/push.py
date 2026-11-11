"""The default branch moves on the person's word: no push to it and no merge, while `merge` is `yours`."""
from __future__ import annotations

from . import Finding
from .destructive import git_words, segments
from ..project import git

NAME = "push"
RULE = "the default branch moves on the person's word (guard `push`, `merge` in harness/settings.json)"


def default_branch(root):
    head = git(root, "symbolic-ref", "--short", "refs/remotes/origin/HEAD").strip()
    if head:
        return head.split("/", 1)[-1]
    names = git(root, "branch", "--format=%(refname:short)").split()
    return "main" if "main" in names or "master" not in names else "master"


def check(call, proj, state):
    if proj.settings.get("merge") == "agent":
        return []
    out = []
    for words in segments(call.command):
        name = words[0].rsplit("/", 1)[-1]
        if name == "git":
            sub, rest = git_words(words)
            if sub != "push":
                continue
            main = default_branch(proj.root)
            current = git(proj.root, "rev-parse", "--abbrev-ref", "HEAD").strip()
            specs = [w for w in rest if not w.startswith("-")][1:]
            targets = [s.split(":")[-1].lstrip("+") for s in specs] or [current]
            targets = [current if t == "HEAD" else t for t in targets]
            if main in targets or "--all" in rest or "--mirror" in rest:
                out.append(Finding(NAME, "block", f"A push to `{main}` is the person's.", RULE,
                                   "push your own branch and open a pull request."))
        elif name == "gh" and words[1:3] == ["pr", "merge"]:
            out.append(Finding(NAME, "block", "A merge is the person's.", RULE,
                               "watch the pull request to green and tell the person it is ready."))
    return out
