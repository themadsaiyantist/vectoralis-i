# Handoff

Three ways to carry a long session over: a handoff document and a new session, a compaction with a prompt you give, and an auto compaction. Read this before a session gets long, not after it forgot something.

**Contents:** The three ways · What survives a compaction · Automatic and idle compaction · In Claude Code · In Codex · With the harness · A memory tool beside the handoff · What can go wrong

---

## The three ways

| The way | What survives | What is lost | Use it when |
|---|---|---|---|
| A handoff, then a new session | what the files say: the handoff, the records, the code | the conversation, its dead ends included | the task changes, or two corrections did not help |
| A compaction with your prompt | a summary shaped by your words, and what the agent reloads from disk | the detail you did not name | the same task goes on and the thread matters |
| Auto compaction | a summary shaped by a prompt you did not write | what that prompt did not think to keep | you did nothing in time |

- **Compact early, on purpose.** At a break between two tasks, with your words. Not in the middle of one, when the window fills.
- **Write it down first, in every case.** A summary can drop a fact. A file cannot.

---

## What survives a compaction

| The piece | After a compaction in Claude Code |
|---|---|
| The instructions file at the project root | read again from disk. An edit you made during the session takes effect now |
| Auto memory, the plan from plan mode | read again from disk |
| The skill descriptions | rebuilt and put back |
| The body of a skill you called | put back: the first 5,000 tokens of each, 25,000 in all, the oldest dropped first |
| The files it read or edited | up to five, the most recently changed. Above 5,000 tokens, the path alone |
| A rule with `paths:`, a `CLAUDE.md` in a subfolder | gone until a matching file is touched again |
| What you said only in the chat | summarized. A detailed instruction from early on may be lost |
| A session-start hook | runs again, and its output is added |

Codex → its docs call it a history compaction and do not list what survives. They do say a session-start hook runs again after it, before the next request to the model.

## Automatic and idle compaction

| | Claude Code | Codex |
|---|---|---|
| When it runs | when the conversation reaches the auto-compact window. On a 1M window that is about 967K tokens by default | at a token limit that defaults to the model's own |
| Make it earlier | `/autocompact 200k`, anything from 100K to 1M | `model_auto_compact_token_limit`. Or `model_post_turn_compact_threshold_percent = 80`, which compacts after an answer once the window is 80% full |
| While you are away | on the one-hour cache of a subscription, a conversation past 200,000 tokens that sits idle for about an hour is compacted before the cache expires. It says `Compacted while idle`. `"idleCompaction": false` stops it | nothing in its docs |

