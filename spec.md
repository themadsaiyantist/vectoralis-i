# The Spec

How Vectoralis I is built. `vectoralis-i.md` says what it contains, this file says how. Read the part you are about to build before you build it, and change this file first when the design changes.

**Contents:** 1 The rules it is built under · 2 The repository · 3 The two plugins · 4 The engine · 5 The guards · 6 The records · 7 The CLI · 8 The skills and the subagents · 9 The smart pieces · 10 Budgets · 11 Solo and team · 12 Codex · 13 The guide · 14 The kit · 15 The roadmaps · 16 The five topics · 17 The communities · 18 The proof · 19 Tests and CI · 20 The release · 21 The build order · 22 Still to prove

---

## 1. The rules it is built under

The absolute rules are in `vectoralis-i.md`. This is what each one means when something is built.

| The rule | What it means here |
|---|---|
| Human readable | plain words, one fact per bullet, a sequence written with →, a table when things are compared |
| Modern | only what both agents ship as stable today, and every page closes with the versions it was verified on |
| Hot topics | the twelve topics of the guide and the five topics beyond the roadmaps each own a page |
| Clean | one fact has one home, and a page that runs past two screens is split |
| Effective | every page ends in something the reader can do now |
| Organized | every folder opens on a `README.md` that lists what is in it |
| Inspirational | show what was built and how, and let that do the work. Never say it is motivation |

**Every claim carries its evidence.** Three marks, and nothing is stated without one:

| Mark | What it means |
|---|---|
| `run` | it ran here, the output is shown, with the versions and the date |
| `read` | it is in the vendor's own docs, linked, with the date it was read |
| `referenced` | it is a public sample, linked, not run here |

Run what cannot be read. Read the rest. That is how the build stays fast and still honest.

---

## 2. The repository

```text
vectoralis-i/
├── README.md               the first screen: what it is, the two workflows, install
├── LICENSE                 MIT
├── CONTRIBUTING.md         ten lines
├── CLAUDE.md               how the work runs in this repository
├── vectoralis-i.md         what it contains
├── spec.md                 how it is built
├── .claude-plugin/
│   └── marketplace.json    the marketplace both agents read
├── plugins/
│   ├── light/              the engine, the CLI and the three light guards
│   │   ├── .claude-plugin/plugin.json
│   │   ├── hooks/hooks.json      every event the engine answers
│   │   ├── hooks/run.py          one entry point: run.py <event>
│   │   ├── engine/               the Python package
│   │   ├── bin/vectoralis        the CLI
│   │   ├── templates/            the starter files init writes
│   │   └── skills/setup/SKILL.md
│   └── heavy/              the skills and subagents that drive the records
│       ├── .claude-plugin/plugin.json    "dependencies": ["light"]
│       ├── skills/               brief, plan, check, record, report, failure, handoff, agents, pr, setup
│       └── agents/               reviewer, builder
├── harness/                this repository's own records, the heavy worked example
├── guide/                  how to run an agent on light and heavy work
├── kit/                    what to install, by situation
├── roadmaps/               three careers
├── topics/                 five topics beyond the roadmaps
├── community/              where people talk, topic by topic
├── tests/                  unit tests and the guard payload runner
├── tools/                  repository checks: the writing rules, the links
└── .github/workflows/ci.yml
```

- **Heavy carries no code.** The engine lives once, in light, and reads the profile from `harness/settings.json`. A heavy guard in a light project exits before it does anything.
- **Every folder a reader opens has a `README.md`**, because GitHub shows it under the file list.
- **Scratch stays out.** Notes, downloads and test projects live outside the repository.

---

## 3. The two plugins

**The marketplace**, `.claude-plugin/marketplace.json`:

```json
{
  "name": "vectoralis",
  "owner": { "name": "themadsaiyantist" },
  "description": "A light and a heavy harness for coding agents.",
  "plugins": [
    { "name": "light", "source": "./plugins/light", "description": "Three guards and one settings file." },
    { "name": "heavy", "source": "./plugins/heavy", "description": "Records that stay true, on top of light." }
  ]
}
```

**What each plugin carries:**

