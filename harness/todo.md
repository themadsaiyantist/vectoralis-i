# To-do

Everything left on Vectoralis I, in order, in two lists: yours and the agent's. `CLAUDE.md` loads it in full, so every session starts having read it.

**Contents:** How it stays true · Now · Yours · The agent's

---

## How it stays true

- ✅ is done and checked. ⬜ is not done. Nothing else.
- A box moves the moment its work is checked → never in a batch, never on a claim.
- **Yours** is ticked on your word alone.
- A new step is added the moment it is known. A step that no longer applies is deleted.

---

## Now

- **Where it stands** → every page is written, checked and pushed: the spec, the harness (41 tests, 106 payloads), the guide's 30 pages, the kit's 19, three roadmaps, five topics, the communities and the people worth following. Light and heavy ran for real in Claude Code. Both plugins install in Codex. CI runs `checkout@v7` and `setup-python@v7`, green on 3.9, 3.12 and 3.13, with no Node.js 20 warning (pull request 1, merged).
- **Next →** the ten heavy skills and the two subagents in a live session, on a copy of this repository → tick their two rows in the tracker.
- **Then** → one last pass: `sh tools/check.sh`, the tracker against the files, this block, the report to the author.
- **Open** → a Codex session needs the author's login. Every CI run now shows a notice that `ubuntu-latest` moves to Ubuntu 26, outside the scope given, so the call is in `c.md`, pick first.
- **Mind** → commit through the hook, with explicit paths while a subagent writes. A ticked file that changed needs `vectoralis affirm` after it is checked again, and a workflow can only be checked by a pull request, so untick its Built box on the branch and tick it on `main` after the merge.

---

## Yours

- ✅ Answer the question round → `a.md`, 25 questions
- ✅ Say start
- ✅ Answer `b.md` → seven short calls, while the build runs
- ⬜ Read `spec.md` while the build runs → say what to change
- ⬜ Trust the hooks once in Codex → `/hooks` → then say so, and I run the first live Codex session
- ⬜ Open the subreddits of `community/README.md` once → Reddit refuses a checker
- ⬜ Give the address of the Coding Agents course → for the README's one link
- ⬜ Say release → the repository goes public

---

## The agent's

**1. Before the spec**

- ✅ Write the outline → `vectoralis-i.md`
- ✅ Ask the question round → `a.md`
- ✅ Create the private repository → `themadsaiyantist/vectoralis-i`
- ✅ Record every ruling so far in the outline
- ✅ Start the to-do list, the failure log and `CLAUDE.md`
- ✅ Fold the 25 answers into the outline → delete `a.md`
- ✅ Ask the second round → `b.md`, seven calls
- ✅ Clean the series text and the history → first push
- ✅ Study the similar repositories → notes kept outside the repository
- ✅ Check each platform fact in the docs → run only what cannot be read
- ✅ Fold the answers of `b.md` into the outline → delete `b.md`

**2. The spec**

- ✅ Write `spec.md`

**3. The build, in this order**

- ✅ Light → three guards, one settings file
- ✅ Heavy → the records, the guards, the skills
- ✅ The smart pieces → staleness check, guard tests, dashboard, proposed guard, the compaction prompt
- ✅ Codex → the same package installs in Codex, and the table of gaps is written
- ⬜ Codex, live → the hooks and the skills in a real Codex session. It needs your Codex login
- ✅ One real run → light on `runlog`, in Claude Code, for `guide/light.md`
- ⬜ Install heavy in this repository → run a live session on its own harness
- ✅ The guide → every page listed in `spec.md`, 30 of them
- ✅ The kit → 19 situations, and the index
- ✅ The roadmaps → 3 careers
- ✅ The five topics → 5 pages
- ✅ The communities → the subreddits and the rest, topic by topic, and the few people worth following
- ✅ The proof → one page, built on the pick of `b.md` until it is answered

**4. The release**

- ⬜ Every page verified → on your word, the repository goes public
