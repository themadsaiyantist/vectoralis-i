# Backend, databases and APIs

Backend work is what sits behind the screen: data stores, migrations, auth, payments and the API other code calls. Read this page before an agent's shell can reach a database, and when it starts to write schema changes, access rules or payment code.

**Contents:** The picks · Also worth it · When each earns its place · Left out, and why · A sample to study · How to do it better · Where people talk

## The picks

| Kind | Pick | What it does | Works in | Cost in context | Install |
|---|---|---|---|---|---|
| Skill | [Supabase Postgres Best Practices](https://github.com/supabase/agent-skills) | Postgres rules from Supabase, written for Postgres running anywhere: schema and column types, migrations, indexes, row-level security, locking, slow queries. Each rule shows the wrong SQL beside the right one. MIT. | Claude Code, Codex | one description, a 3.2 KB index on use, then one rule file at a time out of 34 | `npx skills add supabase/agent-skills --skill supabase-postgres-best-practices`. As a Claude Code plugin: `claude plugin marketplace add supabase/agent-skills` → `claude plugin install postgres-best-practices@supabase-agent-skills` |
| Guard | `no-db-reset` | Warns before a command that empties a database: a reset, a drop, a truncate. | both | none, a hook costs no context | below |
| MCP server | [DBHub](https://github.com/bytebase/dbhub) | One small server for PostgreSQL, MySQL, MariaDB, SQL Server, Oracle and SQLite: run a query, search the schema. Read-only mode and a row limit are settings. MIT. | Claude Code, Codex | 2 tools by default, 1.4k tokens by its README | `claude mcp add --transport stdio dbhub -- npx @bytebase/dbhub@latest --transport stdio --dsn "postgres://user:password@localhost:5432/dbname"`. Codex: `codex mcp add dbhub -- npx @bytebase/dbhub@latest --transport stdio --dsn "postgres://user:password@localhost:5432/dbname"` |

The built-in `destructive` guard watches git and `rm`, and this one watches the database, where a wrong command has no undo.

```json
{
  "id": "no-db-reset",
  "why": "one command can empty a database, and no commit brings the rows back",
  "on": "shell",
  "pattern": "(?i)prisma\\s+migrate\\s+reset|supabase\\s+db\\s+reset|db:(drop|reset)|migrate:fresh|\\bdropdb\\b|\\bdrop\\s+(database|schema|table)\\b|\\btruncate\\s+table\\b",
  "mode": "warn",
  "message": "This command deletes data. Name the database it will hit, check it is not production, and ask the person first.",
  "payloads": [
    { "name": "catches a reset", "text": "npx prisma migrate reset --force", "expect": "hit" },
    { "name": "catches a drop sent through psql", "text": "psql \"$DATABASE_URL\" -c \"DROP TABLE orders\"", "expect": "hit" },
    { "name": "passes a new migration", "text": "npx prisma migrate dev --name add_orders", "expect": "pass" }
  ]
}
```

Save it as `harness/guards/no-db-reset.json`. It starts at `warn`.

## Also worth it

| Kind | Name | What it adds | Free or paid |
|---|---|---|---|
| Skill | [Stripe's plugin](https://github.com/stripe/ai) | Stripe's own skills for payment code, `stripe-best-practices` and `upgrade-stripe` among them. The plugin also connects Stripe's MCP server. | free, MIT |
| Skill | [PlanetScale Database Skills](https://github.com/planetscale/database-skills) | The same kind of help for MySQL, Vitess and sharded Postgres: schema, indexes, query tuning, migration plans. | free, MIT |
| Skill | [Auth0 Agent Skills](https://github.com/auth0/agent-skills) | Auth0's own skills for login, SSO and MFA in the framework you use. | free, Apache-2.0, with a free Auth0 account |
| Skill | [Prisma Skills](https://github.com/prisma/skills) | Prisma's own reference for the Prisma 7 CLI, migrations included, and for the upgrade from v6. | free, MIT |
| Guard | [`secrets`](../guide/guards.md) | Built in, light profile. Blocks a Stripe live key or a cloud key written into a file, and a command that prints `.env`. | free, ours |
| Guard | [`locks`](../guide/locks.md) | Built in, heavy profile. Lock a migration by its path once it has run, and no session rewrites it. | free, ours |
| MCP server | [Supabase MCP server](https://supabase.com/docs/guides/ai-tools/mcp) | Supabase's own: tables, migrations, logs, Edge Functions and docs. About 40 tools in 10 groups, and `read_only=true`, `project_ref` and `features` in the URL narrow it. | free, you pay for the Supabase resources it creates |
| MCP server | [Stripe MCP server](https://docs.stripe.com/mcp) | Stripe's own: 15 tools that search the docs and read or write through the API. A refund or a transfer waits for your approval in the Dashboard. | the docs name no price |
| MCP server | [MCP Toolbox for Databases](https://github.com/googleapis/mcp-toolbox) | Google's open server for many database engines, with prebuilt tools and a way to define narrow ones of your own. | free, Apache-2.0 |
| MCP server | [MongoDB MCP Server](https://github.com/mongodb-js/mongodb-mcp-server) | MongoDB's own, for a document store. Every example in its README carries `--readOnly`. | free, Apache-2.0 |

## When each earns its place

- **The skill** → the agent writes SQL that is fine on ten rows: no index behind the filter, a migration that locks a large table, a row-level policy that lets the wrong tenant read. Its description asks to be loaded before any change to a Postgres database, so expect it to load often.
- **The guard** → the first session whose shell can reach a database you would miss. It reads shell commands, so it does not see a statement sent through an MCP tool. The stronger wall is the role: give the agent a connection that cannot drop.
- **The MCP server** → the agent has to look at the real schema and rows several times in one session. Set `readonly = true` and `max_rows` on [`execute_sql`](https://dbhub.ai/tools/execute-sql) in `dbhub.toml`, and connect as a read-only database user, as [Claude Code's own example](https://code.claude.com/docs/en/mcp#example-query-your-postgresql-database) of this server does. Rows come back into the context, and rows hold other people's text.
- **The CLI first** → one question about a schema needs no server. `psql "$DATABASE_URL" -c '\d orders'` prints a table's columns and indexes, and `sqlite3` and `mysql` do the same for theirs, at no context cost until they run.

## Left out, and why

- [Postgres MCP Pro](https://github.com/crystaldba/postgres-mcp) → index tuning, query plans and health checks in 9 tools. It has one commit since January 2026, a dependency pin in August, so it sits at the edge of the three months this kit asks for.
- [The archived reference servers](https://github.com/modelcontextprotocol/servers-archived) for PostgreSQL and SQLite → archived, with no security fixes, by their own README.
- [Better Auth skills](https://github.com/better-auth/skills) → no licence file and no README in the repository on 2026-11-11.

## A sample to study

[Cal.diy's `AGENTS.md`](https://github.com/calcom/cal.diy/blob/main/AGENTS.md) → the agent rules of a large open-source scheduling product, with Prisma for the data and tRPC for the API. A short Do and Don't list, three boundary lists, always, ask first and never, and 42 rule files in [`agents/rules/`](https://github.com/calcom/cal.diy/tree/main/agents/rules), one each for migrations, DTO boundaries, thin controllers and breaking API changes among them. `referenced`

## How to do it better

- **"Never commit secrets" is a sentence** → the `secrets` guard blocks the write. A rule a machine can check should not rest on the agent's memory.
- **Schema changes sit under "ask first", and nothing makes the agent ask** → a project guard that warns on every write to the schema file, and `no-db-reset` for the commands.
- **"Never modify `*.generated.ts`" is a path rule kept as prose** → one recipe with `"path": "**/*.generated.ts"` holds it in every session, for both agents.
- **`AGENTS.md` does not say which database the agent may reach** → give it a database of its own, a branch or a local copy, and a role that cannot drop. Production gets a read-only user, or nothing.
- **`AGENTS.md` names no rule for payment code** → add the payment maker's skill and work with test mode keys. The `secrets` guard blocks a live Stripe key on its way into a file.

## Where people talk

- [r/Backend](https://www.reddit.com/r/Backend/) → backend work at large: APIs, queues, architecture.
- [r/PostgreSQL](https://www.reddit.com/r/PostgreSQL/) → Postgres itself: schema, indexes, migrations, performance.
- [r/node](https://www.reddit.com/r/node/) → Node.js backends, their ORMs and frameworks.
- [r/Supabase](https://www.reddit.com/r/Supabase/) → Supabase in practice, its MCP server and row-level security included.

Verified 2026-11-11: every link opened except the subreddits, which Reddit does not let a checker open. Every entry is marked `read`: read in its maker's docs, not installed here.
