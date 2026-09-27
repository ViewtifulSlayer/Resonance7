# Library

The **`library/`** directory is the shared Resonance7 foundation: agent protocols, sessions, databases, docs modules, templates, and tools.

Open the **foundation repo root** in your editor (or a multi-root `.code-workspace` that pairs this repo with an external project). External project code lives outside this tree.

## Structure

- **`agent_foundation.json`** - Core agent behavior and protocols
- **`databases/`** - SQLite databases, schemas, ingest scripts, MCP docs
- **`docs/`** - User-curated documentation modules (runtime category folders)
- **`sessions/`** - Session logs (`current/`, `recent/`, `archived/`)
- **`templates/`** - `session_template.md`, `mcp.json.example`, project/library README templates
- **`tools/`** - Python setup scripts and MCP SQLite server

## Setup

First clone:

```bash
python library/tools/scripts/setup.py --init-dirs
python library/tools/scripts/setup_database.py
```

`setup.py` creates the runtime folders (including `library/sessions/current/`); `setup_database.py` writes `.agents/mcp.json` and installs Node dependencies.

See root **`README.md`** for full Quick Start.

## Agent configuration

Agent context and skills live in **`AGENTS.md`** and **`.agents/skills/`** at the foundation repo root; MCP is configured in **`.agents/mcp.json`**. The portable contract remains in `library/agent_foundation.json` and the Python tools above.
