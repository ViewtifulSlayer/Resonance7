# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [4.0.0] - 2026-09-26

Freebuff-first migration. The workspace is no longer Cursor-specific: always-on agent context lives in a root `AGENTS.md`, skills live in `.agents/skills/`, and MCP configuration is generated at `.agents/mcp.json`.

### Breaking changes

- **Cursor integration removed** - `.cursor/commands/` (`foundation`, `help`, `session`, `start`), `.cursor/rules/` (`agent_onboarding`, `workspace_bootstrap`, `workspace_first_run`), `.cursor/skills/`, and `.cursorignore` are deleted. Root `AGENTS.md` and `.agents/skills/` replace them; the `foundation` and `help` command content is folded into `AGENTS.md`.
- **MCP config path** - `setup_database.py` writes `.agents/mcp.json`. Cursor config generation and Cursor-config seeding are gone; no `.cursor/mcp.json` is emitted.
- **`setup_workspace.py` removed** - `library/tools/scripts/setup_workspace.py` (529 lines) is replaced by `setup.py` plus on-demand creation of runtime directories. As a consequence `setup_workspace.py --pair` no longer exists; external projects are paired by adding a multi-root `projects/*.code-workspace` file. See Known issues.
- **No bootstrap step** - The first-run sentinel `library/.workspace_setup_required` is deleted. `session_tools.py` creates `library/sessions/current/` when it is missing, and `setup.py --init-dirs` creates the remaining runtime directories.
- **`RELEASE_NOTES.md` retired** - The file is deleted and all live references are removed. `CHANGELOG.md` is the only ongoing release record.

### Added

- **Root `AGENTS.md`** - Always-on agent context, auto-read at session start: agent onboarding, capability-availability policy, MCP notes, session-logging rules, a skill index, and the file-safety/approval policy.
- **`.agents/skills/`** - Nine portable skill packages converted from `.cursor/skills/`: `codebuff`, `database-specialist`, `freebuff`, `ghidra-expert`, `markdown-punctuation`, `mcp-sqlite`, `python-expert`, `skill-authoring`, `vscode`.
- **`library/tools/scripts/setup.py`** - First-run doctor, runtime-directory creation (`--init-dirs`), dependency and MCP setup, with report-only and `--dry-run` modes.
- **`library/tools/setup_requirements.json`** - Declarative requirements manifest consumed by `setup.py`.
- **`setup_database.py --global-agents`** - Syncs the managed SQLite MCP server entry into a global `~/.agents` config.
- **`session_tools.py --auto`** - Skips the interactive menu and the confirmation prompt, so `--auto --dry-run` runs unattended and exits 0 without writing. Without the flag the interactive menu is unchanged.
- **MCP `list_databases` tool** - Scans `library/databases/db/*.db` and returns alias (filename stem) and absolute path for each file.
- **MCP auto-alias resolution** - `database_path` accepts any stem matching `library/databases/db/<stem>.db` without hand-editing `server.js` or the MCP config.
- **`library/templates/workspace_mcp_servers.md`** - Framework-only MCP reference template; copied to the gitignored `library/databases/workspace_mcp_servers.md` locally (same pattern as `mcp.json.example` -> `.agents/mcp.json`).
- **Session-log lifecycle rules** - `agent_foundation.json` records `previous_session_handoff` (close a prior `Handoff` log as `Completed` when opening a new one) and `log_reuse` (reuse the current log across a day change rather than starting a new file).

### Changed

