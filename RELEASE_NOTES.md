# Resonance7 v3.0.0 - Foundation layout, bootstrap, and session ingest

**Release date:** 2026-06-29

**Documentation note:** This is the **last release** shipped with `RELEASE_NOTES.md` in the repository. From the next release onward, user-facing release notes will appear on **GitHub release pages** and in **`CHANGELOG.md`** only. This file remains in v3.0.0 so you can paste it for the GitHub release post; it will not be updated for future versions.

v3 reorganizes the workspace around an **IDE-neutral `library/` core** with Cursor integration in `.cursor/`. Sessions, databases, templates, and Python tools move to consistent v3 paths. **First-run bootstrap** (`setup_workspace.py`), **external project pairing** (no embedded project trees or symlinks), and a restored **session log ingest** pipeline round out the release. Agent **authorization policy** in `agent_foundation.json` now defaults to assess-then-act with explicit approval before edits.

v3 keeps Cursor as the primary supported editor. **VS Code MCP config** (dual emit from `setup_database.py`) is planned for a follow-up release, not v3.0.0.

## Migration (from 2.x)

### Paths (update scripts, habits, and docs)

| v2.x | v3.0.0 |
|------|--------|
| `sessions/` | `library/sessions/` (`current/`, `recent/`, `archived/`) |
| `library/resources/databases/` | `library/databases/` (`db/`, `schemas/`, `scripts/`, `sources/`) |
| `library/tools/setup_database.py` (etc.) | `library/tools/scripts/setup_database.py` |
| `library/tools/session_tools.py` | `library/tools/scripts/session_tools.py` |
| `library/tools/project_tools.py` | **Removed** - use `setup_workspace.py --pair` |
| `library/templates/configuration_templates/` | Flat `library/templates/` (`mcp.json.example`, `session_template.md`, ...) |

`session_tools.py` still accepts a legacy root `sessions/` fallback when resolving paths, but new work should use `library/sessions/`.

### Projects

- **`projects/`** holds local **`*.code-workspace`** files that pair this repo with **external** project folders (paths are machine-specific and gitignored).
- No more embedded `projects/<name>/` trees or `library/` / `sessions/` symlinks into projects.
- Pair a project: `python library/tools/scripts/setup_workspace.py --pair my-app --project-path "D:\dev\my-app"`

### First clone on a new machine

1. `python library/tools/scripts/setup_workspace.py` - creates runtime dirs; removes `library/.workspace_setup_required` locally when complete.
2. `python library/tools/scripts/setup_database.py` - writes `.cursor/mcp.json`, runs `npm install` in `library/tools/mcp_sqlite_server`.
3. Reload Cursor.

### Session log database (optional)

- Shipped placeholder: `library/databases/db/session_logs.db` (empty).
- Refresh for MCP recall when you want it: `python library/tools/scripts/session_tools.py --ingest`
- Ingest is **not** automatic at handoff; run only when you explicitly want the DB updated.

### MCP config

If you hand-edit MCP, use `library/templates/mcp.json.example` (not `configuration_templates/`). Default DB path is `library/databases/db/session_logs.db`.

## What is new

### Workspace bootstrap and pairing

- **`library/tools/scripts/setup_workspace.py`** - Idempotent runtime directory creation; `--pair` writes multi-root workspace files under `projects/`; `--interactive` menu; `--show` for status.
- **`library/.workspace_setup_required`** - First-run sentinel on fresh clones; removed locally after bootstrap (tracked in Git so new clones know to bootstrap).
- **`.cursor/rules/workspace_first_run.mdc`**, **`workspace_bootstrap.mdc`** - Agent guidance for first-run bootstrap.

### Layout and documentation

- **`library/databases/`** - Consolidated from `library/resources/databases/`; schemas under `schemas/`, ingest under `scripts/`, DB files under `db/`.
- **`library/sessions/`** - Canonical session log location.
- **Root `README.md`** - v3 Quick Start, directory tree, IDE/agents section (Cursor now, IDE-neutral direction for v4).
- **Fewer placeholder READMEs** - Less per-folder noise; session logs and root docs carry more of the story.

### Session log ingest (restored)

- **`library/databases/scripts/ingest_session_logs.py`** - Ingests `library/sessions/current/`, `recent/`, and `archived/*.zip` into `session_logs.db` (FTS5 over section content).
- **`library/databases/schemas/session_logs.sql`** - Schema applied on first ingest.
- **`session_tools.py --ingest`** - Delegates to the ingest script; menu option 5 in interactive mode.

### Agent foundation and commands

- **`agent_foundation.json`** - v3 paths, `workspace_setup` block; **authorization policy** simplified to: assess in chat, act only on clear user approval (replaces phrase-list intent detection).
- **Commands** - `/start`, `/session`, `/help`, `/foundation` aligned with v3 paths and onboarding order.

### Removed

- **`library/tools/project_tools.py`** - Replaced by external pairing via `setup_workspace.py`.

## Planned (not in v3.0.0)

