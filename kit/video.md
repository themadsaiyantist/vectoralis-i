# Video

Video work from an agent session is three jobs: cutting footage you already have, putting captions on it, and generating new pictures in motion, in code or with a model. Read this page before an agent touches a folder of takes, and when a project needs video that a script can render again tomorrow.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [HyperFrames](https://github.com/heygen-com/hyperframes) | The maker's skills for video written as plain HTML and rendered to MP4 on your machine: titles, captions timed to the words, overlays, a tighter cut of a talking clip. Apache-2.0. `tried` 2026-11-11: version 0.9.34: `npx hyperframes skills update` put the 6 core skills in `~/.claude/skills/` and `~/.agents/skills/`, `init` and `snapshot --at 1,2` worked, and `render` wrote a 10 second 1920x1080 MP4 in 7.4 seconds with no account. The plugin line was not run, by this run's rules. | Claude Code, Codex | six descriptions in every session with the core set, nine with the plugin, each body loads on use | `claude plugin marketplace add heygen-com/hyperframes` → `claude plugin install hyperframes@hyperframes`. Codex: `npx hyperframes skills update` |
| Guard | `ffmpeg-overwrite` | Warns when an ffmpeg command that reads an input carries `-y`, the flag that overwrites a file without asking. `tried` 2026-11-11: the engine's proof passes all 4 payloads, and ffmpeg 5.1 with `-n` on an existing file printed `File 'cut.mp4' already exists. Exiting.` | both | none, a hook costs no context | below |
| MCP server | [Comfy MCP](https://github.com/Comfy-Org/comfy-mcp) | Comfy's own local server: runs video and image workflows on the ComfyUI on your machine, searches the nodes and models you have, and in its README hands back a contact sheet of a clip. AGPL-3.0 or a commercial licence, in beta. `tried` 2026-11-11: the install line gave comfy-mcp 0.10.0 and comfy-cli 1.26.0, and `tools/list` over stdio gave 39 tools: `preview_media`, the contact sheet, and `billing_status` are in its README and not yet in that release. | Claude Code. For Codex the maker documents only its hosted server | 39 tools in the release, 41 in its README | `pip install comfy-mcp "comfy-cli>=1.14.0"` → `claude mcp add comfy-mcp -e COMFY_BIN=/path/to/venv/bin/comfy -- comfy-mcp` |

Footage is not in git, and the built-in `locks` guard does not read where ffmpeg writes, so this recipe speaks before `-y` replaces a take.

```json
{
  "id": "ffmpeg-overwrite",
  "why": "footage is not in git, so an overwritten take cannot be brought back",
  "on": "shell",
  "pattern": "(?s)\\bffmpeg\\b(?=.*\\s-i\\s).*\\s-y(\\s|$)",
  "mode": "warn",
  "message": "ffmpeg -y overwrites its output without asking. Write to a new file name, or use -n so it stops when the file exists.",
  "payloads": [
    { "name": "catches an overwrite", "text": "ffmpeg -y -i footage/take1.mov -vf scale=1280:-2 footage/take2.mov", "expect": "hit" },
    { "name": "catches it inside a loop", "text": "for f in *.mov; do ffmpeg -i \"$f\" -c copy -y \"cut/$f\"; done", "expect": "hit" },
    { "name": "passes a write that stops when the file exists", "text": "ffmpeg -n -i footage/take1.mov -vf scale=1280:-2 renders/take1-720p.mp4", "expect": "pass" },
    { "name": "passes an install", "text": "sudo apt-get install ffmpeg -y", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/ffmpeg-overwrite.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [Remotion Agent Skills](https://www.remotion.dev/docs/ai/skills) | Video as React components, 13 skills from the maker: `npx skills add remotion-dev/skills`. `tried` 2026-11-11: that line copied 13 skills into `.claude/skills/`. | free for individuals and companies of up to 3 employees. Above that `paid`, $25 a month per seat with a $100 a month minimum, by its [pricing](https://www.remotion.dev/docs/license/pricing) |
| Skill | [video-use](https://github.com/browser-use/video-use) | Edits raw takes by reading a transcript and a filmstrip: cuts filler words and dead air, burns subtitles, and checks every cut before it shows you the result. `read`: its first step needs a paid ElevenLabs key. Cloned only: MIT, last commit 2026-10-08. | free, MIT. Its transcript step calls ElevenLabs Scribe, `paid`, $0.20 per hour of audio by its [price list](https://elevenlabs.io/pricing/api) |
| Skill | [auto-editor](https://github.com/WyattBlue/auto-editor) | The first pass on a long recording: one command removes the silent parts. It ships five skills: `npx skills add WyattBlue/auto-editor`. `tried` 2026-11-11: that line copied 5 skills into `.claude/skills/`, and `auto-editor take.wav`, version 29.3.1, cut a 16 second file with 10 silent seconds to 6.4. Its binary needs glibc 2.38 or later, so it fails on Debian 12. | free, Unlicense |
| Guard | [`locks`](../guide/locks.md) | Built in, heavy profile. Lock `footage/**` and no `rm`, `mv`, `cp` or redirect reaches a source take. `tried` 2026-11-11: `vectoralis guards` printed `locks block block 11 of 11 payloads behave`. | free, ours |
| Guard | [`tests`](../guide/guards.md) | Built in, light profile. Set `test` to `npx hyperframes check` and the agent cannot say done while the composition fails its checks. `tried` 2026-11-11: `vectoralis guards` printed `tests block block 6 of 6 payloads behave`. | free, ours |
| MCP server | [Comfy Cloud MCP](https://docs.comfy.org/agent-tools/mcp) | The same kind of workflows on hosted GPUs, for a machine with no graphics card. Its docs page lists 37 tools and sets it up for both agents: `codex mcp add comfy-cloud --url https://cloud.comfy.org/mcp`. `read`: paid, and the server answers `Authentication required` without a key. | `paid`, from $20 a month by its [pricing](https://comfy.org/pricing/), with 5 free runs for a new account |

## When each earns its place

- **The skill** → the second time the agent builds captions or a title card from scratch and they look unlike the first. It needs Node.js 22 and FFmpeg, and it renders with no account. The first check, snapshot or render downloads a headless Chrome, and a first `check` gave up after 180 seconds while that download ran: run `npx hyperframes browser ensure` once before. Two of the six core skills, `reverse-any-video` and `style-sampling`, are marked HyperFrames Pro in its README, and its [FAQ](https://hyperframes.heygen.com/faq) prices the Pro plan at $25 a month, `paid`. The other four are free.
- **The guard** → the first session that runs ffmpeg on footage you cannot shoot again. It costs nothing until it speaks, and after one warning the agent writes each render to a new name. It reads the shell, so it does not see a render started through an MCP tool.
- **The MCP server** → the agent has to explore: which nodes and models your install has, which template fits, what the clip looks like. It costs 39 tools, 41 once the README's version ships, and a graphics card: its README calls 24 GB of video memory a good default for local generation, and calls video slow or infeasible below that. Claude Code loads only the tool names until one is called, [by its docs](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search). A workflow with partner nodes spends Comfy credits. Such a run needs your yes: the server asks, or the run fails closed. Its README warns that a custom node billing its own service is not gated, so read a workflow you did not build.
- **The CLI first** → a job you can name needs no skill and no server, and costs no context until it runs.
  - A cut → `ffmpeg -n -ss 00:01:00 -to 00:02:30 -i take.mp4 -c copy cut.mp4`, by the [ffmpeg manual](https://ffmpeg.org/ffmpeg.html). `tried` 2026-11-11: ffmpeg 5.1 cut a 3 minute test clip to 90.2 seconds.
  - Captions → `ffmpeg -n -i cut.mp4 -ar 16000 -ac 1 -c:a pcm_s16le talk.wav` → `whisper-cli -m models/ggml-base.en.bin -f talk.wav -osrt -of talk` with [whisper.cpp](https://github.com/ggml-org/whisper.cpp), MIT and local → `ffmpeg -n -i cut.mp4 -vf subtitles=talk.srt captioned.mp4`. `tried` 2026-11-11: the three commands ran as printed, with whisper.cpp built from source and the 148 MB `base.en` model, and `talk.srt` read ` The quick brown fox jumps over the lazy dog.` On silence the model repeats the last line, so read the captions before you burn them.
  - A generation → `comfy run --workflow shot.json --wait` runs a workflow you exported, with [comfy-cli](https://github.com/Comfy-Org/comfy-cli). `read`: it needs a graphics card.
  - A narration → the text to speech command on the [Voice and audio](voice.md) page.

## Left out, and why

- [Sora 2 and the OpenAI Videos API](https://developers.openai.com/api/docs/deprecations) → removed from the API on 2026-09-24, and the page lists no replacement.
- A separate server for each hosted model → `comfy generate` in [comfy-cli](https://github.com/Comfy-Org/comfy-cli) already calls Kling, Luma, Runway and others from one command. It is `paid`: it spends Comfy credits, which need the subscription above.
- `whisper-1` through the OpenAI API for captions → the same deprecations page removes it on 2027-02-26, and whisper.cpp runs the Whisper model on your own machine for free.

## A sample to study

[OpenMontage](https://github.com/OpenMontageInc/OpenMontage) → an open production system that a coding agent runs from brief to render, with no orchestrator but the agent: a manifest of stages, a checkpoint after each, your approval on the script, the scene plan and the assets, a budget with a cap, and a review of the render before you see it. AGPL-3.0, with instruction files for Claude Code and Codex. `referenced`. Opened 2026-11-11: last push 2026-11-09, not archived.

## How to do it better

- **Its gates live in its own Python tools and instruction files** → a command the agent types in the shell beside them, a raw `ffmpeg -y` or a paid call, is read by none of them. Put the rule in a hook, where every command is read: the recipe above, and one of the same shape for the command that spends.
- **It is a studio: its description counts 12 pipelines and more than 100 tools** → for one cut or one caption track, start with one command and one skill. Add a pipeline when the same job comes back a third time.
- **Its render review samples four frames** → a cut fails at the joins. Look at a frame on each side of every cut, as video-use does.
- **Its default for explainers is Remotion** → a company of more than 3 employees needs the paid licence. Ask for HyperFrames at the proposal step, which it also renders with.

## Where people talk

- [r/ffmpeg](https://www.reddit.com/r/ffmpeg/) → the exact command for a cut, a filter or an encode that fails.
- [r/comfyui](https://www.reddit.com/r/comfyui/) → node graphs and workflow files for video models.
- [r/StableDiffusion](https://www.reddit.com/r/StableDiffusion/) → first tests of new open video and image weights.
- [r/aivideo](https://www.reddit.com/r/aivideo/) → finished clips made with the current video models.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Tried 2026-11-11 in a container, each with its evidence above: HyperFrames, the guard, the Comfy MCP tool list, the Remotion skills, auto-editor, `locks`, `tests`, the ffmpeg cut and the whisper.cpp captions. Still `read`: video-use and Comfy Cloud MCP, which need a paid key, and `comfy run`, which needs a graphics card.