| | `light` | `heavy` |
|---|---|---|
| Hooks | all of them, gated by the profile | none |
| Engine and CLI | yes | no, it uses light's |
| Skills | `setup` | `setup`, `brief`, `plan`, `check`, `record`, `report`, `failure`, `handoff`, `agents`, `pr` |
| Subagents | none | `reviewer`, `builder` |
| Depends on | nothing | `light` |

**Install, in Claude Code** (`read`, plugin docs, 2026-11-11):

```text
claude plugin marketplace add themadsaiyantist/vectoralis-i
claude plugin install light@vectoralis --scope project
```

- Then, in a session → `/light:setup`.
- The switch → `claude plugin install heavy@vectoralis --scope project` → `/heavy:setup`. Installing heavy installs and enables light at the same scope.
- Project scope writes `enabledPlugins` to `.claude/settings.json`, which is committed. Each teammate runs the install once in their clone.
- An update reaches users when `version` in `plugin.json` moves. Both plugins carry the same version.

---

## 4. The engine

One Python package, standard library only, written for Python 3.9 and later. One entry point: `python3 hooks/run.py <event>`. It reads one JSON payload on stdin and answers in one of four ways.

| The answer | How | When |
|---|---|---|
| Pass | exit 0, silent | nothing to say |
| Warn | exit 0, a fact in `hookSpecificOutput.additionalContext` | the guard is not sure, or it is new |
| Block | exit 2, the reason on stderr | a machine can be sure |
| Step aside | exit 1, one line on stderr | the guard itself broke. It never blocks on its own failure |

**A block always says three things:** what was stopped → the rule and the file it lives in → what to do instead.

**The events:**

| Engine event | Claude Code | Codex | Light does | Heavy adds |
|---|---|---|---|---|
| `session` | `SessionStart` | `SessionStart` | nothing | prints the core and the briefing |
| `prompt` | `UserPromptSubmit` | `UserPromptSubmit` | nothing | takes the turn's baseline, reads the grants |
| `write` | `PreToolUse` on Write, Edit, MultiEdit, NotebookEdit | `PreToolUse` on `apply_patch` | `secrets` | `locks`, `yours`, `records` |
| `shell` | `PreToolUse` on Bash | `PreToolUse` on the shell | `secrets` | `destructive`, `locks`, `push` |
| `wrote` | `PostToolUse` on the write tools | `PostToolUse` | `format` | notes the file as touched |
| `stop` | `Stop` | `Stop` | `tests` | `sweep`, `nudge` |
| `compact` | `PreCompact` | `PreCompact` | nothing | prints what the summary must keep |

**The modules of `engine/`:**

| Module | What it holds |
|---|---|
| `payload.py` | reads the payload and turns either agent's shape into one: the event, the tool, the writes as (path, new text), the command, the prompt, whether a subagent made the call |
| `project.py` | finds the project root, loads `harness/settings.json`, answers "which profile" |
| `state.py` | the per-session state: the baseline, the files touched, the grants, what was already said |
| `grants.py` | reads the person's message for `unlock`, `tick`, `lesson:` and `promote` |
| `records.py` | parses the tracker, the to-do list, the failure log and the locks |
| `guards/` | one file per guard, each beside its payloads |
| `rules.py` | loads the project's own guards from `harness/guards/` |
| `checks.py` | the staleness check and the budget |
| `briefing.py` | the session briefing and the compaction prompt |
| `dashboard.py` | the one HTML page |
| `cli.py` | the commands of section 7 |

**The state** is one small JSON file per session. It lives in the session's scratchpad when the payload names one, and in the system's temp folder otherwise. The engine writes one file in the project and no other: `harness/.checked.json`, section 9.

**A grant** is something only the person can give, by typing it:

| The person types | What it opens | For how long |
|---|---|---|
| `unlock <path>` | a write to that locked path | until their next message |
| `tick <unit>` | a "yours" box of that unit | until their next message |
| `lesson: <text>` | one entry in `harness/lessons.md` | until their next message |
| `promote <guard>` | that guard goes from warn to block | until their next message |

- A word of refusal before it cancels it: "do not unlock", "never tick".
- A message that is not the person's is never read for grants: a background task's notice, a message from another session.

