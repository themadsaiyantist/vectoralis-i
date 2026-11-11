# Mobile

Mobile work is building iOS and Android apps, native or from one shared codebase, and running the result in a simulator. Read this page when the agent writes screens it has never seen run, and before it touches the keys an app carries.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [Expo Skills](https://github.com/expo/skills) | 23 skills from the Expo team for one codebase on both platforms: routing, native UI, data, native modules, SDK upgrades. Seven of them, the `eas-*` ones, cover EAS, Expo's cloud services: free up to a limit, then from $19 a month, [by its pricing page](https://expo.dev/pricing). MIT. `tried` 2026-11-11: the `expo` plugin holds 23 skills and passes `claude plugin validate`, and the skills CLI line installed 25, an experimental skill and an eval skill added. | Claude Code, Codex | 23 descriptions in every session, each body loads on use. The plugin also connects the Expo MCP server | `claude plugin install expo@claude-plugins-official`. Codex: `codex plugin add expo@openai-curated`. The skills with no server: `npx skills@latest add expo/skills --skill '*'` |
| Guard | `no-public-secret` | Warns when a secret gets a name that starts with `EXPO_PUBLIC_`, which ships it inside the app. `tried` 2026-11-11: the engine's proof passes on its 2 payloads. | both | none, a hook costs no context | below |
| MCP server | [Mobile MCP](https://github.com/mobile-next/mobile-mcp) | Drives an iOS simulator, an Android emulator or a real device through one set of tools: read the screen as an accessibility tree, tap, type, swipe, take a screenshot, read the logs. Apache-2.0. `tried` 2026-11-11: 1.0.17 answered `tools/list` with no device attached. | Claude Code, Codex | 35 tools: the 34 of its README and `get_more_tools` | `claude mcp add mobile-mcp -- npx -y @mobilenext/mobile-mcp@latest`. Codex: `codex mcp add mobile-mcp npx "@mobilenext/mobile-mcp@latest"` |

Whatever sits in an app bundle can be read by anyone who installs the app, and [Expo's docs](https://docs.expo.dev/guides/environment-variables/) say it of this prefix in plain words.

```json
{
  "id": "no-public-secret",
  "why": "an EXPO_PUBLIC_ variable ships inside the app, in plain text",
  "on": "write",
  "pattern": "EXPO_PUBLIC_[A-Z0-9_]*(SECRET|PRIVATE|SERVICE_ROLE|OPENAI|ANTHROPIC)",
  "mode": "warn",
  "message": "This name puts a secret inside the app bundle, where anyone can read it. Keep the key on a server and call the server.",
  "payloads": [
    { "name": "catches a secret behind the public prefix", "path": ".env", "text": "EXPO_PUBLIC_STRIPE_SECRET_KEY=changeme", "expect": "hit" },
    { "name": "passes a publishable key", "path": ".env", "text": "EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY=changeme", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/no-public-secret.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [Android skills](https://github.com/android/skills) | Google's own, written for the tasks where its evaluations show models do worst, such as R8 rules and edge-to-edge screens. `tried` 2026-11-11: 36 skills, `r8-analyzer` and `edge-to-edge` among them, and the repository passes `claude plugin validate`. | free, Apache-2.0 |
| Skill | [SwiftUI Pro](https://github.com/twostraws/SwiftUI-Agent-Skill) | Current SwiftUI for iOS 26 and later and Swift 6.4: navigation, state, accessibility, and the deprecated API a model still reaches for. `tried` 2026-11-11: one skill, which now makes iOS 27 the default target, and the repository passes `claude plugin validate`. | free, MIT |
| Skill | [Flutter agent plugins](https://github.com/flutter/agent-plugins) | The Flutter team's skills for widget tests, layout fixes and routing, with the Dart and Flutter MCP server wired in. `tried` 2026-11-11: the `dart-flutter` plugin 1.0.7 holds 25 skills, starts `dart mcp-server`, and passes `claude plugin validate`. | free, BSD-3-Clause |
| Skill | [Callstack Agent Skills](https://github.com/callstackincubator/agent-skills) | React Native from a team that ships it: performance, navigation, upgrades, tests, and a path from a native app to React Native. `tried` 2026-11-11: 9 skills in 3 plugins, and the marketplace passes `claude plugin validate`. | free, MIT |
| Guard | [`secrets`](../guide/guards.md) | Built in, light profile. Blocks a private key or a Google API key written into a file, such as a signing key pasted into the project. `tried` 2026-11-11: it blocked a Google API key in `app.py`, exit 2, and its payloads behave, a private key among them. | free, ours |
| Guard | [`locks`](../guide/locks.md) | Built in, heavy profile. Lock `ios/` and `android/` in a project that generates them with `npx expo prebuild`, where a hand edit is lost on the next clean run. `tried` 2026-11-11: a locked path blocked a write, exit 2. | free, ours |
| MCP server | [Xcode's MCP server](https://developer.apple.com/documentation/xcode/giving-external-agents-access-to-xcode) | Apple's own. An agent outside Xcode uses the open project and Xcode's tools, the build among them. One line connects Claude Code, one connects Codex. `read`: needs macOS and Xcode. | free with Xcode |
| MCP server | [MobileBuildMCP](https://github.com/getsentry/MobileBuildMCP) | Builds, runs and tests iOS and macOS projects through `xcodebuild`, as a server or as a CLI. It was XcodeBuildMCP until the rename. `tried` 2026-11-11: `npx -y mobilebuildmcp@2.7.1 mcp` listed 24 tools on Linux. A build needs macOS and Xcode. | free, MIT |
| MCP server | [Expo MCP server](https://docs.expo.dev/mcp/) | Expo's own: docs, EAS builds and workflows, crash reports, store reviews. 53 tools. It needs an Expo account, and its docs search and cloud simulator are paid. `read`: needs an Expo account. | free account, paid parts |
| MCP server | [Maestro MCP](https://docs.maestro.dev/get-started/maestro-mcp) | 9 tools that inspect the screen and run Maestro flows on a simulator or an emulator, so a check the agent made once becomes a test that stays. `read`: its docs list the 9 tools, 3 of them for Maestro Cloud. The CLI needs Java, and neither finished downloading here in ten minutes. | free, Apache-2.0 |

## When each earns its place

- **The skill** → the agent writes React Native from two SDK versions ago, or edits the native folders Expo generates. On a native-only app take the platform's own instead: Android skills or SwiftUI Pro.
- **The guard** → the first time the app talks to an API you pay for. It reads names, so it does not see a secret that was given an innocent one. The fix it asks for is a server between the app and the API.
- **The MCP server** → the agent changes a screen and nobody has seen it run. Four of the 35 tools work with devices in the maker's cloud, so leave those unused on your own machine. It sends anonymous usage data unless `MOBILEMCP_DISABLE_TELEMETRY=1` is set. Claude Code loads only the tool names until one is called, [by its docs](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search), and [Codex's MCP page](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) gives `disabled_tools` to drop the ones you do not want.
- **The CLI first** → [`agent-device`](https://github.com/callstack/agent-device) does the same job from the shell on both platforms: `npm install -g agent-device@latest`, then `agent-device snapshot -i` and `agent-device screenshot`. Google's [`android`](https://developer.android.com/tools/agents/android-cli) CLI runs an app on an emulator and reads its screen. Neither costs context until it runs.

## Left out, and why

- [Radon IDE](https://radon.swmansion.com/pricing) → its AI assistant sits in the Pro plan at $25 a month, and its free plan is for non-commercial use. The picks above run a simulator for free.
- [ios-simulator-mcp](https://github.com/joshuayoes/ios-simulator-mcp) → iOS only. Mobile MCP covers both platforms with one server.

## A sample to study

[Expensify App](https://github.com/Expensify/App) → a production React Native app, open source, with its agent setup in the repository: one `AGENTS.md` that `CLAUDE.md` imports, skills that drive the app on iOS and Android through `agent-device` and record a video as evidence for a pull request, and a [`settings.json`](https://github.com/Expensify/App/blob/main/.claude/settings.json) that formats every edited file and allows the Sentry and Playwright tools one by one. `referenced`

## How to do it better

- **The post-edit checklist is prose: lint, type check, compiler check, spelling** → put those commands in the `test` setting, and the `tests` guard runs them before the agent says done.
- **Its one hook formats, and nothing blocks** → add the guards a machine can be sure of, starting with `secrets`.
- **The skills live in `.claude/skills`, where Codex does not look** → keep shared skills in `.agents/skills`, or install them for both agents with the skills CLI.
- **Evidence is a video a person has to watch** → keep the flow as a test as well. `agent-device` saves the steps as a replay script and exports Maestro YAML, and CI runs it on every change.
- **`AGENTS.md` does not say which keys the app may hold** → write the rule down and guard it: publishable keys in the bundle, everything else behind your server.

## Where people talk

- [r/reactnative](https://www.reddit.com/r/reactnative/) → React Native and Expo in practice.
- [r/iOSProgramming](https://www.reddit.com/r/iOSProgramming/) → Swift, SwiftUI, Xcode and the App Store.
- [r/androiddev](https://www.reddit.com/r/androiddev/) → Kotlin, Compose and the Android toolchain.
- [r/FlutterDev](https://www.reddit.com/r/FlutterDev/) → Flutter and Dart.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Tried 2026-11-11, in Docker or through this repository's engine: every entry but three, each with its evidence. A server tried here answered `tools/list` with no device attached, and no app was driven. Still `read`: Xcode's server, which needs macOS, the Expo server, which needs an account, and Maestro MCP. The sample was opened and is alive.
