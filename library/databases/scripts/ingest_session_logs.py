#!/usr/bin/env python3
"""
Ingest session logs (current/, recent/, and archived/*.zip) into session_logs.db for queryable recall.

Enables agents to search past sessions via MCP (Trill-like memory): full-text over
title, description, and section content (Summary, Key Decisions, Next Work Items, etc.).
Reads archives in place (no unzipping required).

Usage:
    python library/databases/scripts/ingest_session_logs.py [--db-path PATH] [--sessions-root PATH] [--no-archives] [--current-only] [--dry-run]
    Run from workspace root. Default db-path: library/databases/db/session_logs.db
    Default sessions-root: library/sessions/
    --current-only: only ingest library/sessions/current/ (skip recent and archives).
"""

import re
import zipfile
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime, timezone


def get_workspace_root() -> Path:
    """Workspace root: 4 parents from script (library/databases/scripts/)."""
    return Path(__file__).resolve().parent.parent.parent.parent


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (fields dict, body after second ---)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    yaml_block = match.group(1)
    body = match.group(2)
    fields = {}
    for line in yaml_block.splitlines():
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip('"').strip("'")
            fields[key] = val
    return fields, body


def parse_sections(body: str) -> list[tuple[str, str]]:
    """Split body into (section_name, content) by ## headers. First block before ## is skipped or treated as intro."""
    sections = []
    # Normalize and split by ## 
    parts = re.split(r"\n##\s+", body, maxsplit=0)
    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
        if "\n" in part:
            first_line, rest = part.split("\n", 1)
            section_name = first_line.strip()
            content = rest.strip()
        else:
            section_name = part.strip()
            content = ""
        # Skip the H1 line if it's the first block (e.g. "# Session 20260219-01: Title")
        if i == 0 and section_name.startswith("# "):
            continue
        if section_name:
            sections.append((section_name, content))
    return sections


def collect_session_files(sessions_root: Path, current_only: bool = False) -> list[tuple[Path, str]]:
    """Return [(path, location)] for current and recent, excluding README.md."""
    out = []
    locations = ("current",) if current_only else ("current", "recent")
    for location in locations:
        dir_path = sessions_root / location
        if not dir_path.is_dir():
            continue
        for path in sorted(dir_path.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            out.append((path, location))
    return out


def collect_archived_sessions(sessions_root: Path) -> list[tuple[Path, str]]:
    """Return [(zip_path, entry_name)] for each .md inside each .zip in sessions/archived/."""
    out = []
    archived_dir = sessions_root / "archived"
    if not archived_dir.is_dir():
        return out
    for zip_path in sorted(archived_dir.glob("*.zip")):
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                for name in zf.namelist():
                    if name.endswith(".md") and not name.lower().endswith("readme.md"):
                        out.append((zip_path, name))
        except zipfile.BadZipFile:
            continue
    return out


def ingest_content(
    conn: sqlite3.Connection,
    session_id: str,
    file_path: str,
    location: str,
    raw: str,
) -> None:
    """Parse raw markdown and upsert into sessions, session_sections, session_fts."""
    fields, body = parse_frontmatter(raw)
    sections = parse_sections(body)

    title = fields.get("title", "")
    description = fields.get("description", "")
    created_utc = fields.get("created", "")
    last_updated_utc = fields.get("last_updated", "")
    status = fields.get("status", "")
    ingested_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    cur = conn.cursor()
    cur.execute(
        """INSERT OR REPLACE INTO sessions
           (session_id, file_path, location, title, description, created_utc, last_updated_utc, status, ingested_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (session_id, file_path, location, title, description, created_utc, last_updated_utc, status, ingested_at),
    )
    cur.execute("DELETE FROM session_sections WHERE session_id = ?", (session_id,))
    # Normal FTS5 tables support DELETE like any other table (contentless tables need the special 'delete' INSERT)
    cur.execute("DELETE FROM session_fts WHERE session_id = ?", (session_id,))

    for order, (section_name, content) in enumerate(sections):
        cur.execute(
            "INSERT INTO session_sections (session_id, section_name, content, sort_order) VALUES (?, ?, ?, ?)",
            (session_id, section_name, content, order),
        )
        cur.execute(
            """INSERT INTO session_fts (session_id, title, description, section_name, content)
               VALUES (?, ?, ?, ?, ?)""",
            (session_id, title or "", description or "", section_name, content),
        )
    conn.commit()


def ingest_file(conn: sqlite3.Connection, path: Path, location: str) -> None:
    """Read session file from disk and ingest."""
    session_id = path.stem
    raw = path.read_text(encoding="utf-8", errors="replace")
    file_path = str(path.relative_to(path.parent.parent))
    ingest_content(conn, session_id, file_path, location, raw)


def main() -> int:
    root = get_workspace_root()
    default_db = root / "library" / "databases" / "db" / "session_logs.db"
    default_sessions = root / "library" / "sessions"

    ap = argparse.ArgumentParser(description="Ingest session logs into session_logs.db for queryable recall.")
    ap.add_argument("--db-path", type=Path, default=default_db, help="Output SQLite DB path")
    ap.add_argument("--sessions-root", type=Path, default=default_sessions, help="library/sessions/ directory (current + recent + archived)")
    ap.add_argument("--no-archives", action="store_true", help="Skip reading archived/*.zip")
    ap.add_argument("--current-only", action="store_true", help="Only ingest sessions/current/ (skip recent and archives)")
    ap.add_argument("--dry-run", action="store_true", help="List files that would be ingested without writing session_logs.db")
    args = ap.parse_args()

    if args.dry_run:
        count = 0
        if not args.no_archives and not args.current_only:
            for zip_path, entry_name in collect_archived_sessions(args.sessions_root):
                file_path = f"archived/{zip_path.name}/{entry_name}"
                print(f"Would ingest: {file_path}")
                count += 1
        for path, location in collect_session_files(args.sessions_root, current_only=args.current_only):
            print(f"Would ingest: {path.relative_to(args.sessions_root)}")
            count += 1
        print(f"Dry run complete. Would ingest {count} session(s) into {args.db_path}")
        return 0

    args.db_path.parent.mkdir(parents=True, exist_ok=True)
    databases_dir = Path(__file__).resolve().parent.parent
    schema_path = databases_dir / "schemas" / "session_logs.sql"
    if not schema_path.exists():
        raise SystemExit(f"Schema not found: {schema_path}")
    schema_sql = schema_path.read_text(encoding="utf-8")

    conn = sqlite3.connect(str(args.db_path))
    conn.executescript(schema_sql)
    conn.commit()

    # Ingest order: archived first, then current, then recent. Later rows replace same session_id so current/recent win.
    if not args.no_archives and not args.current_only:
        for zip_path, entry_name in collect_archived_sessions(args.sessions_root):
            try:
                with zipfile.ZipFile(zip_path, "r") as zf:
                    raw = zf.read(entry_name).decode("utf-8", errors="replace")
                session_id = Path(entry_name).stem
                file_path = f"archived/{zip_path.name}/{entry_name}"
                ingest_content(conn, session_id, file_path, "archived", raw)
                print(f"Ingested: {file_path}")
            except Exception as e:
                print(f"Skip {zip_path.name}/{entry_name}: {e}")

    for path, location in collect_session_files(args.sessions_root, current_only=args.current_only):
        try:
            ingest_file(conn, path, location)
            print(f"Ingested: {path.relative_to(args.sessions_root)}")
        except Exception as e:
            print(f"Skip {path.name}: {e}")
    conn.close()

    print(f"Done. Session log DB: {args.db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
