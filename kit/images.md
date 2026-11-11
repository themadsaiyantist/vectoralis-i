# Images

Images are the pictures a project ships: generated art, edited photos, diagrams and SVG. Read this page when your agent should make or change an image inside the session, instead of you leaving for another app.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [draw.io skill](https://github.com/jgraph/drawio-mcp/blob/main/plugins/README.md) | Writes a diagram as a native `.drawio` file, from Mermaid or XML, and exports PNG, SVG or PDF with the source embedded, so the picture stays editable. From draw.io's maker, Apache-2.0. | Claude Code, Codex | one description in every session, and in Claude Code the 3 tools of the hosted server the plugin bundles. The body loads on use and fetches its reference from GitHub when it draws | `/plugin marketplace add jgraph/drawio-mcp` → `/plugin install drawio@drawio`. Codex: `codex plugin marketplace add jgraph/drawio-mcp` → `codex plugin add drawio@drawio` |
| Guard | `keep-originals` | Warns when `mogrify` is about to write over the images it was given. | both | none, a hook costs no context | below |
| MCP server | [Hugging Face MCP server](https://huggingface.co/docs/hub/agents-mcp) | Hugging Face's own hosted server: the agent searches the Hub and runs open models on Spaces as tools, an image model among them once you add its Space. No GPU needed. MIT. | Claude Code. Codex as a plain HTTP server with a token, which the maker's README does not spell out | the docs name one built-in tool, `hf_fs`, plus each tool and Space you switch on | `claude mcp add hf-mcp-server -t http https://huggingface.co/mcp?login`. Codex: in `~/.codex/config.toml`, a `[mcp_servers.huggingface]` table with `url = "https://huggingface.co/mcp"` and `bearer_token_env_var = "HF_TOKEN"` |

ImageMagick's [own page](https://imagemagick.org/mogrify/) says `mogrify` overwrites the original file, and a download or a render that was never committed has no copy in git.

```json
{
  "id": "keep-originals",
  "why": "mogrify writes over the files it is given, and an untracked original cannot be brought back",
  "on": "shell",
  "pattern": "\\bmogrify\\b(?![^|;&]*\\s-(?:path|format)\\b)",
  "mode": "warn",
  "message": "mogrify is about to write over its input files. Add -path with an output folder, or use magick with a new file name.",
  "payloads": [
    { "name": "catches a resize in place", "text": "mogrify -resize 1600x1600 assets/photos/*.jpg", "expect": "hit" },
    { "name": "passes an output folder", "text": "mogrify -path build/photos -resize 1600x1600 assets/photos/*.jpg", "expect": "pass" },
    { "name": "passes a new file", "text": "magick assets/logo.png -resize 512x512 build/logo-512.png", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/keep-originals.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [Comfy CLI skills](https://docs.comfy.org/agent-tools/cli) | `comfy skills install` teaches the agent the `comfy` CLI, so it drives a local ComfyUI with no MCP server. The main skill file is 78 KB, and the default install also appends every skill to `~/AGENTS.md`: pass `--target claude-code` to leave that file alone. | free, GPL-3.0 |
| Skill | [canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design) | Anthropic's skill for posters and other static pieces, drawn in code and saved as PNG or PDF. No image model needed. | free, Apache-2.0 |
| Guard | [`secrets`](../guide/guards.md) | Built in, light profile. A hosted image model needs a key or a token, and this guard blocks a key in a known format written into a file. | free, ours |
| MCP server | [Comfy MCP](https://github.com/Comfy-Org/comfy-mcp) | Comfy's own server for the ComfyUI on your machine, and the MCP pick of the [Video](video.md) page. 41 tools, each one wrapping a `comfy` command. | free, AGPL-3.0 or a commercial licence |
| MCP server | [Comfy Cloud MCP](https://docs.comfy.org/agent-tools/mcp) | The same engine on hosted GPUs, with a Claude Code plugin of ready commands. | `paid`, from [$20 a month](https://comfy.org/pricing/), with 5 free runs for a new account |
| MCP server | [draw.io MCP server](https://github.com/jgraph/drawio-mcp) | 3 tools that show the diagram inline in chat apps. A terminal gets a link instead. The Claude Code plugin above already bundles it. | free |

## When each earns its place

- **The skill** → a diagram must stay editable, use shape libraries such as AWS or Kubernetes icons, or leave the session as a file. It needs draw.io Desktop on the machine for PNG, SVG and PDF export. In Claude Code the plugin also adds the hosted draw.io server, which you can switch off under `/mcp`.
- **The guard** → the first time an agent resizes or converts a folder of images. It costs nothing until it speaks. Git brings back a tracked file. It does not bring back a download or a render that was never committed.
- **The MCP server** → the session needs a picture and the machine has no GPU for an image model. It costs one tool plus each Space you add, a Hugging Face account, and a [daily ZeroGPU quota](https://huggingface.co/docs/hub/spaces-mcp-servers) that PRO, `paid`, [$9 a month](https://huggingface.co/pricing), raises 8 times, to 40 minutes. A generated image comes back into the context as an image block unless the URL carries `?no_image_content=true`. The Codex lines join the server URL from Hugging Face's docs with the token setting from [Codex's MCP docs](https://learn.chatgpt.com/docs/extend/mcp).
- **The CLI first** → most image work needs no server and no skill, and costs no context until it runs.
  - A generation on your own GPU → `comfy run --workflow workflow.json --wait | comfy download` runs a workflow you exported, with [comfy-cli](https://github.com/Comfy-Org/comfy-cli). Comfy's docs put images at 8 GB of VRAM or more and send Mac users to the cloud.
  - An edit → one `magick` command with a new output name.
  - A flowchart that lives in Markdown → a Mermaid code block, which [GitHub renders](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).
  - An icon → SVG the agent writes as text. `magick icon.svg icon.png` [renders it](https://imagemagick.org/formats/), so the agent can look at what it drew.

## Left out, and why

- Codex's built-in `$imagegen` → [nothing to install](https://learn.chatgpt.com/docs/image-generation), but a closed model, `gpt-image-2`, that uses plan limits 3 to 5 times faster than a turn without an image. Paid, with a free equal on this page.
- [AUTOMATIC1111 web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) → no commit on its default branch since 2024-07-27.
- [Excalidraw MCP](https://github.com/excalidraw/excalidraw-mcp) → no commit since 2026-03-24, outside the three-month rule.

## A sample to study

[basic_api_example.py](https://github.com/Comfy-Org/ComfyUI/blob/master/script_examples/basic_api_example.py) → ComfyUI's default text to image workflow in API format, with the prompt and the seed changed in code and the job queued on a local server. About 120 lines, and nothing to install beyond Python. Marked `referenced`.

## How to do it better

- **It posts the job and exits** → read the answer, wait for the run and fetch the file, as [websockets_api_example.py](https://github.com/Comfy-Org/ComfyUI/blob/master/script_examples/websockets_api_example.py) beside it does, or let `comfy run --wait` carry the loop.
- **It holds the workflow as a string inside the script** → export it from ComfyUI with File → Export (API), commit the JSON, and let the agent change inputs by node number.
- **It sets a prompt and a seed and writes them nowhere** → write one manifest line per output: file, prompt, seed, model, workflow. Any image can then be made again.
- **It names a model file and assumes it is on disk** → `comfy validate --workflow workflow.json` catches unknown nodes, missing models and bad wiring before the GPU starts.
- **It never opens its output** → have the agent read the image and compare it with the brief before it says done.

## Where people talk

- [r/StableDiffusion](https://www.reddit.com/r/StableDiffusion/) → open image models, compared in the week they come out.
- [r/comfyui](https://www.reddit.com/r/comfyui/) → workflows passed around as files, and help when a node fails.
- [r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/) → how people connect image tools to a Claude Code session.
- [r/codex](https://www.reddit.com/r/codex/) → the same for Codex, built-in image generation included.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
