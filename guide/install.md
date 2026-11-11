# Install

One package, two agents. Two commands, then one skill. Read this when you are ready to try it on a real project.

**Contents:** What you install · In Claude Code · In Codex · Check it works · For a team · Update and remove · What can go wrong

---

## What you install

Two plugins from one marketplace. A plugin is a folder of skills and hooks an agent installs as one thing.

| Plugin | What it carries | Install it when |
|---|---|---|
| `light` | the engine, the `vectoralis` command, three guards | always. It is the base |
| `heavy` | ten skills and two subagents that drive the records | one of [the five signals](start.md) is true |

- **A skill** is a procedure the agent loads when the task calls for it. Only its one-line description is always in the context.
- **A hook** is a command the agent runs at a fixed moment: before a write, after an edit, when it stops. The guards are hooks.
- Nothing is downloaded at run time, nothing phones home, and no MCP server is added.

---

## In Claude Code

```text
claude plugin marketplace add themadsaiyantist/vectoralis-i
claude plugin install light@vectoralis --scope project
```

Then, in a session:

```text
/light:setup
```

- `--scope project` writes the plugin into `.claude/settings.json`, which you commit.
- For heavy → `claude plugin install heavy@vectoralis --scope project` → `/heavy:setup`. It installs and enables light too.

`read`: [plugin dependencies](https://code.claude.com/docs/en/plugins/dependencies.md) and [the plugin commands](https://code.claude.com/docs/en/plugins/cli-reference.md), 2026-11-11.

---

## In Codex

```text
codex plugin marketplace add themadsaiyantist/vectoralis-i
codex plugin add light@vectoralis
```

Then, in a session:

```text
/hooks
$light:setup
```

- `/hooks` → review the hooks and trust them. Codex runs no hook before that, and asks again when a hook changes.
- For heavy → `codex plugin add heavy@vectoralis` as well. Codex has no plugin dependencies, so you add both.

`read`: [Codex plugins](https://learn.chatgpt.com/docs/plugins) and [Codex hooks](https://learn.chatgpt.com/docs/hooks), 2026-11-11. Not run in Codex yet, see [Codex](codex.md).

---

## Check it works

Ask the agent to run this, or run it yourself:

```text
$ vectoralis guards
guard        here    default  proof
secrets      block   block    12 of 12 payloads behave
format       off     warn     5 of 5 payloads behave
tests        block   block    5 of 5 payloads behave
...
81 payloads, the slowest answer took 48 ms
```

- **here** is how the guard is set in this project. `off` means it has nothing to run yet: no formatter was found.
- **proof** is the guard tested against its own payloads, on your machine, now.

`run` on this repository, 2026-11-11.

---

## For a team

- Install at project scope and commit `.claude/settings.json`. The plugin is then switched on for everyone.
- Each person still runs the install once in their own clone. Switching a plugin on does not download it.
- In Codex, a trusted project can switch them on in `.codex/config.toml`. [Team](team.md) has the lines.

---

## Update and remove

| | Claude Code | Codex |
|---|---|---|
| Update | `claude plugin marketplace update vectoralis` | `codex plugin marketplace upgrade vectoralis` |
| Remove | `claude plugin uninstall light@vectoralis` | `codex plugin remove light@vectoralis` |

Your records are plain files in `harness/`. Removing a plugin leaves them where they are.

---

## What can go wrong

- **`vectoralis` is not found in Codex** → Codex does not put a plugin's commands on the path. The skills call it by its path, under `~/.codex/plugins/cache/vectoralis/light/`.
- **A hook never fires in Codex** → it was not trusted. Open `/hooks`.
- **A teammate has no guards** → they pulled the settings and never ran the install.
- **The `tests` guard is off** → no test command was found. Set `test` in `harness/settings.json`.
- **Python is missing** → the engine needs Python 3.9 or later and nothing else.

Next → [Light](light.md).

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. The guard table is `run`. The install commands of both agents are `read` in their docs. The plugin itself was loaded into live Claude Code sessions with `--plugin-dir`, see [Light](light.md).
