# Session Index (Template)

This file is a **workspace-local index** of session logs under `sessions/`. It is intended as a **human-readable companion** to the `session_logs.db` SQLite database, which provides the authoritative, queryable index of all sessions.

- Paths are relative to `sessions/` (e.g. `current/20250101-01.md`).
- Example groupings below are **illustrative only**. Customize them for your own workspace and projects.
- To keep this file reusable, avoid hard-coding private or highly specific session details when sharing the template.

---

## Session Database (Quick Overview)

For long-term, queryable recall, this workspace ships with a **session logs database**:

- **Database path (default)**: `library/resources/databases/db/session_logs.db`
- **Schema**: `library/resources/databases/schemas/session_logs.sql`
- **Ingest script**: `library/resources/databases/scripts/session_logs/ingest_session_logs.py`
- **Sources ingested**:
  - `sessions/current/*.md`
  - `sessions/recent/*.md`
  - `sessions/archived/*.zip` (all `*.md` entries inside, excluding `README.md`)

Basic usage (from workspace root):

```bash
python library/resources/databases/scripts/session_logs/ingest_session_logs.py

# Options
python library/resources/databases/scripts/session_logs/ingest_session_logs.py --db-path path/to/session_logs.db \
  --sessions-root sessions \
  --no-archives \
  --current-only
```

> **Note**: The DB is the best source for searching by text, topics, or date. This `INDEX.md` is for **high-level navigation and examples**.

---

## Example Topic Groups

### Example: Game Project A

**Particularly relevant** (core design, data model, and tooling):

| Path | Title | Why relevant |
|------|-------|--------------|
| `current/20250101-01.md` | Combat System Refactor Plan | High-level plan and trade-offs. |
| `recent/20241215-01.md` | Save System Design Notes | Persistence model and edge cases. |
| `recent/20241120-01.md` | Level Data Format and Tools | Data format and editor tooling. |

**Other related sessions**:

| Path | Title | Why relevant |
|------|-------|--------------|
| `recent/20241010-01.md` | UI Layout Iteration | Major UI decisions. |
| `recent/20241001-01.md` | Enemy AI Behavior Ideas | Brainstorming and constraints. |

---

### Example: Application Project B

**Particularly relevant** (architecture, integrations, and deployment):

| Path | Title | Why relevant |
|------|-------|--------------|
| `current/20250105-01.md` | API Design and Data Contracts | External API surface and payloads. |
| `recent/20241218-01.md` | Authentication and Session Management | Auth flow and security considerations. |
| `recent/20241210-01.md` | Deployment Pipeline Setup | CI/CD and environment strategy. |

**Other related sessions**:

| Path | Title | Why relevant |
|------|-------|--------------|
| `recent/20241105-01.md` | Error Handling Strategy | Centralized error handling decisions. |
| `recent/20241101-01.md` | Logging and Observability Plan | Metrics, logs, and tracing. |

---

### Example: Databases / MCP

**Particularly relevant** (MCP servers, database ingest, query patterns):

| Path | Title | Why relevant |
|------|-------|--------------|
| `current/20250103-01.md` | SQLite MCP Server Configuration | Server config, env vars, and paths. |
| `recent/20241212-01.md` | Session Logs DB Ingest Design | How `session_logs.db` is populated. |
| `recent/20241201-01.md` | Knowledge Base Schema Review | Schema and indexing strategy. |

**Other related sessions**:

| Path | Title | Why relevant |
|------|-------|--------------|
| `recent/20241115-01.md` | FTS Search Tuning | FTS configuration and query examples. |
| `recent/20241102-01.md` | Database Maintenance Plan | Vacuum / backup / migration notes. |

---

### Example: Framework / Workspace

**Particularly relevant** (framework behavior, foundation, tools):

| Path | Title | Why relevant |
|------|-------|--------------|
| `current/20250102-01.md` | Foundation Configuration Review | Core agent behavior decisions. |
| `recent/20241220-01.md` | Ignore Files and Indexing Rules | `.gitignore`, `.cursorignore`, `.agentignore` rationale. |
| `recent/20241205-01.md` | Session Tools and Project Setup Enhancements | Changes to `session_tools.py` / `project_tools.py`. |

**Other related sessions**:

| Path | Title | Why relevant |
|------|-------|--------------|
| `recent/20241125-01.md` | Workspace Cleanup and Paths | Directory layout and symlinks. |
| `recent/20241110-01.md` | Release Planning and Versioning | Changelog and release notes planning. |

---

## Example: All Sessions by Location

In a real workspace, this section can be generated from `session_logs.db` or maintained manually. Below is a **minimal example** layout.

### current/

| File | Title |
|------|-------|
| `20250105-01.md` | API Design and Data Contracts |
| `20250103-01.md` | SQLite MCP Server Configuration |
| `20250102-01.md` | Foundation Configuration Review |
| `20250101-01.md` | Combat System Refactor Plan |

### recent/ (by date, newest first)

| File | Title |
|------|-------|
| `20241220-01.md` | Ignore Files and Indexing Rules |
| `20241218-01.md` | Authentication and Session Management |
| `20241215-01.md` | Save System Design Notes |
| `20241212-01.md` | Session Logs DB Ingest Design |
| `20241210-01.md` | Deployment Pipeline Setup |
| `20241201-01.md` | Knowledge Base Schema Review |
| `20241125-01.md` | Workspace Cleanup and Paths |
| `20241115-01.md` | FTS Search Tuning |
| `20241110-01.md` | Release Planning and Versioning |
| `20241105-01.md` | Error Handling Strategy |
| `20241101-01.md` | Logging and Observability Plan |

---

## Archived

Monthly zips in `archived/` (e.g. `archived/2024-12.zip`) contain copies of sessions from `current/` and `recent/` for that month. The ingest script reads these archives in place (no manual unzip required) so older sessions remain searchable in `session_logs.db`.

See [README.md](README.md) for session lifecycle, maintenance tools, and workspace-specific guidance.
