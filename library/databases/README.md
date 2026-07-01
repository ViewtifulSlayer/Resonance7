# Databases

Canonical location for MCP-queryable SQLite databases in the Resonance7 framework.

## Directory layout (initial clone)

```
library/databases/
  README.md              <- You are here
  schemas/               <- SQL schemas (e.g. session_logs.sql)
  scripts/               <- Ingest and maintenance scripts (e.g. ingest_session_logs.py)
  db/                    <- Local SQLite files (gitignored; created by bootstrap)
    session_logs.db      <- Optional: from session_tools.py --ingest (MCP default)
  workspace_mcp_servers.md
```

After workspace setup, `sources/` may also appear (see root `README.md`).

## Git, indexing, and agents

| What | Git | Cursor index | Agent edit |
|------|-----|--------------|------------|
| `README.md`, `workspace_mcp_servers.md`, schema, ingest script | Tracked (allow-list) | Indexed | Allowed (schema/ingest); docs via normal rules |
| `db/session_logs.db` | Ignored (local) | Excluded (binary); path in this README | Protected; create via `session_tools.py --ingest` |
| `db/*.db` (all) | Ignored | Excluded | Protected |
| `sources/**` | Ignored | Excluded | Allowed |

Agents should use this README and `workspace_mcp_servers.md` for DB paths and MCP aliases, not assume absence from the index means missing.

## Default MCP database

- **File**: `library/databases/db/session_logs.db`
- **MCP alias**: `session_logs`
- **When to use**: Past session recall, FTS search over ingested session markdown.

If `database_path` is omitted, the SQLite MCP server defaults to `session_logs`. Prefer passing `database_path: "session_logs"` for clarity.

Other databases under `library/databases/db/` use the filename stem as alias (e.g. `iog_disassembly`). Use MCP tool `list_databases` to discover aliases after adding files.

Optional env overrides (in `.cursor/mcp.json`): `DEFAULT_DB_PATH`, `SESSION_LOGS_DB_PATH`, or legacy `KNOWLEDGE_BASE_DB_PATH`.

## Setup

1. Run `python library/tools/scripts/setup_workspace.py` (creates `library/databases/db/` among runtime dirs).
2. Run `python library/tools/scripts/setup_database.py` from the workspace root (writes `.cursor/mcp.json`, installs npm deps).
3. Reload Cursor.
4. Optional: run `python library/tools/scripts/session_tools.py --ingest` to create or refresh `session_logs.db`.
5. Query via MCP tools (`execute_query`, `get_tables`, etc.) with `database_path: "session_logs"`.

See `library/tools/mcp_sqlite_server/README.md` and `library/databases/workspace_mcp_servers.md` for details.

## Adding more databases

1. Place the `.db` file in `library/databases/db/<name>.db`.
2. Reload Cursor (restarts the MCP server). The alias is the filename **stem** (e.g. `iog_disassembly.db` -> `iog_disassembly`).
3. Call MCP tool `list_databases` to see all aliases and paths, or pass `database_path: "<stem>"` on other tools.
4. Document purpose in this README when you add a DB agents should know about.

No per-database edits to `.cursor/mcp.json` or `server.js` are required for standard drops under `db/`. Absolute paths still work.
