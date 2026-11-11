# Tracker

The build state of Vectoralis I. ✅ is done and checked, ⬜ is not done. Nothing else goes in a cell. A unit that opens with a path in backticks is bound to that file, and `vectoralis check` flags it when the file changes after the tick. The last column is the author's.

- **Built** → the file exists, on the shape `spec.md` gives it.
- **Checked** → for code, its tests pass and its payloads behave. For a page, every link opens, every claim carries its mark, and the repository checks pass.
- **Yours** → the author read it. Ticked on the author's word alone.

**Contents:** The harness · The guide · The kit · The roadmaps · The five topics · The communities · The repository

---

## The harness

| Unit | Built | Checked | Yours |
|---|---|---|---|
| `plugins/light/engine/payload.py` the payloads of both agents, one shape | ✅ | ✅ | ⬜ |
| `plugins/light/engine/grants.py` what only the person gives | ✅ | ✅ | ⬜ |
| `plugins/light/engine/guards/` ten guards, each with its payloads | ✅ | ✅ | ⬜ |
| `plugins/light/engine/rules.py` the project's own guards | ✅ | ✅ | ⬜ |
| `plugins/light/engine/checks.py` the staleness check and the budget | ✅ | ✅ | ⬜ |
| `plugins/light/engine/briefing.py` the briefing and the compaction prompt | ✅ | ✅ | ⬜ |
| `plugins/light/engine/dashboard.py` the dashboard | ✅ | ✅ | ⬜ |
| `plugins/light/engine/cli.py` the CLI | ✅ | ✅ | ⬜ |
| `plugins/light/hooks/hooks.json` one hooks file, run in a live Claude Code session | ✅ | ✅ | ⬜ |
| `plugins/heavy/skills/` ten skills, used in a live session | ✅ | ⬜ | ⬜ |
| `plugins/heavy/agents/` two subagents, used in a live session | ✅ | ⬜ | ⬜ |
| `.claude-plugin/marketplace.json` the marketplace, validated | ✅ | ✅ | ⬜ |
| Codex: both plugins install from the same marketplace file | ✅ | ✅ | ⬜ |
| Codex: the hooks and the skills, in a live Codex session | ⬜ | ⬜ | ⬜ |

## The guide

| Unit | Built | Checked | Yours |
|---|---|---|---|
| `guide/README.md` the pages, in reading order | ✅ | ✅ | ⬜ |
| `guide/start.md` | ✅ | ✅ | ⬜ |
| `guide/install.md` | ✅ | ✅ | ⬜ |
| `guide/light.md` | ✅ | ✅ | ⬜ |
| `guide/heavy.md` | ✅ | ✅ | ⬜ |
| `guide/plan.md` | ✅ | ✅ | ⬜ |
| `guide/modes.md` | ✅ | ✅ | ⬜ |
| `guide/models.md` | ✅ | ✅ | ⬜ |
| `guide/layout.md` | ⬜ | ⬜ | ⬜ |
| `guide/context.md` | ✅ | ✅ | ⬜ |
| `guide/handoff.md` | ✅ | ✅ | ⬜ |
| `guide/guards.md` | ✅ | ✅ | ⬜ |
| `guide/checks.md` | ✅ | ✅ | ⬜ |
| `guide/tracker.md` | ⬜ | ⬜ | ⬜ |
| `guide/todos.md` | ⬜ | ⬜ | ⬜ |
| `guide/failures.md` | ⬜ | ⬜ | ⬜ |
| `guide/lessons.md` | ⬜ | ⬜ | ⬜ |
| `guide/decisions.md` | ⬜ | ⬜ | ⬜ |
| `guide/locks.md` | ⬜ | ⬜ | ⬜ |
| `guide/agents.md` | ✅ | ✅ | ⬜ |
| `guide/pull-requests.md` | ✅ | ✅ | ⬜ |
| `guide/unattended.md` | ⬜ | ⬜ | ⬜ |
| `guide/safety.md` | ⬜ | ⬜ | ⬜ |
| `guide/cost.md` | ✅ | ✅ | ⬜ |
| `guide/mcp.md` | ⬜ | ⬜ | ⬜ |
| `guide/dashboard.md` | ⬜ | ⬜ | ⬜ |
| `guide/team.md` | ⬜ | ⬜ | ⬜ |
| `guide/codex.md` | ✅ | ✅ | ⬜ |
| `guide/other-agents.md` | ⬜ | ⬜ | ⬜ |
| `guide/proof.md` | ✅ | ✅ | ⬜ |
| `guide/reference.md` | ✅ | ✅ | ⬜ |

