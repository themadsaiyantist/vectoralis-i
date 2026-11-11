#!/bin/sh
# Every check this repository runs before a commit. It stops at the first one that fails.
# Run it from anywhere inside the repository: sh tools/check.sh
# It reads the working tree. The staleness check may write harness/.checked.json.
set -e
cd "$(git rev-parse --show-toplevel)"
python3 -m unittest discover -s tests -q
python3 plugins/light/bin/vectoralis guards > /dev/null
python3 plugins/light/bin/vectoralis check
python3 tools/check_writing.py
