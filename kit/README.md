# The Kit

What to install for the work in front of you: one skill, one guard and one MCP server for each of nineteen situations, and at most four more worth knowing. It is the opposite of a directory. Find your situation, read that one page.

**Contents:** By what you do · By who you are · How to read a page · How a pick is chosen · See also

---

## By what you do

### Build

| The situation | Skill | Guard | MCP server |
|---|---|---|---|
| [Coding](coding.md) | Skills For Real Engineers | `tests` | Context7 |
| [Frontend and UI](frontend.md) | frontend-design | `no-click-div` | Chrome DevTools MCP |
| [Backend, databases and APIs](backend.md) | Supabase Postgres Best Practices | `no-db-reset` | DBHub |
| [Mobile](mobile.md) | Expo Skills | `no-public-secret` | Mobile MCP |
| [Games and 3D](games-3d.md) | awesome-gamedev-agent-skills | `no-old-three-api` | Blender MCP server |

### Think

| The situation | Skill | Guard | MCP server |
|---|---|---|---|
| [Reasoning](reasoning.md) | grill-me | `plan-no-holes` | Sequential Thinking |
| [Research](research.md) | research | `claim-needs-source` | Context7 |
| [Data and ML](data-ml.md) | Hugging Face skills | `paid-compute` | Hugging Face MCP server |

### Make

| The situation | Skill | Guard | MCP server |
|---|---|---|---|
| [Design](design.md) | Impeccable | `raw-colour` | Penpot MCP |
| [Images](images.md) | draw.io skill | `keep-originals` | Hugging Face MCP server |
| [Animation](animation.md) | Motion AI Kit | `no-transition-all` | Chrome DevTools for agents |
| [Video](video.md) | HyperFrames | `ffmpeg-overwrite` | Comfy MCP |
| [Voice and audio](voice.md) | LiveKit Agent Skills | `retired-speech-model` | LiveKit Docs MCP server |
| [Docs and writing](docs.md) | Anthropic document skills | `local-path` | MarkItDown MCP |

### Ship and run

| The situation | Skill | Guard | MCP server |
|---|---|---|---|
| [Testing and browsers](testing.md) | Playwright CLI | `no-skipped-test` | Chrome DevTools MCP |
| [Review and security](security.md) | differential-review | `new-dependency` | Socket MCP |
| [DevOps and cloud](devops.md) | HashiCorp Agent Skills | `plan-before-apply` | Terraform MCP server |
| [Team tools](team-tools.md) | Slack skills plugin | `your-voice` | Linear MCP server |
| [Agents building agents](agents.md) | skill-creator | `mcp-stdout` | OpenAI Docs MCP |

---

## By who you are

| You are | Start with |
|---|---|
| A developer who ships features | [Coding](coding.md) → [Testing and browsers](testing.md) → [Review and security](security.md) |
| A designer who codes | [Design](design.md) → [Frontend and UI](frontend.md) → [Animation](animation.md) |
| A creator: images, video, voice | [Images](images.md) → [Video](video.md) → [Voice and audio](voice.md) |
| A data or ML person | [Data and ML](data-ml.md) → [Research](research.md) → [DevOps and cloud](devops.md) |
| A lead or a founder | [Team tools](team-tools.md) → [Reasoning](reasoning.md) → [Agents building agents](agents.md) |

---

## How to read a page

- **The picks** → one of each kind. Start there, and stop there if it does the job.
- **Also worth it** → at most four more of each kind, one line each.
- **When each earns its place** → the signal that it now pays for itself, and what it costs in context. Often a plain command does the job at no cost, and the page says so first.
- **Left out, and why** → the well-known options that did not make the page.
- **A sample to study** → one public example, and how to do it better.
- **Every entry is marked `read`** → it was read in its maker's own docs on the date at the bottom of the page. Nothing here was installed by this repository, and nothing is installed for you: the page gives the line, and you run it.
- **A guard in backticks with a recipe under the table** is a file you save as `harness/guards/<id>.json`. It runs in light and in heavy, and it starts at `warn`. Each recipe was proved by the engine before it was printed. [Guards](../guide/guards.md)

---

## How a pick is chosen

1. It does the job the situation needs, today.
2. Free and open first. A paid one only where nothing free does the job, marked `paid` with its price.
3. From the tool's own maker before a third party.
4. Alive: a commit in the last three months, not archived.
5. It costs little context for what it gives.

---

## See also

- [MCP](../guide/mcp.md) → when a server earns its context, and when a command is the better choice.
- [Safety](../guide/safety.md) → read it before you install anything that runs with your access.
- [The communities](../community/README.md) → where the people of each situation talk.
