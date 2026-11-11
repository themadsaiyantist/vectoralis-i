# Review and security

Review and security is the second look: reading a change before it merges, keeping secrets out of files and logs, and checking a dependency before its code runs on your machine. Both agents already review a diff when asked, with `/code-review` and `/security-review` in Claude Code and `/review` in Codex. Read this page before an agent installs packages on its own, and when a review has to find more than style.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [differential-review](https://github.com/trailofbits/skills/tree/main/plugins/differential-review) | Trail of Bits' security review of a change: it takes the risky parts first, reads the git history to catch a fix that was undone, counts the callers a change reaches, and names the changes no test covers. CC BY-SA 4.0. `tried` 2026-11-11: `claude plugin validate` passed on Claude Code 2.1.322, and both Codex lines ran in a scratch Codex home on 0.167.0: `Added plugin differential-review`, version 1.1.4. | Claude Code, Codex | one description, a 220-line body on use | `/plugin marketplace add trailofbits/skills` → `/plugin install differential-review@trailofbits`. Codex: `codex plugin marketplace add trailofbits/skills` → `codex plugin add differential-review@trailofbits` |
| Guard | `new-dependency` | Warns when the agent installs a package by name, the moment a new dependency arrives. `tried` 2026-11-11: the engine's proof, 4 of 4 payloads behave. | both | none, a hook costs no context | below |
| MCP server | [Socket MCP](https://github.com/SocketDev/socket-mcp) | Returns Socket's security scores for a package before it is installed, across npm, PyPI, Cargo, Go and more. MIT. `tried` 2026-11-11: the hosted server, 0.3.0, listed 7 tools and answered `depscore` with no sign-in: `browserlist` scored `supplyChain: 15`. | Claude Code, Codex | 7 tools | `claude mcp add --transport http socket-mcp https://mcp.socket.dev/` → `/mcp` to sign in. Codex: `codex mcp add socket-mcp --url https://mcp.socket.dev/` |

The built-in `secrets` guard already blocks a key on its way into a file or onto the screen, so the recipe covers the other half of this page: a package nobody checked.

```json
{
  "id": "new-dependency",
  "why": "one wrong letter in a package name installs a stranger's code, and its install script runs at once",
  "on": "shell",
  "pattern": "\\b(pnpm|yarn|bun|uv|poetry|cargo)\\s+add\\b|\\bnpm\\s+(install|i|add)\\s+[\"']?[a-zA-Z@]|\\bpip3?\\s+install\\s+[\"']?[a-zA-Z]",
  "mode": "warn",
  "message": "A new dependency is about to be installed. Check the name letter by letter and look up the package before its code runs here.",
  "payloads": [
    { "name": "catches a new npm package", "text": "npm install left-pad", "expect": "hit" },
    { "name": "catches a new Python package", "text": "pip install requests", "expect": "hit" },
    { "name": "passes an install from the lockfile", "text": "npm ci", "expect": "pass" },
    { "name": "passes a requirements file", "text": "pip install -r requirements.txt", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/new-dependency.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [supply-chain-risk-auditor](https://github.com/trailofbits/skills/tree/main/plugins/supply-chain-risk-auditor) | A report on the dependencies of an npm, PyPI or Go project: advisories matched to the exact version, abandoned upstreams, install scripts, and a table of what could not be measured. `tried` 2026-11-11: `claude plugin validate` passed: 1 skill. | free, CC BY-SA 4.0 |
| Skill | [static-analysis](https://github.com/trailofbits/skills/tree/main/plugins/static-analysis) | Runs CodeQL and Semgrep and reads the SARIF they write, so a finding comes from a scanner and not from a guess. `tried` 2026-11-11: `claude plugin validate` passed: 3 skills, `codeql`, `semgrep` and `sarif-parsing`. | free, CC BY-SA 4.0 |
| Skill | [Claude Security plugin](https://code.claude.com/docs/en/claude-security) | Anthropic's scan of a repository or a diff in Claude Code: agents hunt, every finding is reviewed again, and the fixes come as patches you apply yourself. `read` → paid. | needs a paid plan or API access, and each scan counts toward your usage |
| Skill | [Codex Security plugin](https://learn.chatgpt.com/docs/security/plugin) | OpenAI's scan of a local repository in Codex. It leaves the source unchanged and saves a report with evidence and fixes. `read` → needs Codex Security access. | needs Codex Security access |
| Guard | [`secrets`](../guide/guards.md) | Built in, light profile. Blocks a key in a known format written to a file, and a command that prints a secrets file. `tried` 2026-11-11: `vectoralis guards`: 84 of 84 payloads behave. | free, ours |
| Guard | [security-guidance](https://code.claude.com/docs/en/security-guidance) | Anthropic's plugin for Claude Code: a pattern check on every edit with no model call, then a model review of each turn and each commit. `tried` 2026-11-11: its pattern hook, fed one write in Docker: `pattern_hits: 2`, for `eval` and `pickle`, with no model call. The model review stays `read`: it spends usage. | free to install, the model reviews count toward your usage |
| Guard | [socket-gate](https://github.com/SocketDev/socket-mcp/blob/main/docs/commands.md) | Socket's hook for Claude Code. It is meant to deny an install when the package's supply-chain score is under 20, and to let it through when Socket cannot be reached. `tried` 2026-11-11: version 0.3.0 let `npm install browserlist` through: `failing open: Socket MCP did not return a session id`. The hosted server sends none, so today it denies nothing. | free |
| Guard | [Gitleaks](https://github.com/gitleaks/gitleaks) | Scans the git history and the working tree for secrets, as a pre-commit hook or in CI. `tried` 2026-11-11: v8.30.1 in Docker, `gitleaks git` on a tiny repository with two planted keys: `leaks found: 2`. | free, MIT |

## When each earns its place

- **The skill** → the change touches login, payments, permissions or anything that parses outside input, and a general review is not enough. Install this one plugin and leave the rest of the marketplace alone: it holds more than forty.
- **The guard** → the first session where the agent may install packages without asking. Socket's own example is `browserlist`, a look-alike of `browserslist`, which scores 15 where `express` and `react` score 75 and up.
- **The MCP server** → the agent picks dependencies itself and you want the score before the install, not after. It costs 7 tools. Its README says every call must be signed in, yet `depscore` answered here without one. `organizations` and `threat_feed` answered "Authentication required for this tool", so the other tools take a Socket account. The [free plan](https://socket.dev/pricing) covers one seat, and the README calls the project early and fast-moving.
- **The CLI first** → known vulnerabilities need no server. [OSV-Scanner](https://github.com/google/osv-scanner) reads your lockfiles against the OSV database with `osv-scanner scan source -r .` (`tried` 2026-11-11: version 2.7.1 found 4 advisories for `lodash` 4.17.20 in a tiny lockfile), and [zizmor](https://github.com/zizmorcore/zizmor) audits the workflows in `.github/`. Each costs no context until it runs. `tried` 2026-11-11: zizmor 1.32.0, `zizmor --offline` on a tiny workflow made for it: 5 findings shown, `unpinned-uses` and `template-injection` among them.

## Left out, and why

- [CodeRabbit](https://www.coderabbit.ai/pricing) → paid, from $24 a developer a month billed yearly, and free on public repositories only. Both agents review a diff at no extra cost.
- [semgrep/mcp](https://github.com/semgrep/mcp) → archived. Its README says the server moved into the `semgrep` binary.
- [detect-secrets](https://github.com/Yelp/detect-secrets) → Yelp's secret scanner. Its last commit is from 2026-04-02, past the three-month line, and Gitleaks, in the table above, is alive.

## A sample to study

[Claude Code Security Reviewer](https://github.com/anthropics/claude-code-security-review) → Anthropic's GitHub Action that reviews the diff of a pull request for vulnerabilities and comments on the lines. The part to study is the second pass: a filter that drops the findings most likely to be noise, such as denial of service and rate limiting, and that you can replace with your own instructions. `referenced`, opened 2026-11-11: not archived, last push 2026-02-11.

## How to do it better

- **Its README says it is not hardened against prompt injection** → run it on trusted pull requests only, and require approval before a workflow runs for an outside contributor, as the README itself advises.
- **Its quick start names both actions by a ref that can move, `@main` and `@v4`** → pin each action to a full commit SHA. zizmor has an audit for the ones you miss, `unpinned-uses`.
- **It looks only at what the pull request changed** → a review of the change cannot see a vulnerable version already in the lockfile, or a key in an old commit. Run OSV-Scanner and Gitleaks in the same workflow.
- **A finding is a comment** → make it count: read the action's `findings-count` output and fail a required check when it is above zero.
- **Its default model is from 2025, and the repository has had no push since February 2026** → the same review ships inside Claude Code as `/security-review`. Take the workflow and the filter from the sample, and set `claude-model` yourself.

## Where people talk

- [r/netsec](https://www.reddit.com/r/netsec/) → technical security write-ups, research first.
- [r/cybersecurity](https://www.reddit.com/r/cybersecurity/) → the wide room: incidents, tools and how teams work.
- [r/devsecops](https://www.reddit.com/r/devsecops/) → scanners in pipelines, dependency and secrets tooling.
- [r/AskNetsec](https://www.reddit.com/r/AskNetsec/) → questions and answers on security practice.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. `tried` 2026-11-11, in Docker or in a scratch folder: the picks, the three Trail of Bits skills, the four guards beside them, OSV-Scanner and zizmor, each with its evidence beside it. Still `read`: the Claude Security plugin, which is paid, and the Codex Security plugin, which needs its access. No plugin was loaded in a live agent session: a plugin counts as loaded when its manifest validates.
