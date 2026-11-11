---
name: setup
description: Set up the heavy harness in this project.
disable-model-invocation: true
---

# Set up heavy

The records, on top of light: a tracker, two to-do lists, a failure log, lessons, decisions and locks.

1. Ask the person one thing first: one person, or a team?
2. Run `vectoralis init heavy`, or `vectoralis init heavy --team`, and show what it printed. It never overwrites a file that exists.
   - If the command is not found, the CLI lives in the light plugin's `bin/` folder.
   - In Codex, find it with `ls ~/.codex/plugins/cache/vectoralis/light/*/bin/vectoralis`.
3. If it found no test command or no formatter, ask the person for the command. If it said a command is not approved on this machine, show the person the command and ask. On a yes, run `vectoralis trust`.
4. If it offered a starter instructions file, ask the person first. On a yes, run it again with `--starter`.
5. Fill the first rows with the person: the units of the work in `harness/tracker.md`, the first steps in `harness/todo.md`.
6. Run `vectoralis check` and show the result.
7. Tell the person the three things that stay theirs, and the words that give them:
   - a box in their column → `tick` and a few words of the line
   - a lesson → a message that starts with `lesson:`
   - a lock → `unlock` and the path

**What to write where:** the first rows → `harness/tracker.md` and `harness/todo.md`. Nothing else yet.