`read`: [what survives compaction](https://code.claude.com/docs/en/context-window.md#what-survives-compaction), [auto-compaction](https://code.claude.com/docs/en/model-config.md#context-window-and-auto-compaction), [`idleCompaction`](https://code.claude.com/docs/en/settings-reference.md#idlecompaction), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [the Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), 2026-11-11.

## In Claude Code

- **A handoff, then a new session** → `/heavy:handoff`, then `/clear`. `/clear refund-path` names the conversation you leave, and `/resume` finds it again.
- **A compaction with your prompt** → `/compact keep the task, the boxes moved, the calls made, what was not verified`.
- **The same prompt every time** → a `# Compact instructions` section in `CLAUDE.md`.
- **One part only** → `/rewind`, pick a message, then `Summarize from here` or `Summarize up to here`. Type what to keep where the row reads `add context (optional)`.
- **After a long break** a `/compact` reads the whole conversation at full price. If you do not need the history, a new session costs less.

## In Codex

- **A handoff, then a new session** → `$heavy:handoff`, then `/clear` or `/new`. `/resume` finds the old chat again.
- **A compaction with your prompt** → `/compact` takes no words in its docs. The prompt is a setting: `compact_prompt = "..."` in `~/.codex/config.toml` replaces the built-in one, so write the whole instruction for the summary there.
- **The gap** → nothing in Codex shapes the summary from the session itself. `compact_prompt` is fixed text. So write the handoff first, every time.

`read`, not run here: Claude Code's [commands](https://code.claude.com/docs/en/commands.md), [reduce token usage](https://code.claude.com/docs/en/costs.md#reduce-token-usage), [rewind and summarize](https://code.claude.com/docs/en/checkpointing.md#rewind-and-summarize) and [prompt caching](https://code.claude.com/docs/en/prompt-caching.md#compacting-the-conversation). Codex's [CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [hooks](https://learn.chatgpt.com/docs/hooks) and [best practices](https://learn.chatgpt.com/guides/best-practices). 2026-11-11.

---

## With the harness

| | Light | Heavy |
|---|---|---|
| The handoff document | none. One sitting needs none | `## Now` in `harness/todo.md`, ten lines at most: where it stands, next, open, mind |
| A new session | starts cold | the session start prints `## Now` and the next open boxes |
| Before a compaction | nothing | in Claude Code, the engine prints what the summary must keep |
| After a compaction | nothing | the session start runs again, in both agents: the core and the briefing are back |

A real `## Now`, as the session that built these pages left it for the next one:

```text
Now:
  - **Where it stands** → the spec, the harness and fourteen guide pages are built, checked and pushed. Light ran for real in Claude Code. Both plugins install in Codex.
  - **Next →** review each page the subagents hand back → open its links → tick its row → commit. Then `kit/README.md`.
  - **Open** → `b.md` is not answered, so every page is built on its pick. The proof's numbers wait on the author.
  - **Mind** → commit with explicit paths while a subagent is writing. A page that is not reviewed is not committed.
```

`run`: `vectoralis status` on this repository, 2026-11-11, one line left out. The steps are the [`handoff` skill](../plugins/heavy/skills/handoff/SKILL.md).

The compaction prompt. The engine prints it at `PreCompact`, for a `/compact` you type and for an automatic or idle one:

```text
Keep these in the summary, in this order:
1. The task in hand and its goal, in the person's own words.
2. The boxes moved this session, and the next open box in harness/todo.md and harness/tracker.md.
3. Every decision made, and every call made without asking.
4. The files changed this session: <the files written since your last message, up to 30>
5. Every failure logged, and everything that was not verified.
6. What the person allowed this turn: <the unlock, tick and promote you typed>.
Drop any tool output that a file already holds. The records in harness/ are read again after the compaction.
```

- The text is `compact_text` in [`plugins/light/engine/briefing.py`](../plugins/light/engine/briefing.py). The two parts in angle brackets are filled in from the session. `run`: its unit test passes here, 2026-11-11. After one write and an `unlock docs`, the output names that file and that grant.
- **This prompt is a Claude Code feature, and a gap in Codex.** `read`: Claude Code uses a `PreCompact` hook's stdout as instructions for the summary, up to 10,000 characters. Codex has the same hook, and its docs say plain text on its stdout is ignored. [Claude Code](https://code.claude.com/docs/en/hooks.md#precompact), [Codex](https://learn.chatgpt.com/docs/hooks)
- Not stated in Claude Code's docs: how the hook's lines combine with the words you type after `/compact`. Say what matters most in your own words too.

## A memory tool beside the handoff

A handoff is what you decided to keep. A memory tool keeps everything that happened, and lets the agent search it later.

| Tool | How it remembers | It costs |
|---|---|---|
| [claude-mem](https://github.com/thedotmack/claude-mem) · Apache-2.0 | hooks record what the agent does, a second model compresses it, and the next session starts with an index it can search | a local worker, a model call for your tool activity, usage analytics on until `npx claude-mem telemetry disable`. The engine is free. `paid` a hosted observer from $30 a month, with a 30-day trial that asks for a payment method |
| [Basic Memory](https://github.com/basicmachines-co/basic-memory) · AGPL-3.0 | notes as plain Markdown that you and the agent both read and edit, served to any agent over MCP | the server's tools in every request. Free locally. Install → `uv tool install basic-memory --prerelease=allow` |

- Install claude-mem → `/plugin marketplace add thedotmack/claude-mem`, then `/plugin install claude-mem`, or `npx claude-mem install`.
- **A memory is what happened. `## Now` is what must happen next.** Neither replaces the other, and only the second is checked by a guard.
- `read` 2026-11-11: the [claude-mem README](https://github.com/thedotmack/claude-mem), [its pricing](https://cmem.ai/pricing), the [Basic Memory README](https://github.com/basicmachines-co/basic-memory). Neither was run here.

## What can go wrong

- **A stale `## Now`.** The briefing prints what the file says, true or not → the `report` skill ends by writing the handoff, and `nudge` warns when work changed and no record moved.
- **A boundary said only in the chat.** "Do not push until I look" can be summarized away → `merge` set to `yours` and the `push` guard, or a deny rule. [Modes](modes.md)
- **One file so large the context refills after every summary.** Claude Code stops compacting after a few tries and shows an error → read the file in parts, or hand it to a subagent.
- **Codex hooks not trusted.** No briefing after `/clear`, none after a compaction → `/hooks`.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `read`: the pages linked in each section, plus [how Claude Code works](https://code.claude.com/docs/en/how-claude-code-works.md#when-context-fills-up), [its troubleshooting page](https://code.claude.com/docs/en/troubleshooting.md#auto-compaction-stops-with-a-thrashing-error) and [its best practices](https://code.claude.com/docs/en/best-practices.md#keep-cost-and-context-down). `run`: `vectoralis status` and the unit tests. No compaction was run in either agent for this page.
