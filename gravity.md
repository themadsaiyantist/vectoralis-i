# Gravity

The authority on what Gravity is and what it contains: the practical guide to running coding agents on light and heavy work, and the harness that installs each. Read it before writing any part of Gravity. Started 2026-11-11 by the author: "the best guide about practical light and heavy workload and workflow with clear steps, skills, hooks".

**Contents:** What it is · Who it is for · The two workflows · When to switch · Every piece, the same four things · The harness · What it is not · Where it comes from · Open questions

---

## What it is

- **A guide:** how to run Claude Code, Codex and other coding agents on real work, light and heavy, in clear steps.
- **A harness:** the same guide as files you install, a `light` profile and a `heavy` profile, so the agent works the guide's way.
- **Open source**, free, human readable.

## Who it is for

- Anyone who already uses a coding agent and wants it to work reliably, from a one-file fix to a project that runs for weeks.
- Students of the Coding Agents course, who build a harness there and keep this one as the reference.

## The two workflows

**Light** → a bug fix, a small feature, one sitting.

- Steps: describe → plan in one line → edit → run the tests → commit.
- Harness: a short `CLAUDE.md` or `AGENTS.md`, and two or three hooks:
  - no secrets written or printed
  - the formatter
  - the tests run before the agent says "done"
- Nothing else: no trackers, no logs, no subagents.

**Heavy** → multi-day work, many files, anything other people rely on.

- Steps: session briefing → plan, every question asked up front → build → check → re-check → record → report.
- Harness, on top of light:
  - a tracker, ✅ and ⬜ only
  - your to-dos and the agent's, kept apart
  - a failure log → fix → hook loop
  - lessons, in your own words
  - decisions and exceptions, dated, with the reason
  - subagents and worktrees for parallel work
  - pull requests watched to green
  - locks on finished work

## When to switch

Move from light to heavy the moment any of these is true:

- the work will not fit in one session
- someone else will read, review or depend on it
- it is hard to undo: deleting, money, law, publishing
- the same mistake has happened twice
- more than one agent works at once

## Every piece, the same four things

Each part of the harness is taught the same way:

1. **When to add it** → the signal that it now pays for itself
2. **The steps** → exactly what to do, in order
3. **The file** → what it creates, and where it lives
4. **The guard** → the hook or skill that enforces it

And each states what it **costs**, in tokens and in attention, so a reader adds only what earns its place.

## The harness

- **Core:** plain Markdown files and a small CLI, readable by any agent and any person.
- **Adapters:**
  - Claude Code first → a plugin with skills, hooks and commands
  - Codex second → `AGENTS.md` and `config.toml`
- **Loaded when needed:** a small core always loaded, everything else as skills the task calls in.
- **MCP only for outside systems** that need it, GitHub or an issue tracker, because every server costs context.
- **On top of the agents' own features, never in place of them:** to-dos, plan mode and memory are theirs. Gravity adds memory of failures, enforcement, and records that stay true.
- **Smart, where the bootcamp's harness was manual:**
  - a staleness check: trackers and rules read against git, and anything out of date flagged
  - every hook shipped with its own test payloads
  - one dashboard page built from the files: open work, failures, what is next
  - after the same failure twice, a proposed guard a person approves

## What it is not

- Not a skills collection. Those give an agent skills, Gravity gives it a working system.
- Not a replacement for the agents' built-in features.
- Not theory. Every recipe is run before it is written, and shows its real output.

## Where it comes from

- **The bootcamp's harness**, `/home/goku/AML_BOOTCAMP/`, weeks of heavy work: `workflow/rules.md`, the trackers in `final_to_do/`, `workflow/failures.md`, `workflow/learned.md`, `docs/flags.md`, `docs/judgments.md` and the hooks in `tools/hooks/`. What worked is generalized. What hurt is fixed:
  - too much loaded every session
  - records that drifted behind the work
  - hooks that misfired
  - state scattered over many files
- **The Coding Agents course**, `/home/goku/coding-agents/`, whose reference harness is built lesson by lesson, shipped as a plugin and mapped to Codex.

## Open questions

- The release date.
- The licence.
- The GitHub account it lives on.
- How deep the Codex adapter goes in the first release.
