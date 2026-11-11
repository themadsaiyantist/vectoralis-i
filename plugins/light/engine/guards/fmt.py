"""The formatter runs after every edit. It never blocks. It says when it rewrote the file."""
from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

from . import Finding
from .. import trust

NAME = "format"


def check(call, proj, state):
    command = str(proj.settings.get("format") or "").strip()
    out = []
    if command and not trust.trusted(proj, "format"):
        if not state.get("format_unapproved_said"):
            state["format_unapproved_said"] = True
            out.append(Finding(NAME, "notice", "Vectoralis did not run this project's formatter, because nobody approved it on "
                                               f"this machine yet: `{command}`. Read it, then approve it with `vectoralis trust`."))
        return out
    for write in call.writes:
        path = Path(write.path)
        rel = proj.rel(write.path)
        if not command or rel is None or not path.is_file() or proj.skipped(NAME, rel):
            continue
        before = path.read_bytes()
        quoted = shlex.quote(str(path))
        line = command.replace("{file}", quoted) if "{file}" in command else command + " " + quoted
        try:
            done = subprocess.run(line, shell=True, cwd=str(proj.root), capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            continue
        if done.returncode != 0:
            first = (done.stderr or done.stdout).strip().splitlines()[:1]
            out.append(Finding(NAME, "warn", f"The formatter failed on `{rel}`" + (f": {first[0]}" if first else "") + "."))
        elif path.read_bytes() != before:
            out.append(Finding(NAME, "warn", f"The formatter rewrote `{rel}`. Read it again before the next edit to it."))
    return out
