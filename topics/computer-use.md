# Computer Use and Browser Agents

Models that work a screen the way a person does: they look at it, click, type and check the result. Read this page when a task has no API and no command line, when you want your coding agent to test what it built in a real browser, or before you let any agent near an account that is signed in.

**Contents:** What it is · Why now · Start here · Resources · Build this · The kit · Where people talk · The future

## What it is

- **Computer use is a loop** → the model gets a screenshot → it answers with an action, a click, a key press or a scroll → your code performs it and sends back a new screenshot. A browser agent runs the same loop in a browser, where it can also read the page structure instead of pixels.
- **Where it works today** → testing a web app the agent just built, filling forms and pulling data on sites with no API, and driving apps that only have a window, such as a simulator.
- **Where it fails** → long tasks, logins and CAPTCHAs, and pages that carry instructions written for the agent → so it runs in a sandbox, and it is the last tool to reach for after an API, an MCP server and a shell command.

## Why now

- **Computer use left beta** → Anthropic shipped the tool as stable on August 19 as `computer_toolset_20260801`, launched a separate browser use tool the same day, and Claude Fable 5.2 has supported it since November 9 → `read` [Claude release notes](https://platform.claude.com/docs/en/release-notes/overview)
- **OpenAI built it into its main models** → GPT-5.4 got a built-in `computer` tool in the Responses API on March 5, the Agents API got computer use in a hosted browser on September 29, and GPT-6.1 Terra shipped on October 26 with precise computer use named as a strength → `read` [OpenAI changelog](https://developers.openai.com/api/docs/changelog)
- **Coding agents got a browser** → Claude Code drives Chrome with `claude --chrome`, and Codex has a browser and computer use in its desktop app → `read` [Claude Code: Chrome](https://code.claude.com/docs/en/chrome) · [Codex: Browser](https://learn.chatgpt.com/docs/browser) · [Codex: Computer Use](https://learn.chatgpt.com/docs/computer-use)
- **Open models can do the clicking** → Microsoft released Fara1.5 on July 22 in three sizes, 4B, 9B and 27B, with the weights on Hugging Face → `read` [microsoft/fara](https://github.com/microsoft/fara)
- **The benchmark got hard again** → OSWorld 2.0 has 108 long workflows that took a top model 318 tool calls on average, and the best run on its page completes 20.6% of them → `read` [OSWorld 2.0](https://osworld-v2.xlang.ai/)

## Start here

- ⬜ Ask whether the screen is needed at all → try an API or an MCP server → then a shell command → then a browser tool → the screen comes last, because it is the broadest and the slowest → `read` [Claude Code: computer use](https://code.claude.com/docs/en/computer-use)
- ⬜ Give your coding agent a browser → Claude Code: add the Claude in Chrome extension → `claude --chrome` → it works in your own signed-in browser, needs a claude.ai login and does not run in WSL. Codex: open the Browser in the desktop app → it uses a separate profile that does not share your tabs or sessions → `read` [Claude Code: Chrome](https://code.claude.com/docs/en/chrome) · [Codex: Browser](https://learn.chatgpt.com/docs/browser)
- ⬜ Or drive the browser through commands → `npm install -g @playwright/cli@latest` → `playwright-cli install --skills` → the agent runs short commands and reads back only what it asks for, in any coding agent → `read` [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli)
- ⬜ Watch the raw loop once → run Anthropic's reference container with your API key: a desktop in Docker, the agent loop and a small web app to talk to it → `read` [computer-use-demo](https://github.com/anthropics/claude-quickstarts/tree/main/computer-use-demo)
- ⬜ Write the loop yourself → send the task and the computer tool → perform the action that comes back → return a new screenshot → stop when no action comes back → `read` [Anthropic: computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) · [OpenAI: computer use](https://developers.openai.com/api/docs/guides/tools-computer-use)
- ⬜ Sandbox it before it touches anything real → a dedicated container or VM with minimal privileges → a fresh browser profile with no saved logins → an allowlist of domains → a person confirms every purchase, message and accepted term → `read` [Anthropic: computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) · [Anthropic: browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)
- ⬜ Attack your own agent → hide an instruction in a page you control and send the agent there → Anthropic's own measurements say no browser agent is immune, so see what yours does → the wider defense is in [AI security](ai-security.md) → `read` [Anthropic research](https://www.anthropic.com/research/prompt-injection-defenses)
- ⬜ Count before you trust → run one task ten times → record how often it finishes, how many steps it takes and what it costs → compare with a plain Playwright script of the same task.

## Resources

| Resource | Free or paid | Clarity | Depth | Hands-on | Current | Excels at |
|---|---|---|---|---|---|---|
| [Anthropic: computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) | free | ★ 9 | ★ 9 | ★ 8 | ★ 10 | The loop, every action and the security section on one page, with a reference container. Better than the others as the page to read first. |
| [OpenAI: computer use guide](https://developers.openai.com/api/docs/guides/tools-computer-use) | free | ★ 8 | ★ 7 | ★ 9 | ★ 10 | Working loops with Playwright for a browser and PyAutoGUI for a desktop. Better than the others on code you can copy. |
| [Gemini: computer use](https://aistudio.google.com/docs/computer-use) | free | ★ 8 | ★ 6 | ★ 7 | ★ 10 | One tool for browser, mobile and desktop, with Gemini 3.8 Flash as the model its docs recommend. Better than the others when the target is a phone screen. |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | free | ★ 8 | ★ 5 | ★ 9 | ★ 10 | A browser driven through the accessibility tree instead of screenshots. Better than the others when no vision model should be involved. |
| [browser-use](https://github.com/browser-use/browser-use) | free | ★ 7 | ★ 6 | ★ 9 | ★ 10 | An open-source browser agent that runs on any model, local browser included. Better than the others for a whole agent in a few lines. |
| [Mitigating prompt injections in browser use](https://www.anthropic.com/research/prompt-injection-defenses) | free | ★ 9 | ★ 7 | ★ 2 | ★ 6 | Measured attack rates, and the plain statement that no browser agent is immune. Better than the others on how this goes wrong. |
| [OSWorld 2.0](https://osworld-v2.xlang.ai/) | free | ★ 7 | ★ 9 | ★ 5 | ★ 9 | The benchmark of long, real workflows. Better than the others for a measured picture of what agents cannot finish yet. |

## Build this

| Project | Difficulty | What it teaches | A repository to study |
|---|---|---|---|
| Your coding agent tests the web app it just built | ★ 3 | ★ 8 → browser control through commands, and checks an agent can rerun | `referenced` [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) |
| The reference loop in a container, every screenshot read | ★ 3 | ★ 7 → the cycle of screenshot, action, screenshot | `referenced` [anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts) |
| A browser agent that fills one real form from a spreadsheet | ★ 5 | ★ 8 → waiting for the page, retries and when to hand back to a person | `referenced` [browser-use/browser-use](https://github.com/browser-use/browser-use) |
| A throwaway desktop that a script starts and destroys | ★ 6 | ★ 9 → isolation, and what the agent can and cannot reach | `referenced` [e2b-dev/desktop](https://github.com/e2b-dev/desktop) |
| An open computer-use model on your own GPU | ★ 7 | ★ 8 → what a 4B to 27B model can click with no hosted API | `referenced` [microsoft/fara](https://github.com/microsoft/fara) |
| Your agent scored on a public benchmark | ★ 9 | ★ 9 → evaluation in real virtual machines, and why long tasks fail | `referenced` [xlang-ai/OSWorld](https://github.com/xlang-ai/OSWorld) |

## The kit

- [kit/testing.md](../kit/testing.md) → the picks for tests. Take them for browser checks the agent writes and reruns.
- [kit/frontend.md](../kit/frontend.md) → the picks for interface work. Take them so the agent looks at the page it built before it calls the work done.
- [kit/security.md](../kit/security.md) → the picks for security work. Take the guard first: an agent with a browser reads text you did not write.
- [kit/agents.md](../kit/agents.md) → the picks for building agents. Take them when you write the loop yourself.
- [kit/devops.md](../kit/devops.md) → the picks for containers and servers. Take them for the container or virtual machine the agent runs in.

## Where people talk

- [r/AI_Agents](https://www.reddit.com/r/AI_Agents/) → how much autonomy to give an agent, and where to make it stop and ask a person.
- [r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/) → Claude and Claude Code in daily use: what people build with them and what breaks.
- [r/codex](https://www.reddit.com/r/codex/) → Codex in daily use, including people wiring it to their own browser.
- [Browser Use Discord](https://link.browser-use.com/discord) → the official server of the open-source browser agent.
- [Playwright Discord](https://aka.ms/playwright/discord) → the official server for the browser automation under many of these tools.
- [Hacker News](https://news.ycombinator.com/) → launches and security write-ups, discussed the day they appear.

## The future

- **Long tasks are the open problem** → the best run on OSWorld 2.0 finishes about one workflow in five → that number is the one to watch.
- **Structure first, pixels last** → Anthropic's browser tool reads the page structure, Playwright uses the accessibility tree, and the proposed [WebMCP](https://learn.chatgpt.com/docs/webmcp) standard lets a site offer its actions to an agent directly → clicking on screenshots becomes the fallback.
- **Small open models take the routine clicks** → Fara1.5 starts at 4B → screens you already know get automated on your own hardware.
- **The sandbox stays your job** → vendors now check screenshots and actions for injected instructions, and Anthropic still says no browser agent is immune → isolation and a person confirming the costly actions stay in every design.

The stars are a judgment, made on 2026-11-11. Verified 2026-11-11: every link opened.
