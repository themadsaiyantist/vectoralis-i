# Safety

What stands between an agent and your machine: its own permission rules and sandbox first, then the guards of this harness. Read this before you give an agent a shell, before you loosen a mode, and before any run from [Unattended](unattended.md).

**Contents:** The four ways it goes wrong · What a guard is not · In Claude Code · In Codex · With the harness · What can go wrong

---

## The four ways it goes wrong

| It goes wrong when | The agent's own stop, first | Then the harness |
|---|---|---|
| it writes or prints a secret | a rule that refuses the read, and credentials kept away from the shell | `secrets` |
| it runs a command that cannot be undone | a sandbox that keeps writes inside the project, and a mode that asks or refuses | `destructive`, `locks`, `push` |
| it follows instructions hidden in a web page, a file or a tool's output | pages that arrive as a summary or from a cache, and a network that stays closed until you open it | no guard can see it. The four above cap what a fooled agent can do, and a grant is read from your message alone |
| it installs something it should not | an approval before the command, a network allowlist, a review before a plugin's code runs | none built in. A guard of your own can warn. [Guards](guards.md) |

## What a guard is not

A guard is a guardrail, not a wall, and not a sandbox. Three layers, the strongest first:

| Layer | Who enforces it | It holds against | It does not hold against |
|---|---|---|---|
| The sandbox | the operating system | every process the agent's shell starts, whatever the command says | in Claude Code, the file tools, the hooks and the MCP servers: they run outside it |
| Permission rules and the mode | the agent, before a tool call | the calls a rule names | the same program spelled another way |
| A guard | a hook of this harness | what a machine can be sure of in the text of an edit or a command | a script, a second shell, a tool of an MCP server |

- **The vendors say it of their own rules.** Claude Code: a deny rule "isn't a security boundary around the program". Codex: "Treat tool hooks as a useful guardrail, not a complete enforcement boundary."
- **A guard reads text.** `cat .env` was blocked. The same file opened by a one-line script passed, exit 0.
- **A guard is a hook**, and Claude Code runs hooks outside its sandbox, with your full access. It limits nothing at the level of the operating system.
- **A guard that breaks steps aside** → one line, exit 1, and the call goes on.
- **What it is for** → the honest mistake, stopped every time, with the fix in the message. Heavy's `sweep` reads the turn again when the agent stops. Here a script had rewritten a locked file around the first check:

