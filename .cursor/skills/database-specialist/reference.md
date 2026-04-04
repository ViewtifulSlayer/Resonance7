# Schema and Data Quality (Reference)

Use this when designing or refining schemas and deciding what data to keep vs omit. For workflows and tool usage, see [SKILL.md](SKILL.md).

## Schema Design Best Practices

- **Normalize to reduce redundancy**: Store each fact once; use foreign keys to relate tables. Avoid duplicating large text or blobs across tables—store once and reference by ID.
- **Constraints**: Use NOT NULL, UNIQUE, CHECK, and FOREIGN KEY so invalid data is rejected at write time. Document any deferred or relaxed constraints.
- **Foreign keys in SQLite**: Foreign key constraints are **not enforced by default**. In compile/populate scripts, enable per connection with `PRAGMA foreign_keys = ON` if you want referential integrity. Create an index on child key columns for efficient FK checks. See [sqlite.org/foreignkeys.html](https://sqlite.org/foreignkeys.html).
- **Indexes**: Create indexes on columns used in WHERE, JOIN, and ORDER BY. Composite indexes: column order should match query patterns (equality before range). For query-planner details and EXPLAIN QUERY PLAN examples, see the `mcp-sqlite` reference.
- **Naming**: Use consistent names (e.g. `section_id` not `sectionId` in SQLite). Table names plural or singular consistently; column names clear and short.
- **Documentation**: Keep schema.sql (or equivalent) under version control. Document reliability/source columns and any external reference caveats. For archival preservation, a **data dictionary** (fields, types, relationships, locations) is essential for transfer and long-term use—see preservation guidelines (e.g. [Utah State Archives Database Preservation](https://archives.utah.gov/), [PREMIS](https://www.loc.gov/standards/premis/)).

## Important vs Filler: Practical Rules

**Important (keep)**:
- Identifiers: primary keys, foreign keys, canonical names (e.g. block name, patch name).
- Provenance: source URL, extraction date, compile timestamp, source file path.
- Cross-reference mappings: which doc section or patch a row relates to.
- Reliability/source: `reliability` (e.g. original_reference, verified, uncertain), `source`, `notes` so consumers can filter or warn.

**Filler or derived (omit or optional)**:
- Duplicate content: same text stored in multiple tables—store once, reference by ID.
- Auto-generated tags/categories: include only if used for search or reporting; otherwise recompute.
- Word counts, checksums: useful for analytics but not canonical; can be recomputed.
- Long notes or blobs: prefer short summary + link to external doc; avoid inlining huge text unless required for search.

**Reference data (mark clearly)**:
- External reference (e.g. DataCrystal): add `reliability` and `source_url`; document that addresses/values may not match current baserom or codebase.
- Archival vs active: if you separate archive tables, use consistent naming and document retention/expiry policy.

**Data quality (fitness for use)**: Standards such as ISO 8000 define data quality as fitness for purpose—prioritize data that is fit for the intended use (queries, cross-reference, preservation) and treat optional or redundant data accordingly. See [ISO 8000-61](https://www.iso.org/standard/63086.html) (process reference model for data quality management).

## Archival and Versioning

- **Archive pattern**: For historical data, consider separate archive tables or partitions so active queries stay fast. Match structure (columns, indexes) for consistency.
- **Data dictionary / schema documentation**: Preservation guidelines (e.g. Utah State Archives, PREMIS) require a data dictionary or schema describing fields, types, relationships, and locations for database preservation and transfer. Keep schema.sql and any field-level docs under version control.
- **Fixity / checksums**: For long-term archival integrity, use checksums (e.g. SHA-256) to verify file or content integrity and support chain of custody; recompute and compare after migrations or bulk updates. See [DPC Fixity and Checksums](https://dpconline.org/handbook/technical-solutions-and-tools/fixity-and-checksums).
- **Versioning**: If schema or source format changes, document in README or CHANGELOG; consider a schema_version table or migration scripts.
- **Intentional redundancy**: Duplicate only when needed for resilience or performance (e.g. denormalized summary table); document why.

## Workspace-Specific Notes

- **Web sources ingest**: Schema may be created by an init script or inside your ingest tool; if not in repo, document table definitions. Cross-references tie extracted content to authoritative doc sections - keep mappings accurate via cross-reference creation + standardization steps.
- **Compiled knowledge base**: `schema.sql` should be the source of truth. Any external reference tables should use `reliability`/`source` fields; if addresses/IDs can drift over time, document that clearly. Recompile after source exports or patch changes; run a `verify_db` step after compile.

When this workspace contains `library/resources/databases/`, see `library/resources/databases/README.md` and `library/resources/databases/scripts/README.md` for database list, workflows, and important-vs-filler notes.

## Authoritative References

- [SQLite Foreign Key Support](https://sqlite.org/foreignkeys.html) — enabling FK, child key indexes.
- [Utah State Archives — Database Preservation Guideline](https://archives.utah.gov/) — data dictionary, schema documentation for preservation.
- [PREMIS (Library of Congress)](https://www.loc.gov/standards/premis/) — preservation metadata and data dictionary for digital preservation.
- [DPC — Fixity and Checksums](https://dpconline.org/handbook/technical-solutions-and-tools/fixity-and-checksums) — integrity verification for archives.
- [ISO 8000-61:2016](https://www.iso.org/standard/63086.html) — data quality management, process reference model (fitness for use).
- [MCP Best Practices](https://mcp-best-practice.github.io/mcp-best-practice/best-practice/) — bounded tools, contracts, security; [MCP Tools (modelcontextprotocol.io)](https://modelcontextprotocol.io/docs/concepts/tools) — tool contracts and discovery (see also the `mcp-sqlite` reference for workspace-specific MCP usage).
