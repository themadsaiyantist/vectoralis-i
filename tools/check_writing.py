#!/usr/bin/env python3
"""Check the repository's writing rules. Exit 1 with one line per finding.

Run from the repository root: `python3 tools/check_writing.py`. It reads every tracked text file and writes nothing.
The rules: no em or en dash, no semicolon in prose, every Contents line in step with its headings,
every relative link resolves.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins" / "light"))

from engine import records  # noqa: E402

DASH = re.compile("[" + chr(0x2013) + chr(0x2014) + "]")
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CODE = re.compile(r"`[^`]*`")


def names(items):
    return [re.sub(r"[^a-z0-9]+", "", re.sub(r"^\d+\.?\s*", "", i.strip().lower())) for i in items]


def main():
    tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True).stdout.split("\n")
    found = []
    for name in sorted(n for n in tracked if n.endswith((".md", ".py", ".json", ".yml", ".txt"))):
        path = ROOT / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.split("\n"), 1):
            if DASH.search(line):
                found.append(f"{name}:{number}: an em or en dash")
        if not name.endswith(".md"):
            continue
        plain = records.plain_lines(text)
        for number, line in plain:
            prose = re.sub(r"https?://\S+", "", CODE.sub("", line))
            if ";" in re.sub(r"&\w+;", "", prose):
                found.append(f"{name}:{number}: a semicolon in prose")
            for target in LINK.findall(CODE.sub("", line)):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                if not (path.parent / target.split("#")[0]).exists():
                    found.append(f"{name}:{number}: the link `{target}` leads nowhere")
        contents = next((line for _, line in plain if line.startswith("**Contents:**")), None)
        if contents and names(contents.replace("**Contents:**", "").split("·")) != names(records.headings(text)):
            found.append(f"{name}: the Contents line is out of step with the headings")
    for line in found:
        print(line)
    print("Clean." if not found else f"{len(found)} finding(s).")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
