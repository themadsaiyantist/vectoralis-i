# Coding

Coding is the everyday work in any language: writing a change, refactoring what is there, finding a bug and proving the fix with a test. Read this page when the agent's code runs and you still do not trust it: tests written after the code that only repeat it, a bug fixed on the first guess, a call to an API that changed a release ago.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [Skills For Real Engineers](https://github.com/mattpocock/skills) | Small skills for the daily loop: `tdd` builds one red-green slice at a time, `diagnosing-bugs` makes the bug fail on demand before any fix, `code-review` and `improve-codebase-architecture` carry the refactor. MIT. | Claude Code, Codex | one description for each skill the agent may call on its own, each body on use: `tdd` is 3.6 KB, `diagnosing-bugs` 8.7 KB | `claude plugin install mattpocock-skills@claude-plugins-official`. Codex: `codex plugin marketplace add mattpocock/skills` → `codex plugin add mattpocock-skills@mattpocock`. Then `/setup-matt-pocock-skills` once per repository |
| Guard | `tests` | Runs your test command at the end of a turn that changed something, and blocks "done" while it fails. | both | none, a hook costs no context | built in, light profile |
| MCP server | [Context7](https://github.com/upstash/context7) | Returns the current docs and code examples of a library, for the version you name, so the agent stops writing calls that no longer exist. The server is MIT, the index behind it is closed. | Claude Code, Codex | 2 tools | `claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY`. Codex: `codex mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY` |

The guard is one of ours and needs no recipe: the one rule of everyday coding a machine can be sure of is that the tests pass before the agent says done. It is off until `test` in `harness/settings.json` names your test command.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [Superpowers](https://github.com/obra/superpowers) | A whole method in 15 skills: brainstorm, plan, build test-first with subagents, review. A session-start hook loads its entry skill in every session. | free, MIT |
| Skill | [Agent Skills](https://github.com/addyosmani/agent-skills) | 25 skills along the life of a change, from spec to ship. Each one carries a table of the excuses an agent uses to skip a step, and ends on the evidence it must show. | free, MIT |
| Skill | [Astral agent plugins](https://github.com/astral-sh/agent-plugins) | Python from the maker of its tools: skills for `uv`, `ruff` and `ty`, and the `ty` language server in Claude Code. | free, Apache-2.0 or MIT |
| Skill | [.NET Agent Skills](https://github.com/dotnet/skills) | The .NET team's plugins, installed one at a time: tests, diagnostics, MSBuild, upgrades, ASP.NET Core. | free, MIT |
| Guard | [`format`](../guide/guards.md) | Built in, light profile. Runs your formatter after every write and says when it rewrote the file, so a diff holds the change and nothing else. | free, ours |
| Guard | [`destructive`](../guide/guards.md) | Built in, heavy profile. Blocks `git reset --hard` and `git clean -f`, the commands a stuck debugging session reaches for. | free, ours |
| Guard | [Probity](https://github.com/nizos/probity) | Blocks production code written before a failing test was seen, in Claude Code and Codex. The rule asks a model, which adds a turn to each check. | free, MIT |
| MCP server | [Serena](https://github.com/oraios/serena) | Finds and edits code by symbol through a language server: references, renames and moves across files. | free, GPL-3.0-or-later |
| MCP server | [Sentry MCP](https://mcp.sentry.dev/) | The stack trace and the events of a production error, beside the code that threw it. | free plan for one user, the server is source-available |

## When each earns its place

- **The skill** → the agent writes the tests after the code and they only repeat it, or it fixes a bug on its first guess. Look at what the agent ships before you add more: Claude Code bundles `/code-review`, `/debug`, `/simplify` and `/verify`, [by its docs](https://code.claude.com/docs/en/skills). The skills you call by name carry `disable-model-invocation`, which keeps their descriptions out of the context there.
- **The guard** → the first time the agent says done on a red suite. It runs only when something changed since the last green run, and it costs the time of your test command at the end of a turn. `vectoralis init light` finds the command for you.
- **The MCP server** → the agent writes a call the library dropped a release ago, and you learn it from the compiler. The free plan gives 1,000 calls a month and the next one is $10 a seat a month, [by its pricing page](https://context7.com/docs/plans-pricing). Claude Code loads only the tool names until one is called, [by its docs](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search). The docs it returns are contributed by the community, and its README says their accuracy and safety are not guaranteed, so read them as data. More servers that look things up are on the [research](research.md) page.
- **The CLI first** → the same maker ships the lookup as a CLI with a skill and no server: `npx ctx7 setup --cli --claude`, or `--cli --codex`, [by its CLI docs](https://context7.com/docs/clients/cli). GitHub needs no server either: [`gh`](https://cli.github.com/manual/) reads issues, pull requests and pipeline runs at no context cost until it runs.

## Left out, and why

- [ECC](https://github.com/affaan-m/ECC) → 314 skills and 71 agents by its own count. Its README says the Claude Code plugin shows the whole installed catalog to the model, and points to a selective install when the context matters.
- [wshobson/agents](https://github.com/wshobson/agents) → a catalog of 94 plugins holding 185 skills, built to be installed one plugin at a time. Go there once you know which plugin you want.
- [TDD Guard](https://github.com/nizos/tdd-guard) → Claude Code only, and its README sends new projects to Probity, in the table above.

## A sample to study

[uv's `AGENTS.md`](https://github.com/astral-sh/uv/blob/main/AGENTS.md) → 30 rules in 3.7 KB that tell an agent how a large Rust project wants its tests: integration tests over unit tests, snapshots over substring checks, one named test per scenario. It also holds the line every agent needs: never assume a failing test or a lint warning was there before you. `referenced`

## How to do it better

- **Every rule is a sentence the agent can skip** → "never assume a failure was there before" is the one a machine can hold. The `tests` guard blocks "done" while the suite fails, whoever broke it.
- **It asks for one specific test while working, and names no check at the end** → keep the fast test in the loop, and let the guard run the whole command once before "done".
- **It says how to write tests, and nothing on how to find a bug** → add a loop for it: make the bug fail on demand, then narrow, then fix, then keep the test. That is `diagnosing-bugs` in the pick.
- **A test switched off to get green breaks no rule in the file** → guard it. The `no-skipped-test` recipe on the [testing](testing.md) page does it for Playwright specs, and the same shape takes the skip marker of your own runner, such as `@pytest\.mark\.skip`.
- **All 30 rules load in every session** → 3.7 KB is small today. Keep in the file what every task needs, and move the rest to a skill that loads when its work comes up.

## Where people talk

- [r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/) → Claude Code day to day: skills, hooks, and what breaks.
- [r/codex](https://www.reddit.com/r/codex/) → the same for Codex.
- [r/ChatGPTCoding](https://www.reddit.com/r/ChatGPTCoding/) → coding with any model or agent, and comparisons of the tools.
- [r/ExperiencedDevs](https://www.reddit.com/r/ExperiencedDevs/) → how senior engineers judge agent-written code, reviews and tests on real teams.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
