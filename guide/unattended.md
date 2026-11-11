# Unattended

Running without you: one command in a script, a job in CI, or a loop that comes back on its own. Read this before the first run you will not watch, and again when one surprised you.

**Contents:** The three ways · Before you leave it alone · What was left out · In Claude Code · In Codex · With the harness · What can go wrong

---

## The three ways

| The way | Claude Code | Codex | The result lands in |
|---|---|---|---|
| One run from a script | `claude -p "<task>"` | `codex exec "<task>"` | stdout, a file, an exit code |
| A job in CI | `anthropics/claude-code-action@v1` | `openai/codex-action@v1` | the run log, a comment, a pull request |
| A loop on a timer | `/loop 5m <prompt>`, in a session you keep open | none in the CLI. A scheduled task is made in the ChatGPT desktop app or on the web | the session |
| A loop until a condition holds | `/goal <condition>` | `/goal <objective>` | the session |

## Before you leave it alone

| It must be true | Why | In Claude Code | In Codex |
|---|---|---|---|
| A check a machine can run | "done" is a claim until an exit code backs it | the test command, named in the task or in the goal: "`npm test` exits 0" | the same command, named as the goal's verification |
| Guards that block and never ask | nobody is there to answer | `--permission-mode dontAsk` and an allow list. Reads still run. Anything else that is not on the list is refused | a sandbox mode, and `approval_policy = "never"` so it does not stop to ask |
| A budget | a run with no ceiling has no reason to stop | `--max-turns` and `--max-budget-usd`, in `-p` only. The second reads an estimate that spend can pass, so leave room. Then the job's `timeout-minutes` | `codex exec` has no turn or spend flag, so the job's `timeout-minutes`. A goal takes `goals.max_goal_token_budget` |
| A place where the result lands | work nobody reads did not happen | a branch and a pull request, or `--output-format json > result.json` | `-o result.md`, or a patch that a second job turns into a pull request |

