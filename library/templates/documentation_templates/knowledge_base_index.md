# {KNOWLEDGE_BASE_NAME} Knowledge Base Index

This directory contains a structured knowledge base extracted from {SOURCE_NAME}, organized for easy reference and agent-friendly querying.

**Source**: [{SOURCE_NAME}]({SOURCE_URL})

## 📊 Knowledge Base Statistics

- **Total Pages**: {TOTAL_PAGES}
- **Total Chunks**: {TOTAL_CHUNKS}
- **Total Size**: {TOTAL_SIZE}
- **Generated**: {GENERATED_DATE}

## 🗄️ Database Access (Primary Interface)

**For AI agents and programmatic access, use the SQLite database:**

- **`{DATABASE_NAME}`** - SQLite database with all knowledge (queryable)
- **`{DATABASE_NAME}.schema.sql`** - Database schema

**⚠️ Database Size**: {DATABASE_SIZE} - Too large for VS Code extensions.

**Recommended Method**: Use SQLite command-line tool (`sqlite3`) - handles databases of any size.

**Quick Start:**
```bash
sqlite3 -header -column {DATABASE_PATH} "SELECT title FROM pages LIMIT 10;"
```

See "Database Access" section below for full usage guide.

**Why use the database?**
- Fast, indexed queries
- Relationship traversal (find all mentions, dependencies)
- Complex joins across multiple topics
- Full-text search (if FTS5 available)
- Agent-friendly SQL interface
- **All data is available in the database - JSON files are optional**

> **Note**: The database contains all knowledge base content. JSON files are optional and only needed for specific use cases (see "JSON Access" section below).

## 📁 Knowledge Base Structure (Optional JSON Files)

### Overview

**`overview.json`** - Knowledge base metadata and structure
- Source information
- Statistics and summary
- File organization
- Chunking strategy

### Namespace Files

{NAMESPACE_DESCRIPTION}

{NAMESPACE_STATISTICS}

{NAMESPACE_FILE_LIST}

### Special Content Files

{SPECIAL_CONTENT_DESCRIPTION}

{SPECIAL_CONTENT_FILE_LIST}

## 🔍 Usage Guide

### For AI Agents

#### Database Access (Recommended)

**Primary Interface**: Use the SQLite database (`{DATABASE_NAME}`) for all queries.

**Database Size**: {DATABASE_SIZE} - Too large for most VS Code extensions.

**Recommended Method for Agents**: Use the **MCP SQLite Server** (preferred) or Python query tool (fallback)

### Option 1: MCP Server (Recommended - No File Creation)

The MCP server provides direct database access through Cursor's tool system, bypassing all terminal output issues.

**Setup:**
1. Install: `cd library/tools/mcp_sqlite_server && npm install`
2. Configure in Cursor: See `library/tools/mcp_sqlite_server/SETUP.md`
3. Restart Cursor

**Agent Usage:**
```
Use execute_query tool with:
- query: SELECT title FROM pages WHERE title LIKE '%{EXAMPLE_SEARCH}%' LIMIT 10
```

**Benefits:**
- ✅ No terminal output capture issues
- ✅ No file creation needed
- ✅ Direct tool integration
- ✅ Structured JSON responses
- ✅ Native Cursor tool system

### Option 2: SQLite Command-Line Tool (Fallback)

If MCP server isn't configured, use the SQLite command-line tool directly:

**How to Use Command-Line:**
```bash
# Open database interactively
sqlite3 {DATABASE_PATH}

# Or run a single query
sqlite3 {DATABASE_PATH} "SELECT title FROM pages LIMIT 10;"

# For better formatted output (column mode)
sqlite3 -header -column {DATABASE_PATH} "SELECT title FROM pages LIMIT 10;"
```

**Command-Line Options:**
- `-header` - Show column headers
- `-column` - Column-aligned output (readable)
- `-line` - One value per line (for wide tables)
- `-csv` - CSV format output
- `-json` - JSON format output (SQLite 3.38+)

