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

Release history: [CHANGELOG.md](CHANGELOG.md)

---

## Overview

- **Agent foundation** - Core behavior and protocols in `library/agent_foundation.json`
- **Session logging** - Markdown logs under `library/sessions/` with lifecycle tooling
- **SQLite MCP** - Query `session_logs.db` and other workspace databases via MCP
- **Shared library** - Databases, docs modules, templates, and tools under `library/`
- **External projects** - Pair out-of-repo project folders via `projects/*.code-workspace` (see [Usage](#usage))
- **Cross-platform** - Python setup scripts; Node for the MCP server package

---

## IDE and agents

The core is **IDE-neutral**. The portable contract lives in `library/agent_foundation.json`, session logs, the Python tools, and the MCP SQLite server; editor-specific integration is a replaceable layer on top.

Agent context and skills live in **`AGENTS.md`** and **`.agents/skills/`** at the repo root, and MCP is configured in **`.agents/mcp.json`**. **Freebuff in VS Code** is the current integration target.

When adding features, prefer:

- Behavior and paths in `library/` and scripts (portable)
- Editor conveniences in `.agents/` (replaceable layer)
- MCP and Node setup that any MCP-capable client can reuse

---

## Quick Start

### Prerequisites

- **Python 3.7+**
- **Git**
- **Node.js 18+** (LTS recommended) - required for default setup; see [Node.js](#nodejs) below
- **Freebuff in VS Code** recommended (agent context, skills, MCP); `library/agent_foundation.json` and the Python tools work without it

### Installation

1. **Clone and enter the repo:**

   ```bash
   git clone https://github.com/ViewtifulSlayer/Resonance7.git
   cd Resonance7
   ```

2. **First-run setup** (idempotent; creates runtime folders and checks prerequisites):

   ```bash
   python library/tools/scripts/setup.py             # report state only
   python library/tools/scripts/setup.py --all --yes # dirs + MCP + missing prerequisites
   ```

   `setup.py` creates the gitignored runtime folders (`library/sessions/`, `library/docs/` categories, `library/databases/db` and `sources`, `projects/`, `tests/`), then runs `setup_database.py` (writes `.agents/mcp.json`, `npm install` in `library/tools/mcp_sqlite_server`, optional `npm audit fix`). It can opt to install missing external prerequisites declared in `library/tools/setup_requirements.json`. `node_modules/` is not in Git; every fresh clone needs this step.

3. **Reload your editor** so MCP picks up the new config.

4. **Verify:**

   - `library/agent_foundation.json` exists
   - `python library/tools/scripts/session_tools.py --help` runs
   - `library/tools/mcp_sqlite_server/node_modules/` exists after step 3

Hand-configuring MCP: copy `library/templates/mcp.json.example` to `.agents/mcp.json` (the Freebuff MCP config), set absolute paths, run `npm install` in `library/tools/mcp_sqlite_server` with the **same** Node binary as in `mcp.json`, then reload the editor.

### First Steps

```bash
# Session log (interactive)
python library/tools/scripts/session_tools.py
```

Onboarding and help are driven by **`AGENTS.md`** and the skills under **`.agents/skills/`**.

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

Legend: **tracked** = in Git by default | **runtime** = created on demand (`setup.py --init-dirs`; session folders also via `session_tools.py`) | **local** = gitignored or machine-specific

```
Resonance7/
├── .agents/                          # local - Freebuff integration; skills and generated mcp.json
│   └── skills/
├── AGENTS.md                         # tracked - always-on agent context
├── .vscode/                          # local - VS Code integration
├── library/                          # tracked - IDE-neutral foundation content
│   ├── agent_foundation.json
│   ├── README.md
│   ├── databases/                    # tracked README, schema, ingest; db/ runtime (gitignored)
│   │   ├── db/                       # runtime - local *.db (gitignored; created on demand)
│   │   ├── schemas/                  # e.g. session_logs.sql
│   │   ├── scripts/                  # e.g. ingest_session_logs.py
│   │   ├── sources/                  # runtime
│   │   ├── README.md
│   │   └── workspace_mcp_servers.md  # local - copy from templates/ when needed
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
│   │   ├── workspace_mcp_servers.md
│   │   ├── session_template.md
│   │   ├── README_LIBRARY.md
│   │   ├── README_PROJECT.md
│   │   └── knowledge_base_index.md
│   └── tools/
│       ├── README.md
│       ├── mcp_sqlite_server/        # tracked - MCP server (npm install -> node_modules local)
│       ├── setup_requirements.json   # external prerequisites manifest (setup.py)
│       └── scripts/                  # tracked
│           ├── setup.py              # first-run: runtime dirs + environment checks
│           ├── setup_database.py     # mcp.json + npm install
│           └── session_tools.py      # session log create / maintain / ingest
├── projects/                         # runtime - created by setup.py; *.code-workspace pairing files
├── tests/                            # runtime - created by setup.py; scratch space for agents and humans
├── .agentignore
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── LICENSE
└── README.md
```

Open **this repo root** in your editor for shared agent config and MCP. External code lives elsewhere; add a multi-root `.code-workspace` file under `projects/` to pair it. VS Code multi-root workspaces use the same file format.

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

Runtime folders (session, docs, and database scaffolding, `projects/`, and `tests/`) are gitignored and absent from a fresh clone. Create them with `python library/tools/scripts/setup.py --init-dirs`; `session_tools.py` also creates `library/sessions/current/` when it is missing.

To work across this foundation and an external folder, create a multi-root `.code-workspace` file under `projects/` listing both roots. Pairing files are gitignored (they contain local paths). Open the `.code-workspace` file in your editor for a multi-root workspace.

### Agent foundation

`library/agent_foundation.json` defines universal agent protocols: communication, session logging, file creation policy, and development workflows. Agents load it via `AGENTS.md` at the repo root; the foundation file itself stays host-neutral.

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
| `.gitignore` | Allowlist for framework files; keeps session payloads, local docs, runtime DBs, `node_modules`, and `.agents/mcp.json` out of Git |

Example `.agentignore` entries:

```
library/agent_foundation.json
library/sessions/archived/
```

**MCP:** `.agents/mcp.json` is local. Regenerate with `python library/tools/scripts/setup_database.py` after clone or when Node paths change. Details: `library/tools/mcp_sqlite_server/SETUP.md`.

---

## Philosophy

1. **Mutual respect** - User and agent are partners; both perspectives matter.
2. **Knowledge persistence** - Session logs, curated docs under `library/docs/`, and MCP-queryable databases accumulate context across sessions.

---

## License

MIT - see [LICENSE](LICENSE).

Contributions welcome: issues, pull requests, and use-case feedback on GitHub.
