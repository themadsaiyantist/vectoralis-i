# Local and Open Models

Running a language model on your own machine: the runtime that loads it, the quantized weights that make it fit, the small models worth the disk space, tuning one with an adapter and serving it to a coding agent. Read this page when you want an agent that works with the network off, code that never leaves your disk, or a model you can change yourself.

**Contents:** What it is · Why now · Start here · Resources · Build this · The kit · Where people talk · The future

## What it is

- **An open model** is a file of weights, such as Gemma 4, Qwen3.8 or gpt-oss, that you download once and run on your own hardware → nothing leaves the machine, and nothing is billed per token.
- **The stack has three layers** → the weights, quantized to fit your memory → the runtime that loads them, such as Ollama, LM Studio, llama.cpp or MLX → the local server your tools call.
- **Tuning** means training a small adapter on your own examples while the model itself stays frozen → the method is called LoRA, and it runs on one consumer GPU or a free notebook.

## Why now

- **A coding agent on a local model became one command** → Ollama added an Anthropic-compatible API on January 16 and `ollama launch` on January 23, which starts Claude Code or Codex on a local model with no config file to edit → `read` [Ollama blog](https://ollama.com/blog/launch)
- **Gemma 4 shipped under Apache 2.0** on April 2 → sizes from a phone-size E2B to a 31B, with 128K to 256K of context → `read` [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)
- **Qwen kept shipping open weights all year** → Qwen3.5 from February in sizes from 0.8B to 397B, Qwen3.6 in April aimed at agentic coding, Qwen3.8-27B on August 14 → `read` [Qwen repository](https://github.com/QwenLM/Qwen3.8)
- **Apple Silicon got a faster engine** → Ollama moved to MLX in preview on March 30 and measured decoding at 112 tokens per second against 58 before, on Qwen3.5-35B-A3B → `read` [Ollama blog](https://ollama.com/blog/mlx)
- **llama.cpp turned into one command** → its README was rewritten on July 30 around `llama serve -hf <repo>`, which downloads a model from Hugging Face and serves it with a web UI, an OpenAI-compatible API and an Anthropic-compatible one → `read` [llama.cpp](https://github.com/ggml-org/llama.cpp)

## Start here

- ⬜ Size your machine first → at 4-bit the Gemma 4 weights take 2.9 GB for E2B, 6.7 GB for 12B, 14.4 GB for 26B A4B and 17.5 GB for 31B, before the context window is counted → `read` [Gemma docs](https://ai.google.dev/gemma/docs/core)
- ⬜ Install one runtime → Ollama or LM Studio → both run GGUF files through llama.cpp, both use MLX on Apple Silicon, and both serve the model on a local port → `read` [Ollama quickstart](https://docs.ollama.com/quickstart) · [LM Studio docs](https://lmstudio.ai/docs/app)
- ⬜ Run a first model → `ollama pull gemma4:e2b`, a download of about 7.2 GB → `ollama run gemma4:e2b` → switch the network off and ask it something → `read` [Ollama quickstart](https://docs.ollama.com/quickstart)
- ⬜ Read the file name before you download → `Q4_K` stores about 4.5 bits per weight, `Q6_K` about 6.6 and `Q8_0` stores 8 → fewer bits is a smaller file, so start at `Q4_K` and go up only when memory allows → `read` [Hugging Face GGUF docs](https://huggingface.co/docs/hub/gguf)
- ⬜ Raise the context window before you blame the model → Ollama defaults to 4k under 24 GiB of VRAM, and coding tools need at least 64000 → `OLLAMA_CONTEXT_LENGTH=64000 ollama serve` → check it with `ollama ps` → `read` [Ollama docs](https://docs.ollama.com/context-length)
- ⬜ Point your coding agent at it → `ollama launch claude` or `ollama launch codex`, and Codex also takes `codex --oss` → pick a model that lists `tools` under `ollama show` → Anthropic does not support Claude Code on non-Claude models, so treat that pairing as an experiment → `read` [Ollama: Claude Code](https://docs.ollama.com/integrations/claude-code) · [Ollama: Codex](https://docs.ollama.com/integrations/codex) · [Claude Code: gateways](https://code.claude.com/docs/en/llm-gateway)
- ⬜ Tune a small model with an adapter → open an Unsloth notebook on a free Colab GPU → LoRA trains two small matrices beside the frozen weights, and QLoRA loads the base model in 4-bit to save memory → `read` [Unsloth guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide)
- ⬜ Serve what you tuned → export it to GGUF → write a `Modelfile` whose `FROM` line points at the file → `ollama create -f Modelfile my-model` → `ollama run my-model` → `read` [Ollama blog](https://ollama.com/blog/improved-performance-and-model-support-with-gguf)

## Resources

| Resource | Free or paid | Clarity | Depth | Hands-on | Current | Excels at |
|---|---|---|---|---|---|---|
| [Ollama docs](https://docs.ollama.com/quickstart) | free | ★ 9 | ★ 5 | ★ 9 | ★ 10 | The shortest path from nothing to a model that answers. Better than the others at wiring a coding agent: one command for Claude Code, one for Codex. |
| [LM Studio docs](https://lmstudio.ai/docs/app) | free | ★ 8 | ★ 5 | ★ 8 | ★ 9 | The desktop app route: search Hugging Face, download and chat in one window. Better than the others when you want no terminal. |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | free | ★ 6 | ★ 9 | ★ 8 | ★ 10 | The engine under most local tools. Better than the others on control: every flag, every backend, your own quantization. |
| [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) | free | ★ 9 | ★ 8 | ★ 7 | ★ 7 | How the models work, then chapter 11 on fine-tuning with chat templates and LoRA. Better than the others at theory you can run. |
| [Unsloth fine-tuning guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide) | free | ★ 8 | ★ 6 | ★ 10 | ★ 8 | Fine-tuning on a free notebook, then the export to GGUF. Better than the others at getting a tuned model back into your runtime. |
| [smol-course](https://github.com/huggingface/smol-course) | free | ★ 8 | ★ 6 | ★ 9 | ★ 7 | Tuning and evaluating small models, in units built to run on most local machines. Better than the others when you have no GPU budget. |
| [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) | free · [the book](https://www.manning.com/books/build-a-large-language-model-from-scratch) beside it is `paid`, $54.99 once | ★ 9 | ★ 10 | ★ 9 | ★ 7 | Building a small GPT yourself in PyTorch, LoRA included, on a laptop. Better than the others at what happens inside the weights. |

## Build this

| Project | Difficulty | What it teaches | A repository to study |
|---|---|---|---|
| A private chat over your own files | ★ 3 | ★ 6 → retrieval, embeddings and a local server behind a real interface | `referenced` [open-webui/open-webui](https://github.com/open-webui/open-webui) |
| A coding agent that works with the network off | ★ 4 | ★ 7 → context windows, tool calls and where a small model breaks | `referenced` [anomalyco/opencode](https://github.com/anomalyco/opencode) |
| One model quantized four ways, compared on your own prompts | ★ 5 | ★ 8 → what each bit costs in memory, speed and answers | `referenced` [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) |
| A small model tuned on your own examples with LoRA | ★ 6 | ★ 9 → datasets, chat templates, adapters and the export to GGUF | `referenced` [unslothai/notebooks](https://github.com/unslothai/notebooks) |
| A model that runs inside a browser tab | ★ 6 | ★ 7 → inference on the user's device with no server at all | `referenced` [mlc-ai/web-llm](https://github.com/mlc-ai/web-llm) |
| A small chat model trained from scratch on a rented GPU | ★ 9 | ★ 10 → tokenizer, pretraining, tuning and serving in one codebase | `referenced` [karpathy/nanochat](https://github.com/karpathy/nanochat) |

## The kit

- [kit/coding.md](../kit/coding.md) → the picks for everyday coding. Keep the guards on when the model behind your agent is local.
- [kit/data-ml.md](../kit/data-ml.md) → the picks for notebooks, datasets and training runs. Take them for the tuning step.
- [kit/agents.md](../kit/agents.md) → the picks for building agents. Take them when you write your own loop on a local endpoint.
- [kit/devops.md](../kit/devops.md) → the picks for containers and servers. Take them when the model moves off your laptop.
- [kit/security.md](../kit/security.md) → the picks for security work. A local server is an open port, so keep it on your own machine.

## Where people talk

- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) → new open weights tested the day they land, llama.cpp changes and hardware builds.
- [r/LocalLLM](https://www.reddit.com/r/LocalLLM/) → which model fits which machine, asked and answered in plain terms.
- [r/ollama](https://www.reddit.com/r/ollama/) → Ollama setup problems, model picks for a given amount of VRAM and a Friday demo thread.
- [llama.cpp Discussions](https://github.com/ggml-org/llama.cpp/discussions) → the official forum of the engine: measured speeds, new backends and design proposals.
- [Hugging Face Forums](https://discuss.huggingface.co/) → the official forum for the Hub, with boards for beginners, datasets and research.
- [Unsloth Discord](https://discord.gg/unsloth) → the official server for fine-tuning questions.

## The future

- **The model that fits one GPU keeps moving up** → this year a 27B open model was aimed at agentic coding and a phone-size one took images and audio → the work that needs a hosted model keeps shrinking.
- **One local server for every tool** → llama.cpp, Ollama, LM Studio and vLLM all speak the OpenAI format and the Anthropic format today → the model behind an agent turns into a setting.
- **Tuning moves from notebooks to a button** → Unsloth now has a web UI and a desktop app that train a model with no code, and Ollama has said it will make tuned models easier to import.
- **Local and hosted in one session** → `ollama launch` already takes a local model or a cloud one → private and cheap steps stay on your machine, and the hard ones go out.

The stars are a judgment, made on 2026-11-11. Verified 2026-11-11: every link opened.
