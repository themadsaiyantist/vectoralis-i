# Vectoralis I

The authority on what Vectoralis I is and what it contains: the practical guide to running coding agents on light and heavy work, and the harness that installs each, with the kit of skills, hooks and MCP servers for each situation and three career roadmaps, both added the same day. Read it before writing any part of it. Started 2026-11-11 by the author: "the best guide about practical light and heavy workload and workflow with clear steps, skills, hooks".

**Contents:** The series · What it is · The absolute rules · Who it is for · The two workflows · When to switch · Every piece, the same four things · The harness · The kit · The roadmaps · What it is not · Where it comes from · Open questions

---

## The series

Named 2026-11-11 by the author.

- **Vectoralis I** → this repository, the guide and harness for coding agents.

---

## What it is

- **A guide:** how to run Claude Code, Codex and other coding agents on real work, light and heavy, in clear steps.
- **A harness:** the same guide as files you install, a `light` profile and a `heavy` profile, so the agent works the guide's way.
- **A kit:** the most important skills, hooks and MCP servers for each situation.
- **Three career roadmaps:** AI Engineering and two more.
- **Open source**, free, human readable.
- **On GitHub** at `themadsaiyantist/vectoralis-i`, private until the release, the author's word of 2026-11-11.
- **Markdown in the repository**, read on GitHub, with no site, the author's word of 2026-11-11. The only HTML is the dashboard, built on the reader's own machine.

## The absolute rules

Ruled 2026-11-11 by the author. They bind every page, every file and every decision here.

- **The absolute rules:** "human readable, modern, hot topics, clean, effective. those are the absolute rules"
- **The utmost priority:** "the utmost prioruty is organization,quality,efficiency,human readable,modern and hot"
- **No dates:** "we will do everything now ASAP, no dates no nothing". Everything is built now, and released the moment it is done.

## Who it is for

- Anyone who already uses a coding agent and wants it to work reliably, from a one-file fix to a project that runs for weeks.
- Students of the Coding Agents course, who build a harness there and keep this one as the reference.
- Anyone heading into AI Engineering, or one of the two other careers of the roadmaps, who wants the steps, the milestones and the projects.

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
- **On top of the agents' own features, never in place of them:** to-dos, plan mode and memory are theirs. Vectoralis I adds memory of failures, enforcement, and records that stay true.
- **Smart, where the bootcamp's harness was manual:**
  - a staleness check: trackers and rules read against git, and anything out of date flagged
  - every hook shipped with its own test payloads
  - one dashboard page built from the files: open work, failures, what is next
  - after the same failure twice, a proposed guard a person approves

## The kit

Added 2026-11-11 by the author: "also write about the most important skills and hooks and mcps depending on the situation such as yk coding, reasoning, desgining, animation, just images, videos, voice,... yk fully all out but fully organized and pleasing to multiple types of people".

- **By situation** → coding, reasoning, designing, animation, images, video, voice, and the rest of tech work.
- **Mainly tech**, the author's words: "mainly in tech obv" and "no biology,chem,math that are purely off the tech".
- **All out, and fully organized**, so it pleases more than one kind of reader.
- **Heavy examples need no run here**, the author's word: "if its things about some heavy workload etc then obv we dont have to do it here you can find samples free online and reference them, in clean format, and how to do it better".

## The roadmaps

Added 2026-11-11 by the author: "and also include in it the perfect roadmap for 3 careers, AI Engineering one, 2 you choose, not ML researcher or any of that heavy thing" and "full clean steps, milestones, projects,future,cleanest possible".

- **Three careers** → AI Engineering, and two chosen by Claude. Nothing research-heavy.
- **Each one holds** → full clean steps, milestones, projects and the future, as clean as it can be.

Widened 2026-11-11 by the author: "add where needed additional free/paid resources that go deeper into a topic/milestone whatever, and about the project say the best resources direct url links free that can give ideas and ispirations to the users (perhaps great github repos of great difficutly), rank things in tables if needed, 1-10 stars in each category and also for any free resource if theres a paid thing thats greeatly better then state it as in () and the price (not too heavy priced tho ofc). also for each stage if needed there can be multiple resources free/paid and in () to be said what they excel at and what are they better in compared to the others on that list), yk cool arrows and thigns to shwocase".

- **Deeper resources** → free or paid, wherever a topic or a milestone needs more.
- **Project inspiration** → the best free direct links that give ideas, great GitHub repositories among them, the hard ones included.
- **Ranked in tables** where it helps → 1 to 10 stars in each category.
- **A paid option beside a free one** → only when it is greatly better, in brackets with its price, and never a heavy price.
- **Several resources per stage** where needed → each with what it excels at, and what it does better than the others on the list, in brackets.
- **Arrows and visuals** → the road is shown, not only listed.

## What it is not

- Not a skills dump. The kit names the few that matter in each situation, and Vectoralis I stays a working system, reworded 2026-11-11 with the kit.
- Not a replacement for the agents' built-in features.
- Not theory. Every light recipe and every guard is run before it is written, and shows its real output. A heavy example may be a free public sample, linked in a clean format with how to do it better, the author's word of 2026-11-11.

## Where it comes from

- **The bootcamp's harness**, `/home/goku/AML_BOOTCAMP/`, weeks of heavy work: `workflow/rules.md`, the trackers in `final_to_do/`, `workflow/failures.md`, `workflow/learned.md`, `docs/flags.md`, `docs/judgments.md` and the hooks in `tools/hooks/`. What worked is generalized. What hurt is fixed:
  - too much loaded every session
  - records that drifted behind the work
  - hooks that misfired
  - state scattered over many files
- **The Coding Agents course**, `/home/goku/coding-agents/`, whose reference harness is built lesson by lesson, shipped as a plugin and mapped to Codex.

## Open questions

Asked in `a.md` at the root, the question round of 2026-11-11, and folded in here once answered.

- The licence.
- How deep the Codex adapter goes in the first release.
- When it goes public, and what the public text says about the series.
- How a profile installs, where the records live and how the guards behave.
- The pages of the guide, the situations of the kit and the two careers Claude chooses.
