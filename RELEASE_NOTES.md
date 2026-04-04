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
