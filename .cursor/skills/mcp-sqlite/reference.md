---
title: MCP SQLite Engine & Protocol Reference
---

# MCP SQLite Engine & Protocol Reference

Use this file when you need **detailed SQLite behavior** or **MCP protocol details** for writing or tuning queries. For when-to-use guidance and workflows, see `SKILL.md`.

---

## 1. SQLite Structure and Schema Discovery

- **Types**: SQLite uses dynamic typing; declared types (INTEGER, TEXT, REAL, BLOB) are type affinity hints. Stored values can be any type; comparisons and sorts follow type rules (e.g. numeric vs text).
- **Rowid**: Every table has an implicit `rowid` (or `INTEGER PRIMARY KEY` alias). Indexes and `ORDER BY rowid` are very fast.
- **`sqlite_master`**: System table listing tables, indexes, and views.
  - List tables:
    - `SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;`
  - List tables and indexes:
    - `SELECT name, type FROM sqlite_master WHERE type IN ('table','index') ORDER BY name;`
- **`PRAGMA table_info(table_name)`**: Returns column definitions (cid, name, type, notnull, dflt_value, pk). The MCP `get_table_schema` tool wraps this.
- **Database stats** (for `get_database_info`):
  - `PRAGMA page_count;`
  - `PRAGMA page_size;`

---

## 2. Indexes and Foreign Keys

### 2.1 Indexes

- **B-tree**: SQLite uses B-trees (B+trees) for tables and indexes. Indexes speed up WHERE, JOIN, and ORDER BY on indexed columns.
- **Single-column**: Best when filtering or sorting on one column. Create on columns used often in WHERE/JOIN.
- **Composite (multi-column)**: Order of columns matters. Put equality columns first, then range; match the order used in WHERE (e.g. `WHERE a = ? AND b > ?` → index on (a, b)).
- **Partial indexes**: `CREATE INDEX ... WHERE condition` indexes only rows matching a condition—smaller index, good for subset queries.
- **Expression indexes**: Index on an expression (e.g. `lower(name)`) allows efficient queries that use the same expression.
- **One index per table per query**: The planner typically uses at most one index per table per query. Choose or design indexes to match the most important query pattern.
- **Covering index**: An index that includes all columns needed to satisfy a query so SQLite can answer from the index without accessing the table—reduces disk I/O. Include frequently selected columns in the index when the same query pattern is hot.

### 2.2 Foreign Keys

- **Not enforced by default**: SQLite does not enforce foreign key constraints unless explicitly enabled. Enable per connection with `PRAGMA foreign_keys = ON` (required for each new connection).
- **Child key index**: Create an index on the child key columns of each foreign key so parent deletes/updates and referential checks are efficient; without it, SQLite may scan the whole child table. Parent key must be PRIMARY KEY or UNIQUE.

---

## 3. EXPLAIN QUERY PLAN and Query Patterns

### 3.1 EXPLAIN QUERY PLAN

Use via MCP by calling `execute_query` with `query` set to `EXPLAIN QUERY PLAN SELECT ...` (your actual SELECT). No data is returned; you get the plan.

Common phrases:

- **`SCAN table`**: Full table scan (all rows). Acceptable for small tables; for large tables consider adding an index or narrowing the query.
- **`SEARCH table USING INDEX index_name`**: Index is used to find rows—preferred when the table is large.
- **`SEARCH table USING INTEGER PRIMARY KEY`**: Lookup by rowid; very fast.

Output format can change between SQLite versions. Use it to confirm index use and spot full scans on big tables.

### 3.2 Query patterns that use indexes well

- Equality: `WHERE col = ?` (single-column or leading column of composite index).
- Range: `WHERE col > ? AND col < ?` (index on `col` or composite with `col` leading).
- ORDER BY: Same column(s) as index (or index prefix) allow index scan instead of sort.
- JOIN: Index on the join column(s) of the inner table.
- LIMIT: Combine with indexed WHERE/ORDER BY so SQLite can stop early.

### 3.3 Query patterns to avoid or limit

- `SELECT *` on wide tables when you only need a few columns—more data than needed.
- Full table scans on large tables without WHERE—add WHERE or an index.
- Expressions in WHERE that do not match an expression index (e.g. `WHERE lower(name) = 'x'` with no expression index on `lower(name)`).
- Very large result sets without LIMIT—use LIMIT (and OFFSET if paging) for MCP responses.

---

## 4. SQLite Features: FTS, JSON, and Writes

### 4.1 Full-text search (FTS)

