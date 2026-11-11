# Testing and browsers

Testing here is what a person would check by hand in a browser: click through a flow end to end, look at the page, compare it with yesterday's. Claude Code can drive your own Chrome with `claude --chrome`, though not under WSL, and Codex's built-in browser is not in its CLI. Read this page when the agent says "it works" about a page it never opened, or when a green suite stops meaning what it says.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [Playwright CLI](https://github.com/microsoft/playwright-cli) | Microsoft's browser CLI for agents: open a page, click, type, take a screenshot, record a trace, one short command at a time. Its skill also covers running and debugging a Playwright suite and writing tests from a plan. Apache-2.0. `tried` 2026-11-11: version 0.1.24 in Docker: `install --skills` wrote `.claude/skills/playwright-cli`, `--skills=agents -g` wrote `~/.agents/skills/playwright-cli`, and `open` then `click` on a tiny page turned its heading to `Saved`. | Claude Code, Codex | one description, a 16 KB body on use | `npm install -g @playwright/cli@latest` → `playwright-cli install --skills`. Codex: `playwright-cli install --skills=agents -g`, which writes to `~/.agents/skills` |
| Guard | `no-skipped-test` | Warns when a spec file gains `.only`, `.skip` or `.fixme`. `tried` 2026-11-11: the engine's proof, 3 of 3 payloads behave. | both | none, a hook costs no context | below |
| MCP server | [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | The Chrome team's server on a live Chrome: console messages with source-mapped stack traces, network requests, performance traces and Lighthouse audits. Apache-2.0. `tried` 2026-11-11: version 1.13.0 over stdio, `tools/list`: 33 tools, and 3 with `--slim`. | Claude Code, Codex | 33 tools on by default, 3 with `--slim` | `claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest`. Codex: `codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest` |

The built-in `tests` guard already refuses "done" while the suite fails, so the recipe closes the gap it leaves: a test that is skipped or run alone cannot fail.

```json
{
  "id": "no-skipped-test",
  "why": "a test that is skipped or run alone cannot fail, so a green suite proves less than it says",
  "on": "write",
  "path": "**/*.spec.ts",
  "pattern": "\\b(test|it|describe)(\\.\\w+)*\\.(only|skip|fixme)\\(",
  "mode": "warn",
  "message": "A test is being skipped or run alone. Fix the test, or tell the person which one and why.",
  "payloads": [
    { "name": "catches a focused test", "path": "tests/login.spec.ts", "text": "test.only('signs in', async ({ page }) => {", "expect": "hit" },
    { "name": "catches a skipped group", "path": "e2e/cart.spec.ts", "text": "test.describe.skip('cart', () => {", "expect": "hit" },
    { "name": "passes a plain test", "path": "tests/login.spec.ts", "text": "test('signs in', async ({ page }) => {", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/no-skipped-test.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [agent-browser](https://github.com/vercel-labs/agent-browser) | A Rust CLI that gives the agent a browser one command at a time, with the page returned as compact text and a ref for each element. `tried` 2026-11-11: version 0.42.0 in Docker: `open` then `snapshot -i` on a tiny page printed `button "Save" [ref=e2]`. Its own Chrome download timed out here, and it took Playwright's Chromium instead. | free, Apache-2.0 |
| Skill | [Playwright Test Agents](https://playwright.dev/docs/test-agents) | Three agent definitions from Playwright: a planner that explores the app and writes a test plan, a generator that turns the plan into tests, a healer that repairs failing ones. `npx playwright init-agents --loop=claude`, or `--loop=codex`. `tried` 2026-11-11: Playwright 1.65.0: each loop wrote its three agents, to `.claude/agents` and `.codex/agents`, with a `seed.spec.ts`. | free, Apache-2.0 |
| Skill | [mutation-testing](https://github.com/trailofbits/skills/tree/main/plugins/mutation-testing) | Sets up a mutation run and reads the survivors: the deliberate changes to the code that no test noticed. `tried` 2026-11-11: `claude plugin validate` passed: 1 skill. No mutation run was made. | free, CC BY-SA 4.0 |
| Guard | [`tests`](../guide/guards.md) | Built in, light profile. Blocks "done" while the test command fails. Put the end-to-end command in `test`, and raise `test_timeout` above its 120 seconds for a slow suite, because a run that times out is not checked. `tried` 2026-11-11: `vectoralis guards`: 6 of 6 payloads behave. | free, ours |
| Guard | [protect-tests](https://github.com/karanb192/claude-code-hooks/tree/main/plugins/protect-tests) | A Claude Code hook that denies deleting a test, renaming it away or adding a skip marker to it. `tried` 2026-11-11: its script fed three calls in Docker: it denied `rm tests/a.spec.ts` and an edit to `test.skip(`, and passed `npm test`. | free, MIT |
| MCP server | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | The same engine as a server, for a long exploratory session that keeps one browser open. 25 tools before the opt-in groups. `tried` 2026-11-11: version 0.0.85 over stdio, `tools/list`: 25 tools. | free, Apache-2.0 |

## When each earns its place

- **The skill** → the first time the agent reports a page as working without having opened it. Microsoft's own README says the CLI suits coding agents better than its MCP server, because a command costs fewer tokens than tool schemas and page trees loaded into the context.
- **The guard** → the first green suite that turned out to run one test. Playwright's [`forbidOnly`](https://playwright.dev/docs/api/class-testconfig#test-config-forbid-only) fails a run that holds `.only`, and its docs set it for CI. The recipe speaks at the write and covers `.skip` too. Point its `path` at your own test files if they are not named `*.spec.ts`.
- **The MCP server** → a test fails and the cause is in the network tab, the console or a slow frame. 33 tools is a lot, so start it with `--slim` for 3. It sends usage statistics to Google unless you pass `--no-usage-statistics`.
- **The CLI first** → the same package ships a `chrome-devtools` CLI and a skill for it, at no tool cost. A visual check needs neither: [`toHaveScreenshot()`](https://playwright.dev/docs/test-snapshots) writes a reference picture on the first run and compares against it on every run after.

## Left out, and why

- [Browserbase MCP server](https://github.com/browserbase/mcp-server-browserbase) → a cloud browser behind a server. The repository is archived.
- [Lost Pixel](https://github.com/lost-pixel/lost-pixel) → open-source visual regression testing. The repository is archived.
- [Puppeteer MCP server](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/puppeteer) → the early reference server for driving a browser. It sits in the archive of servers that are no longer maintained.

## A sample to study

[webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) → a 4 KB skill from Anthropic that tests a local web app with Python Playwright scripts. Its helper starts your servers, runs the script once they are up and stops them after, and the skill tells the agent to call that helper as a black box and keep its source out of the context. `referenced`, opened 2026-11-11: last push 2026-11-06, not archived, `SKILL.md` at 3,913 bytes.

## How to do it better

- **Every check is a script written for the moment** → keep the flows that matter as spec files in the repository, so the `tests` guard runs them at the end of every turn.
- **It waits for `networkidle`** → Playwright's own docs mark that wait as [discouraged for testing](https://playwright.dev/docs/api/class-page#page-wait-for-load-state). Assert on what a user sees: `await expect(page.getByRole('button', { name: 'Save' })).toBeVisible()` waits by itself.
- **The screenshot is judged by the model** → give it a baseline. `toHaveScreenshot()` compares with a stored picture, and a changed baseline is a diff a person reads. Make the baselines on the machine that will compare them, because rendering differs between systems.
- **It lists CSS selectors and IDs beside roles** → Playwright's [best practices](https://playwright.dev/docs/best-practices) prefer what a user sees, such as a role or a label, because those survive a change in the markup.
- **A failure leaves no evidence** → record a trace on the first retry in CI, and attach it to the pull request.

## Where people talk

- [r/Playwright](https://www.reddit.com/r/Playwright/) → the Playwright community's own room: locators, flaky tests, CI.
- [r/QualityAssurance](https://www.reddit.com/r/QualityAssurance/) → QA practice and tools, from people who test for a living.
- [r/softwaretesting](https://www.reddit.com/r/softwaretesting/) → test strategy and automation questions.
- [r/webdev](https://www.reddit.com/r/webdev/) → front-end work at large, browser bugs and visual regressions included.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. `tried` 2026-11-11, in Docker or in a scratch folder: every entry of both tables, each with its evidence beside it. Still `read`: the `chrome-devtools` CLI and `toHaveScreenshot()`, which were not run. No skill was loaded in a live agent session: a skill counts as loaded when it lands in the folder the agent reads, or its manifest validates.
