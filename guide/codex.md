# Codex

The same harness in Codex: the same two plugins, the same guards, the same records. This page maps each piece and lists every gap. Read it before you install in Codex, or when a piece behaves differently there.

**Contents:** Where it stands · The map · The gaps · Set it up · What you type · What can go wrong

---

## Where it stands

- **Built for both.** One marketplace file, one hooks file, one engine. The engine reads a Codex payload and a Claude Code payload into one shape, and its tests feed it both.
- **Run in Claude Code.** Every output in this guide marked `run` came from there.
- **Installed in Codex.** Codex reads the same marketplace file and installs both plugins from it:

```text
$ codex plugin marketplace add /home/goku/vectoralis-i
Added marketplace `vectoralis` from /home/goku/vectoralis-i.
$ codex plugin add light@vectoralis
Added plugin `light` from marketplace `vectoralis`.
$ codex plugin add heavy@vectoralis
Added plugin `heavy` from marketplace `vectoralis`.
$ codex plugin list
PLUGIN            STATUS              VERSION  SOURCE
light@vectoralis  installed, enabled  0.1.0    /home/goku/vectoralis-i/plugins/light
heavy@vectoralis  installed, enabled  0.1.0    /home/goku/vectoralis-i/plugins/heavy
```

`run`: Codex 0.167.0, from a local copy of this repository, in a scratch Codex home, 2026-11-11.

- **Not yet run in a Codex session.** The hooks firing inside Codex, and the skills called there, are `read` in Codex's own docs. That run is an open box in this repository's [to-do list](../harness/todo.md).

---

## The map

| The piece | Claude Code | Codex |
|---|---|---|
| Marketplace | `.claude-plugin/marketplace.json` | reads the same file |
| Add it | `claude plugin marketplace add` | `codex plugin marketplace add` |
| Install | `claude plugin install light@vectoralis` | `codex plugin add light@vectoralis` |
| Hooks | `hooks/hooks.json` in the plugin | the same file, trusted once in `/hooks` |
| The plugin's folder | `CLAUDE_PLUGIN_ROOT` | `PLUGIN_ROOT`, and `CLAUDE_PLUGIN_ROOT` is set too |
| Skills | `skills/<name>/SKILL.md` | the same folders |
| Call a skill | `/heavy:check` | `$heavy:check` |
| A file edit | `Write`, `Edit` | one `apply_patch` |
| The core, always loaded | session-start output | session-start output |
| Instructions file | `CLAUDE.md` | `AGENTS.md` |
| The records | `harness/` | `harness/` |

---

## The gaps

| The gap | What it means | What to do |
|---|---|---|
| No plugin dependencies | `heavy` does not bring `light` | add both |
| Hooks need one review | a hook is skipped until you trust it, and again when it changes | `/hooks`, once, and after an update |
| A plugin cannot carry a subagent | `reviewer` and `builder` are Claude Code only | write yours in `.codex/agents/*.toml`, or use a second session with a read-only sandbox |
| No worktree isolation for a subagent | two agents can meet in one tree | `git worktree add` by hand |
| The compaction prompt | Codex runs the hook and ignores what it prints | set `compact_prompt` in `.codex/config.toml`, and write the handoff before a long session ends |
| The CLI is not on the path | `vectoralis` is not found | the skills call it by its path, under `~/.codex/plugins/cache/vectoralis/light/` |
| No "ask" from a hook | a guard cannot hand a decision to you | here a guard blocks or warns, in both agents |
| A hook cannot tell a subagent | Codex sends no subagent mark with a tool call, so the `records` guard has nothing to go on | tell a subagent in its instructions to stay out of `harness/` |
| Command rules are experimental | Codex has allow, prompt and forbidden rules for commands, and labels them experimental, so nothing here builds on them | `sandbox_mode` and `approval_policy` |

Each row is `read`: [plugins](https://learn.chatgpt.com/docs/plugins), [hooks](https://learn.chatgpt.com/docs/hooks), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [approvals and sandbox](https://learn.chatgpt.com/docs/agent-approvals-security), [command rules](https://learn.chatgpt.com/docs/agent-configuration/rules), [the config reference](https://learn.chatgpt.com/docs/config-file/config-reference), 2026-11-11.

---

## Set it up

```text
codex plugin marketplace add themadsaiyantist/vectoralis-i
codex plugin add light@vectoralis
codex plugin add heavy@vectoralis
```

Then, in a session → `/hooks` → review and trust → `$heavy:setup`.

For a team, a trusted project can switch the plugins on in `.codex/config.toml`:

```toml
[plugins."light@vectoralis"]
enabled = true

[plugins."heavy@vectoralis"]
enabled = true
```

Each person still trusts the project and the hooks on their own machine. A repository cannot grant itself trust.

---

## What you type

The grants are the same words in both agents, because the engine reads them from your message:

| You type | It allows |
|---|---|
| `unlock` and the path | a write to locked work |
| `tick` and a few words of the line | a box in your column |
| `lesson:` and the lesson | one entry in `harness/lessons.md` |
| `promote` and the guard | a guard goes from warn to block |

---

## What can go wrong

- **A guard that never speaks** → the hooks were not trusted, or an update changed them. `/hooks`.
- **`AGENTS.md` grows past its limit** → Codex reads 32 KiB of instructions in all. Keep it short, and let `harness/rules.md` arrive at session start.
- **A push is refused** → in a `workspace-write` sandbox the network is off by default.
- **You find a gap this page does not list** → [open an issue](../CONTRIBUTING.md). A gap table is only as good as its last run.

Verified 2026-11-11. The install is `run` on Codex 0.167.0. Every other Codex line is `read` in the docs of Codex 0.167.1.
