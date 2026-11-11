# The Dashboard

One HTML page, built from the files in `harness/` on your own machine: what is done, what is next, what waits on you, what is stale. Read this when you want the state of the work on one screen, without opening six files or asking the agent.

**Contents:** When to add it · The steps · The file · The guard · What it costs · In Claude Code · In Codex · What can go wrong

---

## When to add it

- The records are long enough that you scroll to find what is open.
- Someone who does not run the agent wants to see where the work stands.
- You come back after a few days and want one screen before your first message.

---

## The steps

1. Have the records → heavy is set up. [Heavy](heavy.md)
2. Build the page → `vectoralis dashboard`. It prints one line, the path of the file it wrote.
3. Open that file in a browser.
4. Run the command again when you want it fresh. The line under the title says when the page was built.

---

## The file

`harness/dashboard.html`, one file. No script, nothing loaded from the network, light or dark by your system's setting. The page of a scratch project, card by card:

| Card | What it shows | In the scratch project |
|---|---|---|
| The numbers | boxes done, open for the agent, open for you, open failures, stale flags, tokens always loaded against the cap | 2 / 6, 2, 2, 2, 0, 1405 of 2000 |
| Now | the lines of `## Now` in the to-do list | one line, the handoff |
| Open work | one bar per section of the tracker, done over total | Checkout, 2 / 6 |
| Next for the agent | its first eight open boxes | two boxes |
| Yours | your first eight open boxes | two boxes |
| Open failures | the date and the title of each open entry | two entries |
| Stale | every stale flag | "Every record is backed by the repository." |
| Locks | every lock | `src/payments/**` |
| Always loaded | each piece of the budget, in tokens | thirteen rows |

- The number of open failures turns red above zero, the stale flags amber, the tokens red over the cap (`run`). Otherwise each is green.
- The numbers count everything. The two lists stop at eight, so a long list shows its top.
- The page was 39 lines and about 4 KB. `run`: `vectoralis dashboard` in a scratch project, 2026-11-11, and the page it wrote.

---

## The guard

There is none, and none is needed: the command reads the records and writes one file, the page. It is rebuilt whole each time you run it, and nothing else writes to it.

One line in `.gitignore` keeps it out of a commit: `harness/dashboard.html`. `vectoralis init heavy` adds that line, and says so at the end of what it wrote (`run`):

```text
Written: harness/settings.json, harness/rules.md, harness/tracker.md, harness/todo.md, harness/failures.md, harness/lessons.md, harness/decisions.md, harness/locks.md, .gitignore, one line
```

The page is a view. The records are the truth, and they are what you commit.

---

## What it costs

- **Tokens** → none. Nothing of the page is loaded, and the agent has no reason to read it. Its last card shows what is always loaded, the same rows as `vectoralis budget`.
- **Attention** → one command when you want the picture.

---

## In Claude Code

- Ask for it: "build the dashboard". The agent runs `vectoralis dashboard` by name and gives you the path.
- A plugin's `bin/` folder is on the path of the agent's shell, so the command needs no path.

## In Codex

- Codex's plugin docs name no folder that lands on the path. Ask the agent to run the CLI by its path: `~/.codex/plugins/cache/vectoralis/light/*/bin/vectoralis dashboard`.
- The page is the same in both agents. It is built from the files, not from the session.
- Not yet run in a Codex session. [Codex](codex.md)

`read`: [Claude Code plugin components](https://code.claude.com/docs/en/plugins/components), [where Codex keeps a plugin](https://developers.openai.com/plugins/build/plugins), 2026-11-11.

---

## What can go wrong

- **A page from last week.** It is a snapshot, and it does not refresh. Read the line under the title, and rebuild before you trust it.
- **Light has no `.gitignore` line.** Only `init heavy` adds it. In a light project the command still wrote a page, all zeros, and git listed it as new (`run`). Add the line yourself, or keep the dashboard for heavy.
- **Run in the wrong folder.** With no `harness/` it made one and wrote an empty page into it (`run`). Run it from inside the project.
- **Markdown shows as typed.** `**Next →**` in `## Now` appeared with its asterisks (`run`). The page prints the text and does not render it.

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11. `run`: every number, every output and every line marked so, from this repository's CLI on scratch projects. `read`: where each agent finds the CLI, in the docs linked above.
