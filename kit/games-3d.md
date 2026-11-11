# Games and 3D

Games and 3D work is building inside an engine or a modelling tool that an agent drives: scenes, scripts, assets, and the loop that runs them. Read this page when the agent writes engine code from the wrong release, and when you want it to see the scene it is changing.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) | 79 skills and a router for 12 engines, Godot, Unity, Unreal, three.js, Phaser and Roblox among them, each pinned to a current engine release. The router finds the engine in the project files and loads the two or three skills the task needs. Apache-2.0. `tried` 2026-11-11: 79 skills and `router/SKILL.md`, the marketplace passes `claude plugin validate`, and the Codex line installed `router` into `.agents/skills`. | Claude Code, Codex | the router and one engine bundle keep it small. The whole set is 80 descriptions in every session | `claude plugin marketplace add gamedev-skills/awesome-gamedev-agent-skills` → `claude plugin install router@awesome-gamedev-agent-skills` → your engine's bundle, such as `claude plugin install godot@awesome-gamedev-agent-skills`. Codex: `npx skills add gamedev-skills/awesome-gamedev-agent-skills -a codex`, and pick the router and your engine's skills when it asks |
| Guard | `no-old-three-api` | Warns when a three.js name that was replaced lands in the code. `tried` 2026-11-11: the engine's proof passes on its 2 payloads. | both | none, a hook costs no context | below |
| MCP server | [Blender MCP server](https://www.blender.org/lab/mcp-server/) | Blender's own, from Blender Lab, for Blender 5.1 and later. The agent inspects the open scene, runs Python in it, renders the viewport, and searches the API docs and the manual that ship with the server. GPL-3.0-or-later. `tried` 2026-11-11: the install line's `uv ... run blender-mcp` started from a clone with no Blender running and answered `tools/list`, 1.30.0. Driving a scene needs Blender 5.1 and its add-on. | Claude Code and Codex, as a plain stdio server. The maker's docs name no agent | 20 tools, and 6 `_for_cli` twins of them: 26 listed | the maker gives one stdio command for any client, once its add-on is on in Blender and `https://projects.blender.org/lab/blender_mcp.git` is cloned into your home folder: `uv --directory $HOME/blender_mcp/mcp run blender-mcp`. Put it after `claude mcp add blender --` or `codex mcp add blender --` |

A model learned each engine from many releases at once, and the three.js [migration guide](https://github.com/mrdoob/three.js/wiki/Migration-Guide) lists the names it still reaches for.

```json
{
  "id": "no-old-three-api",
  "why": "the model learned three.js from many releases, and these names were replaced",
  "on": "write",
  "path": "src/**",
  "pattern": "\\b(outputEncoding|sRGBEncoding|RGBELoader|THREE\\.Clock)\\b",
  "mode": "warn",
  "message": "This three.js name was replaced: outputEncoding → outputColorSpace, sRGBEncoding → SRGBColorSpace, RGBELoader → HDRLoader, Clock → Timer.",
  "payloads": [
    { "name": "catches the old color setting", "path": "src/main.js", "text": "renderer.outputEncoding = THREE.sRGBEncoding;", "expect": "hit" },
    { "name": "passes the current one", "path": "src/main.js", "text": "renderer.outputColorSpace = THREE.SRGBColorSpace;", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/no-old-three-api.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [Unity's plugin](https://github.com/Unity-Technologies/unity-agent-plugin) | Unity's own, for Unity 6 and later: 34 skills, many of which drive the open Editor through the Unity CLI. It is at version 0.1.9-beta, and Unity's docs call the CLI experimental. `tried` 2026-11-11: 34 skills at 0.1.9-beta, and the plugin passes `claude plugin validate`. | free, Unity Companion License |
| Skill | [Three.js Skills](https://github.com/CloudAI-X/threejs-skills) | 13 deeper skills for three.js r186: materials, shaders, loaders, performance, React Three Fiber, a glTF asset pipeline. `tried` 2026-11-11: 13 skills, r186 in its README, and the plugin passes `claude plugin validate`. | free, MIT |
| Skill | [Phaser's skills](https://github.com/phaserjs/phaser/tree/master/skills) | 28 skills from Phaser Studio for Phaser 4, covering each main subsystem and the move from v3. `tried` 2026-11-11: 28 skill folders, each with a `SKILL.md`, in the Phaser 4.2.1 repository. | free, MIT |
| Skill | [Game Studio](https://github.com/openai/plugins/tree/main/plugins/game-studio) | OpenAI's Codex plugin for browser games: Phaser, three.js, React Three Fiber, sprites, and a playtest skill. Codex only. `tried` 2026-11-11: 9 skills at 0.1.2, `game-playtest` among them, listed in the `openai-curated` marketplace. | free, MIT |
| Guard | [`destructive`](../guide/guards.md) | Built in, heavy profile. Blocks `git clean -f`, which deletes every asset git does not track yet. `tried` 2026-11-11: blocked, exit 2. | free, ours |
| Guard | [`locks`](../guide/locks.md) | Built in, heavy profile. Lock the files the editor owns, such as `ProjectSettings/` in Unity or `project.godot` in Godot, so they change through the editor alone. `tried` 2026-11-11: a locked path blocked a write, exit 2. | free, ours |
| MCP server | [Godot AI](https://github.com/hi-godot/godot-ai) | A live Godot 4.7 editor for the agent: scenes, nodes, scripts, signals, UI, animation. 47 tools, signed releases, and a dock that writes the config for Claude Code and Codex. `tried` 2026-11-11: the server from the repository listed 47 tools with no editor open, one more than its README's 46. It wants `GODOT_AI_CAPABILITY_DIR` when the folder it runs from is not its user's own. | free, MIT |
| MCP server | [Roblox Studio MCP server](https://create.roblox.com/docs/studio/mcp) | Built into Studio by Roblox: explore the data model, write and run Luau, playtest. 28 tools. `read`: needs Roblox Studio, on Windows or macOS. | built in, the docs name no price |
| MCP server | [MCP for Blender](https://github.com/ahujasid/mcp-for-blender) | The community server that came first: scene building, assets from Poly Haven and Sketchfab, and 3D model generators. `tried` 2026-11-11: `uvx mcp-for-blender` 1.30.0 listed 9 tools with no Blender running, `search_assets` and `generate_3d` among them. | free, MIT, with a paid tier for generation without your own keys |
| MCP server | [MCP for Unity](https://github.com/CoplayDev/unity-mcp) | A community bridge to the Unity Editor, from 2021.3 LTS to 6.x: scenes, scripts, assets, tests. 49 tools. `tried` 2026-11-11: its server at 10.3.0 listed 49 tools with no editor open. | free, MIT |

## When each earns its place

- **The skill** → the agent writes Godot 3 in a Godot 4 project, or reaches for an API the engine replaced. Install the router and your engine's bundle, and leave the other eleven engines out. It is a third party's set, first published in June 2026, so read the skills your engine loads before you rely on them.
- **The guard** → the second time the same old name comes back. This recipe is for three.js. For another engine keep the shape and change the pattern, such as `KinematicBody2D` in `**/*.gd`, which Godot 4 renamed `CharacterBody2D` [in its upgrade guide](https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.html).
- **The MCP server** → the agent has to see the scene to answer: which objects use a material, where the polygons are, what the viewport shows. One of its 20 tools runs any Python the model writes, and Blender's page says it does so with no guard on your data and advises a machine that holds nothing sensitive. Save and commit before a session.
- **The CLI first** → a script needs no server. `blender --background --python script.py` runs one with no window, [by Blender's manual](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html), and `godot --headless --script` runs one in Godot, with `--check-only` to parse it for errors and quit, [by Godot's docs](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html). Tried 2026-11-11 on Godot 4.7.2: a script ran and printed its line, and `--check-only` stopped one that used `KinematicBody2D` with a parse error.

## Left out, and why

- [Unreal MCP](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor) → Epic's own server inside the editor, and Epic labels it Experimental in Unreal Engine 5.9. It waits here until that label goes.
- [Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp) → no commit since April 2026, past the three months this kit asks for.
- [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) → 49 agents and 72 skills by its own count, a whole studio's process for Claude Code. That is a lot to load for one game, and this page stays with the engine.

## A sample to study

[cyberpunk-hud-demo](https://github.com/hi-godot/cyberpunk-hud-demo) → a Godot HUD built three times over, each pass kept as its own scene, with every change made through MCP tool calls and no scene edited by hand. Its `docs/` folder holds the full prompts and a friction log: each tool that failed, what was tried, and the way around it. `referenced`

## How to do it better

- **The agent could not take a picture of the running game, only of the editor** → make a screenshot of the running game the last step of every change, and stop when it cannot be taken. Looking at the editor is not looking at the game.
- **The project ships no test** → a HUD has logic: cooldowns, health, timers. Put it in scripts a headless run can check, and name that run in the `test` setting so the `tests` guard holds it.
- **Every change went through server tools, which no write guard reads** → write scripts as files, where the guards see them, and keep the server for the scene.
- **The frictions stayed in a log** → turn each one that can repeat into a rule the next session loads: the workaround in a skill, the mistake in a guard.
- **It was built on Godot 4.4, and the server now asks for 4.7** → pin the engine release in the project's rules and say it in every brief, so the skills, the server and the code agree.

## Where people talk

- [r/gamedev](https://www.reddit.com/r/gamedev/) → the craft at large, across every engine: design, production, shipping.
- [r/godot](https://www.reddit.com/r/godot/) → Godot: GDScript, scenes, plugins.
- [r/Unity3D](https://www.reddit.com/r/Unity3D/) → Unity projects and their tooling.
- [r/blender](https://www.reddit.com/r/blender/) → modelling, materials, rendering, and scripting with Python.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Tried 2026-11-11, in Docker or through this repository's engine: every entry but one, each with its evidence. A server tried here answered `tools/list` with no editor running, and no scene was driven. Still `read`: the Roblox Studio server, which needs Roblox Studio on Windows or macOS. The sample was opened and is alive. Its README says Godot 4.4, and its `project.godot` was last saved by 4.6.
