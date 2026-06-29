-- Session logs database: ingest of library/sessions/current and library/sessions/recent for queryable recall
-- Enables agents to search and retrieve past session content (Trill-like memory)
-- Source: library/databases/scripts/ingest_session_logs.py

PRAGMA foreign_keys = ON;

-- One row per session file (session_id = filename stem, e.g. 20260219-01 or 20251101-01_pt1)
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE,
    file_path TEXT NOT NULL,
    location TEXT NOT NULL CHECK (location IN ('current', 'recent', 'archived')),
    title TEXT,
    description TEXT,
    created_utc TEXT,
    last_updated_utc TEXT,
    status TEXT,
    ingested_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_sessions_location ON sessions(location);
CREATE INDEX IF NOT EXISTS idx_sessions_created ON sessions(created_utc);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);

-- One row per H2 section (Summary, Key Decisions, Next Work Items, etc.)
CREATE TABLE IF NOT EXISTS session_sections (
    id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
    section_name TEXT NOT NULL,
    content TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_sections_session ON session_sections(session_id);
CREATE INDEX IF NOT EXISTS idx_sections_name ON session_sections(section_name);

-- Full-text search: one row per section, with session title/description for context
-- Agents can run: SELECT * FROM session_fts WHERE session_fts MATCH 'MCP database'
CREATE VIRTUAL TABLE IF NOT EXISTS session_fts USING fts5(
    session_id,
    title,
    description,
    section_name,
    content,
    tokenize='porter unicode61'
);

-- View: sessions with first line of Summary for quick scan
CREATE VIEW IF NOT EXISTS session_summaries AS
SELECT
    s.session_id,
    s.file_path,
    s.location,
    s.title,
    s.created_utc,
    s.status,
    (SELECT content FROM session_sections ss WHERE ss.session_id = s.session_id AND ss.section_name = 'Summary' LIMIT 1) AS summary_preview
FROM sessions s
ORDER BY s.created_utc DESC;