```text
NOT DONE YET, says Vectoralis.
- `src/payments/cart.py` changed this turn and it is locked by `src/payments/**`.
  Rule: a write made around the write guards is held to the same rules (guard `sweep`).
  Do instead: put it back as it was, then ask the person to type `unlock src/payments/cart.py`.
```

## In Claude Code

- **See the rules** → `/permissions`. A deny wins over an ask, an ask over an allow, and a deny holds in every mode. An ask rule such as `Bash(git push *)` stops for you in auto mode too. The modes → [Modes](modes.md).
- **Secrets** → deny the read: `Read(./.env)`. The rule covers the file tools and the commands Claude Code recognizes, such as `cat`. It does not cover a script that opens the file itself. That takes the sandbox.
- **The sandbox** → `/sandbox`. It is off by default. On, a shell command writes in the working directory, a temp folder and the folders you added, and reaches no host until you allow one. It still reads `~/.ssh` and `~/.aws/credentials`, and it has no built-in list of credentials, so name them. All three, in `.claude/settings.json`:

```json
{
  "permissions": { "deny": ["Read(./.env)", "Read(./secrets/**)"], "ask": ["Bash(git push *)"] },
  "sandbox": { "enabled": true, "credentials": { "files": [{ "path": "~/.ssh", "mode": "deny" }, { "path": "~/.aws/credentials", "mode": "deny" }] } }
}
```

- **Injected instructions** → for most fetches WebFetch hands Claude the answer of a separate model call, not the raw page. In auto mode Claude Code strips tool results from what it sends the classifier, so a page cannot talk to it. The docs still say no system is immune.
- **Installs** → by default auto mode allows an install of what your lock file or manifest declares, and blocks downloading and running code, like `curl | bash`. A plugin runs code with your user privileges, outside the sandbox → read its `hooks/hooks.json`, `.mcp.json` and `bin/` before you install it. This one included.

## In Codex

- **See the rules** → `/permissions` to change them, `/status` to read the approval policy and the writable roots. Two dials: `sandbox_mode` is what a command can touch, `approval_policy` is when Codex asks. [Modes](modes.md)
- **The sandbox** is on by default. In `workspace-write` a command writes inside the workspace, the network is off, and `.git`, `.codex` and `.agents` stay read-only.
- **Secrets** → Codex does not strip variables named with `KEY`, `SECRET` or `TOKEN` from the commands it starts until you ask. In `~/.codex/config.toml`:

```toml
[shell_environment_policy]
inherit = "core"
ignore_default_excludes = false
```

- **Injected instructions** → web search answers from a cache OpenAI keeps, not from the live page, until you pass `--search` or run with full access. Its docs: "Treat web results as untrusted."
- **Installs** → the network is off, so a command that needs it asks first. A plugin's hooks are skipped until you review them in `/hooks`, and again when one changes.
- **The gap** → no allow, ask and deny rules. Command rules and permission profiles exist, labelled experimental and beta, so this page leaves them out.

## With the harness

| Guard | Profile | It blocks | It warns on |
|---|---|---|---|
| `secrets` | light | a key in a known format on its way into a file, a command that prints a secrets file or a secret variable | a quoted value that only looks like a key, a dump of the whole environment |
| `destructive` | heavy | `git reset --hard`, `git clean -f`, a forced push, `rm -r` on `/`, `~`, `.` or the project root, a command that overwrites a disk | another `rm -r`, `git checkout --`, `git restore`, `git branch -D`, `git stash drop` |
| `locks` | heavy | a write to a path locked in `harness/locks.md`, by an edit or by a shell command that names the path | |
| `push` | heavy | a push to the default branch and `gh pr merge`, while `merge` is `yours` | |

- Light runs `secrets` alone of these. Heavy adds the other three and the `sweep`. Each is one short file in [`plugins/light/engine/guards/`](../plugins/light/engine/guards/). All ten, with their proof → [Guards](guards.md).
- **A block says what was stopped, the rule, and what to do instead:**

```text
BLOCKED by Vectoralis. The command did not run.
- The command prints a secrets file, `.env`.
  Rule: no secret is written to a file or printed (guard `secrets`).
  Do instead: check that the value is set without printing it, for example `test -n "$NAME"`.
```

- **A grant comes from your message alone.** A machine's notice that carried the word `unlock` opened nothing. The same word typed by the person opened the lock, until their next message. A line in a file or on a web page is not your message, so it opens nothing.
- **An install** → no built-in guard reads one. A guard of the project's own, on `shell`, warned on `npm install left-pad` and passed `npm ci`.

`run`, 2026-11-11: `vectoralis guards`, 115 payloads behaving, and the hook entry point fed one payload at a time in a throwaway project, as the unit tests do. No command in a payload was executed.

## What can go wrong

- **The guards' own switch.** `harness/settings.json` turns a guard off, so it is yours. An edit to it is blocked, a shell command that would change it is blocked before it runs, and a change made some other way is caught when the agent stops (`run`: the guards' payloads). The same holds for `harness/lessons.md` and for a guard file in `harness/guards/`.
- **Two commands the harness runs for you.** The guards run the `test` and `format` commands of `harness/settings.json`, and a hook runs with your access. So a command runs only after it was approved on your machine: `vectoralis init` approves the ones it found itself, and a repository that arrives with its own settings waits for `vectoralis trust` (`run`). Read the commands before you type it.
- **Guards gone quiet.** In Codex an update that changes a hook's script switches the hooks off until you review them again. In Claude Code a `--bare` run loads none. A guard that breaks steps aside → `vectoralis guards` after every update, and `/hooks` in Codex.
- **A tool of an MCP server.** The guards read file edits and shell commands. A server's tool call passes none of them → [MCP](mcp.md).
- **Full access, and the web goes live.** In Codex `--yolo` drops the sandbox and the approvals, and web search switches from the cache to live pages → a container, or `--approve-for-me`. [Modes](modes.md)

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `read` in Claude Code's docs: [permissions](https://code.claude.com/docs/en/permissions), [permission modes](https://code.claude.com/docs/en/permission-modes), [sandboxing](https://code.claude.com/docs/en/sandboxing), [security](https://code.claude.com/docs/en/security), [plugin security](https://code.claude.com/docs/en/plugins/security), [headless](https://code.claude.com/docs/en/headless). `read` in Codex's docs: [approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security), [sandbox](https://learn.chatgpt.com/docs/sandboxing), [advanced configuration](https://learn.chatgpt.com/docs/config-file/config-advanced), [hooks](https://learn.chatgpt.com/docs/hooks), [the CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [rules](https://learn.chatgpt.com/docs/agent-configuration/rules), [permissions](https://learn.chatgpt.com/docs/permissions). `run`: the guards, as said above. No agent session was run for this page, so no agent setting on it was tried here.