- **`library/tools/scripts/setup_database.py`** - Writes `.agents/mcp.json` (Freebuff/Codebuff) only; retains managed-server merge behaviour and `--skip-audit-fix`; drops Cursor dual-emit and config seeding. Existing JSON is still read with UTF-8 BOM tolerance (Windows).
- **`.gitignore` / `.agentignore`** - Cursor transitional rules, onboarding/bootstrap allowlist entries, and media/bootstrap exceptions replaced with editor-neutral allowlists. Machine-local `.agents/mcp.json`, `node_modules/`, and local `db/*.db` files are ignored.
- **`.gitignore` allowlist policy** - Separates framework from local content: root `AGENTS.md`, `.agents/skills/`, `library/tools/` README, MCP SQLite server package, and setup scripts; database READMEs, schema, and ingest script; session lifecycle `README.md` only. Ignores session log payloads, user `library/docs/**`, runtime `db/*.db` and `sources/`, scratch `tests/`, and project pairing files. Parent-directory un-ignore entries (`!.../**/`) under `library/tools/` and `library/databases/` so Git can reach nested allowlisted files.
- **Database git policy** - All `library/databases/db/*.db` files are local-only; `library/databases/db/` is created by `setup.py`. Populate `session_logs.db` via ingest when desired (MCP starts without it; default queries need the file).
- **`library/agent_foundation.json`** - `workspace_architecture` describes `.agents/` and root `AGENTS.md` instead of `.cursor/`; `workspace_setup` drops `bootstrap_tool` and `first_run_marker` in favour of on-demand runtime folders.
- **Docs and templates** - Root `README.md`, `library/README.md`, `library/databases/README.md`, `library/sessions/README.md`, `library/tools/README.md`, `workspace_mcp_servers.md`, and `README_PROJECT.md` use Freebuff/editor-neutral wording and the `setup.py` flow. `README_PROJECT.md` no longer references the removed `--pair` command and documents `projects/*.code-workspace` files as local-path-specific and gitignored.
- **`session_tools.py`** - Two help/error messages that named the removed `setup_workspace.py` now direct users to create the session directory or run `setup.py --init-dirs`.
- **MCP server package** - `package.json` keyword `cursor` replaced with `freebuff`; `package-lock.json` refreshed (MCP SDK 1.29.0, better-sqlite3 11.10.0). Node import and the better-sqlite3 native binding verified on Windows.
- **`session_tools.py` / `ingest_session_logs.py` ingest dry-run** - Menu option 5 and `--ingest` honor `--dry-run`: list files that would be ingested without writing `session_logs.db` (previously dry-run still updated the database).
- **`library/databases/workspace_mcp_servers.md` git policy** - No longer tracked; userland MCP notes (e.g. Scryfall) belong in the local copy or `library/docs/`, not in the framework repo. Removes erroneous userland content from `main`.
- **`library/tools/mcp_sqlite_server/src/server.js`** - `resolveDatabasePath()` resolves db-dir stems; tool schemas document alias behavior.
- **Docs for auto-aliases** - `library/databases/README.md`, `workspace_mcp_servers.md`, `mcp_sqlite_server/README.md`, and root `README.md` document auto-aliases, local DB policy, and gitignore scope.

### Fixed

- **`session_tools.py` aborted when output was redirected (Windows)** - Piped or redirected stdout fell back to the console code page (cp1252), so the first glyph raised `UnicodeEncodeError` and exited 1 (for example the magnifier in `DRY RUN MODE`). New `enable_utf8_output()`, called at the start of `main()`, reconfigures stdout and stderr with `encoding="utf-8", errors="replace"`.
- **Trailing whitespace in `session_tools.py`** - Removed from the blank line after the new `--auto` argparse block, so `git diff --check` passes.

### Removed

- **`library/tools/scripts/setup_workspace.py`** - Replaced by `setup.py` and on-demand runtime-directory creation.
- **`library/.workspace_setup_required`** - First-run sentinel; the bootstrap step is gone.
- **`RELEASE_NOTES.md`** - Retired; `CHANGELOG.md` is the sole ongoing release record.
- **`.cursor/`** - Commands, rules, skills, and `.cursorignore`.
- **Tracked `session_logs.db` placeholder** - No empty session log database in the repository; created locally via optional ingest.

### Known issues

- **Project pairing is manual again** - `setup_workspace.py --pair` was removed with the bootstrap script and no replacement command exists in `setup.py`. Pairing an external project now means hand-writing a multi-root `projects/*.code-workspace` file. A portable `--pair` equivalent is the obvious follow-up.

