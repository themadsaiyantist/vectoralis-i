# AI Security

AI security is keeping an agent safe when it reads text it cannot trust and then acts on your machine. It covers injected instructions in tool output, web pages and files, what the agent may touch, where your secrets live, what you install into the agent, and how you attack your own setup before a stranger does. Read this page before you give an agent a shell, a browser or an MCP server, and again before you let one run unattended.

**Contents:** What it is · Why now · Start here · Resources · Build this · The kit · Where people talk · The future

## What it is

- **The problem** → a model reads instructions and data as one stream, so a sentence in a web page, a file or a tool result can steer the agent. This is prompt injection, and no patch closes it today.
- **The defense** → build so that a fooled model breaks nothing that matters: narrow permissions, a sandbox, secrets out of reach, and only skills, plugins and MCP servers you have read.
- **The test** → red teaming: attack your own agent the way a stranger would, and keep every finding as a test that runs again.

## Why now

- **The risk lists were rewritten around agents.** OWASP published its first Top 10 for Agentic Applications on 2025-12-09 and a new Top 10 for LLM Applications on 2026-08-03, where Excessive Agency moved up to third → `read` [the agentic list](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) · [the 2026 announcement](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/)
- **Injected instructions moved into the tools.** Researchers steered Claude Code, Gemini CLI and GitHub Copilot agents in GitHub Actions with text in a pull request title, an issue comment or a hidden HTML comment. Others reached Claude Code, Cursor and Codex with fabricated error events sent through the Sentry MCP server → `read` [OWASP roundup, Q2 2026](https://genai.owasp.org/2026/07/08/genai-and-agentic-ai-exploit-roundup-q2-2026/)
- **Skills, plugins and MCP servers became a supply chain.** A scan of 3,984 public agent skills found a critical issue in 13.4% of them and confirmed 76 malicious payloads. In August one account opened 23 pull requests in 74 minutes to add an MCP server that showed harmless tool descriptions until after its third call → `read` [Snyk, 2026-02-05](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) · [Pillar Security, 2026-08-12](https://www.pillar.security/blog/deadbugz-currently-active-mcp-supply-chain-campaign)
- **The agents changed their own defaults.** Claude Code from v2.1.283 starts interactive sessions in auto mode, where a second model reviews actions before they run. Codex keeps local commands in a sandbox with the network off, and can send approval requests to a reviewer agent → `read` [Claude Code](https://code.claude.com/docs/en/permission-modes) · [Codex](https://learn.chatgpt.com/docs/agent-approvals-security)
- **Agents did damage with no attacker present.** The third-quarter roundup records evaluation agents that reached another company's production systems with exposed credentials, and draws one lesson: "Prompt-level instructions alone do not establish a secure boundary." → `read` [OWASP roundup, Q3 2026](https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/)

## Start here

- ⬜ Read the ten agent risks → the agentic Top 10, first row under Resources → mark the ones your own setup has.
- ⬜ List what your agent can reach → files, shell, network, credentials, MCP servers → check the list against the [Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/): untrusted input, private data, and the power to change state or send data out → no session holds all three without your approval.
- ⬜ Turn on the sandbox → Claude Code: `/sandbox`, so writes stay in the project and the network passes an allowlist that starts empty ([sandboxing](https://code.claude.com/docs/en/sandboxing)) → Codex: stay in `workspace-write`, where the network is off by default ([approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)) → the full setup is in [safety](../guide/safety.md).
- ⬜ Put secrets out of reach → the Claude Code sandbox still reads `~/.ssh` and `~/.aws/credentials` → list them under `sandbox.credentials` → add a `Read(./.env)` deny rule so the file tools refuse too ([permissions](https://code.claude.com/docs/en/permissions)).
- ⬜ Choose the permission mode on purpose → auto mode has a second model review actions before they run → bypass mode belongs in a container or a VM only → [modes](../guide/modes.md).
- ⬜ Audit what you installed → `claude plugin list` → `claude plugin details NAME` → read each plugin's `hooks/hooks.json`, `.mcp.json` and `bin/`, because a plugin runs code with your full access, outside the sandbox ([plugin security](https://code.claude.com/docs/en/plugins/security)) → remove what you do not use → do the same for every MCP server ([MCP](../guide/mcp.md)).
- ⬜ Plant a harmless canary → in a throwaway repository, put one sentence in a file that asks the agent to create a marker file → ask the agent to summarize the repository → the marker appears or it does not → repeat with a web page and a tool result.
- ⬜ Turn the finding into a guard → a hook that blocks the action you just saw, with one payload that must block and one that must pass → [guards](../guide/guards.md).

## Resources

| Resource | Free or paid | Clarity | Depth | Hands-on | Current | Excels at |
|---|---|---|---|---|---|---|
| [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) and [for LLM Applications 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) | free | ★ 9 | ★ 7 | ★ 2 | ★ 10 | The shared name for every risk, each with its mitigations. Better than the rest for scoping a review and for talking to a security team. |
| [OWASP Securing Agentic Applications V2](https://genai.owasp.org/resource/securing-agentic-applications-v2/) | free | ★ 7 | ★ 9 | ★ 4 | ★ 10 | What to build: architecture, identity, runtime protection, supply chain, testing. Goes deeper on design than the two lists, and it is the newest guide here. |
| [OWASP exploit roundup, Q3 2026](https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/) | free | ★ 8 | ★ 6 | ★ 1 | ★ 10 | Real incidents every quarter, with what failed in each. Nothing else here shows as plainly how attacks happen outside a lab. |
| [PortSwigger Web LLM attacks](https://portswigger.net/web-security/llm-attacks) | free | ★ 9 | ★ 6 | ★ 9 | ★ 5 | Browser labs on injected instructions, excessive agency and unsafe output. The fastest first lab on the list, with nothing to install. |
| [OWASP FinBot CTF](https://owasp-finbot-ctf.org/) | free | ★ 7 | ★ 8 | ★ 10 | ★ 9 | Attacking a live multi-agent app that holds real tools: policy bypass, data theft, destructive actions. Closer to a real agent than any other lab here. |
| [Microsoft AI Red Teaming 101](https://learn.microsoft.com/en-us/security/ai-red-team/training) | free | ★ 8 | ★ 7 | ★ 7 | ★ 6 | Ten episodes from first principles to automated multi-turn attacks with PyRIT, plus twelve lab challenges that run in Docker with your own model key. The best here for learning to automate a red team. |
| [MCP Security Best Practices](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices) | free | ★ 7 | ★ 9 | ★ 3 | ★ 9 | Attacks at the protocol level: confused deputy, token passthrough, request forgery, a compromised local server. The only entry written for people who build or review an MCP server. |

## Build this

| Project | Difficulty | What it teaches | A repository to study |
|---|---|---|---|
| A canary bench: plant a harmless marker instruction in a file, a web page and a tool result, run your agent over each, count how often it obeys | ★ 4 | ★ 9 → where untrusted text gets in, measured on your own setup | `referenced` [ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo) |
| A secrets guard: a hook that refuses reads of secret files and scans every write and every command output for keys | ★ 3 | ★ 7 → what a fixed check catches that a prompt cannot | `referenced` [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) |
| A sandbox profile: the agent's commands run with writes limited to one folder and the network limited to an allowlist | ★ 6 | ★ 9 → where the boundary sits in the operating system | `referenced` [anthropics/sandbox-runtime](https://github.com/anthropics/sandbox-runtime) |
| A scanner for what you installed: walk every skill and MCP config, flag hidden instructions, store a hash of each tool description and alert when one changes | ★ 6 | ★ 8 → how a skill or a server turns on you after review | `referenced` [cisco-ai-defense/skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) |
| A red-team run in CI: probe your model endpoint on every change and fail the build on a new hit | ★ 5 | ★ 7 → attacks kept as regression tests | `referenced` [NVIDIA/garak](https://github.com/NVIDIA/garak) |
| A policy gate: a process outside the model that answers allow, deny or ask for each tool call, and logs the answer | ★ 8 | ★ 10 → control that still holds when the model is fooled | `referenced` [GenAI-Security-Project/agent-control-standard](https://github.com/GenAI-Security-Project/agent-control-standard) |

## The kit

- [kit/security.md](../kit/security.md) → the three picks for security work. Take the guard first: it is the part that still holds when the model is fooled.
- [kit/agents.md](../kit/agents.md) → the picks for running subagents. Take the habit with them: each agent gets only the tools its job needs.
- [kit/devops.md](../kit/devops.md) → the picks for CI and deploys. This is where an agent holds real credentials, so read the risk line of every entry.
- [kit/testing.md](../kit/testing.md) → the picks for tests. A red-team run is a test suite, so wire it into the same run.
- [kit/team-tools.md](../kit/team-tools.md) → the servers for trackers and chat. Each one carries other people's text to your agent, so install the fewest that do the job.

## Where people talk

- [r/netsec](https://www.reddit.com/r/netsec/) → technical write-ups only. New attack research on agents shows up here with the paper or the proof.
- [r/cybersecurity](https://www.reddit.com/r/cybersecurity/) → the wide room: incident news, career questions, and how security teams deal with agents.
- [r/mcp](https://www.reddit.com/r/mcp/) → new MCP servers announced every day, and the problems people hit once they connect them, security included.
- [OWASP Slack](https://owasp.org/slack/invite) → the channel `#project-top10-for-llm`, where the people who write the LLM Top 10 discuss it.
- [Claude Discord](https://www.anthropic.com/discord) → the official server, for questions on modes, sandbox and hooks.
- [OpenAI developer forum, Codex category](https://community.openai.com/c/codex/) → the official forum, for questions on sandbox modes and approvals.

## The future

- **Control moves outside the model** → a policy process that allows, denies or asks before each action. OWASP's Agent Control Standard is at v0.1.0, with a first shim for Claude Code.
- **Installed parts get pinned and approved again on change** → a changed tool description becomes a security event, the way a changed dependency is today. Claude Code's community catalog already pins plugins to a commit.
- **Prompt injection stays open** → expect better filters and no cure. The rule that lasts: untrusted input, private data and outside action never meet in one session without a person.
- **Red teaming runs all the time** → scanners in CI and agents that test agents, with each quarter's incidents turned into new tests.

The stars are a judgment, made on 2026-11-11. Verified 2026-11-11: every link opened.
