# One Person, Then a Team

One harness for one person and for a team: the same files, the same guards, and four things a team adds. Read this before a second person, or a second person's agent, starts working in a repository that runs heavy.

**Contents:** What stays the same · What a team adds · Whose grant counts · Merging the records · In Claude Code · In Codex · With the harness · What can go wrong

---

## What stays the same

- The records in `harness/`, committed, so everyone reads one truth.
- The ten guards, and the four words that open them: `tick`, `unlock`, `lesson:`, `promote`.
- Five of the seven records. The rules, the failure log, the lessons, the decisions and the locks come out byte for byte the same with `--team` and without it (`run`).

---

## What a team adds

| | One person | A team |
|---|---|---|
| Install | project scope, one clone | project scope, and each person installs once in their own clone |
| To-do list | `## Yours` | one section per person: `## Yours, goku`, `## Yours, vegeta` |
| Tracker | the stages | an `Owner` on every row |
| A change to a rule or a guard | you edit it | it goes through a pull request |

`vectoralis init heavy --team` writes the two team records with your git name filled in, and sets `"team": true` in `harness/settings.json`. The tracker it wrote, `run` in a scratch project:

```markdown
| Unit | Owner | Built | Checked | Yours |
|---|---|---|---|---|
| the first unit of work | goku | ⬜ | ⬜ | ⬜ |
```

The to-do list it wrote has one section for you, `## Yours, goku`. A second person adds theirs by copying the heading. [Tracker](tracker.md) and [To-dos](todos.md) have the rest.

---

## Whose grant counts

- **The person at the keyboard, in the session they type in.** `tick refund webhook`, typed in goku's session, opened nothing in a second session running at the same time (`run`).
- **A row is ticked only in its owner's session.** With `"team": true`, the guard reads the row's `Owner` and the name git is set up with on this machine. goku typing `tick refund` does not open vegeta's row, through an edit or through the shell, and the agent cannot rewrite the `Owner` of an open row to get there (`run`: the guards' payloads). A teammate's own tick that arrives with their commit is left alone, as long as it still stands in the record: the guard reads who committed, not who is named as author (`run`: a test with real commits). A branch of theirs squashed on this machine carries this machine's name, so squash after the merge, not before. The name is git's, so it is as honest as the machine it runs on.
- **A machine's notice is never read as anyone's words.** A notice that said `unlock all` opened nothing (`run`).

---

## Merging the records

- **One line per item.** A box, a row, a decision, a lock: each is one line, so two people who change two items change two lines.
- **A section per person.** Two branches that each ticked a box under their own heading merged with no conflict. So did two branches that ticked rows of one table that were not next to each other.
- **What still collides.** Two neighbouring rows ticked on two branches conflicted, in the tracker and in `harness/.checked.json`, where each branch had recorded its tick.
- **When it happens** → keep each person's row as they ticked it, and every line of both sides in `.checked.json`, commas in place. Then run `vectoralis check`. After that, a file changed after its tick was still flagged.
- **Never delete `.checked.json` to get past a conflict.** [Tracker](tracker.md) says why.

Each merge is `run`: git 2.53.0, two branches of a scratch repository, 2026-11-11.

---

## In Claude Code

```text
claude plugin install heavy@vectoralis --scope project
```

- Project scope writes the plugin into `.claude/settings.json`, which you commit. That switches it on for everyone and downloads nothing.
- Each person runs the same line once in their own clone. Heavy brings light with it. [Install](install.md)
- One person runs `/heavy:setup` and answers "a team". The skill then runs `vectoralis init heavy --team`. Run again by a teammate, it keeps every file that exists.

## In Codex

```toml
[plugins."light@vectoralis"]
enabled = true

[plugins."heavy@vectoralis"]
enabled = true
```

- These lines go in `.codex/config.toml`, committed. Codex reads that file only in a project the person has trusted.
- Each person adds the marketplace and both plugins once, as [Install](install.md) shows, then reviews the hooks once in `/hooks`. Codex skips a hook until that person has trusted it, and again when it changes.
- Then `$heavy:setup`. None of this was run in a Codex session yet. [Codex](codex.md)

`read`: [Claude Code plugin install](https://code.claude.com/docs/en/plugins/install), [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [the `$plugin:skill` form](https://learn.chatgpt.com/docs/security/plugin/changelog), 2026-11-11.

---

## With the harness

- **Light** → nothing changes for a team. Three guards and one settings file, the same for everyone who installs.
- **Heavy** → `init --team` writes the owner column and the section per person. `yours` ties each grant to the session it was typed in.
- **The pull request** → while `merge` is `yours`, the `push` guard keeps the agent off the default branch, so its change to a rule or a guard arrives on a branch (`run`). A guard sees the agent's calls and never your own edits: for people, the pull request is a habit the team keeps. [Pull requests](pull-requests.md)

```text
BLOCKED by Vectoralis. The command did not run.
- A push to `main` is the person's.
  Rule: the default branch moves on the person's word (guard `push`, `merge` in harness/settings.json).
  Do instead: push your own branch and open a pull request.
```

---

## What can go wrong

- **`--team` on a project that already has records.** It keeps every file, sets `"team": true`, and tells you to add the owner column and a section per person by hand (`run`). It does not rewrite your records. Ask the agent to do it and the guard asks for `unlock harness/tracker.md` first: handing out owners is yours to allow (`run`).
- **The agent renames `## Yours` for you.** In the to-do list the heading says whose the boxes are, so the rename is blocked (`run`). Do it in your editor. A section of the tracker is an area of work, and the agent may rename it.
- **A heading that does not start with `Yours`.** `## Vegeta` is not protected, and the agent's tick there passed (`run`).
- **A teammate has no guards.** They pulled the settings and never ran the install. In Codex they also never opened `/hooks`.
- **The briefing counts everyone.** `Open for the person: 2` is the sum of every section, and the first box it names may be a teammate's (`run`).

Verified on Claude Code 2.1.322 and Codex 0.167.1, 2026-11-11, with the install scope `read` in Claude Code's plugin docs, and the project config and the hook review `read` in Codex's. Every output and every line marked `run` came from this repository's CLI and engine on scratch projects, and the merges from git 2.53.0.
