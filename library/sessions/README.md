# Sessions - Session Management and Logging

Session logs live under **`library/sessions/`** in the Resonance7 foundation repo.

## Directory Structure

```
library/sessions/
├── current/      # Active sessions (last 7 days)
├── recent/       # Sessions 7+ days old
└── archived/     # Monthly zip archives (YYYY-MM.zip)
```

Created by `python library/tools/scripts/setup_workspace.py` on first run.

## Session Lifecycle

1. **Active** - Sessions start in `current/` with "Active" status
2. **Handoff** - Marked as "Handoff" when ready for next agent
3. **Completed** - Final status when work is finished
4. **Archived** - Moved to `recent/` after 7 days
5. **Compressed** - Added to monthly archives in `archived/`
6. **Cleaned** - Very old sessions removed after 90 days

## Session File Format

### Naming Convention
- **Format**: `YYYYMMDD-NN.md` (e.g., `20251026-01.md`)
- **Continuations**: `YYYYMMDD-NN_pt2.md`, `YYYYMMDD-NN_pt3.md`, etc.
- **Unique identifiers**: Date + sequential number per day

### Structure
Sessions follow the template in `library/templates/session_template.md`:
- **YAML frontmatter**: Metadata (title, author, status, timestamps)
- **Template sections**: Summary, decisions, accomplishments, etc.
- **Metadata rules**:
  - `created`: Never modify after initial creation
  - `last_updated`: Update only when adding sections, completing work, adding files
  - `status`: Active -> Handoff -> Completed

## Session Management

### Tools

```bash
python library/tools/scripts/session_tools.py           # interactive
python library/tools/scripts/session_tools.py --prune   # maintenance
```

### Maintenance
- **7+ days**: Moved from `current/` to `recent/`
- **Monthly**: Archived into `archived/YYYY-MM.zip`
- **90+ days**: Old sessions can be cleaned up

## Integration

- **Foundation repo**: Open the Resonance7 root (or a multi-root `.code-workspace` pairing) for shared sessions
- **MCP recall**: Ingested logs in `library/databases/db/session_logs.db` via `library/databases/scripts/ingest_session_logs.py` (or `session_tools.py --ingest`)
- **Template**: `library/templates/session_template.md`

## Purpose

Session logs support knowledge persistence, context continuity across agents, project history, and handoff documentation.

## Best Practices

- Keep session logs focused and well-structured
- Update `last_updated` only when adding substantive content
- Use continuations (`_pt2`, `_pt3`) for long-running sessions
- Run maintenance tools periodically
- Run ingest only when the user explicitly requests it