- **`setup_database.py --help` Node install message** - Running `python library/tools/scripts/setup_database.py --help` always prints the Node 18+ install block at the end because it is wired as argparse `epilog` (`_node_install_instructions()`), not because Node failed detection. A successful `--dry-run` or normal run can still find Node. Planned fix: emit install guidance only when `resolve_node_exe()` actually fails.
- **`session_tools.py` prune collision rename** - `move_old_sessions()` appends `_YYYYMMDD_HHMMSS` to the filename when the same `YYYYMMDD-NN.md` already exists in `recent/` (no content check). Consolidating sessions into `current/` while copies remain in `recent/` produces timestamp-suffixed duplicates (e.g. `20260219-01_20260701_014942.md`). Planned fix: compare content (identical = skip move); on real differences, prompt or renumber per policy.
- **`session_tools.py` `extract_session_date()` too strict** - Only matches `^YYYYMMDD-NN.md$`. Prune collision suffixes (`_*_HHMMSS`) and legacy continuation names (`_*_ptN`, `-*-ptN`) are not parsed, so 90-day `recent/` cleanup can skip them and leave orphans. Planned fix: parse session date from the leading `YYYYMMDD-NN` stem for all supported filename variants.
- **`ingest_session_logs.py` stale rows after re-ingest** - Upserts by `session_id` (`INSERT OR REPLACE`) but never deletes rows for files removed or renamed on disk. After a filename cleanup, old IDs (timestamp duplicates, `_pt*` stems) remain in `session_logs.db` until the DB file is deleted or replaced. Planned fix: optional full rebuild or prune pass for IDs not seen in the current ingest set.
- **`ingest_session_logs.py` collision precedence** - Ingest order is archived, then `current/`, then `recent/`; later sources win on the same `session_id`. `recent/` overwrites `current/`, which is counterintuitive when both hold the same session. Planned fix: document clearly or prefer `current/` over `recent/`.
- **Session continuation `_pt*` filenames** - `session_tools.py` continuation flow still uses `YYYYMMDD-NN_pt2.md` (and renames the original to `_pt1`). Convention is redundant with same-day `YYYYMMDD-NN` numbering; historical logs may use inconsistent `_pt` / `-pt` suffixes. Planned fix: retire `_pt*`; continuations use next `-NN` for that date; migrate existing files and `previous_part` / `next_part` links.
- **UTF-8 BOM breaks session frontmatter parsing** - `session_tools.py` (prune status updates) and `ingest_session_logs.py` read session `.md` files with `encoding='utf-8'`, so a UTF-8 BOM (`EF BB BF`) before the opening `---` prevents the frontmatter regex from matching. Prune logs "No YAML frontmatter" / skips status update; ingest may miss metadata. Common when Windows editors save "UTF-8 with BOM". `setup_database.py` already uses BOM-tolerant reads; session tooling does not. Planned fix: read with `utf-8-sig` (and optionally normalize on write).

## [3.0.0] - 2026-06-29

### Added
- **`library/tools/scripts/setup_workspace.py`** - Bootstrap runtime directories; pair external projects via `projects/*.code-workspace`; first-run sentinel `library/.workspace_setup_required`.
- **`.cursor/rules/workspace_first_run.mdc`**, **`workspace_bootstrap.mdc`** - First-run and manual bootstrap guidance for agents.
- **IDE and agents** section in root README (v3 Cursor, v4 IDE-neutral direction).
- **Session log ingest** - `library/databases/scripts/ingest_session_logs.py` + `library/databases/schemas/session_logs.sql`; run via `session_tools.py --ingest`.

### Changed
- **Sessions** - Canonical path is **`library/sessions/`** (not root `sessions/`). `.gitignore` updated accordingly.
- **Databases** - **`library/resources/`** consolidated into **`library/databases/`**; `.gitignore` database policy (allow-list schema, ingest, README breadcrumbs, empty `session_logs.db`; ignore `sources/` and other runtime DBs).
- **Scripts** - Core Python tools under **`library/tools/scripts/`** (`setup_workspace`, `setup_database`, `session_tools`).
- **Templates** - Flat layout: `library/templates/session_template.md`, `mcp.json.example` (removed nested `documentation_templates/` and `project_template/` trees).
- **Projects** - **`projects/`** holds local `*.code-workspace` pairing files only (no embedded project trees).
- **README** - Restructured for v3 Quick Start, directory tree, and external-project model.
- **`session_tools.py`** - Resolves `library/sessions/current/`; `--ingest` calls `library/databases/scripts/ingest_session_logs.py`.
- **Commands** - `/start`, `/session`, `/help` aligned with v3 paths; `agent_foundation.json` updated for `library/sessions/`, `library/tools/scripts/`, and `workspace_setup`.

