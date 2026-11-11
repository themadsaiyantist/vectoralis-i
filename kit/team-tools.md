# Team tools

Team tools are the shared places where work is tracked and talked about: GitHub, an issue tracker, chat and notes. Read this page when you want an agent session to read a ticket, find the discussion behind a decision or post an update, and before it does any of that under your name.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [Slack skills plugin](https://github.com/slackapi/slack-skills-plugin) | Nine skills from Slack. Two serve a working session: write a message people will read, and find a past discussion. Seven are for building Slack apps. MIT. | Claude Code, Codex | nine descriptions in every session, each body loads on use | `/plugin marketplace add slackapi/slack-skills-plugin` → `/plugin install slack@slack`. Codex: `codex plugin marketplace add slackapi/slack-skills-plugin` → `codex plugin add slack@slack` |
| Guard | `your-voice` | Warns before `gh` posts a comment, a review or a new issue, or closes one. | both | none, a hook costs no context | below |
| MCP server | [Linear MCP server](https://linear.app/docs/mcp) | Finds, creates and updates issues, projects and comments in Linear. | Claude Code, Codex | the docs give no count | `claude mcp add --transport http linear-server https://mcp.linear.app/mcp` → `/mcp` to sign in. Codex: `codex mcp add linear --url https://mcp.linear.app/mcp` |

The agent reads the team's tools freely, and what it would post under your name it shows you first.

```json
{
  "id": "your-voice",
  "why": "a comment, a review or a new issue reaches other people as the person's own words",
  "on": "shell",
  "pattern": "\\bgh\\s+(issue\\s+(create|comment|close)|pr\\s+(comment|review|close))\\b",
  "mode": "warn",
  "message": "This posts under your name where other people read it. Show the text first and wait for a yes.",
  "payloads": [
    { "name": "catches a comment on an issue", "text": "gh issue comment 42 --body \"Fixed in #57\"", "expect": "hit" },
    { "name": "catches a review", "text": "gh pr review 57 --approve", "expect": "hit" },
    { "name": "passes the agent's own pull request", "text": "gh pr create --fill", "expect": "pass" },
    { "name": "passes a read", "text": "gh issue view 42 --comments", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/your-voice.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [Notion plugin for Claude Code](https://github.com/makenotion/claude-code-notion-plugin) | Twelve skills from Notion, with its MCP server and ten commands: turn a spec page into a plan and tasks, turn a conversation into a doc, prepare a meeting. | free, the skills are MIT in [Notion's cookbook](https://github.com/makenotion/notion-cookbook) |
| Skill | [Notion plugin for Codex](https://github.com/openai/plugins/tree/main/plugins/notion) | Four of those skills in OpenAI's plugin catalog: knowledge capture, meeting prep, research notes, spec to implementation. | free |
| Skill | [Atlassian skills](https://github.com/atlassian/atlassian-mcp-server/tree/main/skills) | Seven skills for Jira and Confluence: triage a bug against the issues already filed, turn a spec into a backlog, write a status report. | free, Apache-2.0 |
| Guard | [`push`](../guide/guards.md) | Built in, heavy profile. Blocks `gh pr merge` and a push to the default branch while `merge` is `yours`. | free, ours |
| Guard | [`secrets`](../guide/guards.md) | Built in, light profile. Blocks a GitHub or Slack token written into a file, the usual accident when a server is set up by hand. | free, ours |
| MCP server | [Atlassian Rovo MCP server](https://github.com/atlassian/atlassian-mcp-server) | Jira and Confluence in one hosted server. About two dozen tools are visible and the rest are found on demand, by its [tools page](https://support.atlassian.com/atlassian-ai-gateway/docs/supported-tools/). | the docs name no price, and some search tools spend Rovo credits |
| MCP server | [Notion MCP](https://developers.notion.com/guides/mcp/get-started-with-mcp) | Searches, reads and writes the pages and databases of your workspace, signed in with OAuth. | works on every plan, with higher limits on Business and Enterprise |
| MCP server | [Slack MCP server](https://docs.slack.dev/ai/slack-mcp-server/) | Searches, reads, sends and schedules messages, and works with canvases. A workspace admin approves it first. | the docs name no plan or price |
| MCP server | [GitHub MCP server](https://github.com/github/github-mcp-server) | For a session with no shell, where `gh` cannot run. Its README lists 93 tools, 45 of them in the default toolsets. `--read-only` and `--toolsets` cut it down. | free, MIT |

## When each earns its place

- **The skill** → you rewrite the agent's Slack messages before you send them, or you search Slack by hand for the thread behind every ticket. In Claude Code the plugin also connects Slack's own MCP server and adds five commands, and a workspace admin has to approve that first. In Codex it brings the skills alone.
- **The guard** → the first time `gh` runs with your token on a repository other people watch. It reads commands, so it does not see a post made through an MCP tool or through `gh api`. A token that can only read is the stronger wall.
- **The MCP server** → you move tickets several times a day and the tracker has no CLI you trust. MCP access is part of Linear's free plan, by its [pricing page](https://linear.app/pricing). Start on the read-only endpoint, `https://mcp.linear.app/mcp/readonly`. Claude Code loads only the tool names until one is called, [by its docs](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search). The larger cost is trust: every server here carries other people's text into your session, so install the fewest that do the job.
- **The CLI first** → GitHub needs no server. [`gh`](https://cli.github.com/manual/) reads issues, pull requests and pipeline runs at no context cost until it runs, and the guard above watches the same commands.

## Left out, and why

- [korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server) → no commit since July 2026, past the three months this kit asks for.
- [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian) → a third party's server with 98 tools, where Atlassian now runs its own for Cloud. It remains the way in for Jira and Confluence on Server or Data Center.
- [The archived reference servers](https://github.com/modelcontextprotocol/servers-archived) for GitHub and Slack → archived, with no security fixes. Each maker now runs its own.

## A sample to study

[Claude Issue Triage](https://github.com/anthropics/claude-code-action/blob/main/examples/issue-triage.yml) → a workflow that lets an agent read every new issue, text from strangers included, and gives it one way to write: [a script](https://github.com/anthropics/claude-code-action/blob/main/scripts/edit-issue-labels.sh) that only adds or removes labels the repository already has, on the issue the event named. [The command](https://github.com/anthropics/claude-code-action/blob/main/.claude/commands/label-issue.md) behind it allows that script and a `gh` wrapper that can only read, and it forbids comments. `referenced`

## How to do it better

- **The example leaves the network open** → [the copy the repository runs on itself](https://github.com/anthropics/claude-code-action/blob/main/.github/workflows/issue-triage.yml) uses a runner that filters outbound traffic through an allowlist. In a local session the agent's sandbox plays that part, see [safety](../guide/safety.md).
- **It names no tool the agent may never use** → the live copy passes `--disallowedTools "WebFetch,WebSearch,Write,Edit,MultiEdit,NotebookEdit"`, so the web and file-writing tools are gone, whatever an issue asks for.
- **Nothing counts the writes** → the live copy caps the label script at two calls a session with `CLAUDE_CODE_SCRIPT_CAPS`.
- **It stores an API key as a secret** → the live copy trades the workflow's own identity token for a short-lived one, so no key is kept.
- **The same shape works at your desk** → reads through `gh`, one small script for the one write you allow, and a prompt before a tracker's tools run: an `ask` rule on `mcp__linear-server__*` in [Claude Code](https://code.claude.com/docs/en/permissions), and `default_tools_approval_mode = "writes"` in [Codex](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), which asks only for tools not marked read-only.

## Where people talk

- [r/github](https://www.reddit.com/r/github/) → GitHub itself: Actions, issues, pull requests, the CLI.
- [r/mcp](https://www.reddit.com/r/mcp/) → MCP servers day to day: which ones hold up, how people set them up, what goes wrong.
- [r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/) → Claude Code in daily use, plugins and MCP servers included.
- [r/codex](https://www.reddit.com/r/codex/) → the same for Codex: the CLI, plugins and MCP setup.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
