# Vectoralis I

The authority on what Vectoralis I is and what it contains: the practical guide to running coding agents on light and heavy work, the harness that installs each, the kit of skills, hooks and MCP servers for each situation, three career roadmaps, five topics beyond them, the communities worth following and the proof. Read it before writing any part of it. `spec.md` says how each part is built. Started 2026-11-11 by the author: "the best guide about practical light and heavy workload and workflow with clear steps, skills, hooks".

**Contents:** The series · What it is · The absolute rules · Who it is for · The two workflows · When to switch · Inside the workflow · Every piece, the same four things · The harness · The guide · The kit · The roadmaps · The five topics · The communities · The proof · What it is not · Where it comes from · The release · Open questions

---

## The series

Named 2026-11-11 by the author. Vectoralis I is the first of three.

## What it is

- **A guide:** how to run Claude Code, Codex and other coding agents on real work, light and heavy, in clear steps.
- **A harness:** the same guide as files you install, a `light` profile and a `heavy` profile, so the agent works the guide's way.
- **A kit:** the most important skills, hooks and MCP servers for each situation.
- **Three career roadmaps:** AI engineer, agentic software engineer and AI platform engineer.
- **Five topics** beyond the roadmaps, the hottest ones.
- **The communities:** the exact subreddits and the other places worth following, topic by topic.
- **The proof:** what this way of working has already built.
- **Open source**, free, human readable.
- **On GitHub** at `themadsaiyantist/vectoralis-i`, private until the author says otherwise.
- **Markdown in the repository**, read on GitHub, with no site, the author's word of 2026-11-11. The only HTML is the dashboard, built on the reader's own machine.

## The absolute rules

Ruled 2026-11-11 by the author. They bind every page, every file and every decision here.

- **The absolute rules:** "human readable, modern, hot topics, clean, effective. those are the absolute rules"
- **The utmost priority:** "the utmost prioruty is organization,quality,efficiency,human readable,modern and hot"
- **The tone:** "be insipirational"
- **No dates:** "we will do everything now ASAP, no dates no nothing". Everything is built now, and released the moment it is done.

## Who it is for

- Anyone who already uses a coding agent and wants it to work reliably, from a one-file fix to a project that runs for weeks.
- **One person or a team**, the author's word of 2026-11-11: "ofc consider single user vs team organization".
- Students of the Coding Agents course, who build a harness there and keep this one as the reference.
- Anyone heading into one of the three careers of the roadmaps, who wants the steps, the milestones and the projects.

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

## Inside the workflow

Added 2026-11-11 by the author. Each one is shown in action, on both agents: "also consider the workfow on claude code/gpt ofc".

- **Plan mode and the permission modes** → "plan mode in action, bypaass permissions yk, thats the worklfow thing".
- **Which model, what effort** → "which model to use when etc, what effort, yk".
- **Handing a session over** → "hand off documents vs auto compact vs compact with prompt given by the claude code itself right before auto compact or before it, yk, hidden but smart anf very effective things".
- **Where every file goes** → "perfect folder structure, referencing, local level global level etc of the claude md files etc, all taht yk".

## Every piece, the same four things

Each part of the harness is taught the same way:

1. **When to add it** → the signal that it now pays for itself
2. **The steps** → exactly what to do, in order
3. **The file** → what it creates, and where it lives
4. **The guard** → the hook or skill that enforces it

And each states what it **costs**, in tokens and in attention, so a reader adds only what earns its place.

## The harness

Settled 2026-11-11 by the author's answers to the question round.

- **Core:** plain Markdown files and a small CLI, readable by any agent and any person.
- **Two plugins from one marketplace** → `light` and `heavy`. Heavy brings light with it, so the switch is one install, and light loads nothing of heavy.
- **Both agents, all the way** → Claude Code and Codex get the same skills, guards and records, each through its own plugins. One table lists every gap that is left.
- **Python 3, standard library only** → nothing to install.
- **One folder in the reader's project, `harness/`** → light keeps one file there, heavy adds the rest.

