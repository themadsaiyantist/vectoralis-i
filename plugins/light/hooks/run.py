#!/usr/bin/env python3
"""The one entry point of the Vectoralis engine.

Run by a hook as `python3 run.py <event>`, with the hook's JSON payload on stdin.
The events are session, prompt, write, shell, wrote, stop and compact.
It reads `harness/settings.json` in the project and writes nothing there.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine.main import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