- **`setup_database.py` dual emit** - `.vscode/mcp.json` alongside `.cursor/mcp.json` for VS Code / local agent workflows.
- **Session ingest at handoff** - Opt-in automation when session status leaves Active (design only today).
- **Session date recognition** - Smarter continue-vs-new-session behavior in `session_tools.py`.

## Getting started (new clone)

```bash
python library/tools/scripts/setup_workspace.py
python library/tools/scripts/setup_database.py
# Reload Cursor
python library/tools/scripts/session_tools.py    # create or manage session logs
python library/tools/scripts/session_tools.py --ingest   # optional: populate session_logs.db
```

In Cursor: `/start` for onboarding checks, `/foundation` to load protocols, `/help` for topics.

## Requirements

- Python 3.7+
- Git
- **Node 18+** (for SQLite MCP) - same Node for `mcp.json` `command` and `npm install` in `library/tools/mcp_sqlite_server`
- **Cursor** recommended for v3 (rules, skills, MCP); `library/agent_foundation.json` and Python tools work without it

## Full changelog

[Compare v2.1.0...v3.0.0](https://github.com/ViewtifulSlayer/Resonance7/compare/v2.1.0...v3.0.0) - see [CHANGELOG.md](CHANGELOG.md).

---

# Resonance7 v2.1.0 - MCP setup automation and local config

**Release date:** 2026-04-26

This release stops tracking **`.cursor/mcp.json`**, adds **`library/tools/setup_database.py`** (absolute paths, **`npm install`**, optional audit) so each machine uses a consistent Node and native build for the MCP server, and expands **`/start`** so the SQLite MCP setup check is run, not only described. Ignore files, git attributes, **`README`**, and **`LICENSE`** have minor updates.

## Migration (from 2.0.0)

- If you relied on a committed **`.cursor/mcp.json`**, it is no longer in the repo. Run `python library/tools/setup_database.py` from the workspace root, then reload the Cursor window. Alternatively, copy `library/templates/configuration_templates/mcp.json.example` to `.cursor/mcp.json`, set absolute paths to your Node binary, `mcp_sqlite_server/src/server.js`, and `session_logs.db`, then run `npm install` in `library/tools/mcp_sqlite_server` with the same Node, and reload Cursor.

## What is new

### SQLite MCP and setup

- **`library/tools/setup_database.py`** - One entry point: write **`.cursor/mcp.json`**, install npm deps in **`library/tools/mcp_sqlite_server`**, optional **`npm audit fix`**, and clear errors when Node is missing or versions mismatch.
- **Example template** - **`library/templates/configuration_templates/mcp.json.example`** replaces the old **`library/templates/example-mcp.json`** (removed) for hand-edits.
- **Lockfile** - Updated **`package-lock.json`** in **`mcp_sqlite_server`**; **`SETUP.md`** notes aligned with the script.

### Onboarding and commands

- **`/start`** (**.cursor/commands/start.md**) - Documents the full MCP check: script vs. manual, placeholder detection, path validation, dependency install, **reload Cursor** after changes.
- **`.cursor/rules/agent_onboarding.mdc`** - Clarifies when agents load **`agent_foundation.json`** and how that fits **`/start`**.

### Repository hygiene

- **`.gitignore`**, **`.agentignore`**, **`.cursorignore`**, **`.gitattributes`** - Tuned for local MCP config, tool paths, and cross-platform diffs; **`README.md`** and **`LICENSE`** - minor text updates.

## Requirements

- Python 3.7+
- Git
- **Node 18+** (for SQLite MCP) - use the same install for both **`mcp.json`** **`command`** and **`npm install`** in **`library/tools/mcp_sqlite_server`**
- Cursor (recommended) or another IDE with equivalent rules support

## Full changelog

[Compare v2.0.0...v2.1.0](https://github.com/ViewtifulSlayer/Resonance7/compare/v2.0.0...v2.1.0) - see [CHANGELOG.md](CHANGELOG.md).

---

# Resonance7 v2.0.0 - Session MCP, ingest, and project layout

**Release date:** 2026-04-04

This release adds a **queryable session log database** (`session_logs`) with an **ingest pipeline**, tightens **Cursor onboarding and commands**, refines the **agent foundation**, and changes how **new projects** link into the framework (see breaking change below).

## Breaking change: project symlinks

`library/tools/project_tools.py` now creates **`library/`** and **`sessions/`** symlinks only. **`.cursor/` is no longer symlinked** into `projects/<name>/`, so nested projects do not duplicate rules, skills, or MCP configuration. Open the **Resonance7 workspace root** in Cursor for shared `.cursor/`, or add a small local `.cursor/` only if you open a project folder by itself.

If you created projects with an older framework, you may still have a **`.cursor` symlink** under that project; delete it if you see duplicate or conflicting IDE behavior.

## What's new

### Session logs and MCP

- **Ingest** - `library/resources/databases/scripts/session_logs/ingest_session_logs.py` builds or updates **`session_logs.db`** from `sessions/current/`, `sessions/recent/`, and optional archives (FTS for search).
- **Run ingest when you want it** - Not automatic; run when you explicitly want the DB refreshed (see session command guidance).
- **`sessions/INDEX.md`** - Template for a human-readable index alongside the database.
- **MCP SQLite server** - Defaults to `session_logs.db` under `library/resources/databases/db/`; supports a **`session_logs`** alias. Point your SQLite MCP config at that `db/` directory (see `library/resources/databases/workspace_mcp_servers.md` and `library/tools/mcp_sqlite_server/README.md`).

### Tooling and agent workflow

- **`project_tools.py`** - Renamed from `project_setup.py` for clarity; docs and commands updated.
- **Onboarding** - `.cursor/rules/agent_onboarding.mdc` and `.cursor/commands/foundation.md` enforce sequential foundation load and the verification phrase before user work.
- **Commands** - `start` and `session` use GitHub-friendly checklists and ASCII arrows; session flow clarifies `last_updated` and ingest-on-request.
- **`agent_foundation.json`** - Shorter and clearer; adds **intent vs command** detection so goals are not treated as immediate execution orders.
- **Skills** - `database-specialist`, `mcp-sqlite`, and `markdown-punctuation` use portable placeholders and naming examples.

### Repository hygiene

- **`.gitignore`** - Ignores `library/resources/databases/db/*.db` so generated databases stay local.

## Getting started

1. **Clone** the repo and open the **workspace root** in Cursor.
2. **Sessions:** `python library/tools/session_tools.py`
3. **New project:** `python library/tools/project_tools.py --project my-project`
4. **Session DB (optional):** Run the ingest script when you want MCP-queryable logs; configure MCP per `workspace_mcp_servers.md`.

## Requirements

- Python 3.7+
- Git
- Cursor (recommended) or another IDE with equivalent rules support

## Full changelog

[Compare v1.3.0...v2.0.0](https://github.com/ViewtifulSlayer/Resonance7/compare/v1.3.0...v2.0.0) - see [CHANGELOG.md](CHANGELOG.md).

---

# Resonance7 v1.3.0 - Enhanced Foundation & Framework Improvements

**Release Date:** December 13, 2025

This release focuses on enhancing the core agent foundation, reorganizing workspace structure, and improving framework documentation and resource management.

## What's New

### Enhanced Agent Foundation

- Added action authorization policy to distinguish information requests from action requests
- Improved agent behavior guidance and partnership model
- Strengthened file creation protocols and knowledge persistence philosophy
- Enhanced development workflows and best practices

### Workspace Reorganization

- **Documentation Structure**: Moved `library/docs/` to `library/resources/docs/` for better resource grouping
- **Knowledge Base Support**: Added `library/resources/wikis/` for knowledge base databases with MCP SQLite Server integration
- **Template Organization**: Organized templates into `library/templates/documentation_templates/` and `library/templates/project_template/`
- **Tool Naming**: Renamed `setup_project.py` to `project_setup.py`, then to `project_tools.py` for clearer naming

### Resource Management

- Enhanced `.cursorignore` and `.gitignore` patterns for better resource management
- Knowledge base databases excluded from indexing while preserving markdown index files for discoverability
- Fixed `.gitignore` to properly exclude knowledge base database files (`.db`, `.sqlite`, `.sqlite3`) from git tracking
- Fixed `.gitignore` to allow `library/resources/README.md` to be tracked (added exception rule)
- Improved template generation (failsafe only, template tracked in git)

## Implementation Status

### Fully Implemented
- Enhanced agent foundation with action authorization policy
- Workspace reorganization and resource structure improvements
- Knowledge base database support with MCP SQLite Server integration
- Template organization and path fixes
- Updated command system with correct template paths
- Fixed `.gitignore` patterns for knowledge base databases

## Key Features

- Enhanced agent foundation with action authorization policy
- Reorganized resource structure for better organization
- Knowledge base database support
- Improved template management
- Better ignore file patterns for resource management

## Changes

- Enhanced agent foundation with action authorization policy
- Reorganized documentation and resource structure
- Added knowledge base database support
- Improved project template structure and generation
- Updated tool naming and path references
- Fixed `.gitignore` to properly exclude knowledge base databases and allow README tracking

## Getting Started

### For New Projects

1. **Create project**: `python library/tools/project_tools.py --project my-project`
2. **Start working**: Agents follow the universal foundation protocols

### For Existing Projects

Continue using the enhanced agent foundation for consistent behavior across all projects.

## Documentation

- **[Library Documentation](library/README.md)** - Core resources and agent foundation
- **[Documentation Modules](library/resources/docs/README.md)** - Knowledge base organization
- **[Knowledge Bases](library/resources/wikis/README.md)** - Database access and knowledge bases

## Requirements

- Python 3.7 or higher
- Git
- A compatible IDE (Cursor recommended, but any IDE can be adapted)

## Testing

This release is being tested as a branch diverging from main. Enhanced foundation features are ready for testing.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Full Changelog:** [v1.2.0...v1.3.0](https://github.com/ViewtifulSlayer/Resonance7/compare/v1.2.0...v1.3.0)
