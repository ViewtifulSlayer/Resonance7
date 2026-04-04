# Resources

This file describes the **`library/` directory** in a Resonance7 workspace: templates, shared resources, universal tools, and `agent_foundation.json`.

At the **repository root**, `library/` is a normal folder. Under **`projects/<name>/`**, `project_tools.py` adds a **`library/` symlink** (and a **`sessions/`** symlink) so each project sees the same shared tree without copying it.

## Structure

- **`resources/`** - Shared resources
   - **`databases/`** - SQLite databases (downloaded/built on-demand)
   - **`docs/`** - Documentation modules (downloaded on-demand)
   - **`wikis/`** - Knowledge base indexes extracted from wikis
- **`templates/`** - Project and documentation templates
   - **`project_template/`** - Project workspace template
   - **`documentation_templates/`** - Documentation file templates
- **`tools/`** - Universal development tools
   - **`mcp_sqlite_server/`** - MCP SQLite Server for database access
   - **`project_tools.py`** - Project setup and template management
   - **`session_tools.py`** - Script for session log management
- **`agent_foundation.json`** - Core Resonance 7 Agent foundation
- **`README.md`** - Documentation for library directory

## Purpose

Resources in this directory are shared across all Resonance 7 projects, providing centralized access to documentation, knowledge bases, and other reference materials.

## Cursor configuration

`.cursor/` is **not** symlinked into `projects/<name>/` (it caused duplicate rules and MCP configuration). Open the **workspace root** in Cursor for shared rules and skills, or maintain a small local `.cursor/` only if you open a project folder on its own.