### Removed
- **`library/tools/project_tools.py`** - Replaced by `setup_workspace.py` pairing model.
- **Placeholder README proliferation** - Fewer per-folder READMEs under sessions, resources, and project templates.

### Planned
- `setup_database.py` dual emit for Cursor and VS Code MCP config
- Session ingest permissions at handoff (opt-in)
- (Planned) Session log date recognition for continuing vs new sessions

### Deferred hardening (post-v3.0.0)
- **`.cursorignore` alignment** - Mirror `tests/**` and `library/databases/sources/**`; exclude `library/databases/db/*.db` and `.cursor/mcp.json` from indexing (paths documented in `library/databases/README.md`).
- **`.agentignore` scope** - Only `foundation.md` and `agent_onboarding.mdc` are protected among commands/rules; other commands and bootstrap rules remain editable unless policy expands.
- **Ingest/schema** - Intentionally tracked, indexed, and agent-editable; DB binaries protected in `.agentignore` (mutate via ingest scripts).
- **Additional `.db` files** - Gitignored by default under `library/databases/**` allow-list; add explicit `!` exceptions when new reference DBs ship.
- Deeper foundation assessment (overlap with rules/skills, trimming)
- Foundation meta-lesson bullets beyond `lookahead_vs_execute` (user-approved wording)

## [2.1.0] - 2026-04-26

### Added
- **`library/tools/setup_database.py`** - Writes a machine-local **`.cursor/mcp.json`** with absolute paths, runs **`npm install`** (and **`npm audit fix`**, optional skip) in **`library/tools/mcp_sqlite_server`** so Node and `better-sqlite3` match; prints Node/npm guidance if Node is missing.
- **`library/templates/configuration_templates/mcp.json.example`** - Committed template shape for hand-editing if you do not use the setup script; documents **`DEFAULT_DB_PATH`** and Node **`command`** fields.

### Changed
- **SQLite MCP config is no longer tracked** - **`.cursor/mcp.json`** is **gitignored**; clone/fetch no longer overwrites a developer's local MCP entry. Regenerate with **`python library/tools/setup_database.py`** (or copy from the example template) after pull or on a new machine.
- **`.gitignore`** - Ignores **`.cursor/mcp.json`**, with allow-list exceptions so **`library/tools/mcp_sqlite_server/`** and **`setup_database.py`** stay tracked; other ignore refinements.
- **`.agentignore`**, **`.cursorignore`**, **`.gitattributes`** - Tuned patterns and attributes for tools and line endings; fewer noisy diffs in mixed environments.
- **`.cursor/commands/start.md`** - Expanded with mandatory **MCP setup check** (path validation, **`npm install`**, Windows **`Test-Path`** / Unix **`test`**, optional import smoke test, **reload Cursor** after changes).
- **`.cursor/rules/agent_onboarding.mdc`** - Aligned with the **`/start`** flow (when to re-read `agent_foundation.json` vs. session reuse).
- **`library/tools/mcp_sqlite_server/SETUP.md`**, **`package-lock.json`** - Dependency lock and setup notes in step with the setup script and Node 18+ **`engines`**.

### Removed
- **`library/templates/example-mcp.json`** - Replaced by **`mcp.json.example`** under **`library/templates/configuration_templates/`** (kebab-case template layout).

## [2.0.0] - 2026-04-04

### Breaking changes
- **Project symlinks (`project_tools.py`)**: New projects receive **`library/`** and **`sessions/`** symlinks only. **`.cursor/` is not symlinked** into `projects/<name>/` (avoids duplicated Cursor rules and MCP configuration). Use the workspace root in Cursor for shared `.cursor/`, or maintain a minimal local `.cursor/` if you open a single project folder. Older project folders may still have a legacy `.cursor` link; remove it manually if you see duplicate IDE behavior.

