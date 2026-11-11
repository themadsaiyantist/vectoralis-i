# Generative Media

Generative media is making images, video and sound with models, as a pipeline you can script, rerun and review instead of a prompt typed into an app. Read this page when a project needs visuals at volume, such as product shots, explainer clips, game art or a short film, and you want your coding agent to drive the whole run.

**Contents:** What it is · Why now · Start here · Resources · Build this · The kit · Where people talk · The future

## What it is

- **A pipeline, not a prompt** → nodes or code that take a brief to a finished file: generate → edit → animate → upscale → assemble.
- **Two lanes** → open weights on your own GPU (MiniMax H3, LTX-2.5, Qwen-Image 2.1, FLUX 3 Image Klein) or a hosted model behind an API (GPT Image 2.6, Nano Banana 2.1, Gemini Omni Flash, Seedance 2.5, Wan 3.0).
- **The agent runs it** → it writes the workflow, calls the model through MCP or an API, looks at the result and tries again, while you approve the frames that matter.

## Why now

- **Open video reached the top of the board.** MiniMax H3 and LTX-2.5 both published open weights in August, and ComfyUI ran each on its release day. H3's open 768p checkpoint ranks third on the text to video board on 2026-11-11, and LTX-2.5 returns sound in sync and several connected shots from one generation. Both ship under community licenses, so read the terms before commercial use → `read` [Artificial Analysis](https://artificialanalysis.ai/video/leaderboard/text-to-video) · [ComfyUI changelog](https://docs.comfy.org/changelog)
- **An agent can drive the whole graph.** This year Comfy added an MCP connection: hosted at `https://cloud.comfy.org/mcp`, or local and open source with `pip install comfy-mcp`. An agent can search the templates, run a workflow and fetch the outputs, from Claude Code or Codex → `read` [Comfy MCP](https://docs.comfy.org/agent-tools/mcp)
- **Video in code is now written for agents.** Remotion ships official agent skills. HyperFrames, new in March under Apache 2.0, renders plain HTML to MP4 and describes itself as built for agents → `read` [Remotion skills](https://www.remotion.dev/docs/ai/skills) · [HyperFrames](https://github.com/heygen-com/hyperframes)
- **Hosted models were retired mid-year.** OpenAI removed the Videos API and both Sora 2 models on 2026-09-24 and lists no replacement. Google shut down the Veo 3.1 preview models on 2026-10-22 and points to Gemini Omni Flash → `read` [OpenAI deprecations](https://developers.openai.com/api/docs/deprecations) · [Gemini API video](https://aistudio.google.com/docs/video)
- **Marking became law in the EU.** Article 50 of the AI Act applies from 2026-08-02: providers mark generated output in a machine-readable format, and deployers label deepfakes → `read` [European Commission](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)

## Start here

- ⬜ Pick a lane → an NVIDIA RTX card with 8 GB of VRAM runs FLUX 3 Image Klein at home ([Black Forest Labs](https://bfl.ai/blog/flux-3-image-klein)) → no GPU: [Comfy Cloud](https://www.comfy.org/cloud/pricing) (`paid`, $20 a month) or a hosted API that bills per output, such as fal under Resources.
- ⬜ Install ComfyUI → `pip install comfy-cli` → `comfy install` → `comfy launch` ([Comfy CLI](https://docs.comfy.org/comfy-cli/getting-started) · [system requirements](https://docs.comfy.org/installation/system_requirements)).
- ⬜ Make one image by hand → seven nodes, one picture → after this you can read any graph ([your first image](https://docs.comfy.org/get_started/first_generation)).
- ⬜ Export it for code → File → Export Workflow (API) → a JSON file of numbered nodes, the form scripts and agents use ([workflow API format](https://docs.comfy.org/development/api-development/workflow-api-format)) → run it from the terminal: `comfy run --workflow my_workflow.json --wait`.
- ⬜ Connect your agent → local and free: `pip install comfy-mcp`, then register it with the line in [Comfy MCP](https://docs.comfy.org/agent-tools/mcp) → hosted: `claude mcp add --transport http comfy-cloud https://cloud.comfy.org/mcp` or `codex mcp add comfy-cloud --url https://cloud.comfy.org/mcp` → ask it to search the templates, run one and fetch the output.
- ⬜ Batch it → have the agent write a script → it posts the JSON to `/prompt` on `127.0.0.1:8188` once per prompt and seed → waits on the WebSocket → saves each file and one manifest line per output ([server API examples](https://docs.comfy.org/development/comfyui-server/api-examples)).
- ⬜ Add motion → pick your best still → run an image to video template → LTX-2.5 comes with templates for text, image, and first and last frame ([Comfy blog](https://blog.comfy.org/p/ltx-25-day-0-support-in-comfyui)).
- ⬜ Cut it in code → `npx create-video@latest` → `npx skills add remotion-dev/skills` → the agent builds titles, timing and captions as React → render the MP4.

## Resources

| Resource | Free or paid | Clarity | Depth | Hands-on | Current | Excels at |
|---|---|---|---|---|---|---|
| [ComfyUI documentation](https://docs.comfy.org/) | free | ★ 8 | ★ 8 | ★ 9 | ★ 10 | The node graph from a first image to the server API and the agent tools. Picks up new open models faster than anything else here. |
| [Diffusers documentation](https://huggingface.co/docs/diffusers/index) | free | ★ 8 | ★ 9 | ★ 8 | ★ 9 | The same models as plain Python: pipelines, LoRA, quantization, training. Better than a graph when the pipeline must live inside your own code. |
| [MIT 6.S184, flow matching and diffusion models](https://diffusion.csail.mit.edu/2026/index.html) | free | ★ 8 | ★ 10 | ★ 6 | ★ 8 | The math under every current model: flow matching, guidance, latent spaces, with notes, slides and three Colab labs. The only entry that explains why the settings work. |
| [Remotion documentation](https://www.remotion.dev/docs) | free · a company of more than three people needs a [license](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md) | ★ 9 | ★ 8 | ★ 9 | ★ 9 | Video as React components: timelines, captions, rendering on a server. The most complete path here from data to MP4. |
| [HyperFrames documentation](https://hyperframes.heygen.com/introduction) | free | ★ 8 | ★ 6 | ★ 8 | ★ 10 | Plain HTML and CSS rendered to MP4, written for agents, Apache 2.0. The shortest path here if you would rather not write React. |
| [Artificial Analysis video leaderboard](https://artificialanalysis.ai/video/leaderboard/text-to-video) and [image leaderboard](https://artificialanalysis.ai/image/leaderboard/text-to-image) | free | ★ 9 | ★ 4 | ★ 2 | ★ 10 | Which model leads today, from blind votes between pairs, with a filter for open weights. Better than any tutorial for choosing a model, and it changes fast. |
| [fal documentation](https://fal.ai/docs) | free · the API bills by use | ★ 8 | ★ 6 | ★ 8 | ★ 9 | One API over more than 1,000 hosted models. The easiest way here to swap a model without rewriting the client. |

## Build this

| Project | Difficulty | What it teaches | A repository to study |
|---|---|---|---|
| A batch image run: one workflow in API format, a list of prompts and seeds, a manifest of every output | ★ 3 | ★ 7 → a pipeline is a file you can run again | `referenced` [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) |
| A video made from data: release notes or stats in as JSON, a titled and captioned MP4 out | ★ 4 | ★ 8 → video as components, props and frames | `referenced` [remotion-dev/remotion](https://github.com/remotion-dev/remotion) |
| One character, twelve shots: train a LoRA on a small set of stills, then try the same shots with reference images alone | ★ 7 | ★ 9 → what keeps a face and a style stable across shots | `referenced` [ostris/ai-toolkit](https://github.com/ostris/ai-toolkit) |
| A storyboard to a short film: shot list → keyframes → video with sound from first and last frames → one cut | ★ 8 | ★ 9 → planning shots so they join | `referenced` [Lightricks/LTX-2](https://github.com/Lightricks/LTX-2) |
| An upscale pass: restore and upscale the final cut only, then compare every frame against its source | ★ 5 | ★ 6 → where detail is recovered and where it is invented | `referenced` [chaiNNer-org/chaiNNer](https://github.com/chaiNNer-org/chaiNNer) |
| A studio your agent runs: a manifest of stages, with an approval gate before every step that costs money | ★ 9 | ★ 10 → how an agent carries a production from brief to render | `referenced` [OpenMontageInc/OpenMontage](https://github.com/OpenMontageInc/OpenMontage) |

## The kit

- [kit/images.md](../kit/images.md) → the picks for generating and editing stills. Take the MCP server, so the agent can run the model and see the result.
- [kit/video.md](../kit/video.md) → the picks for cutting and rendering. Take the skill that teaches your agent the framework you chose.
- [kit/animation.md](../kit/animation.md) → the picks for motion in code: titles, transitions, diagrams that move.
- [kit/voice.md](../kit/voice.md) → the picks for narration and sound, for cuts where the model's own audio is not enough.
- [kit/design.md](../kit/design.md) → the picks for palette, type and layout rules, so every frame looks like the same project.

## Where people talk

- [r/StableDiffusion](https://www.reddit.com/r/StableDiffusion/) → open image and video models: first tests of new weights, workflows shared as files.
- [r/comfyui](https://www.reddit.com/r/comfyui/) → node graphs, custom nodes, and the fix for the error you just hit.
- [r/aivideo](https://www.reddit.com/r/aivideo/) → finished clips, a quick read on what each video model can do.
- [Comfy Org Discord](https://www.comfy.org/discord) → the official server: release news and help from the people who build ComfyUI.
- [Remotion Discord](https://www.remotion.dev/discord) → the official server for video in React.
- [Banodoco](https://banodoco.ai/) → a community for open source AI art, with its Discord linked from the page.

## The future

- **One model for picture, motion and sound** → [FLUX 3](https://bfl.ai/blog/flux-3) trains images, video and audio in one architecture, and H3 and LTX-2.5 already return video with its soundtrack. Pipelines get shorter.
- **The agent becomes the operator** → tool makers now ship their own MCP servers and skills. Your work moves to the brief, the checks and the approval gates.
- **Marking becomes a render step** → with Article 50 in force, a machine-readable mark on generated media is part of shipping to the public.
- **Models keep changing under you** → open weights are near the top for video and still behind hosted models for stills. Keep the model behind one function, so a swap is one line.

The stars are a judgment, made on 2026-11-11. Verified 2026-11-11: every link opened.