**Speed.** Every event but `stop` answers in under 200 ms. The turn's baseline is skipped when more than 500 files are dirty, and the sweep says so.

---

## 5. The guards

| Guard | Profile | Event | Blocks | Warns |
|---|---|---|---|---|
| `secrets` | light | write, shell | a key in a known format written to a file, a command that prints a secrets file | a quoted value that only looks like a key |
| `format` | light | wrote | never | says when the formatter rewrote the file |
| `tests` | light | stop | "done" while the test command fails | the suite ran out of time |
| `destructive` | heavy | shell | `git reset --hard`, `git clean -f`, `git push --force`, `rm -rf` on the root, the home or `.` | `rm -r`, `git checkout --`, `git branch -D` |
| `locks` | heavy | write, shell | a write to a locked path with no grant | |
| `yours` | heavy | write | a "yours" box ticked, a lesson written, a lock opened, a guard promoted or switched off, with no grant | |
| `records` | heavy | write | a subagent writing a record | |
| `push` | heavy | shell | a push to the default branch or a merge, while `merge` is `yours` | |
| `sweep` | heavy | stop | a file changed around the write guards that breaks `secrets` or `locks` | |
| `nudge` | heavy | stop | | work changed and no record moved. Said once a turn |

- **`tests` runs only when something changed** since the last green run. The fingerprint is the commit plus the diff.
- **`stop` sends the agent back at most once a turn.**
- **Every guard can be set to `block`, `warn` or `off`** in `harness/settings.json`. Switching one off, and promoting one, are the person's.
- **A path can be excused** from one guard in `settings.json`, with its reason in `harness/decisions.md`.

**Every built-in guard ships with its payloads**, in `engine/guards/payloads/<guard>.json`: at least one that must block or warn, at least one that must pass. `vectoralis guards` runs them all.

**A project's own guard** is one file, `harness/guards/<id>.json`. It is data, so approving one means reading ten lines:

```json
{
  "id": "no-debug-print",
  "why": "failures.md, class debug-print, twice",
  "on": "write",
  "path": "src/**/*.py",
  "pattern": "^\\s*print\\(",
  "mode": "warn",
  "message": "A debug print is about to ship. Remove it or use the logger.",
  "payloads": [
    { "name": "catches a print", "path": "src/a.py", "text": "print(x)", "expect": "hit" },
    { "name": "passes the logger", "path": "src/a.py", "text": "log.info(x)", "expect": "pass" }
  ]
}
```

- `on` is `write` or `shell`. On `shell` the pattern is read against the command.
- **A guard without its proof does not run.** It needs one `hit` and one `pass` that behave, or `vectoralis check` reports it and the engine skips it.
- **A new guard starts at `warn`.** Only a grant, or the person's own edit, makes it `block`.

---

## 6. The records

All in `harness/`. Light keeps `settings.json` alone. Each record opens with what it is and a Contents line.

**`settings.json`**

```json
{
  "profile": "heavy",
  "test": "python3 -m unittest discover -s tests -q",
  "test_timeout": 120,
  "format": "",
  "guards": { "secrets": "block", "tests": "block" },
  "skip": { "format": ["legacy/**"] },
  "merge": "yours",
  "team": false
}
```

- An empty `test` or `format` switches that guard off, and `init` says so.
- A guard that is not listed runs in its default mode.

**`rules.md`** → how the work runs here. It is the core that is always loaded, so it stays under 60 lines: the seven steps, where each record lives, the three things that are the person's, when to ask.

**`tracker.md`** → the build state.

```markdown
## Checkout

| Unit | Built | Checked | Yours |
|---|---|---|---|
| `src/cart.py` cart total | ✅ | ✅ | ✅ |
| `src/refund.py` refund webhook | ✅ | ✅ | ⬜ |
```

- ✅ is done and checked, ⬜ is not done, a blank cell does not apply. Nothing else goes in a cell.
- The stages are the project's. The last column is always the person's, whatever it is called.
- A unit that opens with a path in backticks is bound to that path. The staleness check reads it.
- A tick refers to the file as it was when the box was ticked. When the file changes, the row is stale until it is checked again.