### Added
- **`sessions/INDEX.md`** – Human-readable session index template (`session_logs.db`, ingest script, example topic groups).
- **Session log ingest** – `library/resources/databases/scripts/session_logs/ingest_session_logs.py` ingests `sessions/current/`, `sessions/recent/`, and optionally archived zips into **`session_logs.db`** for MCP-queryable recall (FTS).
- **`session_logs` reference database** – Ingest creates the DB and schema on first run when missing.
- **`library/resources/databases/workspace_mcp_servers.md`** – MCP server quick reference; SQLite alias and config pointers.
- **MCP SQLite server** – Default database path targets `session_logs.db` under `library/resources/databases/db/`; **`session_logs`** alias for explicit resolution (see server README and env vars).

### Changed
- Renamed **`library/tools/project_setup.py`** → **`library/tools/project_tools.py`** (commands, documentation, ignore allow-lists).
- **`.cursor/commands`** – `foundation`, `start`, and `session` aligned with onboarding: mandatory step order, verification phrase, GitHub-style task checklists, ASCII arrows where tooling prefers plain ASCII; session `last_updated` only on substantive edits; ingest only when the user asks.
- **`.cursor/skills`** – `database-specialist`, `mcp-sqlite`, and `markdown-punctuation` generalized (placeholders, `Resonance7-<server>` naming examples, ASCII-friendly punctuation guidance).
- **`library/agent_foundation.json`** – Condensed while preserving guidance; `intent_vs_command_detection` under command authorization; `knowledge_persistence` notes MCP-queryable databases; `session_log_database` and pointer to `workspace_mcp_servers.md`.
- **`.cursor/rules/agent_onboarding.mdc`** – Standard MDC format; sequential read → verify → proceed; redundant "Foundational Maintenance" folded into the main rule.
- **`.gitignore`** – `library/resources/databases/db/*.db` so generated MCP databases are not committed.
- **Documentation** – `library/README.md`, project template READMEs, and framework README project tree describe symlink layout (library + sessions only) and root `.cursor/` behavior.
- **`library/resources/databases/`** docs – README and scripts README center `session_logs` as the reference MCP database.

## [1.3.0] - 2025-12-13

### Changed
- Renamed `library/tools/setup_project.py` to `library/tools/project_setup.py` for better naming consistency
- Reorganized documentation structure:
  - Moved `library/docs/` to `library/resources/docs/` for better resource grouping
  - Updated all references to documentation modules to reflect new location
- Updated project template generation:
  - Template generation now acts as failsafe only (template tracked in git)
  - Function checks if template exists before generating
- Updated command files:
  - Fixed session template path in `.cursor/commands/session.md` to point to `library/templates/documentation_templates/session_template.md`
- Enhanced ignore file patterns:
  - Updated `.cursorignore` to properly handle `library/resources/docs/` and `library/resources/wikis/`
  - Updated `.gitignore` to exclude knowledge base databases while preserving index files
  - Refined patterns to allow markdown index files for discoverability
  - Added exception for `library/resources/README.md` to allow tracking of resources directory README
- Refined agent foundation:
  - Consolidated timestamp format specification (removed redundancy between format and timestamp_accuracy fields)
  - Updated session logging tool reference to correct path

### Added
- Knowledge base database support:
  - Added `library/resources/wikis/` directory for knowledge base databases
  - Created `library/resources/wikis/README.md` with database access documentation
  - Added MCP SQLite Server integration documentation
  - Created `knowledge_base_index.md` template for knowledge base navigation
- Resource organization:
  - Created `library/resources/README.md` as index for shared resources
  - Organized templates into `library/templates/documentation_templates/` and `library/templates/project_template/`
  - Renamed README templates to lowercase (`readme_project.md`, `readme_library.md`, `readme_minimal.md`)
- Minimal READMEs for empty documentation subdirectories (`dev_tools/`, `frameworks/`, `languages/`, `hardware/`)
- Enhanced agent foundation:
  - Added `action_authorization_policy` to distinguish information requests ("check", "review", "could we") from action requests
  - Policy prevents agents from taking unauthorized actions on information-gathering requests

### Fixed
- Fixed template path references in `session_tools.py` to point to correct template location
- Fixed project setup tool to properly reference `project_template` directory
- Fixed all path references to use correct documentation and template locations
- Fixed `.gitignore` to properly exclude knowledge base database files (`.db`, `.sqlite`, `.sqlite3`) from being tracked
- Fixed `.gitignore` to allow `library/resources/README.md` to be tracked (added exception rule)
- Fixed `.gitignore` pattern for `.vscode/extensions.json` (added required `!.vscode/` directory re-inclusion)
- Fixed incorrect path in `.cursor/commands/start.md` (updated from `tools/session_tools.py` to `library/tools/session_tools.py`)

