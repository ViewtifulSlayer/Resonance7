# Databases

Canonical location for MCP-queryable SQLite databases in the Resonance7 framework.

## Directory layout (initial clone)

```
library/databases/
  README.md              <- You are here
  schemas/               <- SQL schemas (e.g. session_logs.sql)
  scripts/               <- Ingest and maintenance scripts (e.g. ingest_session_logs.py)
  db/                    <- Database files (MCP reads from here)
    session_logs.db      <- Ingested session logs (default MCP DB)
  workspace_mcp_servers.md
```

After workspace setup, `sources/` may also appear (see root `README.md`).

## Git, indexing, and agents

| What | Git | Cursor index | Agent edit |
|------|-----|--------------|------------|
| `README.md`, `workspace_mcp_servers.md`, schema, ingest script | Tracked (allow-list) | Indexed | Allowed (schema/ingest); docs via normal rules |
| `db/session_logs.db` | Tracked empty placeholder | Excluded (binary); path in this README | Protected; update via `session_tools.py --ingest` |
| `db/*.db` (other) | Ignored | Excluded | Protected |
| `sources/**` | Ignored | Excluded | Allowed |

Agents should use this README and `workspace_mcp_servers.md` for DB paths and MCP aliases, not assume absence from the index means missing.

## Default MCP database

- **File**: `library/databases/db/session_logs.db`
- **MCP alias**: `session_logs`
- **When to use**: Past session recall, FTS search over ingested session markdown.

If `database_path` is omitted, the SQLite MCP server defaults to `session_logs`. Prefer passing `database_path: "session_logs"` for clarity.

Optional env overrides (in `.cursor/mcp.json`): `DEFAULT_DB_PATH`, `SESSION_LOGS_DB_PATH`, or legacy `KNOWLEDGE_BASE_DB_PATH`.

## Setup

1. Run `python library/tools/scripts/setup_database.py` from the workspace root (writes `.cursor/mcp.json`, installs npm deps).
2. Reload Cursor.
3. Query via MCP tools (`execute_query`, `get_tables`, etc.) with `database_path: "session_logs"`.

See `library/tools/mcp_sqlite_server/README.md` and `library/databases/workspace_mcp_servers.md` for details.

## Adding more databases

1. Place the `.db` file in `library/databases/db/<name>.db`.
2. Add an alias in `library/tools/mcp_sqlite_server/src/server.js` (full workspaces) or pass an absolute path.
3. Document the alias in this README.
