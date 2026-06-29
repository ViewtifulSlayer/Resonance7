# Workspace MCP Servers

Quick reference for MCP servers used in this workspace. For setup (e.g. [`.cursor/mcp.json`](../../.cursor/mcp.json)), see the MCP server docs or Cursor settings.

## Database (SQLite)

- **Server**: resonance7-sqlite (or Resonance7-sqlite / user-resonance7-sqlite in Cursor).
- **Use for**: Querying workspace SQLite databases (default: ingested session logs).
- **Default DB**: `library/databases/db/session_logs.db` (alias `session_logs`).
- **Setup**: From the workspace root, run `python library/tools/scripts/setup_database.py`, then reload Cursor. Hand-edit from `library/templates/mcp.json.example` if needed.
- **Server code**: `library/tools/mcp_sqlite_server/` (`README.md`, `SETUP.md`, `mcp-config.json`).
- **More DBs**: See `library/databases/README.md` when present for additional aliases and ingest scripts.
