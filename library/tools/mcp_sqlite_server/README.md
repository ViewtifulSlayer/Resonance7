# Resonance7 SQLite MCP Server

MCP (Model Context Protocol) server that provides direct database access to SQLite knowledge base databases over MCP. This bypasses terminal output capture issues by exposing database tools directly to the agent.

## Features

- 🔍 **Query Execution**: Execute SQL queries and get results directly via MCP tools
- 📋 **Schema Exploration**: List tables and view table schemas
- 🗄️ **Database Info**: Get database statistics and metadata
- 🛡️ **Read-Only Mode**: Database opened in read-only mode for safety
- ⚡ **No Terminal Output Needed**: Results returned directly through MCP tools

## Prerequisites

- Node.js (version 18 or higher)
- An MCP-capable editor (Freebuff in VS Code)
- SQLite knowledge base database

## Installation

1. **Install dependencies:**
   ```bash
   cd library/tools/mcp_sqlite_server
   npm install
   ```

2. **Configure MCP:** run `python library/tools/scripts/setup_database.py` from the workspace root (writes `.agents/mcp.json`). Manual configuration is covered in Setup below.

## Setup

### Option 1: Run the setup script (recommended)

From the workspace root:

```bash
python library/tools/scripts/setup_database.py
```

This writes `.agents/mcp.json` with absolute paths and runs `npm install` in this folder.

### Option 2: Manual configuration

Add to `.agents/mcp.json`:

```json
{
  "mcpServers": {
    "resonance7-sqlite": {
      "command": "node",
      "args": [
        "${workspaceFolder}/library/tools/mcp_sqlite_server/src/server.js"
      ],
      "env": {
        "DEFAULT_DB_PATH": "${workspaceFolder}/library/databases/db/session_logs.db"
      }
    }
  }
}
```

**Important**: See `SETUP.md` for Windows `node` path, `${workspaceFolder}` fallbacks, and optional `DEFAULT_DB_PATH` / `SESSION_LOGS_DB_PATH` / `KNOWLEDGE_BASE_DB_PATH` overrides.

## Available Tools

Once configured, agents can use these tools directly via MCP:

### 0. `list_databases`

List workspace databases under `library/databases/db/` (alias = filename stem, absolute path).

**Parameters:** none

**Example:**
```
Use list_databases tool (no parameters)
```

### 1. `execute_query`

Execute a SQL query against the knowledge base database.

**Parameters:**
- `query` (required): SQL query string
- `database_path` (optional): Alias (filename stem under `library/databases/db/`), `session_logs`, or absolute `.db` path (default: `session_logs`)

**Example:**
```
Use execute_query tool with:
- database_path: session_logs
- query: SELECT session_id, title FROM sessions ORDER BY ingested_at DESC LIMIT 10
```

### 2. `get_tables`

List all tables in the database.

**Parameters:**
- `database_path` (optional): Path to database file

### 3. `get_table_schema`

Get schema information for a specific table.

**Parameters:**
- `table_name` (required): Name of the table
- `database_path` (optional): Path to database file

### 4. `get_database_info`

Get database statistics (size, table count, etc.).

**Parameters:**
- `database_path` (optional): Path to database file

## Usage Examples

### Query session metadata:
```
Use execute_query tool with:
- database_path: session_logs
- query: SELECT session_id, title, status FROM sessions LIMIT 10
```

### Get all tables:
```
Use get_tables tool
```

### Get schema for pages table:
```
Use get_table_schema tool with:
- table_name: pages
```

## Development

### Running the Server

```bash
# Production mode
npm start

# Development mode with auto-restart
npm run dev
```

### Testing

You can test the server independently:

```bash
node src/server.js
```

## Configuration

Default database resolution (first match wins):

1. `SESSION_LOGS_DB_PATH` env var (explicit session log DB)
2. `DEFAULT_DB_PATH` env var (written by `library/tools/scripts/setup_database.py`)
3. `KNOWLEDGE_BASE_DB_PATH` env var (legacy name)
4. Built-in fallback: `library/databases/db/session_logs.db` relative to the workspace

You can override per-query using the `database_path` parameter:

- `session_logs` - default session log DB (env override aware)
- `<stem>` - any `library/databases/db/<stem>.db` that exists (e.g. `iog_disassembly`)
- absolute path - full path to a `.db` file

Use `list_databases` to discover aliases after adding files to `db/`. Reload your editor after `server.js` changes.

## Security Considerations

- Database is opened in **read-only mode** - only SELECT queries are supported
- No write operations (INSERT, UPDATE, DELETE) are allowed
- Database path is configurable but defaults to the knowledge base location

## Troubleshooting

### MCP Server Not Appearing

1. Check that Node.js is in your PATH
2. Verify the path in `args` is correct and absolute
3. Reload your editor after adding MCP configuration
4. Check your editor's developer console or MCP output for errors

### Database Not Found

1. Verify the database path in the `env` section of `mcp-config.json`
2. Use absolute paths (not relative)
3. Check file permissions

### Tools Not Working

1. Check your editor's MCP server status (should show as "connected")
2. Verify Node.js version (18+ required)
3. Check that `better-sqlite3` installed correctly (may need to rebuild native modules)

### Database Files Not Visible to Agents

Database files (`.db`, `.sqlite`, `.sqlite3`) under `library/databases/db/` are gitignored by the `library/databases/**` policy, so they never appear in Git. Freebuff/Codebuff file discovery follows `.gitignore`, which is expected: agents reach the databases through the MCP tools (`list_databases`, `execute_query`) rather than by reading the files directly.

You do not need to expose the `.db` files to file discovery. Adding a `.db` under `db/` makes it reachable as an alias at the next server start.

### Terminal Output Not Captured (Alternative Methods)

If you're using terminal-based queries instead of MCP and experiencing output capture issues:

1. **Use MCP Server** (recommended) - This bypasses all terminal output issues
2. **Use file-based output** - Write results to a file, then read the file

For detailed troubleshooting, see the alternative methods section below.

## Alternative: SQLite Command-Line Tool

If MCP server isn't configured, you can use the SQLite command-line tool directly:

```bash
# Run a query
sqlite3 -header -column library/databases/db/session_logs.db "SELECT session_id, title FROM sessions LIMIT 10;"
```

**Note**: Terminal output capture can be unreliable in some editors. The MCP server is recommended to avoid these issues.

## Benefits Over Terminal-Based Queries

- ✅ **No terminal output capture issues** - Results returned directly through MCP
- ✅ **Structured JSON responses** - Easy for agents to parse
- ✅ **Native tool integration** - Works seamlessly with your editor's tool system
- ✅ **No file creation needed** - Results returned in tool response
- ✅ **Type-safe** - Proper error handling and validation

## License

MIT License