## [1.2.0] - 2025-11-21

### Added
- `ARCHITECTURE.md` template in workspace template (`library/workspace_template/docs/ARCHITECTURE.md`) - Generic architecture documentation template for future projects with sections for system architecture, data architecture, repository setup, and technical stack documentation

### Changed
- Enhanced `agent_foundation.json` with improved agent behavior guidance:
  - Added `mutual_respect` to core_philosophy - establishes partnership model with complementary strengths
  - Strengthened file creation prohibition - explicitly includes documentation files, analysis files, summary files with only session logs as exception
  - Refined `knowledge_persistence` philosophy - clarified it means using existing resources, not creating new files
  - Enhanced critical friend guidance - added specific criteria for when to challenge (safety, best practices, factual errors) vs. when to follow (preference, style, non-critical)
  - Added confidence language - encourages agents to work confidently within capabilities while maintaining humility
  - Added "When to challenge vs. when to follow" guidance to communication rules
  - Split long documentation rule into separate items for better readability
  - Removed redundant `documentation_principle` from development_protocols (covered in communication rules)
  - Added `timestamp_accuracy` rule to session_logging metadata_rules - explicitly requires getting actual current time via command, prohibits rounding to quarter hours
- Reorganized tools structure for better separation of concerns:
  - Moved universal tools (`session_tools.py`, `setup_workspace.py`) to `library/tools/` - now accessible via `library/` symlink
  - Moved batch launchers (`session_tools.bat`, `setup_workspace.bat`) to `library/tools/` for consistency
  - Projects now get independent `tools/` directories (not symlinked) for project-specific tools
  - Removed `tools/` symlink from shared resources - projects create their own `tools/` directories
  - Root `tools/` directory remains for user-specific tools (excluded from repository via `.git/info/exclude`)
  - Updated `setup_workspace.py` to create independent `tools/` directories in new projects
  - Updated workspace template to include `tools/` directory structure
  - Enhanced template regeneration to preserve `ARCHITECTURE.md` during regeneration
  - Updated workspace template `.gitignore` with symlink notes for clarity
- Updated LICENSE copyright to ViewtifulSlayer

### Fixed
- Fixed typos in `agent_foundation.json`: "collobration" → "collaboration", "well-stuctured" → "well-structured"
- Fixed JSON syntax error in communication array (nested array converted to separate string items)

## [1.1.1] - 2025-11-10

### Added
- README.md for projects directory documenting project creation, structure, and best practices

### Changed
- Removed `projects/.gitkeep` as it's been replaced by README.md

## [1.1.0] - 2025-11-09

### Added
- `.cursorignore` and `.agentignore` templates in workspace template
- Cursor command system (`/foundation`, `/help`, `/start`, `/session`)
- Batch file launchers for Python tools (`session_tools.bat`, `setup_workspace.bat`)
- README.md files in workspace template directories (`docs/`, `src/`, `tests/`)
- README.md files in sessions subdirectories (`current/`, `recent/`, `archived/`)

### Changed
- Enhanced `setup_workspace.py` to automatically create ignore files
- Updated prerequisites to make Python the sole manual requirement
- Improved workspace setup to support file symlinks (not just directories)

### Fixed
- Workspace template directories now tracked in Git (v1.0.0 had missing folders)

## [1.0.0] - 2025-11-09

### Added
- Initial release of Resonance7 framework
- Core workspace template system
- Session management tools (`session_tools.py`)
- Foundation configuration system (`agent_foundation.json`)
- Workspace setup automation (`setup_workspace.py`)
- Shared resource symlinking for projects
- Session lifecycle management (current → recent → archived)
- Cross-platform Python tooling

[Unreleased]: https://github.com/ViewtifulSlayer/Resonance7/compare/v4.0.0...HEAD
[4.0.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v3.0.0...v4.0.0
[3.0.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v2.1.0...v3.0.0
[2.1.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ViewtifulSlayer/Resonance7/releases/tag/v1.0.0

