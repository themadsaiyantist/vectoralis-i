# Other agents

Vectoralis installs as a plugin in Claude Code and in Codex. In any other agent that reads `AGENTS.md`, the records and the command still work, and the guards do not. Read this when your agent is neither of the two, or when one team uses several.

**Contents:** What carries over · Which agents read AGENTS.md · The smallest setup · In Claude Code · In Codex · With the harness · What can go wrong

---

## What carries over

| The piece | What it needs | In another agent |
|---|---|---|
| The records in `harness/` | an agent that reads and writes files | yes. They are plain Markdown |
| `vectoralis check`, `status`, `budget`, `dashboard`, `fail`, `affirm`, `init` | Python 3 | yes, run by hand or by a script |
| The guards | hooks. The engine reads the hook payloads of Claude Code and of Codex, and no other | no |
| The grants: `unlock`, `tick`, `lesson:`, `promote` | the hook that reads your message | no. They become a rule the agent is asked to keep |
| The skills and the two subagents | a plugin | no. The seven steps are written in `harness/rules.md` |
| The briefing at session start | the session hook | `vectoralis status` prints the same lines |

## Which agents read AGENTS.md

Each row was read in that agent's own docs on 2026-11-11, and the link goes there.

| Agent | What its docs say |
|---|---|
| [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | reads it before any work: one in `~/.codex`, then each one from the project root down to your folder |
| [Claude Code](https://code.claude.com/docs/en/memory) | reads it when no `CLAUDE.md` sits in your folder or above it, from v2.1.277 |
| GitHub Copilot [on GitHub](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions), [in its CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions), [in VS Code](https://code.visualstudio.com/docs/agent-customization/custom-instructions) | reads the `AGENTS.md` files of the repository. On GitHub the nearest one wins |
| [Cursor](https://cursor.com/docs/rules) | in the project root and in subfolders, as the plain alternative to `.cursor/rules` |
| [Amp](https://ampcode.com/docs/customize/agents-md) | always includes the ones in the working folder and its parents |
| [OpenCode](https://opencode.ai/docs/instructions/) | loads each one from the workspace folder upward, and does not fall back to `CLAUDE.md` |
| [Zed](https://zed.dev/docs/ai/instructions) | takes the first match of a list of rule files. `AGENTS.md` is on it, after `.rules` and `.cursorrules` |
| [goose](https://goose-docs.ai/docs/guides/context-engineering/using-goosehints/) | looks for `AGENTS.md`, then `.goosehints`, by default |
| [Junie](https://junie.jetbrains.com/docs/guidelines-and-memory.html) | its CLI reads the one in the project root, after `.junie/AGENTS.md` |
| [Warp](https://docs.warp.dev/agents/capabilities/rules/) | the default project rules file. `WARP.md` wins where both exist |
| [Devin](https://docs.devin.ai/onboard-devin/agents-md), [Devin Local](https://docs.devin.ai/desktop/devin-local/customizations) | Devin looks for it before it codes, and takes the first 16 KiB of each file. Devin Local reads it as an always-on rule |
| [Factory Droid](https://docs.factory.com/harness/agents-md) | carries it into every session |
| [Kilo Code](https://kilo.ai/docs/customize/agents-md), [Roo Code](https://roocodeinc.github.io/Roo-Code/features/custom-instructions/) | load the one in the project root by default |
| [OpenHands](https://docs.openhands.dev/overview/skills) | puts the root one in full in the first system prompt, and also knows `CLAUDE.md` and `GEMINI.md`. Skills in `.agents/skills/` |

- **Only after a setting** → [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/) reads `GEMINI.md`. It reads `AGENTS.md` once `context.fileName` in its `settings.json` lists it.
- **Not listed** → [Aider](https://aider.chat/docs/usage/conventions.html): its docs load a conventions file you name with `--read`, and name no `AGENTS.md`. [Jules](https://jules.google/docs/) looks for the file and calls itself experimental.

## The smallest setup

For GitHub Copilot CLI. Steps 1 to 3 and 5 are the same in every agent of the table.

1. **Get the command** → clone this repository beside your work. The command is `plugins/light/bin/vectoralis`, with its engine in the folder next to it. Python 3, standard library only.
2. **Write the records** → in your project, `python3 path/to/plugins/light/bin/vectoralis init heavy`. It writes `harness/` and one line in `.gitignore`, and touches no instructions file.
3. **Point `AGENTS.md` at them** → these lines are yours to add. Vectoralis never edits that file:

```markdown
## How the work runs here

- If this session did not open with a Vectoralis briefing, read `harness/rules.md` and the `## Now` section of `harness/todo.md` before the first edit.
- Before you say done, run the tests and `python3 path/to/plugins/light/bin/vectoralis check`.
- Never tick a box under `## Yours` or in the last column of the tracker, never write in `harness/lessons.md`, never remove a line of `harness/locks.md`. Ask the person.
```

4. **Check that it loaded** → start the agent in the repository root. In Copilot CLI, `/instructions` lists the instruction files it found.
5. **Give the check to a machine** → an instruction can be skipped. An exit code cannot. Run the command in a git pre-commit hook and in CI, as this repository does with `tools/check.sh` and its CI workflow. It exits 1 on any flag:

```text
$ python3 path/to/plugins/light/bin/vectoralis check
STALE: tracker: `cart.py` changed after its row was ticked
1 flag(s).
```

`run`: a new project, set up by hand with no agent and no hook, 2026-11-11. The row was ticked, then the file changed.

## In Claude Code

- **With the plugin** → the hooks print `harness/rules.md` and the briefing, and the guards run. The first line above then asks for nothing: the session opened with a briefing.
- **Both files** → Claude Code reads `AGENTS.md` by itself only where there is no `CLAUDE.md`. With both it reads `CLAUDE.md` alone. So keep one file, and let a one-line `CLAUDE.md` import it: `@AGENTS.md`. `vectoralis init light --starter` wrote exactly that pair in a folder that had neither. `run`.
- **Check** → `/memory` lists the instruction files that loaded.

## In Codex

- **With the plugins**, and the hooks trusted → the same as in Claude Code. [Codex](codex.md)
- **The limit** → Codex stops adding instruction files at 32 KiB in all. Pointers, not copies.
- **The command** is not on the path in Codex. The skills call it by its path, and so do you.

## With the harness

| | Light | Heavy |
|---|---|---|
| In Claude Code and Codex | three guards, enforced | the records, and the guards that keep them true |
| In another agent | nothing carries over, because light is its guards. Use the agent's own hooks, or a git pre-commit hook that runs the tests | the records, kept by instruction, and `vectoralis check` to catch what drifted |

## What can go wrong

- **An instruction is not a guard.** In another agent nothing blocks a secret, a write to locked work or a ticked box → the check in a pre-commit hook and in CI, and your own eyes on `harness/` in every pull request.
- **Two instruction files that drift.** `CLAUDE.md` says one thing, `AGENTS.md` another, and Claude Code reads the first alone → one file, imported.
- **A file that hides `AGENTS.md`.** Zed takes the first match of its list, so an old `.cursorrules` wins. Warp prefers `WARP.md`. Gemini CLI needs its setting → ask the agent which instruction files it loaded before you trust that it read yours.
- **A hook format that looks the same.** OpenHands reads hooks from `.openhands/hooks.json` in Claude Code's format, with its own tool names, such as `terminal` for `Bash`. The engine reads neither its file nor its names, so no guard runs there → the pre-commit hook and CI. `read`: [OpenHands hooks](https://docs.openhands.dev/openhands/usage/customization/hooks), 2026-11-11.
- **A file past its limit.** Codex stops at 32 KiB in all. Devin takes the first 16 KiB of each file → keep `AGENTS.md` to pointers, and let `harness/rules.md` hold the rules.
- **The rules loaded twice.** A plain "read `harness/rules.md`" costs about 740 tokens a second time where the hook already printed them → the "if" that opens the first line above. `run`: `vectoralis budget`.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `read`: each agent's own docs, linked in the table, with Claude Code [memory](https://code.claude.com/docs/en/memory) and Codex [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) for the two sections on them. `run`: every `vectoralis` command of the first table, by hand in new projects. No agent of the second table was run here, so the setup is proven up to the moment the agent starts.
