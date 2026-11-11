# Layout

Where every file of an agent setup goes, at which level, and how the files point at each other. Read it before you lay out a new project, and each time you are about to add a file and ask where it belongs.

**Contents:** The levels · Where each thing lives · How one file points at another · The folders · Rules of thumb · In Claude Code · In Codex · With the harness · What can go wrong

---

## The levels

| | Claude Code: [memory](https://code.claude.com/docs/en/memory.md), [settings](https://code.claude.com/docs/en/settings.md) | Codex: [`AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [config](https://learn.chatgpt.com/docs/config-file/config-basic) |
|---|---|---|
| **Managed** → everyone on the machine, set by an admin | `CLAUDE.md` and `managed-settings.json` in `/etc/claude-code/` on Linux and WSL, loaded first | `config.toml` for defaults and `requirements.toml` for limits, in `/etc/codex/` |
| **User**, the global level → you, in every project | `~/.claude/CLAUDE.md` and `~/.claude/rules/`, at launch | `~/.codex/AGENTS.override.md`, else `~/.codex/AGENTS.md`, at launch |
| **Project**, committed → everyone who clones it | `CLAUDE.md` or `.claude/CLAUDE.md` in the folder you start in and in every folder above it, and `.claude/rules/`, at launch | one file per folder, from the root that holds `.git` down to the folder you start in, at launch: `AGENTS.override.md`, else `AGENTS.md`, else a name from `project_doc_fallback_filenames` |
| **Local** → you, in this project, never committed | `CLAUDE.local.md`, at launch, right after the `CLAUDE.md` beside it | no such file in its docs |
| **A subfolder** → the work in that folder | its `CLAUDE.md`, once Claude reads or edits a file there. A rule with `paths`, once a matching file is opened | its `AGENTS.md`, only when you start Codex in that folder or below it |
| **When two disagree** | no file wins. All are joined, the widest level first and the nearest last, and Claude may follow either line | the nearest file wins. The chain is joined from the root down, so it comes last |
| **Settings**, highest first | managed → `--settings` → `.claude/settings.local.json` → `.claude/settings.json` → `~/.claude/settings.json`. Lists such as `permissions.allow` merge, and a deny at any level holds | flags and `--config` → `.codex/config.toml`, the closest first → a `--profile` file → `~/.codex/config.toml` → managed defaults → `/etc/codex/config.toml` |

## Where each thing lives

| The thing | Claude Code: [its folder](https://code.claude.com/docs/en/claude-directory.md) | Codex: [customization](https://learn.chatgpt.com/docs/customization/overview) | Who sees it | Commit it |
|---|---|---|---|---|
| The instructions file | `CLAUDE.md` at the root | `AGENTS.md` at the root | the team | yes |
| A personal preference | `~/.claude/CLAUDE.md`. For one project, `CLAUDE.local.md` | `~/.codex/AGENTS.md` | you | no |
| A rule for one folder | `<folder>/CLAUDE.md`, or `.claude/rules/<name>.md` with `paths` | `<folder>/AGENTS.md` | the team | yes |
| Settings and permissions | `.claude/settings.json`. Yours: `.claude/settings.local.json`, `~/.claude/settings.json` | `.codex/config.toml`. Yours: `~/.codex/config.toml` | the team, or you | the project file |
| A skill | `.claude/skills/<name>/SKILL.md`. Yours: `~/.claude/skills/` | `.agents/skills/<name>/SKILL.md`. Yours: `~/.agents/skills/` | the team, or you | the project one |
| A subagent | `.claude/agents/<name>.md`. Yours: `~/.claude/agents/` | `.codex/agents/<name>.toml`. Yours: `~/.codex/agents/` | the team, or you | the project one |
| A hook | the `hooks` key of a settings file. There is no hooks file of its own | `.codex/hooks.json`, or `[hooks]` in `config.toml`. Yours: `~/.codex/hooks.json` | whoever has the file | with its file |
| An MCP server | `.mcp.json` at the root, not inside `.claude/`. Yours: `~/.claude.json`, written by `claude mcp add` | `[mcp_servers.<name>]` in `.codex/config.toml`. Yours: `~/.codex/config.toml` | the team, or you | the project file |
| Memory the agent writes itself | `~/.claude/projects/<project>/memory/`, on by default | under `~/.codex/`, off by default | you, on this machine | never. It sits outside the repository |
| A secret | an environment variable, written `${VAR}` in `.mcp.json`. Your login stays in `~/.claude/` or the Keychain | an environment variable, named by `bearer_token_env_var`. Your login stays in `~/.codex/auth.json` or the keyring | you | never |

## How one file points at another

- **An import** → `@path` in a `CLAUDE.md` loads that file at launch, with the file that names it. It organizes and saves nothing: the file loads in full, in every session. [Imports](https://code.claude.com/docs/en/memory.md#import-additional-files)
- **Its path** is relative to the file that holds the import, not to the folder you work in. A path that resolves outside your working folder asks for your approval once per project, and stays off if you decline. An imported file may import another, four hops deep at most.
- **In a code span or a code block** it is plain text → `` `@docs/api.md` `` imports nothing. It is a pointer: nothing loads, and the agent opens the file only when it decides the task needs it.
- **Instead of one long file** → a rule in `.claude/rules/` with `paths` loads when a matching file is opened, and a skill holds a procedure until it is called.
- **One source for both agents** → `AGENTS.md` holds the instructions and `CLAUDE.md` is one line, `@AGENTS.md`, with anything for Claude Code alone below it. Claude Code also reads `AGENTS.md` by itself, but only while no `CLAUDE.md` and no `CLAUDE.local.md` sits in your folder or above it. The one line keeps that from changing the day you add a `CLAUDE.local.md`.
- **Codex has no import** → [its docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md) describe none. In its place: one file per folder, joined from the root down, and `AGENTS.override.md` to replace the `AGENTS.md` beside it. For a file that grows, its [best practices](https://learn.chatgpt.com/guides/best-practices) keep the main file short and name the task files in it: pointers.

## The folders

```text
shop/                                   the project. Committed, except the lines marked ignored
├── AGENTS.md                           the instructions, for both agents
├── CLAUDE.md                           one line: @AGENTS.md
├── CLAUDE.local.md                     your own notes for this project, Claude Code only. Ignored
├── .mcp.json                           the MCP servers the team shares in Claude Code. Secrets as ${VAR}
├── .gitignore                          CLAUDE.local.md, .claude/settings.local.json, .env, harness/dashboard.html
├── .claude/settings.json               permissions, hooks, the plugins switched on
├── .claude/settings.local.json         your own overrides. Ignored
├── .claude/rules/payments.md           a rule with `paths`, loaded with the files it names
├── .claude/agents/reviewer.md          a subagent
├── .claude/skills/release              a symlink to .agents/skills/release, so the skill has one home
├── .agents/skills/release/SKILL.md     a procedure. Both agents read this format
├── .codex/config.toml                  settings, MCP servers, plugins. Read once you trust the project
├── .codex/hooks.json                   hooks, each one reviewed in /hooks
├── .codex/agents/reviewer.toml         a subagent
├── harness/                            the records of this harness: settings.json for light, seven more for heavy
└── src/payments/AGENTS.md              what holds in that folder alone, beside a one-line CLAUDE.md

~/                                      your home folder. How you work, never a fact about one project
├── .claude/CLAUDE.md                   how you like to work, in every project
├── .claude/settings.json               your model, your theme, your own permission rules
├── .claude/rules/  skills/  agents/    your own, in every project
├── .claude/projects/<project>/memory/  what Claude wrote for itself. Read it, prune it
├── .claude.json                        kept by Claude Code: your account, your MCP servers, the folders you trusted
├── .codex/AGENTS.md                    how you like to work, in every project
├── .codex/config.toml                  your model, sandbox and approvals, your MCP servers, the projects you trusted
├── .codex/hooks.json  agents/          your own, in every project
└── .agents/skills/                     your own Codex skills, in every project
```

## Rules of thumb

1. **The instructions file is paid in every turn** → keep it short. Claude Code's docs advise under 200 lines. Codex stops adding files at 32 KiB, the key `project_doc_max_bytes`. [Context](context.md)
2. **A procedure goes into a skill** → never into the instructions file.
3. **A rule a machine can check goes into a guard** → an instruction is a request, a hook is enforcement. [Guards](guards.md)
4. **A personal habit goes to the user level** → how you like answers, your shortcuts, a skill you use everywhere. Never a fact about one project, or a rule the team relies on.
5. **A secret goes nowhere in the repository** → a file names the variable, never the value. [Safety](safety.md)
6. **One fact has one home** → every other file points at it.

## In Claude Code

- **See what loaded** → `/context all` lists the instruction files, `/memory` opens them, `/status` names the settings files, and `/doctor prompt-audit` finds lines that contradict each other. [Debug your configuration](https://code.claude.com/docs/en/debug-your-config.md)
- **Start in the root** → `.claude/settings.json` is read from the folder you start in, not from the folders above it. That file is where the team's permissions, hooks and plugins are switched on.

## In Codex

- **See what loaded** → `codex --ask-for-approval never "Summarize the current instructions."` for the chain, `/debug-config` for the settings layers. [The CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- **Trust the project** → Codex reads a repository's `.codex/` only in a project you trust: `trust_level = "trusted"` under `[projects."<path>"]` in `~/.codex/config.toml`. Untrusted, it skips that folder's config, hooks and rules. [Project config](https://learn.chatgpt.com/docs/config-file/config-advanced)

## With the harness

- **In the project** → light adds one file, `harness/settings.json`. Heavy adds seven records beside it and one line in `.gitignore`. In Claude Code the plugins sit at project scope: an entry under `enabledPlugins` in `.claude/settings.json`. In Codex a trusted project switches them on in `.codex/config.toml`. [Install](install.md)
- **At the user level** → one file, `~/.vectoralis/trusted.json`: the test and format commands you approved on this machine, kept outside the repository so that a repository cannot approve itself. No instruction, no rule and no guard goes there. The agent's own installer adds the plugin's files, under `~/.claude/plugins/` or `~/.codex/plugins/`, and Claude Code names the marketplace in `~/.claude/settings.json`.
- **It never edits an instructions file** → heavy's core, `harness/rules.md`, reaches the agent through a hook at session start, not through an import. [Context](context.md)
- **The starter** → `vectoralis init light --starter` writes the first two files of the tree above, `AGENTS.md` and a one-line `CLAUDE.md`, only where the project has no instructions file at all, a `.claude/CLAUDE.md` included: the project's name, the test and format commands it found, two conventions, one ask-first line. It printed `Written: AGENTS.md, CLAUDE.md`, and `Written: nothing` on a second run. `run`, in an empty scratch project, on [`cmd_init`](../plugins/light/engine/cli.py) and [its template](../plugins/light/templates/AGENTS.md).

## What can go wrong

- **A rule lives in two files and drifts.** `CLAUDE.md` names one test command, `AGENTS.md` another, and each agent follows its own → one home, and the other file imports it.
- **A local file is committed.** A `CLAUDE.local.md`, or a `.claude/settings.local.json` made by hand: Claude Code keeps that file out of git only when it creates it itself → both names in `.gitignore`, on the first day.
- **An import loads a large file in every session.** `@docs/architecture.md` reads like a link and loads the whole document at every launch → put the path in backticks, or move the text to a rule with `paths`.
- **A global instruction surprises a teammate.** "Always use pnpm" in your `~/.claude/CLAUDE.md` holds on your machine alone. A teammate's clone and a cloud session never see it → a fact about the project goes into the project's file.
- **A nested file never loads.** Claude Code reads `src/payments/CLAUDE.md` only after it opens a file in that folder, and Codex reads `src/payments/AGENTS.md` only when you start there → a rule that must always hold goes in the root file, or in a guard.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `read` in Claude Code's docs, beside the pages linked above: [permissions](https://code.claude.com/docs/en/permissions.md), [managed settings](https://code.claude.com/docs/en/managed-settings.md), [skills](https://code.claude.com/docs/en/skills.md), [subagents](https://code.claude.com/docs/en/sub-agents.md), [hooks](https://code.claude.com/docs/en/hooks.md), [MCP](https://code.claude.com/docs/en/mcp.md), [plugin scopes](https://code.claude.com/docs/en/plugins/install.md), [plugin loading](https://code.claude.com/docs/en/plugins/loading.md), [extending Claude Code](https://code.claude.com/docs/en/features-overview.md), [large codebases](https://code.claude.com/docs/en/large-codebases.md), [authentication](https://code.claude.com/docs/en/authentication.md), [cloud sessions](https://code.claude.com/docs/en/cloud-environments.md). `read` in Codex's docs: [the configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration), [skills](https://learn.chatgpt.com/docs/build-skills), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [hooks](https://learn.chatgpt.com/docs/hooks), [MCP](https://learn.chatgpt.com/docs/extend/mcp), [memories](https://learn.chatgpt.com/docs/customization/memories), [authentication](https://learn.chatgpt.com/docs/auth). `run`: `vectoralis init light`, `--starter` and `init heavy`, in an empty scratch project with `VECTORALIS_HOME` pointed at a scratch folder. No agent session was run for this page, and the symlinked skill folder is `read` in both docs, not tried.
