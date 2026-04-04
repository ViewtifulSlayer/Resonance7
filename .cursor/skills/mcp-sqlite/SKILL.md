---
name: mcp-sqlite
description: Professional guidance for MCP (Model Context Protocol) and SQLite - configuring Cursor MCP servers, using tools and resources, and querying workspace SQLite databases efficiently. Use when setting up or editing `.cursor/mcp.json`, debugging MCP servers, or querying SQLite databases via MCP (knowledge bases, wikis, project DBs).
---

# MCP SQLite (Server + Queries)

Use this skill when a task involves **MCP + SQLite together**:

- Configuring or debugging Cursor MCP (`.cursor/mcp.json`, server not starting, `"node" not recognized`).
- Adding, changing, or documenting the SQLite MCP server and its environment (commands, args, env vars, default DB).
- Discovering and querying workspace SQLite databases via MCP tools (`execute_query`, `get_tables`, `get_table_schema`, etc.).
- Choosing between MCP tools and direct file/terminal access for SQLite.

For schema design, data quality, and archival concerns (what to store, important vs filler, ingest/compile workflows), use the **database-specialist** skill.

---

## 1. MCP Setup in Cursor

### Where Cursor Loads MCP Config

| Location | Scope |
|----------|--------|
| **Project** | `.cursor/mcp.json` in repo root - primary; shared via version control. Use for project-specific servers (e.g. `Resonance7-my-app-sqlite`). |
| **User** | `~/.cursor/mcp.json` (Windows: `%USERPROFILE%\\.cursor\\mcp.json`) - global; better for cross-project servers (e.g. `Resonance7-sqlite`). |

Prefer project-level `.cursor/mcp.json` for project-only servers; keep shared servers in user-level settings to avoid duplicates.

### `mcp.json` Structure

```json
{
  "mcpServers": {
    "server-key": {
      "command": "<executable or full path>",
      "args": ["<arg1>", "<path to script or entrypoint>"],
      "env": {
        "VAR_NAME": "value"
      }
    }
  }
}
```

- **server-key**: Prefer the naming convention `Resonance7-<server>` (e.g. `Resonance7-sqlite`). Used in logs and UI.
- **command**: Program to run. On Windows, **use full path to the executable** (e.g. `C:\\Program Files\\nodejs\\node.exe`) so Cursor’s subprocess does not depend on PATH.
- **args**: Array passed to the program. Script path should be absolute for reliability.
- **env**: Environment variables for the server process (e.g. default database path).

### Avoiding `"node" is not recognized` (Windows)

Cursor spawns the server with its own environment. If `"command": "node"` fails with ENOENT or "not recognized", PATH does not include Node for that process.

**Fix:** Set `command` to the full path to `node.exe`, for example:

- Default install: `C:\\Program Files\\nodejs\\node.exe`
- User/nvm: e.g. `C:\\Users\\<You>\\AppData\\Roaming\\nvm\\v20.x.x\\node.exe`

In PowerShell (in a shell where `node` works): `(Get-Command node).Source` gives the path to use. In JSON, escape backslashes as `\\`.

### Example: SQLite MCP Server Entry

```json
{
  "mcpServers": {
    "Resonance7-sqlite": {
      "command": "C:\\Program Files\\nodejs\\node.exe",
      "args": [
        "<workspace_root>\\tools\\mcp_sqlite_server\\src\\server.js"
      ],
      "env": {
        "DEFAULT_DB_PATH": "<workspace_root>\\resources\\databases\\knowledge_base.db"
      }
    }
  }
}
```

After editing `.cursor/mcp.json` (project) or user MCP settings, reload the window or restart Cursor so the server (re)starts.

---

## 2. MCP Concepts (Tools vs Resources)

| Concept | Who controls | Purpose |
|--------|--------------|---------|
| **Tools** | Model | Actions the model can call (e.g. run a query, send a message). Protocol: `tools/list`, `tools/call`. |
| **Resources** | Application | Read-only data the app fetches for context (e.g. file contents, schema). Protocol: `resources/list`, `resources/read`. |
| **Prompts** | User | Parameterized prompt templates; user invokes explicitly. |