```text
harness/
├── settings.json   the profile, the test command, which guards are on
├── rules.md        how the work runs here, the small core that is always loaded
├── tracker.md      the build state, ✅ and ⬜ only
├── todo.md         two lists: yours, the agent's
├── failures.md     the failure log
├── lessons.md      what you taught after a failure, in your words
├── decisions.md    decisions and exceptions, dated, with the reason
├── locks.md        finished work nothing may write to
└── guards/         this project's own guards, each with its test payloads
```

- **The tracker** → one row per unit of work, one column per stage, the stages named by the project. The default is three: built, checked, and yours, the pass only the person's word ticks.
- **A guard blocks only what a machine can be sure of** → a secret, a write to a locked file, a destructive command, "done" with failing tests. Each guard ships with payloads that prove one block and one pass. A new or proposed guard only warns until the person promotes it.
- **A hard cap on what is always loaded** → light at most 300 tokens, heavy at most 2,000, the session briefing included. Everything else loads when the task calls it.
- **What the agent may do alone** → it commits, and pushes only to a branch it opened. It watches its pull request to green and fixes what breaks. It never touches the default branch and never merges. One setting hands it the merge.
- **Three things stay the person's alone** → ticking a "yours" box, writing a lesson, opening a lock. A guard enforces all three.
- **The person's instructions file is theirs** → Vectoralis never edits a `CLAUDE.md` or an `AGENTS.md`. It offers a starter only where none exists.
- **One harness for one person and for a team.**
- **MCP only for outside systems** that need it, because every server costs context. No MCP server ships with Vectoralis, and GitHub goes through the `gh` CLI.
- **On top of the agents' own features, never in place of them:** to-dos, plan mode and memory are theirs. Vectoralis I adds memory of failures, enforcement, and records that stay true.
- **Nothing leaves the reader's machine** → no telemetry, no account, no network call.
- **Linux, macOS and WSL.**
- **Modern, never preview** → a feature either agent still labels experimental waits.
- **Efficient to build and to check**, the author's word: "dont run everything always, search the internet not this machine for everything, be efficicent".
- **Smart, where the harness it comes from was manual:**
  - a staleness check: trackers and rules read against git, and anything out of date flagged
  - every hook shipped with its own test payloads
  - one dashboard page built from the files: open work, failures, what is next
  - after the same failure twice, a proposed guard a person approves
  - the prompt for a compaction written by the harness itself, right before the agent compacts

## The guide

Settled 2026-11-11 by the author's answers, each list open to "improve and refine if needed".

- **Markdown pages in `guide/`.** `spec.md` holds the list.
- **Every page that adds a piece keeps the four things and its cost.** Cost is stated plainly: tokens from a real measurement, attention as what the person does and how often.
- **Twelve topics, each owned by a page** → harness engineering · context · skills and plugins · hooks as guards · parallel agents · unattended runs · permissions and safety · verification · a harness that learns · cost · spec and plan first · MCP.
- **The worked examples** → light is run on `runlog`, the course's public starter. Heavy is shown two ways: this repository's own records, and free public samples, each linked with what it does well and how to do it better. The author's word: "seek sources online for free and legal to share".
- **No version is pinned** → every page closes with the agent versions, the model and the date it was verified on.
- **The writing** → plain words that make a reader want to build, bullets and arrows, no em or en dash, one line per paragraph, `goku` and `vegeta`.

## The kit

Added 2026-11-11 by the author: "also write about the most important skills and hooks and mcps depending on the situation such as yk coding, reasoning, desgining, animation, just images, videos, voice,... yk fully all out but fully organized and pleasing to multiple types of people".

- **By situation** → coding, reasoning, designing, animation, images, video, voice, and the rest of tech work.
- **Mainly tech**, the author's words: "mainly in tech obv" and "no biology,chem,math that are purely off the tech".
- **All out, and fully organized**, so it pleases more than one kind of reader.
- **Heavy examples need no run here**, the author's word: "if its things about some heavy workload etc then obv we dont have to do it here you can find samples free online and reference them, in clean format, and how to do it better".

Settled 2026-11-11 by the author's answers.

