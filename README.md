# Vectoralis I

**Run a coding agent on real work, and trust the result.** A light harness for a fix you finish in one sitting, a heavy one for work that runs for weeks, in Claude Code and in Codex. It starts as three guards. It grows into records that stay true, only when the work asks for them.

**Contents:** Which one · Install · See it work · What is inside · What it built · The limits · The map · Where it comes from

---

## Which one

| | Light | Heavy |
|---|---|---|
| The work | a bug fix, a small feature, one sitting | days of work, many files, anything other people rely on |
| The steps | describe → plan in one line → edit → run the tests → commit | briefing → plan → build → check → re-check → record → report |
| You get | three guards and one settings file | light, plus a tracker, two to-do lists, a failure log, lessons, decisions and locks |
| Always loaded | 0 tokens | about 1,400, capped at 2,000 |
| Read | [guide/light.md](guide/light.md) | [guide/heavy.md](guide/heavy.md) |

Start light. Switch the moment one of [five signals](guide/start.md) is true.

---

## Install

```text
claude plugin marketplace add themadsaiyantist/vectoralis-i
claude plugin install light@vectoralis --scope project
```

Then `/light:setup` in a session. Check it on your own machine:

```text
$ vectoralis guards
167 payloads, the slowest answer took 21 ms
```

<details>
<summary>In Codex</summary>

```text
codex plugin marketplace add themadsaiyantist/vectoralis-i
codex plugin add light@vectoralis
```

Then `/hooks` to trust the hooks, and `$light:setup`. [guide/codex.md](guide/codex.md) lists every gap.

</details>

Python 3.9 or later, and nothing else. No account, no telemetry, no network call. [guide/install.md](guide/install.md)

---

## See it work

A task asked for a GitHub token as a constant in a script. The write never happened:

```text
BLOCKED by Vectoralis. Nothing was written.
- `scripts/upload.py` would hold a GitHub token.
  Rule: no secret is written to a file or printed (guard `secrets`).
  Do instead: read the value from the environment, and keep it out of the repository.
```

The agent read the reason, wrote the script to use an environment variable, and told the person to rotate the token. A real run, 19 seconds. [guide/light.md](guide/light.md) has it and two more.

---

## What is inside

| Part | What it is | Start at |
|---|---|---|
| The guide | how to run an agent on light and heavy work, 30 pages, both agents on every page | [guide/](guide/README.md) |
| The harness | two plugins, ten guards, each guard with its proof | [plugins/](plugins/) |
| The kit | the few skills, guards and MCP servers that matter, for 19 kinds of work | [kit/](kit/README.md) |
| The roadmaps | three careers, stage by stage, with ranked resources and a project per stage | [roadmaps/](roadmaps/README.md) |
| The topics | five topics beyond the roadmaps | [topics/](topics/README.md) |
| The communities | where the people of each topic talk, and the few worth following | [community/](community/README.md) |

---

## What it built

- **A 130-lesson machine learning bootcamp**, its platform and a free course, by one person and an agent, in three months.
- **708 tracker boxes ticked, 26 pull requests merged green, 29 mistakes turned into guards.**
- **This repository**, built under its own harness. Its tracker, its decisions and its failures are in [harness/](harness/), as they were written.

[guide/proof.md](guide/proof.md) has every number and how it was counted.

---

## The limits

- **A guard is a guardrail, not a wall.** It stops the mistakes a machine can be sure of. It is not a sandbox.
- **Run in Claude Code, installed in Codex.** Codex installs both plugins from the same package. The guards are tested against Codex's payloads, and not yet run inside a Codex session.
- **A kit entry marked `read` was read in its maker's docs**, not installed here.
- **Linux, macOS and WSL.**

---

## The map

```text
guide/        how to run an agent on light and heavy work
kit/          what to install, by situation
roadmaps/     three careers
topics/       five topics beyond the roadmaps
community/    where people talk, and who to follow
plugins/      the harness: light and heavy
harness/      this repository's own records
tests/        the unit tests and the guard payloads
spec.md       how every part is built
```

---

## Where it comes from

The harness that carried weeks of heavy work on a machine learning bootcamp, and Coding Agents, a free course whose starter project is [`runlog`](https://github.com/themadsaiyantist/runlog). What worked is kept. What hurt is fixed: too much loaded every session, records that fell behind the work, hooks that misfired, state scattered over many files.

MIT. Issues are open, and a pull request comes with the run that proves it. [CONTRIBUTING.md](CONTRIBUTING.md)