Both tables are `read`, 2026-11-11. Claude Code: [headless](https://code.claude.com/docs/en/headless), [CLI flags](https://code.claude.com/docs/en/cli-reference), [permission modes](https://code.claude.com/docs/en/permission-modes), [GitHub Actions](https://code.claude.com/docs/en/github-actions), [scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks), [goal](https://code.claude.com/docs/en/goal). Codex: [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode), [the CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [GitHub Action](https://learn.chatgpt.com/docs/github-action), [scheduled tasks](https://learn.chatgpt.com/docs/automations), [long-running work](https://learn.chatgpt.com/docs/long-running-work), [sandbox](https://learn.chatgpt.com/docs/sandboxing), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference). GitHub: [`timeout-minutes`](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idtimeout-minutes).

## What was left out

- **Claude Code** → [cloud scheduled tasks](https://code.claude.com/docs/en/routines), once called routines: research preview. [Channels](https://code.claude.com/docs/en/channels): research preview. [Agent teams](https://code.claude.com/docs/en/agent-teams): experimental. [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd): beta.
- **Codex** → the `codex cloud` command: experimental. [Command rules](https://learn.chatgpt.com/docs/agent-configuration/rules) in `.rules` files: experimental. [Permission profiles](https://learn.chatgpt.com/docs/permissions): beta. The rollout budget: under development.
- Each label is the vendor's own, `read` on 2026-11-11. This page builds on none of them.

## In Claude Code

- **The run** → `claude -p "<task>"`. It exits 0 on success and non-zero when the run fails, so a script can branch on it.
- **The output** → `--output-format text` is the default. `json` puts the answer in `result`, with `session_id` and `total_cost_usd`. `stream-json` prints one event per line. `--json-schema` adds a `structured_output` field that fits your schema.
- **The permissions** → a `-p` run with no mode set starts in Manual, and a call that needs approval is denied, from v2.1.302. So the run names every tool it may use, and its ceiling:

```bash
claude -p "Make tests/test_cart.py pass. Change cart.py only." \
  --permission-mode dontAsk \
  --allowedTools "Read" "Edit" "Bash(python3 -m unittest *)" \
  --max-turns 20 --max-budget-usd 2 \
  --output-format json > result.json
```

- **Or a second model** → `--permission-mode auto --permission-prompts none`. A classifier reviews each action, and what would have fallen back to a prompt is denied. [Modes](modes.md)
- **`--bare`** → skips hooks, skills, plugins, MCP servers and `CLAUDE.md`, so a run starts fast and the same on every machine. No guard runs in a bare run. The docs name it the future default of `-p`.
- **CI** → `/install-github-app` in a session sets the Action up. With a `prompt` input it runs on any event, a `schedule` included. A plain prompt gets no shell until `claude_args` allows one. The step, after a checkout:

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Run the tests. Say which fail and why. Change nothing."
    claude_args: '--max-turns 10 --allowedTools "Read,Bash(python3 -m unittest *)"'
```

- **A loop** → `/loop 5m <prompt>` repeats on a fixed interval. `/loop <prompt>` lets Claude pick the wait, between one minute and one hour. It fires only while the session is open and idle, and a recurring loop ends itself after seven days. `/goal <condition>` starts the next turn as soon as one ends, until a second model reads the condition as met.

## In Codex

- **The run** → `codex exec "<task>"`, inside a Git repository. Progress goes to stderr and the final message to stdout.
- **The sandbox** → read-only by default. `--sandbox workspace-write` lets it edit. `--approve-for-me`, in its place, is the same sandbox with a reviewer agent answering what needs approval. `danger-full-access` is for an isolated runner or a container.
- **The output** → `--json` makes stdout a stream of JSON Lines. `-o <file>` writes the final message to a file. `--output-schema <file>` makes that message fit a JSON Schema.

```bash
codex exec --sandbox workspace-write --json -o result.md \
  "Make tests/test_cart.py pass. Change cart.py only." > events.jsonl
```

- **The key** → `CODEX_API_KEY=<key> codex exec "<task>"` sets it for that one command. Set at the job level, every step of the job can read it.
- **CI** → the Action installs the CLI, starts a proxy that holds the key and runs `codex exec`. `safety-strategy` drops `sudo` by default. The docs split the work into two jobs → one runs Codex with `contents: read` and saves a patch → the other applies it and opens the pull request, and never sees the key. The step, after a checkout:

```yaml
- uses: openai/codex-action@v1
  with:
    openai-api-key: ${{ secrets.OPENAI_API_KEY }}
    prompt-file: .github/codex/prompts/fix.md
    sandbox: workspace-write
```

- **A loop** → `/goal <objective>` in a session. The goal is the first prompt and the finish line, and it keeps your sandbox and your approval policy. `/goal pause`, `/goal resume`, `/goal clear`. Its docs: "Codex CLI doesn't provide the Scheduled management interface."
- **The hooks** → Codex skips a [hook](https://learn.chatgpt.com/docs/hooks) nobody reviewed. On a fresh runner that is every hook. `--dangerously-bypass-hook-trust` runs them for one invocation, and the docs keep it for automation that already vets where its hooks come from.

## With the harness

| | Light | Heavy |
|---|---|---|
| The machine check | `tests` runs the `test` command of `harness/settings.json` when the agent stops, and sends it back while it fails, once a turn | adds `sweep`: what the turn changed is read again |
| Never asks | every guard answers pass, warn or block. None can ask | the same |
| Where the result lands | your script decides | `push` refuses the default branch and a merge while `merge` is `yours`, so the work leaves as a branch and a pull request. [Pull requests](pull-requests.md) |
| Where the next run starts | from nothing | from the briefing, built from `## Now` in `harness/todo.md`. [Handoff](handoff.md) |
| What stays yours | | nobody types `tick` or `unlock`, so your boxes and your locks stay closed |

- **In Claude Code** the guards load in a `-p` run that is not `--bare`. Three real headless runs of light, a refused secret and a refused "done" among them → [Light](light.md). Their turns, time and cost → [Cost](cost.md).
- **In the Action** two inputs install the plugin for the job: `plugin_marketplaces` takes this repository's Git URL, `plugins` takes `light@vectoralis`. In Codex the guards run only where the hooks were trusted. [Codex](codex.md). Both are `read`, not run here.

## What can go wrong

- **A run with no guard, and no sign of it.** `--bare` loads no hook. A fresh Codex runner trusted none. Neither says so in the result → keep `--bare` out of a run that needs the guards, and stop the job when `light` is missing from the `plugins` list of the `system/init` event that `--output-format stream-json --verbose` prints. In Codex let the sandbox and the two jobs be the boundary.
- **"Done" with failing tests.** The `tests` guard sends the agent back once. `/goal` judges from the transcript and runs nothing itself → the script runs the test command after the agent, and trusts that exit code alone.
- **Someone else's text in the prompt.** An issue body or a pull request title pasted into the prompt is read as instructions. Heavy reads the prompt for grants too: a headless `claude -p` run whose prompt carried `unlock tests` opened that lock. `run`, in a live session, see [Heavy](heavy.md) → write that text to a file and name the file in the prompt. Both Actions start only for people with write access by default. Keep it so.
- **A repository you did not write.** `claude -p` shows no trust dialog: it runs the project's hooks and connects the servers of its `.mcp.json` → `--setting-sources user`, or `--bare`. `read`: [permissions](https://code.claude.com/docs/en/permissions).
- **A permission list that is too short.** A headless run cannot ask. A command outside `--allowedTools` is denied, and a subagent inherits the list. In a live run two builders wrote files they could not test, and the session refused to tick a box on work it could not check (`run`) → allow what the builders need before the run starts.
- **A loop nobody ends.** A goal keeps taking turns until its condition holds → write the limit into it, "or stop after 20 turns", and in Codex set `goals.max_goal_token_budget`.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. Every agent line is `read` in the docs linked on this page, and none of those commands was run here. `run`: this repository's unit tests, which hold the `tests` guard sending the agent back once and never twice, and the engine's answer to a prompt that carries an `unlock`. One line is `run` in a live headless session: the permission list that was too short.
