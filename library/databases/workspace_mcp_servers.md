# Workspace MCP Servers

Quick reference for MCP servers used in this workspace. For setup (e.g. [`.cursor/mcp.json`](../../.cursor/mcp.json)), see the MCP server docs or Cursor settings.

## Database (SQLite)

- **Server**: resonance7-sqlite (or Resonance7-sqlite / user-resonance7-sqlite in Cursor).
- **Use for**: Querying workspace SQLite databases (default: ingested session logs).
- **Default DB**: `library/databases/db/session_logs.db` (alias `session_logs`).
- **Other DBs**: Any `library/databases/db/<stem>.db` is reachable as alias `<stem>` (e.g. `iog_disassembly`). Discover via MCP tool `list_databases`.
- **Setup**: From the workspace root, run `python library/tools/scripts/setup_database.py`, then reload Cursor. Hand-edit from `library/templates/mcp.json.example` if needed.
- **Server code**: `library/tools/mcp_sqlite_server/` (`README.md`, `SETUP.md`, `mcp-config.json`).
- **More DBs**: See `library/databases/README.md` for layout, git policy, and ingest scripts.

## Scryfall (Magic: The Gathering API)

- **Server**: `Resonance7-scryfall` in [`.cursor/mcp.json`](../../.cursor/mcp.json) (project-local; gitignored).
- **Package**: [`@olaservo/scryfall-mcp-server`](https://github.com/olaservo/scryfall-mcp-app) via `npx` (live card search and fetch; not in-game Arena state).
- **Default**: `"disabled": true` in config - enable in **Cursor Settings > MCP** when needed for MTG work.
- **API policy**: [Scryfall API docs](https://scryfall.com/docs/api) (HTTPS, rate limits, fan content guidelines).
- **Tools** (typical): `search` (Scryfall query syntax), `fetch` (card by UUID; card viewer UI in MCP App-capable hosts).
