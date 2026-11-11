# MCP

An MCP server gives the agent tools for a system outside the repository: an issue tracker, a database, a browser. Each one costs context and widens what the agent can reach. Read this before you add one, and when a session feels crowded.

**Contents:** What a server costs · The test · The cheaper choice first · Scopes and where the config lives · In Claude Code · In Codex · With the harness · What can go wrong

---

## What a server costs

| | Claude Code | Codex |
|---|---|---|
| Always in the context | the tool names and the server's instructions. Tool search is on by default, so a tool's full definition loads when Claude uses it | its docs give no figure. They name two places a server's tools reach the model: the initial tools, and tool search |
| When everything loads up front | `ENABLE_TOOL_SEARCH=false`, a server marked `alwaysLoad`, a model older than Opus 4 and Sonnet 4 | not said. `omit_tools_from` takes a server out of either place |
| One tool's output | a warning past 10,000 tokens. Past 25,000 it goes to a file and Claude gets the path | `tools.<tool>.output_token_limit` sets the budget of one tool |
| How you measure it | `/context`, and `/mcp` for the tool count of each server | `/mcp` lists the tools, `/status` shows the token usage |
| How you trim it | switch a server off in `/mcp`, deny a tool with a rule | `enabled = false`, `enabled_tools`, `disabled_tools` |

- **Attention** → one more sign-in to keep alive, one more program to keep trusted.
- **For scale** → this whole harness holds itself to 2,000 tokens always loaded in heavy, and loads about 870 in a new project. `run`: `vectoralis budget`, 2026-11-11. What else loads → [Context](context.md).

`read`: Claude Code [MCP](https://code.claude.com/docs/en/mcp), [MCP quickstart](https://code.claude.com/docs/en/mcp-quickstart), [costs](https://code.claude.com/docs/en/costs). Codex [MCP](https://learn.chatgpt.com/docs/extend/mcp), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [the CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli). 2026-11-11.

## The test

Add a server when all three are true.

1. **It reaches a system outside the repository** → a tracker, a design file, a database, a browser. Both vendors draw this line: Claude Code says to connect one "when you find yourself copying data into chat from another tool", Codex when it "needs capabilities that live outside the local repo".
2. **You use it often** → a server sits in every session, the idle ones too.
3. **It has no good CLI** → the next section.

The first is `read`. The other two are this guide's own rule, from its outline: MCP only for outside systems that need it, because every server costs context.

## The cheaper choice first

- **A CLI** → Claude Code's docs: tools like `gh`, `aws`, `gcloud` and `sentry-cli` "are still more context-efficient than MCP servers because they don't add any per-tool listing". A command costs context when it runs, and not before.
- **A skill around the CLI**, when the steps repeat → its body loads on use. [Cost](cost.md)
- **Then a server**, for what no command reaches. Codex's docs build in the same order: instructions first, then a skill, then MCP "when workflows need external systems".

## Scopes and where the config lives

| Who gets the server | Claude Code | Codex |
|---|---|---|
| You, in this project | `local` scope, the default → `~/.claude.json`, under this project's entry | no such scope |
| Everyone who clones the project | `project` scope → `.mcp.json` at the root. Each person approves it once | `.codex/config.toml` in the project, read in trusted projects only |
| You, in every project | `user` scope → `~/.claude.json` | `~/.codex/config.toml` |
| Brought by something else | a plugin's servers, and the connectors of your claude.ai account | a plugin's servers |

When one name is defined twice, Claude Code takes local, then project, then user.

## In Claude Code

```text
claude mcp add --transport http <name> <url>                    a hosted server
claude mcp add --transport stdio <name> -- <command>            a local program
claude mcp add --scope project --transport http <name> <url>    the same, shared in .mcp.json
claude mcp list                                                 every server, and whether it connects
claude mcp get <name>                                           one server, and its scope
claude mcp remove <name>                                        gone
```

- **In a session** → `/mcp` shows each server, its status and its tool count, and switches one off without removing it.
- **A rule** names a server's tools as `mcp__<server>__<tool>`, or `mcp__<server>__*` for all of them → put it under `ask` or `deny` in `/permissions`.
- **A token** in a shared `.mcp.json` is written as `${VAR}`, so the file holds the name and your environment holds the value.

## In Codex

```text
codex mcp add <name> -- <command>      a local program
codex mcp add <name> --url <url>       a hosted server
codex mcp list                         every server
codex mcp get <name>                   one server
codex mcp login <name>                 sign in, for a server with OAuth
codex mcp remove <name>                gone
```

- **In a session** → `/mcp` lists the tools Codex can call.
- **Where it writes** → `codex mcp add` writes `~/.codex/config.toml`. A project server is a `[mcp_servers.<name>]` table you write in `.codex/config.toml`.
- **Per server** → `enabled = false` switches it off and keeps it. `enabled_tools` is an allow list. `default_tools_approval_mode = "writes"` asks before any tool that is not marked read-only. `bearer_token_env_var` reads the token from your environment.

## With the harness

- **Vectoralis ships no MCP server.** Everything it does is a file in `harness/` or one command, `vectoralis`, and an agent already reads files and runs commands. A server would add a listing to every session and one more program to trust, and give nothing a file does not.
- **GitHub goes through `gh`.** The `pr` skill opens the pull request, watches its checks and reads a failed log with it. [Pull requests](pull-requests.md)
- **Nothing leaves your machine** → no account, no network call. Light loads 0 tokens before you type. `run`: `vectoralis budget`.
- **Light and heavy do not see a server.** The guards read file edits and shell commands, as `plugins/light/hooks/hooks.json` shows. A call to a server's tool passes none of them. Heavy's `sweep` compares the turn's start with its end whoever wrote, so a locked file or a known key that a tool put in the project is still caught when the agent stops.
- **Which server for which work** → one pick per situation, with its cost and its risk, in [the kit](../kit/README.md).

## What can go wrong

- **A tool's output that carries instructions.** A server that fetches outside content hands it to the agent as a tool result. Claude Code's docs: such servers "can expose you to prompt injection risk" → servers you trust, an approval before a tool that writes, and no secrets or push rights in that session. [Safety](safety.md)
- **A token with too much reach.** The server acts with the token you gave it → one repository, read only, where the service offers it. And out of the config: `bearer_token_env_var`, `${VAR}`.
- **A server you never added.** In a `claude -p` run a cloned repository's `.mcp.json` connects with no question. Plugins and claude.ai connectors bring servers too → `/mcp` shows all of them, and `--strict-mcp-config` loads only the ones you pass.
- **Every definition loaded up front, unnoticed.** Tool search off, an old model or `alwaysLoad` puts each tool's full definition in the context → `/context`.
- **A sign-in that outlives the server.** In Claude Code a remove deletes the token on your machine and leaves it valid at the service → `claude mcp logout <name>` first. Codex has `codex mcp logout <name>`.

Left out, each under its vendor's own label: MCP tasks in Claude Code, public beta. [Channels](https://code.claude.com/docs/en/channels), research preview. Code Mode in Codex, under development.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. Every agent line is `read` in the docs linked under the first table, plus Claude Code [permissions](https://code.claude.com/docs/en/permissions) and [CLI flags](https://code.claude.com/docs/en/cli-reference), and Codex [customization](https://learn.chatgpt.com/docs/customization/overview). No server was added or removed here. `run`: `vectoralis budget`, in a new heavy project and a new light one.
