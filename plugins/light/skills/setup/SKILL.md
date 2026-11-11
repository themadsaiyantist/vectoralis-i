---
name: setup
description: Set up the light harness in this project.
disable-model-invocation: true
---

# Set up light

Three guards and one settings file. Nothing else is added.

1. Run `vectoralis init light` and show the person what it printed.
   - If the command is not found, the CLI lives in this plugin, at `${CLAUDE_PLUGIN_ROOT}/bin/vectoralis`.
   - In Codex, find it with `ls ~/.codex/plugins/cache/vectoralis/light/*/bin/vectoralis`.
2. If it found no test command or no formatter, ask the person for the command and set `test` or `format` in `harness/settings.json`.
3. If it offered a starter instructions file, ask the person first. On a yes, run `vectoralis init light --starter`.
4. If it said a command is not approved on this machine, show the person the command and ask. On a yes, run `vectoralis trust`.
5. Run `vectoralis guards` and show the table.
6. Tell the person what is on now:
   - no secret is written to a file or printed
   - the formatter runs after every edit
   - the tests run before the agent says done

**What to write where:** only `harness/settings.json`. The person's instructions file is theirs.
