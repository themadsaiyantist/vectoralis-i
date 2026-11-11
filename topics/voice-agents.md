# Voice and Real-Time Agents

Agents you talk to: speech to text, a model that decides what to say, text to speech, and the timing that turns the three into a conversation. Read this page when you want to build a voice assistant, put an agent on a phone number, or find out why a voice demo feels slow.

**Contents:** What it is · Why now · Start here · Resources · Build this · The kit · Where people talk · The future

## What it is

- **A voice agent** runs a loop called the cascade → speech to text, such as Deepgram Flux, `gpt-live-transcribe` or Parakeet → a language model → text to speech, such as ElevenLabs, Cartesia or Qwen3-TTS.
- **A speech-to-speech model** does the loop in one model, audio in and audio out, such as `gpt-realtime-2.1`, Gemini Live or PersonaPlex → fewer parts to wire, less control over each one.
- **The hard part is timing** → knowing when the person has finished, called turn taking → how fast the first sound comes back, called latency → what to do when they cut in, called interruption.

## Why now

- **Speech-to-speech models learned to reason, then to listen while they talk** → OpenAI released `gpt-realtime-2` with configurable reasoning on May 7, `gpt-realtime-2.1` on July 6, and made GPT-Live-1 generally available on September 10 for full-duplex conversations → `read` [OpenAI changelog](https://developers.openai.com/api/docs/changelog)
- **Older hosted transcription models are being retired** → OpenAI deprecated `whisper-1` and the `gpt-4o-transcribe` models on August 26, with shutdown on February 26, 2027, and points to `gpt-transcribe` and `gpt-live-transcribe` → `read` [OpenAI changelog](https://developers.openai.com/api/docs/changelog)
- **Full duplex went open** → NVIDIA published PersonaPlex in January, a speech-to-speech model built on Moshi that listens while it speaks and runs on your own GPU → `read` [NVIDIA/personaplex](https://github.com/NVIDIA/personaplex)
- **A whole voice agent runs on a laptop** → Hugging Face's speech-to-speech reached 1.0 in September, one command that starts a local pipeline and speaks the OpenAI Realtime protocol, and Ollama added text to speech on October 24 → `read` [huggingface/speech-to-speech](https://github.com/huggingface/speech-to-speech) · [Ollama blog](https://ollama.com/blog/speech-models)
- **Turn taking got its own models** → the June update of the voice AI primer describes the best setup as three layers: a short voice-activity trigger, an audio turn model and the language model's own decision → `read` [Voice AI & Voice Agents](https://voiceaiandvoiceagents.com/)

## Start here

- ⬜ Talk to an agent on your own machine → `pip install speech-to-speech` → `speech-to-speech local` → no API key, and the first run downloads the models → `read` [huggingface/speech-to-speech](https://github.com/huggingface/speech-to-speech)
- ⬜ Build the cascade from hosted parts → `uv tool install "pipecat-ai[cli]"` → `pipecat init quickstart` → put three keys in `.env`, one each for speech to text, the model and text to speech → `uv sync` → `uv run bot.py` → open `http://localhost:7860/client` → `read` [Pipecat quickstart](https://docs.pipecat.ai/pipecat/get-started/quickstart)
- ⬜ Measure voice-to-voice latency → the gap from the end of your sentence to the first sound of the answer → people answer each other in about 500 ms, and the primer sets 1,500 ms as the target for an agent → `read` [Voice AI & Voice Agents](https://voiceaiandvoiceagents.com/)
- ⬜ Replace the silence timer → a pause is not the end of a turn → add an audio turn model such as Smart Turn: open weights, 23 languages, 8 MB on CPU → `read` [pipecat-ai/smart-turn](https://github.com/pipecat-ai/smart-turn)
- ⬜ Handle the interruption → when the person cuts in, stop the speech and trim the history to what they heard → `read` [LiveKit: turns and interruptions](https://docs.livekit.io/agents/logic/turns/)
- ⬜ Try one speech-to-speech model → the OpenAI Realtime API over WebRTC in a browser, or the Gemini Live API → run the same script as your cascade and compare the delay and the mistakes → `read` [OpenAI Realtime guide](https://developers.openai.com/api/docs/guides/realtime) · [Gemini Live API](https://aistudio.google.com/docs/live-api)
- ⬜ Give it one tool → a function the agent calls in the middle of a conversation, such as an order lookup → listen to what it says while it waits.
- ⬜ Put it on a phone number → a SIP trunk into LiveKit, or Twilio ConversationRelay passing text to your WebSocket → test on a real call, because many phone platforms carry only 8 kHz audio → `read` [LiveKit telephony](https://docs.livekit.io/telephony/) · [Twilio ConversationRelay](https://www.twilio.com/docs/voice/conversationrelay)

## Resources

| Resource | Free or paid | Clarity | Depth | Hands-on | Current | Excels at |
|---|---|---|---|---|---|---|
| [Voice AI & Voice Agents: An Illustrated Primer](https://voiceaiandvoiceagents.com/) | free | ★ 9 | ★ 9 | ★ 4 | ★ 9 | The whole map on one page: the latency budget, turn detection, telephony, evaluation. Better than the others at why each part exists. |
| [Pipecat docs](https://docs.pipecat.ai/pipecat/get-started/quickstart) | free · the quickstart needs three API keys | ★ 8 | ★ 7 | ★ 10 | ★ 10 | An open-source framework where every stage of the pipeline is a part you can swap. Better than the others for building the cascade yourself. |
| [LiveKit Agents docs](https://docs.livekit.io/agents/start/voice-ai/) | free · the quickstart needs a free LiveKit Cloud account | ★ 8 | ★ 7 | ★ 9 | ★ 10 | Open-source agents on a WebRTC stack with phone calls built in. Better than the others on transport, telephony and interruptions. |
| [OpenAI Realtime guide](https://developers.openai.com/api/docs/guides/realtime) | free to read · needs an API key | ★ 8 | ★ 6 | ★ 8 | ★ 10 | One speech-to-speech model in a browser over WebRTC. Better than the others as the shortest path to a model that hears and speaks directly. |
| [Gemini Live API docs](https://aistudio.google.com/docs/live-api) | free to read · needs an API key | ★ 7 | ★ 6 | ★ 7 | ★ 10 | Live voice and vision in one session, in 70 languages. Better than the others when the agent must also see. |
| [Deepgram Flux docs](https://developers.deepgram.com/docs/flux/quickstart) | free to read · needs an API key | ★ 8 | ★ 5 | ★ 8 | ★ 10 | Speech recognition with end-of-turn detection inside the model. Better than the others at showing turn events in working code. |
| [Hugging Face Audio Course](https://huggingface.co/learn/audio-course/chapter0/introduction) | free | ★ 8 | ★ 8 | ★ 7 | ★ 4 | How sound becomes data, and how recognition and synthesis models work. Better than the others on fundamentals, and written in 2023. |

## Build this

| Project | Difficulty | What it teaches | A repository to study |
|---|---|---|---|
| A voice assistant that runs with no cloud at all | ★ 4 | ★ 8 → the full cascade on open models, and what each stage costs in delay | `referenced` [huggingface/speech-to-speech](https://github.com/huggingface/speech-to-speech) |
| A browser voice bot built from hosted parts you can swap | ★ 4 | ★ 8 → pipelines, transports and interruption handling | `referenced` [pipecat-ai/pipecat-examples](https://github.com/pipecat-ai/pipecat-examples) |
| A live captioner for meetings or streams | ★ 5 | ★ 7 → streaming recognition, partial and final transcripts | `referenced` [collabora/WhisperLive](https://github.com/collabora/WhisperLive) |
| A phone number that answers and books something | ★ 6 | ★ 9 → SIP, phone-grade audio and tool calls during a call | `referenced` [livekit/agents](https://github.com/livekit/agents) |
| Your own end-of-turn detector, measured against a silence timer | ★ 7 | ★ 9 → why timing decides how the agent feels | `referenced` [pipecat-ai/smart-turn](https://github.com/pipecat-ai/smart-turn) |
| A full-duplex model on your own GPU | ★ 8 | ★ 9 → what changes when the model listens while it talks | `referenced` [NVIDIA/personaplex](https://github.com/NVIDIA/personaplex) |

## The kit

- [kit/voice.md](../kit/voice.md) → the picks for speech work. Start with this one: it is the page for recognition and synthesis.
- [kit/agents.md](../kit/agents.md) → the picks for building agents. Take them for the part between hearing and speaking: the loop and its tool calls.
- [kit/backend.md](../kit/backend.md) → the picks for servers. Take them for the service that holds a live WebSocket or WebRTC session.
- [kit/testing.md](../kit/testing.md) → the picks for tests. Take them to replay a scripted conversation after every change.

## Where people talk

- [r/speechtech](https://www.reddit.com/r/speechtech/) → new open recognition and synthesis models, benchmarks and datasets.
- [r/voiceagents](https://www.reddit.com/r/voiceagents/) → people shipping phone agents: latency on real calls, echo, call flows.
- [r/TextToSpeech](https://www.reddit.com/r/TextToSpeech/) → voices and engines compared, open models against paid APIs.
- [Pipecat Discord](https://discord.gg/pipecat) → the official server of the framework.
- [LiveKit Community](https://community.livekit.io) → the official forum, with boards for Agents and Telephony.
- [OpenAI Developer Community](https://community.openai.com/) → the official forum for the OpenAI API.

## The future

- **Full duplex becomes the normal shape** → GPT-Live and PersonaPlex already listen while they speak → interruptions and small acknowledgements move from your code into the model.
- **A fast voice in front, a slower agent behind** → GPT-Live holds the conversation while a backend agent looks things up and uses tools → expect that split in most designs.
- **The cascade stays where control matters** → the primer's June update still finds a tuned cascade faster than the speech-to-speech models from OpenAI and Google, and it lets you log the text, swap one part and pick the voice.
- **Open and local keeps closing in** → one command runs a local agent today, and Ollama lists Windows and Linux speech support as coming → real-time voice with no provider becomes ordinary.

The stars are a judgment, made on 2026-11-11. Verified 2026-11-11: every link opened.
