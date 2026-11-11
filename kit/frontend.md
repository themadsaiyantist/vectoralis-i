# Frontend and UI

Frontend work is building what people see and touch: components, a design system, a design file turned into code, and a look at the result in a real browser. Read this page when the agent's screens all look alike, when its controls answer a mouse and not a keyboard, or when it says a page works and has never opened it.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [frontend-design](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design) | Anthropic's skill for new UI. The agent plans a palette, type and a layout for this brief, checks the plan against the looks every generated page shares, then builds to a floor: responsive, visible keyboard focus, reduced motion respected. Apache-2.0. | Claude Code. Codex through the skills CLI, which the maker's README does not cover | one description, a 9.4 KB body on use | `/plugin install frontend-design@claude-plugins-official`. Codex: `npx skills add anthropics/skills --skill frontend-design -a codex` |
| Guard | `no-click-div` | Warns when a `div` or a `span` gets a click handler, where a button belongs. | both | none, a hook costs no context | below |
| MCP server | [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Chrome's own team gives the agent a real browser: open the page, read the console and the network, take a screenshot, record a performance trace, run a Lighthouse audit. Apache-2.0. | Claude Code, Codex | 63 tools in its reference, some groups off by default, 3 with `--slim` | `claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest`. Codex: `codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest` |

A `div` takes no focus and no Enter key, and the [Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines/blob/main/command.md) list one with a click handler among their anti-patterns.

```json
{
  "id": "no-click-div",
  "why": "a div with a click handler cannot be reached or pressed from the keyboard",
  "on": "write",
  "path": "src/**",
  "pattern": "<(div|span)\\b(?![^>]*\\brole=)[^>]*(\\bon[Cc]lick|@click[.\\w]*)=",
  "mode": "warn",
  "message": "A div or a span is getting a click handler. Use a button, or a link when it goes somewhere, so the keyboard and a screen reader can reach it.",
  "payloads": [
    { "name": "catches a clickable div", "path": "src/components/Card.tsx", "text": "<div className=\"card\" onClick={open}>", "expect": "hit" },
    { "name": "catches one in a Vue template", "path": "src/components/Card.vue", "text": "<span class=\"link\" @click=\"open\">", "expect": "hit" },
    { "name": "passes a button", "path": "src/components/Card.tsx", "text": "<button type=\"button\" onClick={open}>", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/no-click-div.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | `react-best-practices` for React and Next.js performance, `composition-patterns` for component APIs, and `web-design-guidelines`, which fetches more than 100 rules from GitHub at each review and checks UI code against them: accessibility, forms, focus, motion. | free, MIT by its README |
| Skill | [shadcn skill](https://ui.shadcn.com/docs/skills) | Reads `components.json` and the project through `shadcn info`, so the agent finds, adds and composes components the way the project already does. | free, MIT |
| Skill | [Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance) | Guides stewarded by the Chrome, Edge, Firefox and MDN teams that steer the agent to today's web platform, such as container queries, popover and view transitions, with fallbacks. | free, Apache-2.0 |
| Skill | [Impeccable](https://github.com/pbakaus/impeccable) | Commands for one design move on a page that already exists, a `critique` and an `audit`, and 62 fixed rules that flag the tells of a generated page with no model call. The pick of the [design](design.md) page. | free, Apache-2.0 |
| Guard | [`format`](../guide/guards.md) | Built in, light profile. Runs your formatter, Prettier or Biome, after every write, so markup stays the way the team keeps it. | free, ours |
| Guard | [`tests`](../guide/guards.md) | Built in, light profile. Blocks "done" while the test command fails. Put the type check and the component tests in that command. | free, ours |
| MCP server | [Figma MCP server](https://developers.figma.com/docs/figma-mcp-server/) | Figma's own: the layout, variables and components of a frame, for turning a design file into code. Its docs list 41 tools. | paid for real use: the free plan gets 20 tool calls a month, a Dev seat is $12 a month |
| MCP server | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Microsoft's server for the same job in Chrome, Firefox, WebKit and Edge. | free, Apache-2.0 |
| MCP server | [shadcn MCP server](https://ui.shadcn.com/docs/mcp) | Browses, searches and installs components from the registries named in `components.json`, private ones included. | free |
| MCP server | [Storybook MCP](https://storybook.js.org/docs/ai/mcp/overview) | Lets the agent read your components and their docs, write stories and run their tests. Its docs say the AI features are in preview and the API may change. | free, MIT |

## When each earns its place

- **The skill** → the first screen comes back looking like every other generated page. It pays most on new UI. Where a design system already decides the look, the skill's own text says the brief wins.
- **The guard** → the first review that finds a control no keyboard can reach. A `div` that carries a `role` passes, because someone has already thought about it. It reads what the agent writes, so a clickable `div` that is already in a file stays until someone touches it. For colors that drift from the tokens, the guard is `raw-colour` on the [design](design.md) page.
- **The MCP server** → the agent says the page works and has not opened it, or the bug shows only in the browser: a console error, a failed request, a slow first paint. `--slim` keeps 3 tools: navigate, evaluate, screenshot. Claude Code loads only the tool names until one is called, [by its docs](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search), and [Codex's MCP page](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) gives `enabled_tools` to trim a server. It sends usage statistics to Google unless you add `--no-usage-statistics`, and it shows the agent everything in the browser it drives, so keep private accounts out of that browser.
- **The CLI first** → the same package ships a `chrome-devtools` command and a skill that teaches it: `npm i chrome-devtools-mcp@latest -g`, then `chrome-devtools take_screenshot 1 --filePath shot.png`. One screenshot after a change needs no server in the session. Microsoft's [`playwright-cli`](https://github.com/microsoft/playwright-cli) does the same, and it is the pick of the [testing](testing.md) page.

## Left out, and why

- [Framelink MCP for Figma](https://github.com/GLips/Figma-Context-MCP) → a third party's server for Figma data, with no commit on its default branch since June 2026. Figma now runs its own, in the table above.
- [21st MCP](https://21st.dev/mcp) → search is free, a free account fetches two components a day, and more needs a paid plan. The shadcn server reads registries for free.

## A sample to study

[Frontend Aesthetics: A Prompting Guide](https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb) → a notebook that builds the same pages twice, with and without one design prompt, and shows the two screenshots side by side. It also shows how to steer one dimension alone, such as typography, or to lock a theme. `referenced`

## How to do it better

- **The prompt goes into the system prompt or `CLAUDE.md`, so every session pays for it** → use a skill, which loads when UI work starts. `frontend-design` is that skill, and its README points back to this notebook.
- **Each run invents its colors and its type again** → write the choice down once as tokens, CSS variables in one file, and let the `raw-colour` guard of the [design](design.md) page keep the components on them.
- **The notebook opens the page for a person to look at, and nothing reads it back** → have the agent open the page itself, read the console, and look at it at phone width before it says done.
- **Nothing checks who can use the page** → run an accessibility pass on every new screen: the Lighthouse audit in Chrome DevTools MCP, or the `a11y-debugging` skill its plugin ships.
- **It builds whole pages from nothing** → most real work is one component inside a system. Hand the agent what exists, the Figma frame, the registry, the file next door, and ask for one component at a time.

## Where people talk

- [r/webdev](https://www.reddit.com/r/webdev/) → the widest room for web work, tools included.
- [r/Frontend](https://www.reddit.com/r/Frontend/) → the craft: CSS, components, accessibility, performance.
- [r/reactjs](https://www.reddit.com/r/reactjs/) → React questions and library choices.
- [r/nextjs](https://www.reddit.com/r/nextjs/) → Next.js in production, where agent-written code meets the framework's rules.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
