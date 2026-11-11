# Models

Which model, what effort, for which job, in both agents. Read this when a task feels slow, costs more than it should, or comes back wrong at the first try.

**Contents:** Two dials · The job, the model, the effort · In Claude Code · In Codex · With the harness · What can go wrong

---

## Two dials

- **The model** → how capable, how fast, what a token costs.
- **The effort** → how much it thinks before it acts. More effort checks more cases and spends more tokens. Less returns a starting point sooner.
- Start from the default of both, and move one dial at a time.
- Choose at the start of a task. In Claude Code a model switch in the middle of a session reads the whole conversation again with no cache.

---

## The job, the model, the effort

| The job | Claude Code | Effort | Codex | Effort |
|---|---|---|---|---|
| A one-line fix | `sonnet` | `low` | `gpt-6-luna` | `low` |
| A feature in one sitting | `opus`, the default | `medium`, the default | `gpt-6.1-sol` | `medium` |
| A plan for heavy work | `opusplan`, or `fable` for the hardest | `high` | `gpt-6.1-sol` | `high`, set for plan mode alone |
| A re-check by a reviewer | a subagent on the session's model | `high` | a reviewer agent on `gpt-6.1-sol` | `high` |
| A search across a large codebase | the Explore subagent, on `haiku` | its default | an explorer agent on `gpt-6-luna` | `high` |
| A long unattended run | `fable`, at standard speed | `medium`, or `high` | `gpt-6.1-sol` | `xhigh` |

- Each cell is the vendor's own guidance for that kind of work, `read` in the pages linked under each agent. A starting point, not a measurement.
- For measured runs, see [Cost](cost.md): three light tasks on Sonnet 5.5, with their turns, time and price.
- A reviewer on the same model is not a smarter answer. What it adds is that it did not write the code. [Checks](checks.md)

---

## In Claude Code

| You type | The model today | Its docs say |
|---|---|---|
| `/model fable` | Fable 5.2 | the hardest and longest tasks, larger than one sitting |
| `/model opus` | Opus 5.5 | complex reasoning. The default on every Claude plan |
| `/model sonnet` | Sonnet 5.5 | daily coding, at a lower price than Opus |
| `/model haiku` | Haiku 5.5 | simple tasks, and subagents with simple jobs |
| `/model opusplan` | Opus in plan mode, Sonnet after | Opus reasons through the plan, Sonnet writes the code |

- `/model` alone opens the picker: `Enter` saves the choice as your default, `s` keeps it to this session. At launch → `claude --model opus`.
- These are the names on Anthropic's own API. On Bedrock, Agent Platform and Foundry an alias can point at an older model.
- **Effort** → `/effort low`, `medium`, `high`, `xhigh` or `max`. All four models start at `medium`.

| Effort | Use it for | What you trade |
|---|---|---|
| `low` | a rename, a first sketch, quick turns you review one by one | the fastest answer, the least checking |
| `medium` | a feature with a clear scope | the default balance |
| `high` | a bug in code you did not write, a flaky test, edge cases | more cases checked, more tokens |
| `xhigh` | deeper reasoning still | a higher token spend |
| `max` | a hard problem worked through without you | the most. It lasts one session and overthinks ordinary tasks |

- **One hard question in routine work** → put `ultrathink` in that prompt and leave the setting alone.
- **Fast mode** → `/fast`. The same model, up to 2.5 times faster, at a higher price: on Fable 5.2, $16 in and $80 out per million tokens against $8 and $40. A subscription pays it from usage credits. Turn it on at the start, because the first switch pays for the whole conversation again.
- **A different model for a subagent** → `model: haiku` and `effort:` in its file. With neither it runs on your session's model. A subagent file named `Explore` with `model: haiku` makes the wide searches cheaper. `/tasks` shows the model of each one.
- Fable can be billed to usage credits. The picker says so on its row.

`read`: [model configuration](https://code.claude.com/docs/en/model-config.md), [fast mode](https://code.claude.com/docs/en/fast-mode.md), [subagents](https://code.claude.com/docs/en/sub-agents.md#choose-a-model), [best practices](https://code.claude.com/docs/en/best-practices.md#change-the-model-and-effort), [prompt caching](https://code.claude.com/docs/en/prompt-caching.md#switching-models), [the changelog](https://code.claude.com/docs/en/changelog.md), 2026-11-11.

---

## In Codex

| The name | Its docs say |
|---|---|
| `gpt-6-astra` | the most capable, for the hardest work end to end. The slowest of the four |
| `gpt-6.1-sol` | near Astra at a lower cost, for repeated, long-running work. Where its docs start most tasks |
| `gpt-6.1-terra` | fast, for writing, images and screens, and scoped fixes. Needs Codex CLI 0.159.0 or later |
| `gpt-6-luna` | the most efficient, for focused, repeatable, high-volume tasks |

- **Choose** → `/model` in a session, `codex -m gpt-6.1-sol` at launch, `model = "gpt-6.1-sol"` in `~/.codex/config.toml`.
- **Effort** → `model_reasoning_effort`, or `/model --reasoning=high`. It takes `low`, `medium`, `high`, `xhigh`, `max` or `ultra`, as far as the model supports them. Its docs start Sol at its default, Luna at `high`, Astra at `low`.
- `max` gives one task more time to reason. `ultra` splits the work across subagents. Its docs: most tasks need neither.
- `plan_mode_reasoning_effort` sets the effort for plan mode alone. `review_model` sets the model that `/review` uses.
- **Fast mode** → `/fast`. On a subscription it spends the included limits at 2.5 times the standard rate.
- **A different model for a subagent** → `model` and `model_reasoning_effort` in its `.codex/agents/*.toml`, or `default_subagent_model` under `[agents]`. With neither it inherits the parent's.

`read`: [models](https://learn.chatgpt.com/docs/models), [model selection](https://learn.chatgpt.com/docs/model-selection), [speed](https://learn.chatgpt.com/docs/agent-configuration/speed), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [the CLI commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [the configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), 2026-11-11.

---

## With the harness

| | Light | Heavy |
|---|---|---|
| The model | never set. A guard is a script and calls no model | never set. Every skill runs on your session's model |
| The subagents | none | `reviewer` and `builder` name no model and no effort, so they run on your session's |
| In Codex | the same | the two subagents are a gap. Write the reviewer in `.codex/agents/` with its own `model` and `model_reasoning_effort`. [Codex](codex.md) |

- To run the reviewer on another model or effort in Claude Code, say so in the task. The agent can pass both for that one call.

## What can go wrong

- **A level carried over from an older model.** Efforts are calibrated per model. Claude Code's docs put Opus 5.5 at `medium` level with Opus 5 at `high`, and Codex's say efforts do not map between generations → after a model change, start from the default again.
- **`max` as a habit.** It overthinks ordinary work, and you pay for it → `high` first, `ultrathink` for one prompt.
- **Fast mode switched on halfway.** The first switch pays the full input price for the whole conversation → at the start, or not at all.
- **A subagent on the big model without you knowing.** It inherits the session's → `model:` in its file, `/tasks` to check.
- **A model name that went stale in a file.** `gpt-5.5` left Codex for ChatGPT sign-ins on 14 October 2026, and fast mode for Opus 4.8 ends on 30 November 2026 → an alias where the agent has one, and `/model` for today's list. This page names the models of its date.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. Every model name, level and price on this page is `read` that day in the docs linked under each agent. Nothing here was run: no model was called for this page.
