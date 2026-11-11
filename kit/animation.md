# Animation

Animation is motion written as code: transitions and scroll effects on a web page, and titles, charts and explainers rendered to video from HTML. Read this page when a page should move without stutter, or when a moving chart or title should come out of a repository instead of an editor.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [Motion AI Kit](https://github.com/motiondivision/ai-kit) | The `/motion` skill from the maker of Motion: rules for motion on a page in React, Vue and plain JavaScript, when plain CSS is enough, and a search of the current Motion docs. MIT. | Claude Code, Codex | one skill description in every session, and one subagent description in Claude Code. The body loads on use. The installer also adds Motion's hosted docs server, and the docs give no count of its tools | `npx motion-ai`, for both agents |
| Guard | `no-transition-all` | Warns when CSS or a Tailwind class puts a transition on every property. | both | none, a hook costs no context | below |
| MCP server | [Chrome DevTools for agents](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Gives the agent a real Chrome: it records a performance trace, emulates reduced motion and a slow CPU, takes screenshots and records the page as MP4. From the Chrome DevTools team, Apache-2.0. | Claude Code, Codex | 63 tools in its reference, 3 with `--slim` | `claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest`. Codex: `codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest` |

`transition: all` is the shortest transition to write, and it animates every property that changes, layout properties included.

```json
{
  "id": "no-transition-all",
  "why": "transition: all animates every property that changes, layout properties included",
  "on": "write",
  "path": "src/**",
  "pattern": "transition(?:-property)?\\s*:\\s*['\"]?all\\b|\\btransition-all\\b",
  "mode": "warn",
  "message": "A transition on every property is about to ship. Name the properties, and keep to transform and opacity where you can.",
  "payloads": [
    { "name": "catches it in CSS", "path": "src/styles/card.css", "text": ".card { transition: all 0.3s ease; }", "expect": "hit" },
    { "name": "catches the Tailwind class", "path": "src/components/Card.tsx", "text": "<div className=\"rounded-lg transition-all duration-300\">", "expect": "hit" },
    { "name": "passes named properties", "path": "src/styles/card.css", "text": ".card { transition: transform 0.2s ease-out, opacity 0.2s ease-out; }", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/no-transition-all.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [HyperFrames](https://github.com/heygen-com/hyperframes) | For motion that must become a file: a video written as HTML, moved with GSAP, CSS or the Web Animations API, and rendered to MP4. It is the skill pick of the [Video](video.md) page, where the install lines are. | free, Apache-2.0. Its Pro plan is `paid`, [$25 a month](https://hyperframes.studio/pricing) |
| Skill | [Remotion skills](https://www.remotion.dev/docs/ai/skills) | The same job in React components: `npx skills add remotion-dev/skills`. | free for individuals and companies of up to 3 employees. Above that `paid`, [$25 a seat a month, $100 a month minimum](https://www.remotion.dev/docs/license/pricing) |
| Skill | [emilkowalski/skills](https://github.com/emilkowalski/skills) | The craft of interface motion as separate skills, for any library: build an animation, review one, fix dropped frames, decide what should not move. `npx skills@latest add emilkowalski/skills`. | free, MIT |
| MCP server | [LottieFiles Creator MCP](https://docs.lottiefiles.com/en/creator-mcp) | Makes a small looping animation from a brief and exports Lottie JSON, dotLottie or video: loaders, success states, animated icons. | free to connect. Generated media uses the free plan's free uses, then AI credits |

## When each earns its place

- **The skill** → the project animates more than a hover: elements that enter and leave, layout that changes, gestures, scroll. It brings the rules an agent skips, such as which properties to animate, how long a UI animation runs and what to do under reduced motion. It costs one hosted MCP server beside the skill. Part of the skill points at a paid plan: audits, example source and the transition editor need Motion+, `paid`, [$399 once](https://motion.dev/plus). The rules and the docs search stay free.
- **The guard** → as soon as an agent writes CSS for you. It costs nothing until it speaks. Set `path` to where your styles live. [web.dev](https://web.dev/articles/animations-guide) says to avoid animating any property that triggers layout or paint, and `all` cannot tell which ones do.
- **The MCP server** → motion on a page has to be judged in a browser: dropped frames, layout shift, the page under reduced motion. It costs up to 63 tool definitions, where a flag such as `--category-memory=false` switches a group off, and usage statistics sent to Google unless you pass `--no-usage-statistics`. Claude Code loads only the tool names until one is called, [by its docs](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search).
- **The CLI first** → the same package ships [`chrome-devtools`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/cli.md), a CLI over the same tools, all but a few such as `wait_for` and `fill_form`, that costs no context until it runs: `npm i chrome-devtools-mcp@latest -g` → `chrome-devtools navigate_page 1 --url "http://localhost:3000"` → `chrome-devtools take_screenshot 1 --filePath frame.png`. Keep the server for a session with no shell.

## Left out, and why

- [GSAP's own skills](https://github.com/greensock/gsap-skills) → the library is alive and free to use, but the skills repository has no commit since 2026-04-21.
- [Motion Canvas](https://github.com/motion-canvas/motion-canvas) → no commit since 2026-07-02, outside the three-month rule.
- Manim → [the engine](https://github.com/ManimCommunity/manim) is alive, but its maker ships no skill, and the most starred community one, [manim_skill](https://github.com/adithya-s-k/manim_skill), has no commit since 2026-01-23.

## A sample to study

[NYT Graph](https://github.com/heygen-com/hyperframes/tree/main/registry/examples/nyt-graph) → a 15 second animated chart from the HyperFrames registry: bars and a line built as SVG from two arrays, every move placed on one paused GSAP timeline. HyperFrames previews it in a browser and renders it to video by seeking that timeline frame by frame. Two HTML files, about 500 lines. Marked `referenced`.

## How to do it better

- **It hard-codes six months of numbers and both axis maximums** → read a JSON file and compute the scales, so next month's chart is the same composition with a new input, and a larger value cannot leave the plot.
- **It pulls its fonts from Google Fonts and GSAP from a CDN** → put both in the project, so a render does not depend on the network.
- **Its start times are sums spread through the script, such as `1.5 + i * 0.5`** → keep them in one place as named constants or timeline labels, and a change of pace is one edit.
- **It ships no check** → run [`npx hyperframes check`](https://hyperframes.heygen.com/packages/cli), then `npx hyperframes snapshot my-video --at 1,5,9` and have the agent look at the stills. A full render is the slowest way to find a clipped label.
- **It is a video, so it never meets a slow phone or a person who asked for less motion** → on a page, put the same timeline behind a [`prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion) check, and trace it with the CPU throttled.

## Where people talk

- [r/css](https://www.reddit.com/r/css/) → transitions, scroll-driven animation and view transitions in plain CSS.
- [r/webdev](https://www.reddit.com/r/webdev/) → which library to use, and why a page stutters.
- [r/MotionDesign](https://www.reddit.com/r/MotionDesign/) → timing, easing and critique of finished pieces.
- [r/manim](https://www.reddit.com/r/manim/) → math and diagram animation written in Python.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
