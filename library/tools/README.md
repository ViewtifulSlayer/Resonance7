# Tools

Universal Python and Node tooling for the Resonance7 workspace. Scripts here are shared with every project via the **`library/`** symlink under **`projects/<name>/`**.

Run commands from the **repository root** (or use full paths); examples below assume the root as the current directory.

## Python scripts

| Script | Purpose |
|--------|---------|
| [**`session_tools.py`**](session_tools.py) | Create and maintain session logs under **`sessions/`** (interactive by default). |
| [**`project_tools.py`**](project_tools.py) | Create project workspaces with **`library/`** and **`sessions/`** symlinks and project template files. |
| [**`setup_mcp_sqlite.py`**](setup_mcp_sqlite.py) | Write a local **`.cursor/mcp.json`**, run **`npm install`** in **`mcp_sqlite_server/`** (same Node for native modules), optional **`npm audit fix`**. |

Quick help:

```bash
python library/tools/session_tools.py --help
python library/tools/project_tools.py --help
python library/tools/setup_mcp_sqlite.py --help
```

## MCP SQLite server (Node)

[**`mcp_sqlite_server/`**](mcp_sqlite_server/) implements the Cursor MCP server that talks to SQLite (including **`session_logs.db`**). It is not used by the Python scripts directly; Cursor starts it per **`.cursor/mcp.json`**.

- [**`mcp_sqlite_server/README.md`**](mcp_sqlite_server/README.md) - Behavior, env vars, and database aliases.
- [**`mcp_sqlite_server/SETUP.md`**](mcp_sqlite_server/SETUP.md) - Install and troubleshooting.

After clone or when Node paths change, run **`python library/tools/setup_mcp_sqlite.py`** from the workspace root, then reload Cursor. To hand-configure, start from **`library/templates/configuration_templates/mcp.json.example`**.

## See also

- **[Library overview](../README.md)** - Full **`library/`** layout and purpose.
- **[Root README](../../README.md)** - Quick start, prerequisites, and Cursor MCP overview.