For SQLite in Cursor, the usual pattern is **tools**: the agent calls `execute_query`, `get_tables`, `get_table_schema`, `get_full_schema`, `get_indexes`, `get_table_row_count`, or `get_database_info` to read the database. Resources can expose schema or sample rows if the server implements them.

---

## 3. How the SQLite MCP Server Works

- **One server, multiple databases**: The server is configured with a default database path via an env var (example: `DEFAULT_DB_PATH`). Every tool accepts an optional `database_path`; when provided, that database is used instead of the default. Use `database_path` when the task involves a specific DB - do **not** assume the default is the right one.
- **Read-only**: MCP tools are **SELECT-only** for safety. INSERT/UPDATE/DELETE should be done via ingest/migration scripts outside MCP (see database-specialist).
- **Server name**: In MCP tool calls use the server name from your workspace config (e.g. `Resonance7-sqlite` or `user-Resonance7-sqlite`). Check the MCP config or the `mcps/` folder for the exact name.
- **Tool discovery**: Before calling any tool, read the tool schema from the MCP file system (e.g. `mcps/<server>/tools/<tool>.json`) so parameter names and required fields are correct.

### Workspace Database Locations (Examples)

When passing `database_path`, prefer **aliases or absolute paths** for reliability. Common locations:

| Purpose | Example alias / path (adjust to actual config) |
|--------|-----------------------------------------------|
| Default knowledge base | `DEFAULT_DB_PATH` (e.g. `<workspace_root>/resources/databases/knowledge_base.db`) |
| Web sources | Alias `web_sources` -> `<workspace_root>/resources/databases/web_sources.db` |
| Compiled knowledge base | Alias `compiled_kb` -> `<workspace_root>/resources/databases/compiled_kb.db` |
| Session logs | Alias `session_logs` -> `<workspace_root>/library/resources/databases/db/session_logs.db` (if configured) |
| Project app DB | Alias `app_db` -> `<workspace_root>/resources/databases/app.db` |

If the workspace root differs (e.g. a project under `projects/`), resolve paths from that root or from the path shown in your MCP config.

---

## 4. Workflow: Discover DBs, Then Schema, Then Query

### 4.1 Discover databases (optional but recommended)

- Call `list_databases` to see which database aliases exist and their paths.
- Use these aliases as `database_path` in other tools instead of hard-coding file paths where possible.

### 4.2 Discover schema

- Call `get_tables` (with `database_path` if not using default) to list tables, or `get_full_schema` to get every table's columns in one call.
- For a single table use `get_table_schema`. Use `get_indexes` to see indexes for a table (helps with query efficiency).
- Use `get_table_row_count` to gauge table size before querying.

Always **inspect schema first** before writing non-trivial queries.

### 4.3 Write targeted queries

- Use column names from the schema. Prefer specific columns over `SELECT *` when the table is wide or you only need a few columns.
- Add `WHERE`, `JOIN`, and `ORDER BY` as needed. Use `LIMIT` to cap result size (e.g. 10–100) unless the user needs full result sets.
- For large or complex queries, consider using `EXPLAIN QUERY PLAN` via `execute_query` to confirm index use (see `reference.md`).

### 4.4 Execute and interpret

- Call `execute_query` with the SQL string (and `database_path` if not default). Results are returned as JSON; use them directly in reasoning or in chat.
- For cross-DB questions, run **separate** queries per database and combine results in reasoning—SQLite via MCP does not support cross-database JOINs in a single call.

---

## 5. SQLite Efficiency (MCP Focus)

