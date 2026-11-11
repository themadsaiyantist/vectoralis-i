# Docs and writing

Docs and writing work is an agent producing files that people read: technical docs in Markdown, slide decks, PDFs and spreadsheets, new or edited in place. Read this page when someone needs the file itself, a `.docx`, a `.pptx`, an `.xlsx` or a PDF, and before an agent writes the docs that ship with your code.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [Anthropic document skills](https://github.com/anthropics/skills) | Four skills that create, read and edit `.docx`, `.pdf`, `.pptx` and `.xlsx` files with scripts, and check the result before they hand it over. Apache-2.0. `tried` 2026-11-11: the Codex line, skills CLI 1.8.1, copied `docx`, `pdf`, `pptx` and `xlsx` into `.agents/skills/`, each with an Apache-2.0 licence, and the repository's marketplace lists `document-skills` with those four. | Claude Code. Codex through the skills CLI, which the maker's README does not cover | four descriptions in every session, each body loads on use | `/plugin marketplace add anthropics/skills` → `/plugin install document-skills@anthropic-agent-skills`. Codex: `npx skills add anthropics/skills --skill docx --skill pdf --skill pptx --skill xlsx -a codex` |
| Guard | `local-path` | Warns when a Markdown file gets a path from your own machine, such as a home folder. `tried` 2026-11-11: the engine's proof passes all 4 payloads. | both | none, a hook costs no context | below |
| MCP server | [MarkItDown MCP](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp) | Microsoft's converter as a local server: turns a PDF or a Word, PowerPoint or Excel file into Markdown the agent can read. MIT. `tried` 2026-11-11: `pip install markitdown-mcp` gave version 0.0.1a8, and `tools/list` over stdio gave 1 tool, `convert_to_markdown`. | Claude Code and Codex, as a plain stdio server. The maker's README shows Claude Desktop | 1 tool | `pip install markitdown-mcp` → `claude mcp add markitdown -- markitdown-mcp`. Codex: `codex mcp add markitdown -- markitdown-mcp` |

An agent reads absolute paths all session and pastes them into the docs it writes, where they name a user and work on one machine.

```json
{
  "id": "local-path",
  "why": "a path from the session names a user and works on one machine, and the agent pastes it into docs",
  "on": "write",
  "path": "**/*.md",
  "pattern": "(?<![\\w.])(/home/|/Users/)[\\w.-]+/|[A-Za-z]:\\\\Users\\\\",
  "mode": "warn",
  "message": "A path from your own machine is about to ship in a doc. Write it from the repository root, or from ~.",
  "payloads": [
    { "name": "catches a home folder", "path": "docs/setup.md", "text": "Open /home/goku/app/config/settings.json and set the port.", "expect": "hit" },
    { "name": "catches a Windows profile", "path": "README.md", "text": "Copy the file to C:\\Users\\vegeta\\app\\config.", "expect": "hit" },
    { "name": "passes a repository path", "path": "docs/setup.md", "text": "Open `config/settings.json` and set the port.", "expect": "pass" },
    { "name": "passes a web address", "path": "docs/setup.md", "text": "See https://example.com/home/guide/ for the full list.", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/local-path.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) | A way to write a spec or a decision doc in three stages: gather the context, refine it section by section, then test the draft on a fresh agent that has none of the context. It ships in `example-skills`, in the same marketplace. `tried` 2026-11-11: cloned: one `SKILL.md`, listed under `example-skills`. | free |
| Skill | [Slidev skill](https://sli.dev/guide/work-with-ai) | Slides as Markdown with live code, exported to PDF or PPTX. From the maker: `npx skills add slidevjs/slidev`. `tried` 2026-11-11: that line copied one skill, `slidev`, into `.claude/skills/`. | free, MIT |
| Skill | [Google Workspace CLI](https://github.com/googleworkspace/cli) | Google Docs, Sheets and Slides through the `gws` command, with one skill per API. Its README says it is not an officially supported Google product. `read`: needs a Google account. Cloned only: 95 skill files, Apache-2.0. | free, Apache-2.0 |
| Guard | [`tests`](../guide/guards.md) | Built in, light profile. Set `test` to a link check such as `lychee --offline .` and the agent cannot say done while a link between your files is dead. `tried` 2026-11-11: `vectoralis guards` printed `tests block block 6 of 6 payloads behave`. | free, ours |
| Guard | [`format`](../guide/guards.md) | Built in, light profile. Set `format` to `npx prettier --write --ignore-unknown` and every Markdown table and list comes out in one style after each edit. `tried` 2026-11-11: `vectoralis guards` printed `format off warn 6 of 6 payloads behave`. | free, ours |
| MCP server | [Docling MCP](https://github.com/docling-project/docling-mcp) | For the hard PDFs: Docling reads page layout, reading order and table structure, and runs OCR on scans. `tried` 2026-11-11: `uvx --from docling-mcp docling-mcp-server --transport stdio` started, and `tools/list` gave 21 tools. | free, MIT |
| MCP server | [Notion MCP](https://developers.notion.com/guides/mcp/get-started-with-mcp) | Reads and writes the pages of a Notion workspace, for a team whose docs live there. Its guide sets it up for Claude Code and for Codex. `read`: needs a Notion account. | works on every Notion plan, and the guide names no price |
| MCP server | [Excel MCP server](https://github.com/haris-musa/excel-mcp-server) | Charts, PivotTables and slicers with no Excel installed. Its README lists 46 tools, and `--tools` loads only the areas you name. `tried` 2026-11-11: `uvx excel-mcp-server stdio`, version 2.3.0, gave 46 tools to `tools/list`, and `stdio --help` lists `--tools AREAS`. | free, MIT |

## When each earns its place

- **The skill** → someone needs the file itself and not the Markdown behind it. The skills call `pandoc`, LibreOffice and a few Python and Node packages, so have those installed. The Codex line is from the [skills CLI](https://github.com/vercel-labs/skills), which puts the four folders in `.agents/skills/`, where Codex looks for skills [by its docs](https://learn.chatgpt.com/docs/build-skills). The `xlsx` skill recalculates with LibreOffice and rewrites the file in place, so hand it a copy.
- **The guard** → the first doc an agent writes after a session in your terminal. It costs nothing until it speaks. A doc that must show a home folder can write `~`.
- **The MCP server** → a session with no shell. One tool is as small as a server gets, and the CLI is smaller still: `markitdown report.pdf -o report.md` reads the same file and costs no context until it runs. `tried` 2026-11-11: markitdown 0.1.9 turned a Typst PDF into text and a pandoc `.docx` into Markdown with its table intact. The `pptx` and `xlsx` skills already read files with that command. The two register lines are the plain stdio form from the MCP docs of [Claude Code](https://code.claude.com/docs/en/mcp) and of [Codex](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), because the maker's README shows Claude Desktop only. The server reads any file or address its user can reach, by its README, so keep it local.
- **The CLI first** → a conversion needs no skill and no server.
  - Markdown to Word → `pandoc -o notes.docx notes.md`, by the [Pandoc manual](https://pandoc.org/MANUAL.html). `tried` 2026-11-11: pandoc 2.17 wrote a 10 KB `notes.docx`.
  - A typeset PDF → `typst compile report.typ`, with [Typst](https://github.com/typst/typst), Apache-2.0. `tried` 2026-11-11: typst 0.15.1 wrote `report.pdf`.
  - Slides from Markdown → `npx @marp-team/marp-cli@latest deck.md --pptx`, with [Marp CLI](https://github.com/marp-team/marp-cli), MIT. `tried` 2026-11-11: marp-cli 4.5.1 printed `deck.md => deck.pptx`. It renders through Chrome, Edge or Firefox, so a machine without one needs it first.

## Left out, and why

- [MkDocs](https://github.com/mkdocs/mkdocs) → its last release, 1.6.1, is from August 2024. The team behind its Material theme now builds [Zensical](https://github.com/zensical/zensical).
- [Office-Word-MCP-Server](https://github.com/GongRzhe/Office-Word-MCP-Server) and its [PowerPoint sibling](https://github.com/GongRzhe/Office-PowerPoint-MCP-Server) → both archived on GitHub.
- [python-pptx](https://github.com/scanny/python-pptx) → no commit since August 2024. The `pptx` skill builds decks another way.

## A sample to study

[The `AGENTS.md` of Cloudflare's docs](https://github.com/cloudflare/cloudflare-docs/blob/production/AGENTS.md) → how a public docs repository of more than 5,400 pages briefs an agent: the folder map, the front matter each page needs, the commands that check a change, and its twelve common mistakes. The style rules live in a reference file the agent opens when it writes. `referenced`. Opened 2026-11-11: 298 lines, twelve mistakes, last changed 2026-10-19.

## How to do it better

- **It asks the agent to run the checks, and CI runs them on the pull request** → a request can be skipped, and CI answers late. Make the fast check the `test` command, `pnpm run check` in that repository, and the `tests` guard blocks "done" while it fails.
- **The file is 298 lines, read in every session** → keep the always-loaded file to what every task needs. Move the rest into skills that load on use, as its own `contributing` skill already does for the steps of a change.
- **Its style rules are prose, with a Semgrep pass in CI that only warns** → turn each mistake that comes back into a guard recipe that speaks at the edit, starting at `warn`.
- **It covers a website and nothing else** → for a deck, a PDF or a sheet, keep the source as text, Markdown, Typst or CSV, so a diff shows what changed, and build the file from it.

## Where people talk

- [r/technicalwriting](https://www.reddit.com/r/technicalwriting/) → docs as a craft: structure, style guides, docs kept beside the code.
- [r/excel](https://www.reddit.com/r/excel/) → formulas and models, the place to check what a generated sheet should do.
- [r/LaTeX](https://www.reddit.com/r/LaTeX/) → typesetting, for the PDF that has to look exact.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Tried 2026-11-11 in a container, each with its evidence above: the document skills, the guard, MarkItDown MCP and its CLI, doc-coauthoring, the Slidev skill, `tests`, `format`, Docling MCP, the Excel MCP server, pandoc, Typst and Marp. Still `read`: the Google Workspace CLI and Notion MCP, which need an account.