- If a DB has `CREATE VIRTUAL TABLE ... USING fts5(...)`, use `MATCH` for full-text queries.
- Typical pattern:
  - `SELECT * FROM entity_fts WHERE entity_fts MATCH 'search terms' LIMIT 20;`
- For non-FTS tables, fall back to `LIKE` or application-side search.

### 4.2 JSON in columns

- SQLite provides JSON helpers for JSON stored in TEXT columns:
  - `json_extract(column, '$.path')`
  - `json_each`, `json_tree` for iterating structures.
- Use these for structured filtering without unpacking JSON in application code.

### 4.3 Transactions, parameterization, and migrations (outside MCP)

When the process writing to the DB has write access (ingest/migration scripts, not MCP tools):

- **Transactions**: Use `BEGIN; ...; COMMIT;` (or `ROLLBACK;`) for multi-statement updates so changes are atomic.
- **Parameterization**: In application code (Node, Python, etc.) use parameterized statements instead of string-concatenated SQL.
- **Idempotent migrations**: Prefer `CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`, and guarded `ALTER TABLE ... ADD COLUMN` so re-runs are safe.

For migration strategy and data-quality decisions, see the `database-specialist` reference.

---

## 5. MCP Protocol (Tools, Resources, Transport)

### 5.1 Tools

| Method | Purpose | Returns |
|--------|---------|---------|
| `tools/list` | Discover tools | Array of tool definitions (name, description, inputSchema) |
| `tools/call` | Run a tool | Result payload (e.g. content array with text) |

Tool definitions use **JSON Schema** for `inputSchema`. The client (Cursor) sends `tools/call` with `name` and `arguments`; the server executes and returns content or an error.

### 5.2 Resources

| Method | Purpose | Returns |
|--------|---------|---------|
| `resources/list` | List direct resources | Resource descriptors (URI, name, mimeType) |
| `resources/templates/list` | List URI templates | Template definitions for parameterized URIs |
| `resources/read` | Get resource content | Resource body + metadata |

Resources are read-only. The application decides when to fetch and pass them to the model.

### 5.3 Transport

- Cursor typically uses **stdio**: the server is spawned as a subprocess; Cursor sends JSON-RPC over stdin and reads from stdout.
- Stderr is for server logs.
- `command` and `args` in `mcp.json` must start the server process correctly; PATH is not reliable on Windows unless the full executable path is used (e.g. full path to `node.exe`).

---

## 6. MCP-Specific SQLite Notes

- **Read-only**: MCP SQLite tools are typically configured for **SELECT-only**. `EXPLAIN QUERY PLAN` and read-only `PRAGMA` calls are fine.
- **One DB per call**: Each tool call uses one database (default or `database_path`). No `ATTACH` or cross-database JOIN in a single call; do multiple calls if you need data from more than one DB.
- **Paths and aliases**:
  - Use aliases (e.g. `database_path: "web_sources"`, `"compiled_kb"`, `"session_logs"`) where configured.
  - When a raw path is needed, use absolute paths so the server finds the file regardless of current working directory.
- **Default DB**: If a default DB env var is set (e.g. `DEFAULT_DB_PATH`), omitting `database_path` uses that DB. Prefer named aliases for clarity when multiple DBs exist.

When this workspace contains `library/resources/databases/`, see `library/resources/databases/README.md` for the canonical alias list and paths.

---

## 7. Authoritative References

**SQLite**

- [SQLite Foreign Key Support](https://sqlite.org/foreignkeys.html) — enabling FK, child key indexes, ON DELETE/UPDATE.
- [SQLite Query Planner](https://sqlite.org/queryplanner.html) — indexing, covering indexes, search strategies.
- [EXPLAIN QUERY PLAN](https://sqlite.org/eqp.html) — interpreting execution plans.
- [SQLite CREATE TABLE](https://sqlite.org/lang_createtable.html) — constraints, types, PRIMARY KEY.
- [SQLite SQL reference](https://www.sqlite.org/lang.html) — SQL commands overview.
- [SQLite PRAGMA](https://www.sqlite.org/pragma.html) — pragmas like `page_size`, `page_count`, `foreign_keys`.
- [SQLite FTS5](https://www.sqlite.org/fts5.html) — full-text search virtual tables.
- [Use The Index, Luke — SQLite](https://use-the-index-luke.com/sql/explain-plan/sqlite) — execution plans and indexing.

**MCP**

- [MCP Server Concepts](https://modelcontextprotocol.io/docs/learn/server-concepts)
- [MCP Specification](https://modelcontextprotocol.io/specification)