**`todo.md`** → `## Now`, then `## Yours`, then `## The agent's`. One line per step, ✅ or ⬜, arrows for a sequence. `## Now` is the handoff: where things stand and what is next, in ten lines at most.

**`failures.md`** → one entry per failure, newest first.

```markdown
### ⬜ 2026-11-11 · agent · What failed, in a few words

**Class.** `stale-record`

**What failed.** The facts, in one or two sentences.

**Cause.** Why it happened, not what happened.

**Fix.** ⬜ the instance · ⬜ the cause · ⬜ the guard
```

- Facts only. The person's failures are written exactly like the agent's.
- The class is a short slug. The second entry of one class asks for a guard.
- An entry closes when its three boxes are ✅.

**`lessons.md`** → what the person taught after a failure, in their words. Written only on `lesson:`.

**`decisions.md`** → two lists: decisions, and exceptions. Each one dated, with the reason. An exception names the rule it bends and its exact scope.

**`locks.md`** → finished work nothing may write to.

```markdown
- `src/payments/**` → locked 2026-11-11, the checkout is live
```

**`guards/`** → the project's own guards, section 5.

---

## 7. The CLI

`vectoralis`, in light's `bin/`, so it is on the agent's path whenever a plugin is on.

| Command | What it does |
|---|---|
| `vectoralis init light` | writes `harness/settings.json`, finds the test and the format command, offers a starter instructions file only where none exists |
| `vectoralis init heavy` | adds the records. `--team` adds an owner column and one to-do section per person |
| `vectoralis status` | the briefing, as a session start prints it |
| `vectoralis check` | staleness, budget and every guard's proof in one pass. Exit 1 on any flag |
| `vectoralis affirm <path>` | says a ticked file was checked again as it is now |
| `vectoralis guards` | every guard, its mode and whether its payloads behave |
| `vectoralis budget` | what is always loaded, against the cap |
| `vectoralis dashboard` | writes one HTML page and prints its path |
| `vectoralis fail "title" --class slug` | adds an entry to the failure log, and says when the class has failed before |
| `vectoralis version` | the version |

- `init` never edits a `CLAUDE.md` or an `AGENTS.md`.
- Every command prints plain text a person can read and an agent can parse.

---

## 8. The skills and the subagents

A skill holds one procedure. Its description is the only part that is always loaded, so each one is a single short line.

| Skill | Plugin | Who calls it | What it does |
|---|---|---|---|
| `setup` | light, heavy | the person | runs `vectoralis init`, shows what it found, asks before a starter file |
| `brief` | heavy | the agent | reads `## Now` and the next open boxes, states the session's goal |
| `plan` | heavy | the agent | every question in one round, before the first edit: the crucial few in the dialog, the rest in a file, the pick first |
| `check` | heavy | the agent | check, then re-check a different way: read the diff, sweep for siblings, re-run what found it |
| `record` | heavy | the agent | moves a box, writes a decision or an exception, locks finished work |
| `report` | heavy | the agent | what changed, what ran and what it printed, what was not verified, every call made without asking |
| `failure` | heavy | the agent | logs a failure, sweeps for siblings, drafts a guard the second time |
| `handoff` | heavy | either | rewrites `## Now` so the next session starts cold and loses nothing |
| `agents` | heavy | the agent | briefs a subagent in full, one owner per file, a worktree for work that could collide, and re-checks its claim |
| `pr` | heavy | the agent | opens a pull request, watches it to green, fixes what breaks, never merges unless `merge` is `agent` |

- `setup` is person-only (`disable-model-invocation: true`), so it costs nothing until it is called.
- A skill body stays under 60 lines and ends with what to write where.

| Subagent | What it does | Limits |
|---|---|---|
| `reviewer` | the re-check, read with fresh eyes | cannot write or edit |
| `builder` | builds one unit it owns, in its own worktree | reports, never writes a record |

---

## 9. The smart pieces

**The staleness check**, `vectoralis check`. A record is stale when it says something the repository no longer backs.

| The flag | How it is found |
|---|---|
| A ✅ older than its work | the bound file is no longer what it was when its row was ticked |
| A path that is gone | a backticked path in a record names no file |
| A lock on nothing | a lock's pattern matches no file |
| A Contents line out of step | it differs from the file's `##` headings |
| A guard without its proof | a payload is missing or misbehaves |
| Over the cap | section 10 |

The briefing shows the count and the first three.

**How a tick knows its version.** `harness/.checked.json` holds, for every bound and ticked row, a short hash of the file as it was at the tick. The engine writes it the moment the agent ticks a box, and `vectoralis check` records a row it has not seen. It compares content, never dates, so it is right before a commit and after one.

- The file changed and was checked again → `vectoralis affirm <path>`, or untick the box and tick it.
- The file changed and was not checked → untick the box.

**The guard tests** → section 5. One command proves every guard, in a temporary project, in seconds.

**The dashboard**, `vectoralis dashboard` → one self-contained HTML file: open work by section, the next boxes, yours and the agent's, open failures, locks, stale flags, the budget. Light and dark, no script, no brand colours. `init` adds it to `.gitignore`.

**The proposed guard.** `vectoralis fail` says when a class fails a second time → the `failure` skill drafts `harness/guards/<class>.json` in `warn` mode, with payloads cut from the two failures → the person reads ten lines and types `promote <class>`.

**The compaction prompt.** Right before the agent compacts, the engine prints what the summary must keep: the task in hand, the boxes moved this session, the decisions made, the files touched, the failures logged, the next step. After the compaction, `session` prints the core and the briefing again.

**The handoff.** `## Now` in `todo.md` is the handoff document. Three ways to carry a long session over, and when each fits:

| The way | What survives | Use it when |
|---|---|---|
| Handoff, then a new session | exactly what `## Now` and the records say | the task changes, or the context is full of dead ends |
| Compact with a prompt | a summary shaped by your instructions | the same task goes on and the thread matters |
| Auto compact | a summary shaped by the engine's prompt | you did nothing, and the harness covered you |

---

## 10. Budgets

| What | Cap | How it is measured |
|---|---|---|
| Light, always loaded | 300 tokens | the descriptions of light's skills |
| Heavy, always loaded | 2,000 tokens | the skill and subagent descriptions, `rules.md`, the briefing |
| A hook's answer | 200 ms | the payload tests time it. `stop` is exempt |
| A skill body | 60 lines | counted |
| `rules.md` | 60 lines | counted |

- `vectoralis budget` counts characters and divides by four. It says it is an estimate.
- The numbers printed in the guide come from a real session's context reading, marked `run`.

---

## 11. Solo and team

One harness, the same files. A team adds four things.

| | Solo | Team |
|---|---|---|
| Install | project scope, one clone | project scope, each person installs once in their clone |
| To-do list | `## Yours` | one section per person |
| Tracker | three stages | an owner on every row |
| A change to a rule or a guard | the person edits it | goes through a pull request |

- The records are committed, so the team reads one truth.
- A grant belongs to the person at the keyboard. Nobody's agent can tick another person's box.
- Asked in `b.md`. Built on this until answered.

---

## 12. Codex

The same two plugins, the same engine, the same records.

| The piece | Claude Code | Codex |
|---|---|---|
| Marketplace | `.claude-plugin/marketplace.json` | reads the same file |
| Add it | `claude plugin marketplace add` | `codex plugin marketplace add` |
| Hooks | `hooks/hooks.json` in the plugin | the same file, trusted once in `/hooks` |
| Plugin root | `CLAUDE_PLUGIN_ROOT` | `PLUGIN_ROOT`, and `CLAUDE_PLUGIN_ROOT` is set too |
| Skills | `skills/<name>/SKILL.md` | the same folders |
| File edits | Write, Edit | `apply_patch` |
| The core, always loaded | session-start output | session-start output |
| Instructions file | `CLAUDE.md` | `AGENTS.md` |

- `payload.py` is the only module that knows which agent is calling.
- **The table of gaps** lists what Codex cannot do yet, each one marked `read` or `run`. It lives in `guide/codex.md`.
- Each row above is checked against Codex's docs before the Codex part is called done.

---

## 13. The guide

`guide/`, one page each. A page marked ★ owns one of the twelve topics.

| Page | What it holds |
|---|---|
| `start.md` ★ | what a harness is, and light or heavy in one minute |
| `install.md` ★ | one package, two agents: plugins and skills |
| `light.md` | the five steps and the three guards, one real run |
| `heavy.md` | the seven steps, one real session from briefing to report |
| `plan.md` ★ | the brief and the plan, every question asked up front |
| `modes.md` | plan mode in action, and the permission modes, bypass included |
| `models.md` | which model, what effort, for which job |
| `context.md` ★ | what loads, what it costs, how the core stays small |
| `handoff.md` | handoff, compact with a prompt, auto compact |
| `guards.md` ★ | hooks as guards: block or warn, the payloads, switching one off |
| `checks.md` ★ | done is a claim: check, re-check, the staleness check |
| `tracker.md` | ✅ and ⬜, and nothing else |
| `todos.md` | yours and the agent's, kept apart |
| `failures.md` ★ | failure → fix → guard, and the guard proposed the second time |
| `lessons.md` | in your own words |
| `decisions.md` | decisions and exceptions, dated, with the reason |
| `locks.md` | finished work stays finished |
| `agents.md` ★ | subagents, worktrees and workflows, one owner per file |
| `pull-requests.md` | watched to green |
| `unattended.md` ★ | headless runs, CI and loops |
| `safety.md` ★ | permissions, sandbox, secrets, injected instructions |
| `cost.md` ★ | tokens and attention, piece by piece |
| `mcp.md` ★ | when a server earns its context |
| `dashboard.md` | one page built from the files |
| `team.md` | one person, then a team |
| `codex.md` | the same harness in Codex, and every gap |
| `other-agents.md` | what works in any agent that reads `AGENTS.md` |
| `proof.md` | what this way of working built |
| `reference.md` | every command, file, guard and setting |

**The shape of a page that adds a piece:**

```text
# The piece
What it is, and when to read this page.
Contents

When to add it        the signal that it now pays for itself
The steps             exactly what to do, in order
The file              what it creates, and where it lives
The guard             what enforces it
What it costs         tokens · attention
In Claude Code        the same step, as you type it
In Codex              the same step, as you type it
What it built         one line of proof, only where one exists
Verified on           the versions, the model, the date
```

- **Both agents on every page**, side by side, never a separate guide.
- A page that adds no piece keeps the same close: both agents, what can go wrong, verified on.
- An output shown on a page is real, marked `run`.

---

## 14. The kit

`kit/`, one page per situation, and a `README.md` that shows all nineteen on one screen, sorted by what you do and by who you are.

```text
# The situation
One line: what the work is.
Contents

The picks             one each: skill, guard, MCP server
Also worth it         at most four more of each, one line each
When each earns it    the signal, and what it costs in context
A sample to study     free, linked
How to do it better   what the sample misses
Where people talk     the subreddits for this situation
Verified on           the date, and tried or read for every entry
```

**How a pick is chosen:**

1. It does the job the situation needs, today.
2. Free and open first. A paid one only where nothing free does the job, marked `paid` with its price.
3. From the tool's maker before a third party.
4. Alive: a commit in the last three months.
5. It costs little context for what it gives.

- Every entry says `tried` or `read`, with the date.
- A guard in the kit is one of ours, or a recipe short enough to read.
- Nothing is installed by Vectoralis. The page gives the line, the cost and the risk.

---

## 15. The roadmaps

`roadmaps/`, three pages and a `README.md` that shows the three roads side by side and how to pick.

```text
# The career
Contents

The job               what you ship, who hires for it
The road              the stages, drawn with arrows
Stage by stage        the steps as boxes → the milestone → the project
Resources             a table per stage: free and paid, the stars, what each excels at
Project inspiration   free links, hard repositories included, with the stars
The future            where the job is going, what to learn next
Where people talk     the subreddits for this career
Grounded in           the job postings of the month, and which month
```

- **No hours and no weeks.** A stage ends when its milestone is met.
- **The stars** are `★` and a number from 1 to 10, and the page says they are a judgment. A resource gets four: clarity, depth, hands-on, current. A repository gets two: difficulty, what it teaches.
- **A paid option** sits in brackets beside the free one, only when it is greatly better, with its price. The cap is $60 once or $30 a month.
- **Several resources on one stage** each say what they excel at and what they do better than the others on the list.
- **Every project names the kit page it uses** and the workflow it runs under, light or heavy.
- The star categories and the price cap are asked in `b.md`.

---

## 16. The five topics

`topics/`, five pages and a `README.md`. None is a milestone of the three careers.

1. Local and open models
2. Voice and real-time agents
3. Computer use and browser agents
4. AI security
5. Generative media

```text
# The topic
Contents

What it is            in three lines
Why now               what changed this year
Start here            the first steps, as boxes
Resources             a table: free and paid, the stars, what each excels at
Build this            project ideas, with free links
The kit               the kit pages that serve it
Where people talk     the subreddits and the rest
The future            where it is going
```

The five are asked in `b.md`.

---

## 17. The communities

`community/README.md`, one page: every topic of this repository, and where its people talk.

| The column | What it holds |
|---|---|
| Topic | a kit situation, a career or one of the five topics |
| Reddit | the exact subreddits, each with what it is good for |
| Elsewhere | the official Discord server, the forum, Hacker News, where one matters |

- Communities and official channels only. No single person is named. Asked in `b.md`.
- Every entry was opened on the day it was listed, and a dead one is cut.

---

## 18. The proof

`guide/proof.md`, and one line under "What it built" on the page of the piece it proves.

- **The lines** are facts counted from the author's own repositories, each with how it was counted. Asked in `b.md`.
- **The frame** is what one person and an agent built, and how the pieces made it possible. A reader should finish the page wanting to start.
- **Never the word motivation**, and never a claim the count does not back.

---

## 19. Tests and CI

- **Unit tests** in `tests/`, on `unittest`, so nothing is installed: the payload shapes of both agents, the grants, the records parsers, the staleness check, the budget.
- **Guard payloads** run by `vectoralis guards`, in a temporary project. A guard with no failing payload fails the run.
- **Repository checks** in `tools/`: no em or en dash, no hard-wrapped paragraph, every Contents line in step, every relative link resolves.
- **CI**, on every push: the unit tests and the guard payloads on Python 3.9, 3.12 and 3.13, then the repository checks.
- **Plugin validation** with `claude plugin validate --strict`, run here before a release.

---

## 20. The release

Private until the author says release.

1. Every box of `harness/tracker.md` is ✅.
2. `vectoralis check` is clean on this repository.
3. Every page's verified-on line is current.
4. The author says release → the repository goes public → the tag `v1.0.0`.

**The first screen of the README**, in this order: one line on what it is → the two workflows side by side → install in two commands → the four parts, each one link → what it built, in three lines.

- `LICENSE` → MIT, `Copyright (c) 2026 themadsaiyantist`.
- `CONTRIBUTING.md` → ten lines: issues are open, a pull request comes with the run that proves it, the writing rules, one fact one home.

---

## 21. The build order

`harness/tracker.md` holds the state, one row per unit. The order:

1. Light → the engine's core, `secrets`, `format`, `tests`, the CLI's `init`, the plugin
2. Heavy → the records, the grants, the heavy guards, the skills, the subagents
3. The smart pieces → the staleness check, the guard tests, the dashboard, the proposed guard, the compaction prompt
4. Codex → the payload shape, the marketplace, the table of gaps
5. The guide
6. The kit
7. The roadmaps
8. The five topics
9. The communities
10. The proof

The research for 6 to 9 runs beside the build of 1 to 4, because neither waits on the other.

---

## 22. Still to prove

Each is marked `read` or `run` on its page before that page is called done.

- The hooks fire inside a Codex session, once trusted. The install itself is proven: `run`, Codex 0.167.0, 2026-11-11.
- Codex's `apply_patch` payload gives the paths and the new text.
- Session-start output works as the always-loaded core in Codex.
- Codex prints a compaction prompt from a hook, or it is a gap.
- A plugin's `bin/` reaches the shell in Codex, or the skills call the CLI by its path.
- Heavy's always-loaded cost, read from a real session.
