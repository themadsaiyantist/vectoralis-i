# Data and ML

Data and ML work is notebooks, datasets, training runs, evals and the record of every experiment. Two things set it apart for an agent: the files are too large to read, and one command can rent a GPU by the hour. Read this page before an agent touches your data, and before it starts a run you pay for.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [Hugging Face skills](https://github.com/huggingface/skills) | `hf-cli` teaches the agent every command of the `hf` CLI: models, datasets, Spaces, jobs. The rest load by name, such as `huggingface-llm-trainer` for fine-tuning, `huggingface-community-evals` for evals and `huggingface-trackio` for experiment tracking. Apache-2.0. | Claude Code, Codex | one description each, then the body on use: `hf-cli` is 34 KB, the trainer 29 KB | `hf skills add --global`, then `hf skills add <skill-name>` for each of the rest. Claude Code as a plugin: `/plugin marketplace add huggingface/skills` → `/plugin install hf-cli@huggingface-skills` |
| Guard | `paid-compute` | Warns before the agent starts a Hugging Face job, which bills by the second. | both | none, a hook costs no context | below |
| MCP server | [Hugging Face MCP server](https://huggingface.co/docs/hub/agents-mcp) | Searches models, datasets, Spaces, papers and the docs, and runs the Spaces you add as tools. | Claude Code, Codex | one built-in tool, `hf_fs`, plus the ones you switch on in your MCP settings | `claude mcp add hf-mcp-server -t http https://huggingface.co/mcp?login`. Codex: the snippet your MCP settings page at `huggingface.co/settings/mcp` writes for it |

The skill can start cloud jobs, so the recipe makes each one a decision: add your own launcher to the pattern if you rent compute elsewhere.

```json
{
  "id": "paid-compute",
  "why": "a cloud job bills by the second, and the money is the person's",
  "on": "shell",
  "pattern": "\\bhf\\s+jobs\\s+(scheduled\\s+)?(uv\\s+)?(run|rerun|trigger|resume)\\b",
  "mode": "warn",
  "message": "This starts paid compute. Tell the person the hardware, the timeout and the price for an hour, and wait for their yes.",
  "payloads": [
    { "name": "catches a GPU job", "text": "hf jobs uv run --flavor a10g-large --timeout 2h train.py", "expect": "hit" },
    { "name": "catches a scheduled job", "text": "hf jobs scheduled run @daily python:3.12 python report.py", "expect": "hit" },
    { "name": "passes a look at the logs", "text": "hf jobs logs 687f911eaea852de79c4a50a", "expect": "pass" },
    { "name": "passes the list of jobs", "text": "hf jobs ps", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/paid-compute.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [marimo skills](https://github.com/marimo-team/skills) | Skills for marimo, whose notebooks are stored as plain Python files an agent can read, diff and run as scripts. One converts a Jupyter notebook. | free, Apache-2.0 |
| Skill | [MLflow skills](https://github.com/mlflow/skills) | Ten skills for open-source MLflow: tracing, evaluation and regression tests for LLM apps, and one that sets it up for classic ML. | free, Apache-2.0 |
| Guard | [`locks`](../guide/locks.md) | Built in, heavy profile. Put `data/raw/` in `harness/locks.md`, and no write reaches the raw data. | free, ours |
| Guard | [nbstripout](https://github.com/kynan/nbstripout) | A git filter that strips the outputs from a notebook before it is committed, so rows of data and a key printed in a cell stay out of history. | free, MIT |
| MCP server | [Jupyter MCP server](https://github.com/datalayer/jupyter-mcp-server) | Runs cells in a live kernel of a Jupyter you already run, and reads the output back. | free, BSD-3-Clause |
| MCP server | [DuckDB local MCP server](https://github.com/motherduckdb/mcp-server-motherduck) | SQL over local files and DuckDB databases, with an answer capped at 1,024 rows. 4 tools. | free, MIT |

## When each earns its place

- **The skill** → the first time the agent guesses an `hf` flag or writes a training script from memory. `hf-cli` is generated from the CLI you have installed, so it matches your version. Add the others one at a time, because they are large when they open.
- **The guard** → before the first job the agent starts on its own. A job runs on any account with a positive credit balance and stops after 30 minutes unless a timeout says otherwise. A GPU costs from $0.40 an hour for a small T4 to $40 for eight H200s, [by the jobs guide](https://huggingface.co/docs/huggingface_hub/guides/jobs). It reads shell commands only: switch on the Jobs tool of the MCP server, and a job can start with no shell line.
- **The MCP server** → you need what the CLI lacks: a search of the docs by meaning, or a Space run as a tool. It costs one tool until you add more.
- **The CLI first** → [by Hugging Face's own page](https://huggingface.co/docs/hub/agents-cli), the `hf` CLI is how an agent searches models, manages datasets and runs jobs, and the skill is its manual. Experiment tracking needs no server either: [Trackio](https://github.com/gradio-app/trackio) keeps runs in a local SQLite file and answers questions through its CLI.

## Left out, and why

- [DuckDB skills](https://github.com/duckdb/duckdb-skills) → DuckDB's own Claude Code plugin for exploring data. Its last commit is from 2026-04-14, past the three-month line.
- [MLflow MCP server](https://mlflow.org/docs/latest/genai/mcp/) → its docs open with "This feature is experimental".
- [W&B skills](https://github.com/wandb/skills) → Weights & Biases marks every skill in its own table as experimental.

## A sample to study

[autoresearch](https://github.com/karpathy/autoresearch) → an agent that runs training experiments on its own, all night: it edits one file, trains for five minutes, reads one number, and keeps the change or throws it away. The whole method is one Markdown file of instructions, with a results log and every run's output sent to a file so it never floods the context. `referenced`

## How to do it better

- **`prepare.py` is marked "do not modify", and nothing enforces it** → that file holds the metric the agent is judged by. Lock it: `locks` refuses the write.
- **Its README says to disable all permissions** → give it a sandbox or a container instead, and the guard above once the GPU is rented.
- **One validation number picks the winner, a hundred times a night** → the winner ends up fitted to that number. Hold out a test split the loop never reads, and score the winner on it once.
- **One five-minute run decides** → run the baseline a few times first, and keep a change only when it beats the spread between those runs.
- **Results sit in an untracked file, and a discarded idea is reset away** → log every run to a tracker with its commit, its settings and its curve, so a failed idea can still be read.

## Where people talk

- [r/MachineLearning](https://www.reddit.com/r/MachineLearning/) → research and training talk, papers first.
- [r/mlops](https://www.reddit.com/r/mlops/) → pipelines, experiment tracking and serving, from people who run them.
- [r/datascience](https://www.reddit.com/r/datascience/) → analysis work and the tools around notebooks.
- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) → fine-tuning and evals of open models on your own hardware.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
