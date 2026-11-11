# Voice and audio

Voice and audio work is three jobs: turning recordings into text, turning text into speech, and building an agent that listens and answers in real time. Read this page when a project needs a transcript, a narration or a voice agent, and before an agent writes speech code from memory, because the models and the APIs here change faster than its training data.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [LiveKit Agent Skills](https://github.com/livekit/agent-skills) | Seven skills from LiveKit for the loop of a voice agent: look up the current API, build for low latency, talk to the agent turn by turn, write turn tests, simulate, deploy. MIT, on a framework that is Apache-2.0. `tried` 2026-11-11: lk 2.19.4 installed the 7 skills into `.claude/skills/` and `.agents/skills/` and wrote the Docs server to `.mcp.json` and `.codex/config.toml`. With neither agent on the machine it printed `no coding agents detected`, so pass `--agent claude-code --agent codex`. | Claude Code, Codex | seven descriptions in every session, and its README says a task loads two or three bodies | `lk skills install`, for both agents. Or in Claude Code alone: `/plugin marketplace add livekit/agent-skills` → `/plugin install livekit@livekit` |
| Guard | `retired-speech-model` | Warns when Python code names a speech model that OpenAI removes from its API in early 2027. `tried` 2026-11-11: the engine's proof passes all 4 payloads. | both | none, a hook costs no context | below |
| MCP server | [LiveKit Docs MCP server](https://docs.livekit.io/reference/developer-tools/docs-mcp/) | Browses and searches LiveKit's current docs, its public code and its changelogs. Free, hosted by LiveKit. `tried` 2026-11-11: `tools/list` with no account gave 9 tools, server version 1.5.0. | Claude Code, Codex | 9 tools | `claude mcp add --transport http livekit-docs https://docs.livekit.io/mcp`. Codex: `codex mcp add --url https://docs.livekit.io/mcp livekit-docs` |

Agents learned these names from years of tutorials, and [OpenAI's deprecations page](https://developers.openai.com/api/docs/deprecations) removes `tts-1`, `tts-1-hd` and `gpt-4o-mini-tts` on 2027-01-06, then `whisper-1` and the `gpt-4o` transcribe models on 2027-02-26.

```json
{
  "id": "retired-speech-model",
  "why": "OpenAI removes these speech models on 2027-01-06 and 2027-02-26, and an agent still writes them from memory",
  "on": "write",
  "path": "**/*.py",
  "pattern": "[\"'](whisper-1|gpt-4o-(mini-)?transcribe|tts-1|gpt-4o-mini-tts)\\b",
  "mode": "warn",
  "message": "This speech model is on OpenAI's removal list for early 2027. Use gpt-transcribe for speech to text and gpt-realtime-2.1-mini for speech, or a local model.",
  "payloads": [
    { "name": "catches a retired transcription model", "path": "bot/stt.py", "text": "client.audio.transcriptions.create(model=\"whisper-1\", file=audio)", "expect": "hit" },
    { "name": "catches a retired speech model", "path": "bot/tts.py", "text": "speech = client.audio.speech.create(model='tts-1-hd', voice='alloy', input=text)", "expect": "hit" },
    { "name": "passes the replacement", "path": "bot/stt.py", "text": "client.audio.transcriptions.create(model=\"gpt-transcribe\", file=audio)", "expect": "pass" },
    { "name": "passes an open model", "path": "bot/stt.py", "text": "model = WhisperModel(\"large-v3\")", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/retired-speech-model.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [ElevenLabs Skills](https://github.com/elevenlabs/skills) | Twelve skills from ElevenLabs for what the free tools on this page do not do, dubbing, music and sound effects, and for its hosted voices and transcription: `npx skills add elevenlabs/skills`. `tried` 2026-11-11: that line copied 13 skills: the twelve, and the repository's own `update-skills-from-changelog`. Every skill needs a paid key to do its work. | the skills are free, MIT. The API is `paid` by use: speech from $0.04 per 1,000 characters, transcription $0.20 per hour, by its [price list](https://elevenlabs.io/pricing/api) |
| Skill | [Twilio for AI](https://github.com/twilio/ai) | Twilio's skills and its docs server in one plugin, for the phone side of a voice agent, which nothing free covers: numbers, calls, compliance. Public beta. `read`: needs a Twilio account. Cloned only: 57 skills, MIT. | the skills are free, MIT. Twilio is `paid`: a US local number $1.15 a month, $0.0085 a minute to receive a call, by its [pricing](https://www.twilio.com/en-us/voice/pricing/us) |
| Guard | [`secrets`](../guide/guards.md) | Built in, light profile. A voice agent holds one key per provider: speech to text, the model, text to speech, the carrier. It blocks a known key format written into a file, and a command that prints `.env.local`. `tried` 2026-11-11: `vectoralis guards` printed `secrets block block 84 of 84 payloads behave`. | free, ours |
| Guard | [`tests`](../guide/guards.md) | Built in, light profile. Set `test` to your turn tests, such as `uv run pytest`, and the agent cannot say done while a conversation test fails. `tried` 2026-11-11: `vectoralis guards` printed `tests block block 6 of 6 payloads behave`. | free, ours |
| MCP server | [Pipecat Context Hub](https://docs.pipecat.ai/api-reference/context-hub/overview) | For the other open framework, Pipecat: a local index of its docs, examples and API source. 8 tools, and each one is also a CLI command. The index takes about 900 MB of disk. `read`: version 0.9.3 refused to serve on an empty index, and the index was not built here. Its `--help` lists the 8 query commands. | free, BSD-2-Clause |
| MCP server | [Hugging Face MCP server](https://huggingface.co/docs/hub/agents-mcp) | Searches the Hub's models, datasets and Spaces, so the agent finds today's open speech models, and runs a Space as a tool. `tried` 2026-11-11: `tools/list` with no token gave 4 tools, `hub_repo_search` among them. | the search answers with no account. A Space you add needs a Hugging Face account, and its docs name no price |

## When each earns its place

- **The skill** → the agent writes framework code that fails on an API that moved since it was trained, or it changes the voice agent's prompt and never holds a conversation with the result. `lk skills install` needs the LiveKit CLI 2.19.0 or later. Install it one way only: the plugin and `lk skills install` together load every description twice, by its README. The build, debug and test skills run on your machine. Simulations and deploys need a LiveKit Cloud project, free on the Build plan with 1,000 agent minutes a month by its [pricing](https://livekit.com/pricing). The `operating-livekit-agents` skill can deploy and roll back a live agent, so keep that step yours.
- **The guard** → the project calls a hosted speech API, or the agent copies a snippet from an older tutorial. It costs nothing until it speaks. For a Node project, change `path` to `**/*.ts`. Edit the list when a provider retires a model.
- **The MCP server** → a session with no shell. With a shell, `lk docs` gives the same lookups, by the server's own reference, and costs no context until it runs. `tried` 2026-11-11: `lk docs search "turn detection"` printed matching pages. Both skill installs add the server for you. Claude Code loads only the tool names until one is called, [by its docs](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search). One of the 9 tools, `submit_docs_feedback`, sends text to LiveKit, so read what the agent submits.
- **The CLI first** → a transcript, a narration or a first talk with a local agent needs no skill and no server, and costs no context until it runs.
  - Speech to text → `ffmpeg -i talk.mp3 -ar 16000 -ac 1 -c:a pcm_s16le talk.wav` → `whisper-cli -m models/ggml-base.en.bin -f talk.wav -osrt -of talk` writes `talk.srt` on your machine, with [whisper.cpp](https://github.com/ggml-org/whisper.cpp), MIT. Burning it into a clip is on the [Video](video.md) page. `tried` 2026-11-11: both commands ran as printed on a spoken test file, and `talk.srt` held the sentence with one word misheard.
  - Text to speech → `uvx pocket-tts generate --text "Hello."` writes `tts_output.wav` on a CPU, with [Pocket TTS](https://github.com/kyutai-labs/pocket-tts), MIT. `read`: two tries of up to 15 minutes did not finish the download on this run's slow network. On Linux the plain line pulls the CUDA build of `torch`, over 1 GB, and adding `--index https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match` takes the 200 MB CPU build instead.
  - A voice agent to talk to, with no key → `pip install speech-to-speech` → `speech-to-speech local`, with [speech-to-speech](https://github.com/huggingface/speech-to-speech), Apache-2.0. `read`: it needs a microphone and a speaker, and on Linux its `torch` dependency pulls the CUDA build, a download over 1 GB.

## Left out, and why

- [ElevenLabs MCP server](https://github.com/elevenlabs/elevenlabs-mcp) → archived on GitHub, with its last commit in August 2026. Its maker's skills are in the table above.
- [Coqui TTS](https://github.com/coqui-ai/TTS) → no commit since August 2024, far past the three months this kit asks for.
- [`whisper-1` and `tts-1` through the OpenAI API](https://developers.openai.com/api/docs/deprecations) → the names older tutorials use, and both are on the removal list the guard reads.

## A sample to study

[LiveKit Agents starter for Python](https://github.com/livekit-examples/agent-starter-python) → a working voice agent laid out for a coding agent: a short `AGENTS.md` that sends it to the live docs, conversation scenarios that CI runs on every merge to `main`, and a turn test kept as a commented example. MIT. `referenced`. Opened 2026-11-11: last push 2026-11-10, a 62 line `AGENTS.md`, not archived.

## How to do it better

- **It runs on LiveKit Cloud and hosted models** → the whole loop also runs on your machine: `speech-to-speech serve` as the realtime model and `livekit-server --dev` as the room, in [this example](https://github.com/huggingface/speech-to-speech/tree/main/demo/livekit). Its makers tested it on Apple Silicon only.
- **Its turn test ships commented out, and its `AGENTS.md` only asks the agent to try a change before calling it done** → a request can be skipped. Uncomment the test, set `test` to `uv run pytest`, and the `tests` guard blocks "done" while it fails.
- **Its scenarios run after the merge, because each run pays for inference** → keep them there, and run `lk agent debugger` after every edit. Its text mode costs only your agent's own model and tool calls, by LiveKit's [coding agent guide](https://docs.livekit.io/intro/coding-agents/).
- **Nothing in it watches model names** → add the recipe above.
- **Its keys sit in `.env.local`** → the built-in `secrets` guard blocks a command that prints that file.

## Where people talk

- [r/speechtech](https://www.reddit.com/r/speechtech/) → news of speech technology: new models, papers and datasets.
- [r/voiceagents](https://www.reddit.com/r/voiceagents/) → people building voice agents and call automation: call flows, SIP and WebRTC trouble.
- [r/TextToSpeech](https://www.reddit.com/r/TextToSpeech/) → text to speech engines, open and paid, talked through by the people who use them.
- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) → running open models on your own hardware.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Tried 2026-11-11 in a container, each with its evidence above: LiveKit Agent Skills, the guard, the LiveKit Docs server and `lk docs`, the ElevenLabs skills, `secrets`, `tests`, the Hugging Face server's tool list and the whisper.cpp transcript. Still `read`: Twilio for AI, which needs an account, Pipecat Context Hub, whose index was not built, Pocket TTS, whose download did not finish, and speech-to-speech, which needs a microphone.
