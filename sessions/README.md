# Sessions - Session Management and Logging

The `sessions/` directory manages development session logs that track work progress, decisions, and context across multiple agent sessions.

## Directory Structure

```
sessions/
├── current/      # Active sessions (last 7 days)
├── recent/       # Sessions 7+ days old
└── archived/     # Monthly zip archives (YYYY-MM.zip)
```

## Session Lifecycle

1. **Active** → Sessions start in `current/` with "Active" status
2. **Handoff** → Marked as "Handoff" when ready for next agent
3. **Completed** → Final status when work is finished
4. **Archived** → Moved to `recent/` after 7 days
5. **Compressed** → Added to monthly archives in `archived/`
6. **Cleaned** → Very old sessions removed after 90 days

## Session File Format

### Naming Convention
- **Format**: `YYYYMMDD-NN.md` (e.g., `20251026-01.md`)
- **Continuations**: `YYYYMMDD-NN_pt2.md`, `YYYYMMDD-NN_pt3.md`, etc.
- **Unique identifiers**: Date + sequential number per day

### Structure
Sessions follow the template defined in `library/session_template.md`:
- **YAML frontmatter**: Metadata (title, author, status, timestamps)
- **Template sections**: Summary, decisions, accomplishments, etc.
- **Metadata rules**:
  - `created`: Never modify after initial creation
  - `last_updated`: Update only when adding sections, completing work, adding files
  - `status`: Active → Handoff → Completed

## Session Management

### Tools
Use `tools/session_tools.py` for session management:
- Create new sessions
- Continue existing sessions
- Prune old sessions
- Create monthly archives
- Full maintenance workflow

### Maintenance
Sessions are automatically maintained:
- **7+ days**: Moved from `current/` to `recent/`
- **Monthly**: Archived into `archived/YYYY-MM.zip`
- **90+ days**: Old sessions can be cleaned up

## Integration

Sessions are:
- **Shared across projects**: Available via symlink in all projects
- **Referenced by agents**: Provide context for ongoing work
- **Template-based**: Follow consistent structure from `library/session_template.md`
- **Managed by tools**: `session_tools.py` handles creation and maintenance

## Purpose

Session logs serve as:
- **Knowledge persistence**: Track decisions and rationale across sessions
- **Context continuity**: Enable agents to understand previous work
- **Project history**: Maintain a record of development progress
- **Handoff documentation**: Smooth transitions between agents

## Best Practices

- Keep session logs focused and well-structured
- Update `last_updated` only when adding substantive content
- Use continuations (`_pt2`, `_pt3`) for long-running sessions
- Run maintenance tools periodically to keep directories organized
- Archive completed sessions to maintain a clean workspace

