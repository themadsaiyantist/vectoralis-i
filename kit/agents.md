# Agents building agents

This is the work of extending an agent or making a new one: writing skills, packaging plugins, building MCP servers, and building on an agent SDK. Read this page when you have explained the same thing to your agent three times and want it to be a skill, and before you ship a plugin or a server to other people.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) | Writes a skill with you, runs test prompts with and without it, grades the runs, and tunes the description until the skill loads on the right requests. Apache-2.0. | Claude Code. Codex ships its own, built in | one description, a 485-line body on use | `/plugin install skill-creator@claude-plugins-official`. Codex: type `$skill-creator`, [nothing to install](https://learn.chatgpt.com/docs/build-skills) |
| Guard | `mcp-stdout` | Warns when the code of a stdio MCP server writes to stdout, which belongs to the protocol. | both | none, a hook costs no context | below |
| MCP server | [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp) | Searches and reads OpenAI's developer docs: the API, the Agents SDK, Codex and plugins. Public and read-only. | Claude Code, Codex | the docs give no count, only search and page content | `codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp`. Claude Code: `claude mcp add --transport http openaiDeveloperDocs https://developers.openai.com/mcp` |

A stdio server talks to its client over stdout, so one stray log line breaks the session.

```json
{
  "id": "mcp-stdout",
  "why": "a stdio MCP server speaks JSON-RPC on stdout, and one stray line breaks the session",
  "on": "write",
  "path": "src/**/*.ts",
  "pattern": "console\\.log\\(",
  "mode": "warn",
  "message": "A stdio MCP server owns stdout for JSON-RPC. Log with console.error, which writes to stderr.",
  "payloads": [
    { "name": "catches a log to stdout", "path": "src/server.ts", "text": "console.log('listening')", "expect": "hit" },
    { "name": "passes a log to stderr", "path": "src/server.ts", "text": "console.error('listening')", "expect": "pass" },
    { "name": "leaves other folders alone", "path": "scripts/build.ts", "text": "console.log('built')", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/mcp-stdout.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [plugin-dev](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev) | Seven skills for Claude Code plugins: hooks, MCP wiring, structure, settings, commands, agents, skills. `/plugin-dev:create-plugin` walks the build from the first question to validation and testing. | free |
| Skill | [mcp-server-dev](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev) | Three skills that choose the shape of an MCP server with you, remote HTTP or local stdio, and scaffold it. | free |
| Skill | [agent-sdk-dev](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/agent-sdk-dev) | `/new-sdk-app` scaffolds a Claude Agent SDK project in Python or TypeScript, and a verifier agent checks it against the docs. | free |
| Skill | [OpenAI Developers plugin](https://github.com/openai/plugins/tree/main/plugins/openai-developers) | The Codex side: an `agents-sdk` skill that builds, runs and evaluates Agents SDK apps, and one that sorts API failures by cause. | free |
| Guard | [`secrets`](../guide/guards.md) | Built in, light profile. Blocks an API key written into `.mcp.json`, a manifest or an SDK script. | free, ours |
| Guard | [`tests`](../guide/guards.md) | Built in, light profile. Blocks "done" while the test command fails, so a server or a plugin ships with its checks green. | free, ours |
| Guard | [hookify](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/hookify) | Turns a sentence, or a mistake it finds in the conversation, into a hook rule kept as a small Markdown file. Claude Code only. | free |
| MCP server | [Claude Code Docs MCP](https://code.claude.com/docs/en/agent-sdk/mcp) | The same idea from the other maker, at `https://code.claude.com/docs/mcp`, for a Codex session that builds a Claude Code plugin. | free |
| MCP server | [Context7](https://github.com/upstash/context7) | Current docs and code examples for a library you name. Two tools, or its `ctx7` CLI with a skill and no server. | free, a free API key raises the rate limit |
| MCP server | [Everything server](https://github.com/modelcontextprotocol/servers/tree/main/src/everything) | A test server that exercises every feature of MCP. Point the client or the agent you are building at it. | free |

## When each earns its place

- **The skill** → the second time you rewrite a skill by hand because it loads on the wrong request, or not at all. Its description is all a session carries until you call it. For a whole plugin, Codex has [`$plugin-creator`](https://developers.openai.com/plugins/build/plugins) built in, and Claude Code has `plugin-dev` from the table above.
- **The guard** → the day you start a server that runs over stdio, because [MCP's build guide](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server) says it plainly: never write to stdout. For a Python server, set `"path"` to `"src/**/*.py"` and `"pattern"` to `"^\\s*print\\((?!.*file=)"`.
- **The MCP server** → you build on an OpenAI SDK or write a Codex plugin, and the agent's memory of the API is older than the API. OpenAI's page gives one line for `AGENTS.md` so the agent reaches for the server unasked. Claude Code loads only the tool names until one is called, [by its docs](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search). For questions about Claude Code itself it needs no server: the built-in [`claude-code-guide` subagent](https://code.claude.com/docs/en/sub-agents) costs nothing until it runs.
- **The CLI first** → testing a server you built needs no MCP client in the session. The [Inspector](https://github.com/modelcontextprotocol/inspector) lists its tools from the shell: `npx @modelcontextprotocol/inspector --cli node build/index.js --protocol-era modern --method tools/list`.

## Left out, and why

- [openai/skills](https://github.com/openai/skills) → its README opens with "This repository is deprecated" and points to `openai/plugins`.
- [The reference servers](https://github.com/modelcontextprotocol/servers) for files, git and memory → their README calls them educational examples, not production-ready, and both agents already read files and run git on their own.
- [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) → no commit since March 2026, and no licence file.

## A sample to study

[Slack skills plugin](https://github.com/slackapi/slack-skills-plugin) → one folder that its maker ships to Claude Code, Codex and Cursor: three manifests, nine skills, five commands and a hosted MCP server. Its tests are the part to study: unit tests hold every skill's frontmatter to rules, such as a description of at most 1,024 characters that opens on its trigger, and an eval checks that a model picks the right tool or skill for each request on a list. `referenced`

## How to do it better

- **The eval asks one model to pick a name from a list** → it never starts Claude Code or Codex, so it cannot show that a skill loads in a real session. Run the same requests through the agents you ship to: `skill-creator` does it for a skill, [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals) for a plugin against a run without it, and OpenAI's [plugin-eval](https://github.com/openai/plugins/tree/main/plugins/plugin-eval) with real `codex exec` runs.
- **Nothing measures what the plugin costs** → nine descriptions and five commands ride along in every session. [`claude plugin details`](https://code.claude.com/docs/en/plugins/measure) prints the always-on tokens, and `plugin-eval explain-budget` does the sum on the Codex side.
- **The agents do not get the same thing** → the Codex manifest carries an empty `mcpServers`, so Codex gets the skills and no server. The README says so in a sentence. Say it in a table of gaps, one row per piece and one column per agent, next to the install lines.
- **A plugin that can send messages ships no hook** → a plugin can carry its own guard: a `hooks/hooks.json` with a `PreToolUse` matcher on the send tool, which [the hooks reference](https://code.claude.com/docs/en/hooks) shows for `mcp__<server>__<tool>` names.

## Where people talk

- [r/mcp](https://www.reddit.com/r/mcp/) → building and running MCP servers, and what breaks in them.
- [r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/) → skills, plugins and hooks in daily use.
- [r/codex](https://www.reddit.com/r/codex/) → Codex skills, plugins and the SDK.
- [r/AI_Agents](https://www.reddit.com/r/AI_Agents/) → agents at large: frameworks, tools, and what people build with them.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
