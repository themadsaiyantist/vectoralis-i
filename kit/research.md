# Research

Research is finding out what is true today: what the current version of a library does, what a source says in its own words, which of three options the evidence favours. Both agents already search the web. Claude Code ships `/deep-research` for a cited report, and Codex searches a cached index by default and the live web with `--search`. Read this page when answers come back from memory, or come back with no source.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [research](https://github.com/mattpocock/skills/tree/main/skills/engineering/research) | Sends a background agent to the primary sources, such as official docs, source code and specs, and saves the findings as one Markdown file in the repository with the source of each claim. MIT. | Claude Code, Codex | one description, then under 1 KB | `claude plugin install mattpocock-skills@claude-plugins-official`. Codex: `codex plugin marketplace add mattpocock/skills` → `codex plugin add mattpocock-skills@mattpocock` |
| Guard | `claim-needs-source` | Warns when a bullet in the research notes carries no URL. | both | none, a hook costs no context | below |
| MCP server | [Context7](https://github.com/upstash/context7) | Looks up the docs and code examples of a library, for the version you name. The server is MIT, the index behind it is closed. | Claude Code, Codex | 2 tools | `claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY`. Codex: `codex mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY` |

The skill asks for a source on every claim and the recipe checks that it is there: point `path` at the folder your notes go to.

```json
{
  "id": "claim-needs-source",
  "why": "a claim with no source cannot be checked, and nobody sees it go stale",
  "on": "write",
  "path": "research/**/*.md",
  "pattern": "^\\s*[-*] (?!.*https?://).+",
  "mode": "warn",
  "message": "A line in the research notes has no source. Add the URL it came from, or cut the line.",
  "payloads": [
    { "name": "catches a bare claim", "path": "research/rate-limits.md", "text": "- The API allows 100 requests a minute", "expect": "hit" },
    { "name": "passes a sourced claim", "path": "research/rate-limits.md", "text": "- The API allows 100 requests a minute → https://example.com/docs/limits", "expect": "pass" },
    { "name": "leaves other files alone", "path": "docs/setup.md", "text": "- Run the installer", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/claim-needs-source.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [Tavily skills](https://github.com/tavily-ai/skills) | Search, page extraction, site crawl and a cited research run from one CLI, `tvly`. | free to start: search and extract run with no key under a fair-use cap. An account gives [1,000 credits a month](https://docs.tavily.com/documentation/api-credits), then $0.008 a credit |
| Skill | [hyperresearch](https://github.com/jordan-gibbs/hyperresearch) | A full pipeline for a large question: many sources, every citation checked against its source before the report ships, each source kept for the next run. | free, MIT |
| Guard | [gh-cli](https://github.com/trailofbits/skills/tree/main/plugins/gh-cli) | A Claude Code hook that turns a fetch of a GitHub URL into the signed-in `gh` command, so a private repository or the 60 requests an hour of an anonymous read stop breaking the research. | free, CC BY-SA 4.0 |
| MCP server | [Exa](https://github.com/exa-labs/exa-mcp-server) | Web search, and a page reader that returns clean Markdown. 2 tools by default. | free with rate limits and no account |
| MCP server | [arXiv MCP server](https://github.com/blazickjp/arxiv-mcp-server) | Finds papers, reads them one section at a time, and exports BibTeX from arXiv's own metadata. 19 tools. | free, Apache-2.0 |
| MCP server | [DeepWiki MCP](https://docs.devin.ai/work-with-devin/deepwiki-mcp) | Answers questions about any public GitHub repository. 3 tools, no sign-in. | free |
| MCP server | [Microsoft Learn MCP](https://github.com/MicrosoftDocs/mcp) | Microsoft's own docs and code samples. 3 tools, no key. | free |

## When each earns its place

- **The skill** → the second time an answer came from memory and was wrong. The reading happens in a background agent with a fresh context, so the pages it opens never enter yours. It comes in the plugin the [coding](coding.md) page picks.
- **The guard** → the first note you could not trace back to a page.
- **The MCP server** → the agent writes calls from an older release of a library. It costs 2 tools and a free account: [1,000 calls a month](https://context7.com/docs/plans-pricing), then $10 a seat a month. Its README says the docs it returns are contributed by the community, with no promise that they are accurate or safe, so read them as data.
- **The CLI first** → the same maker ships the lookup as a CLI with a `find-docs` skill and no server: `npx ctx7 setup --cli --claude`, or `--cli --codex`, [by its CLI docs](https://context7.com/docs/clients/cli). A PDF needs no server either: [markitdown](https://github.com/microsoft/markitdown) turns it into Markdown with `markitdown paper.pdf > paper.md`.

## Left out, and why

- [GitMCP](https://github.com/idosal/git-mcp) → a remote docs server for any GitHub project. Its last commit is from 2026-05-08, past the three-month line.
- [Open Deep Research](https://github.com/langchain-ai/open_deep_research) → LangChain's open research agent. The repository is archived.
- [deep-research](https://github.com/dzhng/deep-research) → a research loop over search engines and scraping. Its last commit is from 2026-04-11.

## A sample to study

[Research lead, subagent and citations prompts](https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents/prompts) → three prompts from Anthropic's cookbook for a research system. A lead sorts the question and splits it across subagents, the subagents search inside a budget of tool calls and judge each source, and a last agent adds citations to the finished report without changing a word of it. `referenced`

## How to do it better

- **Citations are added at the end, by a separate pass** → cite at the moment of reading. Each note carries its URL when it is written, so nothing has to be matched back later. That is the skill and the guard above.
- **The prompts keep what was read in the conversation, and it is gone after it** → save the findings to a file in the repository, where the next session and a reviewer can open them.
- **It says not every statement needs a citation** → in technical work, give one to every claim a decision rests on: a version, a limit, a price, a date.
- **The agent that adds a citation is the only one that checks it** → open each cited URL in a second pass, with a reviewer that did not write the report.
- **The prompts name tools your agent may not have** → they date from 2025. Keep the roles and the budget, and swap in the tools you run.

## Where people talk

- [r/mcp](https://www.reddit.com/r/mcp/) → MCP servers day to day, the search and docs ones included.
- [r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/) → research workflows and skills in Claude Code.
- [r/codex](https://www.reddit.com/r/codex/) → the same for Codex, web search modes included.
- [r/Rag](https://www.reddit.com/r/Rag/) → retrieval at large: finding the right passage and keeping its source.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
