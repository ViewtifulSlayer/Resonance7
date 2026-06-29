# Resonance7

A structured workspace for collaborative human-AI development: agent protocols, session logging, shared libraries, and SQLite MCP integration.

## Table of Contents

- [Overview](#overview)
- [IDE and agents](#ide-and-agents)
- [Quick Start](#quick-start)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
- [Documentation](#documentation)
- [Configuration](#configuration)
- [Philosophy](#philosophy)
- [License](#license)

Release history: [RELEASE_NOTES.md](RELEASE_NOTES.md) | [CHANGELOG.md](CHANGELOG.md)

---

## Overview

- **Agent foundation** - Core behavior and protocols in `library/agent_foundation.json`
- **Session logging** - Markdown logs under `library/sessions/` with lifecycle tooling
- **SQLite MCP** - Query `session_logs.db` and other workspace databases via MCP (Cursor today)
- **Shared library** - Databases, docs modules, templates, and tools under `library/`
- **External projects** - Pair out-of-repo project folders via `projects/*.code-workspace` (see [Usage](#usage))
- **Cross-platform** - Python setup scripts; Node for the MCP server package

---

## IDE and agents

**v3.x (now):** Cursor is the primary supported editor. Rules, skills, slash commands, and MCP wiring live under `.cursor/`. Setup scripts target `.cursor/mcp.json` today.

**v4.0 (planned):** Move toward an **IDE-neutral core** with editor-specific integration layered on top. The portable contract stays in `library/agent_foundation.json`, session logs, Python tools, and the MCP SQLite server - not in Cursor-only paths. A locally hosted agent in **VS Code** is the likely next integration target; details will land in v4 release notes.

When adding v3 features, prefer:

- Behavior and paths in `library/` and scripts (portable)
- Cursor conveniences in `.cursor/` (replaceable layer)
- MCP and Node setup that any MCP-capable client can reuse

This repo may gain `.vscode/` (or similar) configuration over time without removing the shared foundation layout above.

---

## Quick Start

### Prerequisites

- **Python 3.7+**
- **Git**
- **Node.js 18+** (LTS recommended) - required for default setup; see [Node.js](#nodejs) below
- **Cursor** recommended for v3 (rules, skills, MCP); `library/agent_foundation.json` and Python tools work without it

### Installation

1. **Clone and enter the repo:**

   ```bash
   git clone https://github.com/ViewtifulSlayer/Resonance7.git
   cd Resonance7
   ```

2. **Bootstrap runtime directories** (idempotent; safe to re-run):

   ```bash
   python library/tools/scripts/setup_workspace.py
   ```

   Creates session folders, docs/database scaffolding, `projects/`, and `tests/` if missing. Fresh clones include `library/.workspace_setup_required`; successful bootstrap removes that file locally (do not commit the deletion).

3. **MCP and Node dependencies** (standard post-clone step):

   ```bash
   python library/tools/scripts/setup_database.py
   ```

   Writes `.cursor/mcp.json`, runs `npm install` in `library/tools/mcp_sqlite_server`, and optional `npm audit fix`. `node_modules/` is not in Git; every fresh clone needs this step.

4. **Reload your editor** (Cursor today) so MCP picks up the new config.

5. **Verify:**

   - `library/agent_foundation.json` exists
   - `python library/tools/scripts/session_tools.py --help` runs
   - `library/tools/mcp_sqlite_server/node_modules/` exists after step 3

Hand-configuring MCP: copy `library/templates/mcp.json.example` to `.cursor/mcp.json` (Cursor project MCP config today), set absolute paths, run `npm install` in `library/tools/mcp_sqlite_server` with the **same** Node binary as in `mcp.json`, then reload the editor.

### First Steps

```bash
# Session log (interactive)
python library/tools/scripts/session_tools.py

# Workspace bootstrap or pairing menu
python library/tools/scripts/setup_workspace.py --interactive
```

In Cursor (v3), use `/start` for onboarding checks and `/help` for topic explanations. Equivalent flows for other editors are planned for v4.

### Node.js

The repo requires **Node 18 or newer**. The version floor is set in `library/tools/mcp_sqlite_server/package.json`:

```json
"engines": { "node": ">=18.0.0" }
```

That matches `@modelcontextprotocol/sdk` (ESM, modern Node APIs) and `better-sqlite3` native builds. `setup_database.py` enforces the same minimum (`MIN_NODE_MAJOR = 18`).

**Maintain compatibility by:**

- Keeping `engines.node` in `package.json` as the single source of truth
- Using one Node install for both `mcp.json` `command` and `npm install` (avoids `NODE_MODULE_VERSION` / native module mismatches)
- Re-running `setup_database.py` after upgrading Node or switching machines

Current LTS (20.x or 22.x) is fine as long as it satisfies `>=18.0.0`. Pinning an exact Node version in docs is unnecessary unless you add CI that tests a specific runtime.

---

## Directory Structure

Legend: **tracked** = in Git by default | **runtime** = created by `setup_workspace.py` if missing | **local** = gitignored or machine-specific

```
Resonance7/
├── .cursor/                          # local - Cursor integration (v3); rules, skills, commands, mcp.json
│   ├── commands/
│   ├── rules/
│   │   └── agent_onboarding.mdc
│   └── skills/
├── .vscode/                          # (future) VS Code / local agent integration - not in v3
├── library/                          # tracked - IDE-neutral foundation content
│   ├── agent_foundation.json
│   ├── .workspace_setup_required     # tracked first-run marker (removed locally after bootstrap)
│   ├── README.md
│   ├── databases/                    # tracked README + db; runtime subdirs below
│   │   ├── db/                       # tracked - session_logs.db (MCP default)
│   │   ├── schemas/                  # e.g. session_logs.sql
│   │   ├── scripts/                  # e.g. ingest_session_logs.py
│   │   ├── sources/                  # runtime
│   │   ├── README.md
│   │   └── workspace_mcp_servers.md
│   ├── docs/                         # runtime category folders (user content)
│   │   ├── devtools/
│   │   ├── frameworks/
│   │   ├── hardware/
│   │   ├── languages/
│   │   └── wikis/
│   ├── sessions/                     # runtime log dirs; README tracked
│   │   ├── current/                  # local - active session .md files
│   │   ├── recent/                   # local
│   │   ├── archived/                 # local - monthly .zip archives
│   │   └── README.md
│   ├── templates/                    # tracked - copy/edit templates
│   │   ├── mcp.json.example
│   │   ├── session_template.md
│   │   ├── README_LIBRARY.md
│   │   ├── README_PROJECT.md
│   │   └── knowledge_base_index.md
│   └── tools/
│       ├── README.md
│       ├── mcp_sqlite_server/        # tracked - MCP server (npm install -> node_modules local)
│       └── scripts/                  # tracked
│           ├── setup_workspace.py    # bootstrap dirs + workspace pairing
│           ├── setup_database.py     # mcp.json + npm install
│           └── session_tools.py      # session log create / maintain / ingest
├── projects/                         # runtime - *.code-workspace pairing files (local paths)
├── tests/                            # runtime - scratch space for agents and humans
├── .agentignore
├── .cursorignore
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
└── RELEASE_NOTES.md
```

Open **this repo root** in your editor (Cursor for v3) for shared agent config and MCP. External code lives elsewhere; link it with `setup_workspace.py --pair` (writes under `projects/`). VS Code multi-root workspaces use the same file format.

---

## Usage

### Sessions

Session logs live in `library/sessions/current/` (archived automatically after maintenance runs).

```bash
python library/tools/scripts/session_tools.py           # interactive
python library/tools/scripts/session_tools.py --prune   # maintenance
```

### Workspace and projects

Resonance7 is the **foundation** repo. Project source code stays in separate folders on disk.

```bash
# Bootstrap only (also runs with no flags)
python library/tools/scripts/setup_workspace.py

# Pair an existing external folder (writes projects/my-app.code-workspace)
python library/tools/scripts/setup_workspace.py --pair my-app --project-path "D:/dev/my-app"

# Menu: bootstrap, pair, status
python library/tools/scripts/setup_workspace.py --interactive
```

Pairing files are gitignored (they contain local paths). Open the `.code-workspace` file in Cursor or VS Code for a multi-root workspace.

### Agent foundation

`library/agent_foundation.json` defines universal agent protocols: communication, session logging, file creation policy, and development workflows. In v3, Cursor loads onboarding from `.cursor/rules/agent_onboarding.mdc`, which points agents at this file; v4 will add parallel entry points for other hosts without moving the foundation file.

---

## Documentation

- [Library overview](library/README.md)
- [Databases and MCP](library/databases/README.md)
- [Session management](library/sessions/README.md)
- [Tools and scripts](library/tools/README.md)
- [MCP SQLite server](library/tools/mcp_sqlite_server/README.md)

---

## Configuration

| File | Role |
|------|------|
| `.agentignore` | Paths agents should not modify without explicit request |
| `.cursorignore` | Cursor indexing exclusions (editor-specific; v3) |
| `.gitignore` | Keeps local session payloads, `node_modules`, and `.cursor/mcp.json` out of Git |

Example `.agentignore` entries:

```
library/agent_foundation.json
library/sessions/archived/
```

**MCP:** `.cursor/mcp.json` is local. Regenerate with `python library/tools/scripts/setup_database.py` after clone or when Node paths change. Details: `library/tools/mcp_sqlite_server/SETUP.md`.

---

## Philosophy

1. **Mutual respect** - User and agent are partners; both perspectives matter.
2. **Knowledge persistence** - Session logs, curated docs under `library/docs/`, and MCP-queryable databases accumulate context across sessions.

---

## License

MIT - see [LICENSE](LICENSE).

Contributions welcome: issues, pull requests, and use-case feedback on GitHub.
