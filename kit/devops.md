# DevOps and cloud

DevOps and cloud work is what happens between a merged change and a running system: CI pipelines, deploys, containers, infrastructure as code, and reading logs when something breaks. Read this page before an agent's shell holds cloud credentials, and when you want it to write Terraform or explain a failed pipeline.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [HashiCorp Agent Skills](https://github.com/hashicorp/agent-skills) | 16 Terraform skills from its maker: style, tests, module refactoring, import, Stacks, policy, and nine for provider development. Four more cover Packer. MPL-2.0. | Claude Code, Codex | 16 descriptions in every session, each body loads on use | `claude plugin marketplace add hashicorp/agent-skills` → `claude plugin install terraform@hashicorp`. Codex: `codex plugin marketplace add hashicorp/agent-skills` → `/plugins` → install `terraform` |
| Guard | `plan-before-apply` | Warns when the agent runs `terraform apply` or `terraform destroy`, OpenTofu included. | both | none, a hook costs no context | below |
| MCP server | [Terraform MCP server](https://github.com/hashicorp/terraform-mcp-server) | Looks up providers, modules and policies in the Terraform Registry, so an argument comes from today's docs and not from memory. MPL-2.0. | Claude Code, Codex | 9 tools in the registry toolset, the one that needs no token | `claude mcp add terraform -s user -t stdio -- docker run -i --rm hashicorp/terraform-mcp-server`. Codex: `codex mcp add terraform -- docker run -i --rm hashicorp/terraform-mcp-server` |

The agent plans as often as it likes, and the apply stays yours.

```json
{
  "id": "plan-before-apply",
  "why": "an apply or a destroy changes live infrastructure, and nobody has read the plan",
  "on": "shell",
  "pattern": "\\b(terraform|tofu)(\\s+-chdir=\\S+)?\\s+(apply|destroy)\\b",
  "mode": "warn",
  "message": "This changes live infrastructure. Save a plan with `plan -out=tfplan`, show it, and leave the apply to the person.",
  "payloads": [
    { "name": "catches an apply with no prompt", "text": "terraform apply -auto-approve", "expect": "hit" },
    { "name": "catches a destroy in another folder", "text": "tofu -chdir=envs/prod destroy", "expect": "hit" },
    { "name": "passes a saved plan", "text": "terraform plan -out=tfplan", "expect": "pass" },
    { "name": "passes the plan of a destroy", "text": "terraform plan -destroy", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/plan-before-apply.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [Docker Skills](https://github.com/docker/skills) | Docker's own skills for Dockerfiles, image builds and Compose files. | free, Apache-2.0 |
| Skill | [Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws) | AWS's skills and its MCP server in one plugin, `aws-core`: service choice, CDK and CloudFormation, containers, observability, deploys. | free, you pay for the AWS resources it touches |
| Skill | [Azure Skills](https://github.com/microsoft/azure-skills) | Microsoft's skills to prepare, validate, deploy and diagnose on Azure. The plugin also wires in the Azure MCP server, which its README counts at more than 200 tools. | free, MIT |
| Skill | [Google Skills](https://github.com/google/skills) | Google's skills for Google Cloud, picked one by one after `npx skills add google/skills`. | free, Apache-2.0 |
| Guard | [`destructive`](../guide/guards.md) | Built in, heavy profile. Blocks `rm -rf` on the root, the home or `.`, and warns on every other `rm -r`, which is how build folders get cleaned. | free, ours |
| Guard | [`secrets`](../guide/guards.md) | Built in, light profile. Blocks a cloud key written into a file, and a command that prints `.env` or a `.pem`. | free, ours |
| Guard | [`push`](../guide/guards.md) | Built in, heavy profile. Blocks a push to the default branch, which in many pipelines is the deploy. | free, ours |
| MCP server | [Grafana MCP server](https://github.com/grafana/mcp-grafana) | Logs from Loki, metrics from Prometheus, alerts and incidents. Its README lists 123 tools, 80 of them on by default. `--disable-<category>` and `--disable-write` cut it down. | free, Apache-2.0 |
| MCP server | [Kubernetes MCP server](https://github.com/containers/kubernetes-mcp-server) | Pods, events, logs and resources of a cluster, with `read_only = true` in its config. 23 tools in the two default toolsets. | free, Apache-2.0 |
| MCP server | [AWS MCP Server](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/understanding-mcp-server-tools.html) | 8 tools: search and read the AWS docs with no credentials, run API calls under your own IAM role. | free, you pay for the AWS resources it touches |
| MCP server | [Sentry MCP](https://mcp.sentry.dev/) | The errors and traces of the incident you are debugging, behind your Sentry login. | free plan, the server is source-available |

## When each earns its place

- **The skill** → the agent's Terraform keeps coming back from review: loose variables, no tests, a module shaped unlike your others. For one skill and one description, install it alone: `npx skills add hashicorp/agent-skills/plugins/terraform/skills/terraform-style-guide`. The Codex line joins HashiCorp's README, which names the marketplace file, with the command from [Codex's plugin docs](https://developers.openai.com/plugins/build/plugins).
- **The guard** → the first session whose shell holds credentials that can change real infrastructure. It costs nothing until it speaks. Set it to `block` yourself once it has only spoken when it should.
- **The MCP server** → the provider moved since the model was trained, and the agent writes arguments that no longer exist. It costs the 9 registry tools of its [reference](https://developer.hashicorp.com/terraform/mcp-server/reference) and a running Docker, and `--toolsets=registry` at the end of the command keeps it at those 9. Claude Code loads only the tool names until one is called, [by its docs](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search), while [Codex's MCP page](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) names no such step and gives `enabled_tools` to trim a server. With `TFE_TOKEN` set it reaches your workspaces, and `ENABLE_TF_OPERATIONS=true` lets it apply and destroy, so leave both unset until you need them.
- **The CLI first** → reading a failure needs no server. [`gh run view --log-failed`](https://cli.github.com/manual/gh_run_view) prints the failed steps of a pipeline, `kubectl logs` a pod, `terraform plan` the change. Each costs no context until it runs.

## Left out, and why

- [AWS Labs MCP servers](https://github.com/awslabs/mcp) → its own README names the Agent Toolkit for AWS as the successor, and that toolkit is in the table above.
- [PagerDuty's local MCP server](https://github.com/PagerDuty/pagerduty-mcp-server) → archived, with its last commit in September 2026. PagerDuty moved the work to a hosted server.
- [Destructive Command Guard](https://github.com/Dicklesworthstone/destructive_command_guard) → rule packs for Kubernetes, Docker, cloud CLIs and Terraform, under an MIT licence with an added rider. Read the rider before a team adopts it.

## A sample to study

[Auto Fix CI Failures](https://github.com/anthropics/claude-code-action/blob/main/examples/ci-failure-auto-fix.yml) → a GitHub Actions workflow that wakes when CI fails on a pull request, makes a fix branch, and hands Claude Code the logs of the failed jobs with tools to edit, run git and call `gh`. It opens with a frank security note, and it skips its own fix branches so it cannot loop on itself. `referenced`

## How to do it better

- **It pastes the whole log of every failed job into the prompt** → pass the failed steps alone, as [its sibling example](https://github.com/anthropics/claude-code-action/blob/main/examples/test-failure-analysis.yml) does with `gh run view --log-failed`. Fewer tokens, and less text the agent did not choose to read.
- **Its tool list allows any `gh`, `npm` and `npx` command in a job that may write to the repository** → name the exact commands, such as `Bash(npm test *)` and `Bash(gh pr create *)`. On Codex, [codex-action](https://github.com/openai/codex-action) narrows the run with its `safety-strategy` and `permission-profile` inputs.
- **Nothing ends a run that goes wrong** → add `timeout-minutes` to the job and `--max-turns` to `claude_args`.
- **The prompt calls `/fix-ci`, a command the file does not ship** → write it yourself, and make its first rule that no test and no workflow is changed to get green.
- **Every action is named by a tag** → lock the workflow's dependencies with a lockfile, or pin each action to a full-length commit SHA, the two measures [GitHub's own guide](https://docs.github.com/en/actions/reference/security/secure-use) gives, in that order.

## Where people talk

- [r/devops](https://www.reddit.com/r/devops/) → the widest room: pipelines, deploys and tool choices, from people who run them.
- [r/kubernetes](https://www.reddit.com/r/kubernetes/) → cluster problems and the tools around them.
- [r/Terraform](https://www.reddit.com/r/Terraform/) → Terraform and OpenTofu questions: modules, state, providers.
- [r/sre](https://www.reddit.com/r/sre/) → reliability work: incidents, on-call, postmortems, observability.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