## The kit

| Unit | Built | Checked | Yours |
|---|---|---|---|
| `kit/README.md` the nineteen on one screen | ⬜ | ⬜ | ⬜ |
| `kit/coding.md` | ⬜ | ⬜ | ⬜ |
| `kit/frontend.md` | ⬜ | ⬜ | ⬜ |
| `kit/backend.md` | ⬜ | ⬜ | ⬜ |
| `kit/mobile.md` | ⬜ | ⬜ | ⬜ |
| `kit/games-3d.md` | ⬜ | ⬜ | ⬜ |
| `kit/reasoning.md` | ⬜ | ⬜ | ⬜ |
| `kit/research.md` | ⬜ | ⬜ | ⬜ |
| `kit/data-ml.md` | ⬜ | ⬜ | ⬜ |
| `kit/design.md` | ⬜ | ⬜ | ⬜ |
| `kit/images.md` | ⬜ | ⬜ | ⬜ |
| `kit/animation.md` | ⬜ | ⬜ | ⬜ |
| `kit/video.md` | ⬜ | ⬜ | ⬜ |
| `kit/voice.md` | ⬜ | ⬜ | ⬜ |
| `kit/docs.md` | ⬜ | ⬜ | ⬜ |
| `kit/testing.md` | ⬜ | ⬜ | ⬜ |
| `kit/security.md` | ⬜ | ⬜ | ⬜ |
| `kit/devops.md` | ⬜ | ⬜ | ⬜ |
| `kit/team-tools.md` | ⬜ | ⬜ | ⬜ |
| `kit/agents.md` | ⬜ | ⬜ | ⬜ |

## The roadmaps

| Unit | Built | Checked | Yours |
|---|---|---|---|
| `roadmaps/README.md` the three side by side | ✅ | ✅ | ⬜ |
| `roadmaps/ai-engineer.md` | ✅ | ✅ | ⬜ |
| `roadmaps/agentic-software-engineer.md` | ✅ | ✅ | ⬜ |
| `roadmaps/ai-platform-engineer.md` | ✅ | ✅ | ⬜ |

## The five topics

| Unit | Built | Checked | Yours |
|---|---|---|---|
| `topics/README.md` the five on one screen | ✅ | ✅ | ⬜ |
| `topics/local-models.md` | ✅ | ✅ | ⬜ |
| `topics/voice-agents.md` | ✅ | ✅ | ⬜ |
| `topics/computer-use.md` | ✅ | ✅ | ⬜ |
| `topics/ai-security.md` | ✅ | ✅ | ⬜ |
| `topics/generative-media.md` | ✅ | ✅ | ⬜ |

## The communities

| Unit | Built | Checked | Yours |
|---|---|---|---|
| `community/README.md` where people talk, topic by topic | ⬜ | ⬜ | ⬜ |

## The repository

| Unit | Built | Checked | Yours |
|---|---|---|---|
| `README.md` the first screen | ✅ | ✅ | ⬜ |
| `LICENSE` MIT | ✅ | ✅ | ⬜ |
| `CONTRIBUTING.md` ten lines | ✅ | ✅ | ⬜ |
| `spec.md` how it is built | ✅ | ✅ | ⬜ |
| `tools/check_writing.py` the repository checks | ✅ | ✅ | ⬜ |
| `tools/check.sh` every check before a commit, as one command | ✅ | ✅ | ⬜ |
| `.github/workflows/ci.yml` tests and payloads on every push | ✅ | ⬜ | ⬜ |