- **Nineteen situations in four groups:**
  - Build → coding · frontend and UI · backend, databases and APIs · mobile · games and 3D
  - Think → reasoning · research · data and ML
  - Make → design · images · animation · video · voice and audio · docs and writing
  - Ship and run → testing and browsers · review and security · DevOps and cloud · team tools · agents building agents
- **Curated** → one pick each for skills, guards and MCP servers, then at most four more worth knowing, one line each. Every entry says what it does, when it earns its place, what it costs and how to install it. The page closes with a free sample to study and how to do it better.
- **Tried before it is listed** → every pick carries the date it was tried. Anything only referenced says so.
- **Free and open first** → a paid service appears only where nothing free does the job, and it is marked paid. The author's word: "mostly free proirity".
- **Nothing third-party ships in or through Vectoralis** → a kit page gives the install line, the cost and the risk, and the reader runs it.

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

Settled 2026-11-11 by the author's answers.

- **The three** → AI engineer, agentic software engineer, AI platform engineer. Together they close one loop: build with agents, build AI into the product, run it in production.
- **Each page** → the job, the road in stages, a milestone and a project for every stage, the future.
- **No hours and no weeks** → a stage ends when its milestone is met.
- **Grounded** → each is checked against real job postings of the month it is written, and says which month.

## The five topics

Added 2026-11-11 by the author: "also per topic things besides the 3 career paths have 5 hottest topics outside the any milestones of those 3 career paths".

- **Five topics, one page each**, none of them a milestone of the three careers.

## The communities

Added 2026-11-11 by the author: "also mention the msot important social medias about this such as reddit and what exact subreddits for what topic, and otehr social medias per topics if needed".

- **Reddit first** → the exact subreddits, topic by topic.
- **Other social media** → per topic, where one matters.

## The proof

Added 2026-11-11 by the author: "also mention about the efficincy etc about those smart things and orchestration and workflow that they helped grreatly in the creation of the bootcamp and the entire thing e2e and the additonal products with it", "where it matters, as in direct proof that these tips that you give in this repo actualyl are beneficial and useful and worthy" and "dont just read the pure hard numbers, give motivation boost too additional, dont say its motivational tho obv".

- **Where it matters** → beside the piece each fact proves, and on one page of its own.
- **Direct proof** → what this way of working built: the bootcamp end to end, its platform, the free course and the products around it.
- **More than numbers** → it shows a reader what one person and an agent can build, and never calls itself motivation.
- It replaces the answer of the same day that the guide says nothing about the bootcamp's harness.

## What it is not

- Not a skills dump. The kit names the few that matter in each situation, and Vectoralis I stays a working system, reworded 2026-11-11 with the kit.
- Not a replacement for the agents' built-in features.
- Not theory. Every light recipe and every guard is run before it is written, and shows its real output. A heavy example may be a free public sample, linked in a clean format with how to do it better, the author's word of 2026-11-11.

## Where it comes from

- **The harness behind the bootcamp**, weeks of heavy work. What worked is generalized. What hurt is fixed:
  - too much loaded every session
  - records that drifted behind the work
  - hooks that misfired
  - state scattered over many files
- **Coding Agents**, the free course, whose reference harness is built lesson by lesson, shipped as a plugin and mapped to Codex.
- **In the README** → one short section says so, with one link to the course. Nothing paid is named.

## The release

- **Private until the author decides**, the author's word of 2026-11-11: "make the repo private for now, i will decide when public dont worry".
- **One release, the whole outline**, built in this order → light → heavy → the smart pieces → Codex → the guide → the kit → the roadmaps → the five topics → the communities.
- **MIT for everything.**
- **Issues open, pull requests welcome**, each with the run that proves it. Ten lines of rules in `CONTRIBUTING.md`.
- **It goes public with its full history.**

## Open questions

Asked in `b.md` at the root while the build runs, and folded in here once answered.

- Which five topics.
- Whether a single person is ever named among the communities.
- The price cap on a paid resource.
- How much a team adds.
- Whether ChatGPT itself is covered beside Codex.
- The categories of the stars.
- The lines of the proof.