**Installation (if needed):**
- **Windows**: Download from [sqlite.org](https://www.sqlite.org/download.html) or use `choco install sqlite` (Chocolatey)
- **Linux**: `sudo apt install sqlite3` (Debian/Ubuntu) or `sudo yum install sqlite` (RHEL/CentOS)
- **macOS**: Usually pre-installed, or `brew install sqlite`

**Why Command-Line?**
- **No size limits** - Handles databases of any size (SQLite supports up to 281 TB)
- **Reliable output** - Proper formatting options for readable results
- **No extensions needed** - Built into most systems or easily installed
- **Agent-friendly** - Direct terminal output that agents can read
- **Fast** - No GUI overhead, direct database access

**Why Database?**
- **Performance**: Indexed queries are orders of magnitude faster than parsing JSON
- **Relationships**: SQL joins enable relationship traversal (mentions, dependencies, cross-references)
- **Complex Queries**: Filter, aggregate, and combine data across namespaces
- **Full-Text Search**: FTS5 enables fast content searches (if available)
- **Agent-Friendly**: SQL is natural for AI agents to construct and understand

#### Agent Mode Usage Patterns

**Coder Mode** - Targeted Technical Queries:
- Find specific API details, function signatures, code examples
- Look up technical specifications (offsets, memory addresses, protocols)
- Get reverse engineering information (structs, algorithms, encryption)
- Fast lookups by title or technical term
- Single-page or targeted multi-page queries

**Researcher Mode** - Exploratory Comprehensive Queries:
- Find all mentions of a topic across the entire wiki
- Discover relationships between concepts
- Map dependencies and cross-references
- Get comprehensive coverage of a subject
- Explore historical context through revisions
- Find related pages through categories and templates

**Initializer Mode** - Project Setup & Foundation:
- Find setup guides, installation instructions, getting started pages
- Discover relevant tools, libraries, frameworks, utilities
- Understand development workflows, processes, best practices
- Find code examples or patterns for project structure
- Identify dependencies, prerequisites, requirements
- Map the ecosystem (related tools, concepts, workflows)

**Example Queries:**

```sql
-- Coder: Find specific technical page
SELECT * FROM pages WHERE title = '{EXAMPLE_TECHNICAL_PAGE}';

-- Coder: Find code examples or technical details
SELECT title, text FROM revisions 
WHERE text LIKE '%struct%' OR text LIKE '%offset%'
LIMIT 20;

-- Researcher: Find all pages related to a topic
SELECT DISTINCT p.title, p.namespace 
FROM pages p
JOIN revisions r ON p.id = r.page_id
WHERE r.text LIKE '%{EXAMPLE_TOPIC}%'
ORDER BY p.namespace, p.title;

-- Researcher: Explore relationships
SELECT p1.title AS source, p2.title AS target
FROM cross_references cr
JOIN pages p1 ON cr.source_page_id = p1.id
JOIN pages p2 ON cr.target_page_id = p2.id
WHERE p1.title LIKE '%{EXAMPLE_CONCEPT}%';

-- Initializer: Find setup/installation guides
SELECT p.title, r.text 
FROM pages p
JOIN revisions r ON p.id = r.page_id
WHERE (p.title LIKE '%Setup%' OR p.title LIKE '%Install%' 
       OR p.title LIKE '%Getting Started%' OR p.title LIKE '%Tutorial%')
AND p.namespace = 0
ORDER BY p.title;

-- Initializer: Find tools and utilities
SELECT DISTINCT p.title
FROM pages p
JOIN revisions r ON p.id = r.page_id
WHERE (r.text LIKE '%tool%' OR r.text LIKE '%utility%' 
       OR r.text LIKE '%library%' OR r.text LIKE '%framework%')
AND p.namespace = 0
LIMIT 50;
```

#### JSON Access (Optional - Only if JSON files are present)

> **Note**: JSON files are **optional**. The database contains all the same data. Only use JSON files if they are present in this directory and you have a specific need for them.

Use JSON files when:
- Human inspection or manual editing needed
- Version control of knowledge base structure
- Loading specific chunks without database overhead
- Working with the raw structured data format

**JSON Structure** (if files are present):
- Load `overview.json` for metadata and structure
- Load namespace chunk files for specific content
- Use special content files for redirects, stubs, etc.

### For Humans

**Recommended**: Use the database for all queries (see "Database Access" section above).

If JSON files are present:
- Browse namespace files for organized content
- Check special content files for redirects and stubs
- Review overview.json for statistics and structure

## 📚 File Reference

### Required Files

- **`{DATABASE_NAME}`** - SQLite database (required for database access)
- **`{DATABASE_NAME}.schema.sql`** - Database schema (optional, for reference)

### Optional JSON Files

> **Note**: These files are optional. All data is available in the database. JSON files are only needed for specific use cases.

If JSON files are present in this directory:

**Core Files**:
- **`overview.json`** - Metadata, statistics, and file structure
- **`cross_references.json`** - Cross-references between chunks (if available)

**Namespace Files**:
Files are named: `namespace_{number}_{chunk_id}.json`

Example: `namespace_0_main.json` contains main namespace pages in the main chunk.

**Special Content Files**:
- **`redirects_{chunk_id}.json`** - Redirect pages
- **`stubs_{chunk_id}.json`** - Stub pages
- **`disambiguation_{chunk_id}.json`** - Disambiguation pages (if available)

## 🔗 Cross-References

Cross-references between pages are maintained in:
- **Database `cross_references` table** (primary source, always available)
- `cross_references.json` - Chunk-to-chunk references (optional, only if JSON files are present)

## 📝 Notes

- Knowledge base generated from {SOURCE_TYPE}
- Content organized by namespace with size-based chunking
- Special content (redirects, stubs) extracted to separate files
- All metadata and cross-references preserved
