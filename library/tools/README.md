# Tools

Universal Python and Node tooling for the Resonance7 foundation workspace. Run commands from the **repository root**.

## Python scripts (`scripts/`)

| Script | Purpose |
|--------|---------|
| [**`scripts/setup_workspace.py`**](scripts/setup_workspace.py) | Bootstrap runtime dirs; pair external projects via `projects/*.code-workspace` |
| [**`scripts/setup_database.py`**](scripts/setup_database.py) | Write/merge `.cursor/mcp.json` (framework SQLite entry), run `npm install` in `mcp_sqlite_server/` |
| [**`scripts/session_tools.py`**](scripts/session_tools.py) | Create and maintain session logs under **`library/sessions/`** |

Quick help:

```bash
python library/tools/scripts/setup_workspace.py --help
python library/tools/scripts/setup_database.py --help
python library/tools/scripts/session_tools.py --help
```

## MCP SQLite server (Node)

[**`mcp_sqlite_server/`**](mcp_sqlite_server/) implements the MCP server for SQLite (including **`session_logs.db`**). Cursor starts it per **`.cursor/mcp.json`**.

- [**`mcp_sqlite_server/README.md`**](mcp_sqlite_server/README.md) - Behavior, env vars, database aliases
- [**`mcp_sqlite_server/SETUP.md`**](mcp_sqlite_server/SETUP.md) - Install and troubleshooting

After clone or when Node paths change:

```bash
python library/tools/scripts/setup_database.py
```

Hand-configure from **`library/templates/mcp.json.example`**.

## See also

- **[Library overview](../README.md)**
- **[Root README](../../README.md)** - Quick start and prerequisites
