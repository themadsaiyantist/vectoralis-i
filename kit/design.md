# Design

Design is deciding how a product looks and reads: its layout, its type, its colour, and the system that keeps them the same on every screen. Read this page when an agent builds or changes an interface for you, when a brand has to hold across many screens, or when the work moves between code and a design tool.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [Impeccable](https://github.com/pbakaus/impeccable) | Gives the agent 24 design commands, from `layout` and `typeset` to `critique` and `audit`, and a detector with 62 fixed rules for generic output. It keeps the brand in `PRODUCT.md` and the visual system in `DESIGN.md`. Apache-2.0. | Claude Code, Codex | one skill description in every session, and four subagent descriptions in Claude Code. The body and one reference file per command load on use | `npx impeccable install`, for both agents |
| Guard | `raw-colour` | Warns when a component gets a hex value or a colour function where a token belongs. | both | none, a hook costs no context | below |
| MCP server | [Penpot MCP](https://help.penpot.app/mcp/) | Penpot's own server: the agent reads and changes the design file you have open, its tokens, components, layouts and exports. Penpot is open source, MPL-2.0, and can be self-hosted. | Claude Code, Codex | 5 tools | `npx -y @penpot/mcp@stable` and leave it running → `npx -y add-mcp -g -n penpot http://localhost:4401/mcp`, for both agents |

A generated component carries its own hex values unless something stops it, and each one is a colour the token file no longer controls.

```json
{
  "id": "raw-colour",
  "why": "a visual system holds only while every colour comes from the token file",
  "on": "write",
  "path": "src/components/**",
  "pattern": "(:\\s*|['\"]|-\\[)#[0-9a-fA-F]{3,8}\\b|\\b(?:rgba?|hsla?|oklch)\\(\\s*[\\d.]",
  "mode": "warn",
  "message": "A raw colour is about to ship in a component. Use a token, or add the colour to the token file first.",
  "payloads": [
    { "name": "catches a hex colour", "path": "src/components/Button.css", "text": ".button { background: #f59e0b; }", "expect": "hit" },
    { "name": "catches a colour function", "path": "src/components/Card.tsx", "text": "<div style={{ boxShadow: '0 8px 24px rgba(0, 0, 0, 0.08)' }} />", "expect": "hit" },
    { "name": "passes a token", "path": "src/components/Button.css", "text": ".button { background: var(--color-primary); }", "expect": "pass" },
    { "name": "passes the token file", "path": "src/styles/tokens.css", "text": ":root { --color-primary: #f59e0b; }", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/raw-colour.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Anthropic's own skill in one file: a palette, a type plan and a layout made for the brief before any code. No hook and no binary. In Claude Code: `/plugin install frontend-design@claude-plugins-official`. | free, Apache-2.0 |
| Skill | [web-design-guidelines](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) | Vercel's review skill: it fetches the current Web Interface Guidelines and checks your UI code against more than 100 rules for accessibility, performance and UX. | free, MIT |
| Skill | [Product Design](https://github.com/openai/plugins/tree/main/plugins/product-design) | OpenAI's plugin for Codex: three visual directions first, then a prototype from a brief, a URL or a screenshot, and UX audits. Install it from `/plugins`. | free with Codex, proprietary licence |
| Guard | [`locks`](../guide/locks.md) | Built in, heavy profile. Lock `DESIGN.md` and the token file, and the system changes only after you type `unlock`. | free, ours |
| MCP server | [Figma MCP server](https://developers.figma.com/docs/figma-mcp-server/) | The same round trip for a team whose files live in Figma, with Figma's own skills in its plugin. Its docs list 41 tools. | `paid` in practice: the free Starter plan gets [20 tool calls a month](https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/), and a Dev seat with 200 a day is [$12 a month](https://www.figma.com/pricing/) |
| MCP server | [Storybook MCP](https://storybook.js.org/docs/ai/mcp/overview) | For a system that lives in code: the agent reads your documented components before it writes UI, then previews and tests its own stories. In preview. | free, MIT |

## When each earns its place

- **The skill** → the second time a page comes back looking like every other generated page, or when you want a review in sharper words than "make it pop". Start with `/impeccable init`, or `$impeccable init` in Codex. It costs more than context: its [hook](https://impeccable.style/docs/hooks) runs the detector after UI edits and hands back the findings, the engine is a binary that may download on first run, and a new design fetches visual directions from the maker's site even with telemetry off. Its live mode can start `codex` or `claude` with approvals off, so read that part of its README first.
- **The guard** → the day the colours live in one file. Before that it has nothing to protect. It costs nothing until it speaks. Set `path` to your component folder. Impeccable's hook checks drift from `DESIGN.md` as well, and this recipe is the rule you can read in ten lines and keep without the skill.
- **The MCP server** → a design file is the source of truth and code must follow it, or the code is and the file must catch up. It costs 5 tools, and a Penpot tab that stays open with the plugin loaded from `http://localhost:4400/manifest.json` and connected. One of the tools runs code inside your file, so ask for the plan before a change. Penpot also hosts the server: switch it on under Your account → Integrations → MCP Server.
- **The CLI first** → tokens need no server and no skill. [Export them from Penpot](https://help.penpot.app/user-guide/design-systems/design-tokens/) as JSON, build them with the [Style Dictionary CLI](https://styledictionary.com/getting-started/using_the_cli/), and check a `DESIGN.md` with `npx @google/design.md lint DESIGN.md`. Each costs no context until it runs.

## Left out, and why

- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) → 84 `DESIGN.md` files extracted from other companies' sites. Its MIT licence covers the files, and its README claims no ownership of the identities in them, so the right to ship someone else's look is unclear.
- [Framelink MCP for Figma](https://github.com/GLips/Figma-Context-MCP) → a third party, where Figma now ships its own server, and no commit on its default branch since 2026-06-24.
- [Talk to Figma MCP](https://github.com/grab/cursor-talk-to-figma-mcp) → no commit since 2026-07-26, outside the three-month rule.

## A sample to study

[Paws & Paths](https://github.com/google-labs-code/design.md/tree/main/examples/paws-and-paths) → one brand written as a `DESIGN.md` in [Google Labs' open format](https://github.com/google-labs-code/design.md): colours, type, radius, spacing and component tokens in the front matter, the reasons in prose below. Beside it sit the Tailwind config and the DTCG token file derived from it. Marked `referenced`.

## How to do it better

- **Its prose and its tokens disagree** → the prose says a button radius is 12px while the `rounded.lg` token is 1rem, and it calls the spacing a strict 8px scale beside a 12px step. Give every number one home: the prose names the token and never repeats the value.
- **Its shadows are a range and its page width has no number** → the prose gives a blur of "20px-40px" at "4-8%" opacity, and a "maximum width" with no value. Write one exact value for each, and the agent reads a number instead of choosing one.
- **Its components stop at default and hover** → add focus, disabled and error, and a dark scheme if the product has one.
- **Its README never says how to check the file** → `npx @google/design.md lint DESIGN.md` reports token references that resolve to nothing and component text below WCAG AA contrast on its background. Run it in CI.
- **Nothing holds the code to it** → the `raw-colour` recipe above speaks when a component leaves the system, and `locks` keeps the file itself from drifting.

## Where people talk

- [r/UI_Design](https://www.reddit.com/r/UI_Design/) → critique of real interfaces, screen by screen.
- [r/web_design](https://www.reddit.com/r/web_design/) → layout, type and CSS on the web.
- [r/FigmaDesign](https://www.reddit.com/r/FigmaDesign/) → variables, components, Dev Mode and Figma's MCP server.
- [r/UXDesign](https://www.reddit.com/r/UXDesign/) → flows, research and how design teams work.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
