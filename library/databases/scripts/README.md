# Database scripts

## Session log ingest

Ingests `library/sessions/current/`, `library/sessions/recent/`, and `library/sessions/archived/*.zip` into `session_logs.db` for MCP queryable recall. Archives are read in place (no unzipping).

**Layout under `library/databases/`**

```
library/databases/
  schemas/session_logs.sql
  scripts/ingest_session_logs.py
  db/session_logs.db
```

### Run

From the workspace root (preferred):

```bash
python library/tools/scripts/session_tools.py --ingest
```

Or directly:

```bash
python library/databases/scripts/ingest_session_logs.py
```

Options: `--db-path`, `--sessions-root`, `--no-archives`, `--current-only`. See script docstring and `library/databases/README.md`.

Re-run ingest only when you explicitly want the DB refreshed.
