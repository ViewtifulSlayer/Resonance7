---
name: database-specialist
description: Guides agents on designing and refining workspace databases and archival datasets. Covers schema design best practices, distinguishing important data from filler, archival/data-quality considerations, and workflows for source-ingest pipelines (populate, compile, cross-references, verification). Use when the user wants to add or refine database contents, design or change schemas, run ingest/compile/verify scripts, or decide what data to keep vs omit.
---

# Database Specialist

Use this skill when a task involves **adding or refining** database contents—schema design, populating tables, cross-references, verification, and archival/data-quality decisions—not just querying via MCP. For configuring or querying SQLite via MCP, use the **mcp-sqlite** skill.

## Core Principles

**Schema first**: Design or review schema (tables, constraints, indexes) before bulk data. Normalize to reduce redundancy; use constraints and foreign keys for integrity. In SQLite, enable `PRAGMA foreign_keys = ON` per connection if referential integrity is required. See [reference.md](reference.md) for schema best practices, data dictionary for archival, and authoritative references (SQLite, PREMIS, ISO 8000).

**Important vs filler**: Prioritize data that is source-of-truth, cross-referenced, or explicitly marked reliable. Treat as filler or secondary: duplicated content, unverified external reference data, and metadata that can be recomputed. Use reliability/importance fields (e.g. `reliability`, `source`) so consumers can filter.

**Workflow over ad-hoc writes**: Prefer the workspace scripts (populate, compile, standardize, verify) over one-off INSERTs. They enforce structure and consistency.

## Workspace Databases and Workflows

### Example A: Web Sources (Ingest + Cross-References)

- **Purpose**: Web-extracted content and cross-references to authoritative docs (e.g. "Section X.Y").
- **Location (example)**: `<workspace_root>/resources/databases/web_sources.db`
- **Tables** (conceptually): `web_sources`, `web_topics`, `web_pages`, `web_content_chunks`, `extraction_metadata`, `web_content_fts`; cross-reference tables link sources to doc sections.
- **Add/refine content**:
  1. **Populate from extracted content**: `python <workspace_root>/tools/db_ingest/populate_web_sources.py --db-path PATH --sources-dir PATH`. Reads per-source extracted markdown + metadata; inserts pages and chunks. Ensure DB schema exists (tables above) before running.
  2. **Create cross-references**: `python <workspace_root>/tools/db_ingest/create_cross_references.py --db-path PATH`. Links sources to authoritative sections (e.g. "Section 1.4").
  3. **Standardize references**: `python <workspace_root>/tools/db_ingest/standardize_references.py --db-path PATH [--verify-only]`. Normalizes section refs to a consistent format and verifies subsection refs.
  4. **Verify**: `python <workspace_root>/tools/db_ingest/verify_references.py --db-path PATH`. Sanity-checks cross-reference targets against the authoritative docs index.
- **Important vs filler**: Source titles, URLs, extraction dates, and cross-reference mappings are important. Topic tags and word counts are derived; keep if useful for search/analytics, else omit or recompute.

### Example B: Knowledge Base from Source Data (Compile + Verify)

- **Purpose**: Cross-reference DB for structured entities (blocks, parts, patches, labels, commands, transforms) plus optional external reference data.
- **Location (example)**: `<workspace_root>/resources/databases/knowledge_base.db`; schema in `<workspace_root>/tools/db_compile/schema.sql`.
- **Add/refine content**:
  1. **Compile database**: `python <workspace_root>/tools/db_compile/compile_database.py --input PATH --output DB_PATH [--profile PROFILE] [--reference-data PATH]`. Builds DB from structured source exports and patches/transforms. Run from repo root or set paths.
  2. **Update reference dataset (optional)**: `python <workspace_root>/tools/db_compile/update_reference_data.py --input PATH --reference-data PATH`, then re-run compile with `--reference-data` to load into DB.
  3. **Verify**: `python <workspace_root>/tools/db_compile/verify_db.py --db-path DB_PATH`. Prints table counts and sanity checks.
- **Important vs filler**: Blocks, parts, patches, labels, patch_addresses, patch_labels, cop_definitions are core. DataCrystal tables are **reference** data: mark with `reliability` (e.g. `original_reference`, `verified`, `uncertain`) and document that addresses may not match expanded baserom. Notes and long text can be summarized or linked instead of inlining.

## Deciding What Data Is Important vs Filler

- **Keep (important)**: Primary keys, foreign keys, canonical names, source URLs, extraction/compile timestamps, cross-reference mappings, reliability/source fields. Data that answers "where did this come from?" and "can I trust it?"
- **Optional or derived**: Word counts, auto-generated topic tags, duplicate text that exists elsewhere. Include only if needed for search, analytics, or UX; otherwise omit or recompute on demand.
- **Reference vs source-of-truth**: External reference data (e.g. DataCrystal) should have a reliability/source column and clear docs that it may be outdated or address-shifted. Prefer linking to external docs over copying large blobs.

## Workflow Checklist

1. **Schema**: Ensure tables, indexes, and constraints exist (schema.sql/migrations may be required before ingest/compile runs).
2. **Source data**: Prepare inputs (extracted content + metadata for web sources; structured exports + patches/transforms for compiled KB; optional external reference dataset if applicable).
3. **Run populate/compile**: Use the scripts above; fix paths and options as needed.
4. **Cross-references / standardization**: For web sources, run cross-reference creation then standardization.
5. **Verify**: Run your verification step(s) (e.g. reference verification for web sources; `verify_db` for the compiled KB); fix any reported issues.
6. **Document**: Note reliability/source for reference data; update README or docs if schema or workflow changes.

## Anti-Patterns

- **Ad-hoc INSERTs** without going through populate/compile: bypasses validation and can corrupt refs.
- **Storing large duplicate text** in multiple tables: normalize or store once and reference by ID.
- **Omitting reliability/source** for external reference data: consumers cannot weight or filter.
- **Skipping verification** after bulk updates: subsection refs and counts can drift.

## Additional Resources

- Schema and data-quality details: [reference.md](reference.md)
- MCP querying (read-only): use the **mcp-sqlite** skill