- **Indexes**: Queries that filter or join on indexed columns are much faster. Schema exploration (`get_table_schema`, `get_indexes`) or docs can reveal indexes; otherwise `EXPLAIN QUERY PLAN` shows whether an index is used.
- **Avoid full table scans when avoidable**: Use `WHERE` on columns that are (or can be) indexed; prefer equality or range conditions that match index order.
- **Limit result size**: Use `LIMIT` (and optionally `OFFSET`) so responses stay manageable and tool output is useful.
- **One index per table per query**: SQLite typically uses at most one index per table per query; composite indexes should match the order of conditions in `WHERE`/`JOIN`.

For deeper SQLite structure, index types, and query-planner behavior, see `reference.md`.

---

## 6. Tool Reference (Quick)

| Tool | Purpose |
|------|--------|
| `list_databases` | List configured DB aliases and paths (only existing DBs). No params. Use first to discover `database_path` values. |
| `get_tables` | List table names. Optional: `database_path`. |
| `get_full_schema` | Get columns/types for every table in one call. Optional: `database_path`. |
| `get_table_schema` | Get columns/types for one table. Required: `table_name`. Optional: `database_path`. |
| `get_indexes` | List indexes for a table (for query efficiency). Required: `table_name`. Optional: `database_path`. |
| `get_table_row_count` | Row count for one table or all tables. Optional: `table_name`, `database_path`. |
| `get_database_info` | Database stats (size, table count). Optional: `database_path`. |
| `execute_query` | Run SQL (SELECT only). Required: `query`. Optional: `database_path`, `max_rows` (default 1000; use -1 for no cap). |

Always check each tool's JSON schema in `mcps/<server>/tools/` before calling (required vs optional arguments, names, types).

---

## 7. Encouraging Use of MCP Databases

- When the user mentions "database," "look up," "query," "wiki," or "knowledge base," consider whether the answer can come from an MCP-accessible SQLite DB and use these tools.
- Prefer: MCP tool calls -> your configured sqlite server -> `get_tables` / `get_table_schema` / `execute_query` over suggesting terminal `sqlite3` or opening DB files directly.
- If a task spans multiple DBs, call the tools once per database with the appropriate `database_path`; combine results in reasoning.

For schema changes, migrations, and decisions about what to store, see the **database-specialist** skill.

---

## 8. Quick Checklists

**MCP server not starting in Cursor**

- [ ] `.cursor/mcp.json` (project) or user MCP settings exist and are valid JSON.
- [ ] `command` is full path to executable on Windows (e.g. `node.exe`).
- [ ] `args` script path exists and is correct (absolute recommended).
- [ ] Environment variables (e.g. `KNOWLEDGE_BASE_DB_PATH`) point to existing `.db` files.
- [ ] Reload window or restart Cursor after config changes.

**Querying a DB via MCP**

- [ ] Server is running (check MCP logs or tools list).
- [ ] Default DB path in `env` is correct, or pass `database_path` in the tool call.
- [ ] Use `get_tables` / `get_table_schema` / `get_indexes` to learn schema before writing SELECTs.
- [ ] Use `LIMIT` and targeted columns instead of unconstrained `SELECT *` on large tables.

**Changing schema or data**

- [ ] Determine whether the MCP server has write access or is read-only (typically read-only).
- [ ] Apply schema/data changes via ingest or migration scripts outside MCP.
- [ ] Prefer additive, transaction-wrapped changes (see database-specialist reference).

---

## 9. Additional Resources

- MCP / SQLite behavior details: `reference.md`
- MCP server implementation and config: your MCP server repo/folder (`README.md`, `SETUP.md`, `mcp-config.json` if present)
- **Workspace MCP index**: When this workspace contains `library/resources/databases/workspace_mcp_servers.md`, see it for a list of all MCP servers (SQLite, Ghidra, etc.), paths, and tool summaries.
- **Workspace DBs**: When this workspace contains `library/resources/databases/`, see `library/resources/databases/README.md` for which databases exist, trigger words, and the canonical DB table. For this minimal framework release, use `database_path: "session_logs"` (resolved by the bundled MCP server) or the **absolute path** to `library/resources/databases/db/session_logs.db`.