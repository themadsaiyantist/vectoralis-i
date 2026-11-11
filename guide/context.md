# Context

What loads into an agent's context, what it costs, and how the core stays small. Read this when a session slows down or forgets a rule, and before you add one more thing that is always loaded.

**Contents:** What loads before you type · How to see it · The habits that keep it small · In Claude Code · In Codex · With the harness · What can go wrong

---

## What loads before you type

The context is everything the model reads on a turn. Claude Code sends the whole of it again on every turn, at a discount while its cache is warm. So what is always loaded is paid for in every turn of every session.

| The piece | Claude Code | Codex |
|---|---|---|
| The system prompt and the built-in tools | always | always |
| The instructions file | every `CLAUDE.md` from your folder up, in full. `AGENTS.md` where there is no `CLAUDE.md` | the `AGENTS.md` chain, yours and then the project's, up to 32 KiB in all |
| Skills | each name and description. The body loads on use | each name, description and path. The body loads on use |
| Subagents | each description | not stated in its docs |
| MCP servers | the tool names and the server's instructions. A tool's schema loads when it is used | the tools of each enabled server. Its docs give no cost |
| Memory | the first 200 lines or 25 KB of `MEMORY.md` | off by default. Switched on, its memories go into new sessions |
| A hook's output at session start | added as context, up to 10,000 characters | added as context, about 2,500 tokens per message |

The window is large: 1M tokens on Claude Code's current models, 500,000 for GPT-6.1 Sol in Codex. Small is not about running out. A long file is paid for in every turn, and its rules are followed less.

`read`: [the context window](https://code.claude.com/docs/en/context-window.md), [context cost by feature](https://code.claude.com/docs/en/features-overview.md#understand-context-costs), [memory](https://code.claude.com/docs/en/memory.md), [Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Codex memories](https://learn.chatgpt.com/docs/customization/memories), 2026-11-11.

---

## How to see it

| You want to see | Claude Code | Codex |
|---|---|---|
| Everything, by category | `/context`, and `/context all` for every item | `/status`: the model, the token usage, the context left |
| The context share, all the time | a status line, set up with `/statusline` | `/statusline` → the context item |
| Which instruction files loaded | `/context` lists them under memory files. `/memory` opens them | start with `codex -c log_dir=./.codex-log`, then read `codex-tui.log` |
| The skills, by cost | `/skills`, then `t` | `/skills` |
| The MCP tools | `/mcp` | `/mcp` |
| What one plugin adds | `claude plugin details <name>`, in your shell | not in its docs |

- `/context` lists the system prompt, the system tools, the MCP tools, the subagents, the memory files, the skills and the messages. Codex's docs show no breakdown by piece.
- `claude plugin details` counts names and descriptions, and gives a hook no cost. Heavy's larger share arrives through a hook, which is why `vectoralis budget` counts it.

---

## The habits that keep it small

1. **A short instructions file.** Claude Code's docs: under 200 lines. Codex's: keep it small, and past 32 KiB nothing more is added. A procedure belongs in a skill.
2. **Skills that load on use.** Only the description is always there, so write it short, with the use case first. Claude Code cuts one at 1,536 characters and gives the whole list 1% of the window. Codex gives it 2%.
3. **A search instead of a read.** A file that is read stays in the conversation. Name the function and the file in the task, and let the agent search for the rest.
4. **A subagent for a flood of files.** It reads in a context of its own and returns a summary. Ask for a short one. [Agents](agents.md)
5. **A new session between unrelated tasks.** `/clear` in both agents. The next task stops paying for the last one. [Handoff](handoff.md)
6. **A command before a server.** `gh` adds nothing to the context until it runs. An MCP server lists its tools in every session. [MCP](mcp.md)

---

## In Claude Code

- `/doctor` proposes trims for a checked-in `CLAUDE.md`, and estimates what the skill list costs.
- `disable-model-invocation: true` in a skill keeps even its description out until you call it.
- An idle MCP server costs its tool names and its instructions, no more. Tool search is on by default.
- An edit to `CLAUDE.md` in the middle of a session reaches the session at the next `/clear`, `/compact` or restart, not before.
- A comment in `CLAUDE.md`, `<!-- like this -->`, is stripped before the file loads. A note for people costs nothing.

## In Codex

- `project_doc_max_bytes` is the 32 KiB limit on the instruction files. Past it, the rest is not added.
- `skills.max_context_tokens` is the budget of the skill list, up to 10,000 tokens.
- `enabled_tools` under an MCP server names the only tools Codex may see.
- **The gap** → `disable-model-invocation` is a Claude Code field. Codex's own switch is `allow_implicit_invocation: false` in a skill's `agents/openai.yaml`, so the two `setup` descriptions may be listed there, one line each. Not run here.

---

## With the harness

What is always loaded on the day you set it up, in tokens:

| The piece | Light | Heavy | How it arrives |
|---|---|---|---|
| The guards | 0 | 0 | hooks. A guard costs context only when it speaks |
| The skill and subagent descriptions | 0 | about 240 | with the plugin |
| `harness/rules.md`, the core | 0 | about 500 | printed by the session-start hook |
| The briefing | 0 | about 130 | printed right after it |
| **Always loaded** | **0** | **about 870** | the caps are 300 and 2,000 |

- `run`: `vectoralis budget` printed 871 in a project fresh from `vectoralis init heavy`, and 0 for light, 2026-11-11. It counts characters and divides by four, and says it is an estimate.
- **The briefing is the piece that moves.** It prints up to ten lines of `## Now`, the next three boxes, the open failures, the locks and the stale flags. In this repository it read 191 and, later the same afternoon, 303, when `## Now` went from one line to five. That is why the total in [Cost](cost.md), measured on this repository, is higher. `run`.
- **Over the cap, `vectoralis check` fails.** What each skill weighs when it loads is in [Cost](cost.md).
- The core arrives through a hook because your instructions file is yours. Both agents run that hook again after a compaction, so the core comes back by itself.

---

## What can go wrong

- **An import that hides the size.** Splitting `CLAUDE.md` into imported files changes nothing, because they load together → a skill, or a rule scoped to a path.
- **A skill that stopped triggering.** With too many skills, Claude Code drops the descriptions of the least used and Codex shortens them or leaves skills out → `/skills`, and switch off what you do not use.
- **A subagent's report that floods you anyway.** Twenty long reports fill the context they were meant to spare → ask for the answer, not the journey.
- **A `## Now` that grows.** It is printed in every session and after every compaction → ten lines, then `vectoralis budget`.
- **A rule that vanished after a compaction.** It was said in the chat, or it lives in a rule scoped to a path → [Handoff](handoff.md).

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `read` in Claude Code's docs: the pages linked above, plus [skills](https://code.claude.com/docs/en/skills.md), [MCP tool search](https://code.claude.com/docs/en/mcp.md#scale-with-mcp-tool-search), [reduce token usage](https://code.claude.com/docs/en/costs.md#reduce-token-usage), [prompt caching](https://code.claude.com/docs/en/prompt-caching.md), [debug your configuration](https://code.claude.com/docs/en/debug-your-config.md), [plugin cost](https://code.claude.com/docs/en/plugins/measure.md), [hooks](https://code.claude.com/docs/en/hooks.md). `read` in Codex's docs: the pages linked above, plus [hooks](https://learn.chatgpt.com/docs/hooks), [the CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [the configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [models](https://learn.chatgpt.com/docs/models). `run`: `vectoralis budget`, in a fresh light project, a fresh heavy project and this repository.
