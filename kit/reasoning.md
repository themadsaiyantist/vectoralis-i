# Reasoning

Reasoning is the work before the first edit: turning a loose request into decisions, planning a change that is hard to undo, and letting a second model look for the hole in the plan. Both agents already plan with `/plan`, and both let you set how hard the model thinks. Read this page when plan mode keeps starting from the wrong question, or when a plan reaches the build with gaps in it.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) | Interviews you about a plan in rounds of numbered questions, each with the answer it recommends, and builds nothing until you confirm the plan is shared. MIT. | Claude Code, Codex | one description, then 2 KB with the `grilling` skill it calls | `claude plugin install mattpocock-skills@claude-plugins-official`. Codex: `codex plugin marketplace add mattpocock/skills` → `codex plugin add mattpocock-skills@mattpocock` |
| Guard | `plan-no-holes` | Warns when a plan is written with an undecided step in it, such as "TBD". | both | none, a hook costs no context | below |
| MCP server | [Sequential Thinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | One tool that takes the model's thinking as numbered steps it can revise and branch. From the MCP project itself, MIT. | Claude Code, Codex | 1 tool | `claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking`. Codex: `codex mcp add sequential-thinking npx -y @modelcontextprotocol/server-sequential-thinking` |

A plan with "TBD" in it is a guess waiting to happen, so the recipe reads every write under a `plans/` folder: point `path` at where your plans live.

```json
{
  "id": "plan-no-holes",
  "why": "a hole in the plan is a decision the build will make without you",
  "on": "write",
  "path": "**/plans/**",
  "pattern": "(?i)\\b(tbd|todo|to be decided|figure out later)\\b|\\?\\?\\?",
  "mode": "warn",
  "message": "The plan has an open hole. Decide it now, or ask the person before the first edit.",
  "payloads": [
    { "name": "catches a hole", "path": "docs/plans/auth.md", "text": "3. Token storage: TBD", "expect": "hit" },
    { "name": "passes a decided step", "path": "docs/plans/auth.md", "text": "3. Token storage: an httpOnly cookie that lasts 15 minutes", "expect": "pass" },
    { "name": "leaves code alone", "path": "src/auth.py", "text": "# TODO: rename this helper", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/plan-no-holes.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [second-opinion](https://github.com/trailofbits/skills/tree/main/plugins/second-opinion) | A review of your uncommitted changes, a branch or a commit by another model, through the Codex, Antigravity or Gemini CLI you are signed in to. It reports and fixes nothing. | free, CC BY-SA 4.0 |
| Skill | [Superpowers](https://github.com/obra/superpowers) | The whole road in 15 skills: brainstorm → design → plan → build → review. A session-start hook loads its 3 KB entry skill in every session. | free, MIT |
| Skill | [Spec Kit](https://github.com/github/spec-kit) | GitHub's toolkit for a spec, then a plan, then a task list, with one skill for each step. | free, MIT |
| Skill | [EGM](https://github.com/google/elephant-goldfish-model) | Google's plugin for a design: one agent drafts it with the full context, then reviewers that never saw the conversation read it cold. | free, Apache-2.0 |
| Guard | [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | Keeps the plan in three files on disk. A hook puts the live part back in front of the agent each turn, and a stop gate can hold it until the plan reports complete. | free, MIT |
| Guard | [`locks`](../guide/locks.md) | Built in, heavy profile. Lock the plan the person approved, and the build cannot quietly rewrite it. | free, ours |

## When each earns its place

- **The skill** → the request reads two ways, or a wrong start would cost more than ten minutes of answering questions. It comes in the plugin the [coding](coding.md) page picks, 27 skills in one install. The same plugin holds `wayfinder` for work too big for one session and `prototype` for a design question a throwaway build answers faster than a debate.
- **The guard** → the first time the build filled a hole in the plan with a guess. It costs nothing until it speaks.
- **The MCP server** → rarely now. Both agents' models think on their own, and you set how hard at no tool cost: [`/effort`](https://code.claude.com/docs/en/model-config#adjust-effort-level) in Claude Code, [`/model --reasoning=high`](https://learn.chatgpt.com/docs/developer-commands?surface=cli) in Codex. The server pays for itself on a model with no thinking of its own, such as a small local one, or when a reviewer must read every step in the transcript. It costs 1 tool, a round trip for each thought, and Node.js 24.
- **The CLI first** → a second opinion needs no server. From Claude Code run [`codex exec`](https://learn.chatgpt.com/docs/non-interactive-mode) with the question, from Codex run [`claude -p`](https://code.claude.com/docs/en/headless). The other agent reads the files itself, and nothing sits in your context until you ask. Codex's own server mode, `codex mcp-server`, [was removed](https://learn.chatgpt.com/docs/mcp-server).

## Left out, and why

- [codex-plugin-cc](https://github.com/openai/codex-plugin-cc) → OpenAI's own bridge from Claude Code to Codex. Its last commit is from 2026-07-08, past the three-month line.
- [PAL MCP](https://github.com/BeehiveInnovations/pal-mcp-server), once Zen MCP → many models behind one server. Its last commit is from 2025-12-15.
- [The advisor tool](https://code.claude.com/docs/en/advisor) in Claude Code → a stronger model the agent consults at key moments. Its docs still label it experimental.

## A sample to study

[Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans) → OpenAI's recipe for a plan an agent can follow for hours: one self-contained file a newcomer to the repository could carry out, with four sections it must keep current for progress, surprises, decisions and the outcome. The page is archived and names older models, so take the shape and leave the settings. `referenced`

## How to do it better

- **It tells the agent to resolve every ambiguity on its own** → ask the person the questions only they can answer, in one round, before the first edit. Then let it run.
- **One model writes the plan and the same model follows it** → have a second model read the plan cold before the build starts.
- **"Validation is not optional" is a sentence** → make it a guard. The built-in `tests` guard refuses "done" while the tests fail, and the recipe above warns on a plan with a hole.
- **Every revision must stay fully self-contained, so the file grows with the work** → keep the part that is read every time short: the next step and the open decisions on top, finished milestones folded away.

## Where people talk

- [r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/) → plan mode, effort levels and planning skills in daily use.
- [r/codex](https://www.reddit.com/r/codex/) → the same on the Codex side: reasoning levels, long runs and what a plan needs.
- [r/ChatGPTCoding](https://www.reddit.com/r/ChatGPTCoding/) → workflow talk across agents and models.
- [r/PromptEngineering](https://www.reddit.com/r/PromptEngineering/) → how to word a request so the model reasons before it answers.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
