# Resonance7 SQLite MCP Server

MCP (Model Context Protocol) server that provides direct database access to SQLite knowledge base databases in Cursor IDE. This bypasses terminal output capture issues by exposing database tools directly through Cursor's MCP system.

## Features

- 🔍 **Query Execution**: Execute SQL queries and get results directly in Cursor
- 📋 **Schema Exploration**: List tables and view table schemas
- 🗄️ **Database Info**: Get database statistics and metadata
- 🛡️ **Read-Only Mode**: Database opened in read-only mode for safety
- ⚡ **No Terminal Output Needed**: Results returned directly through MCP tools

## Prerequisites

- Node.js (version 18 or higher)
- Cursor IDE
- SQLite knowledge base database

## Installation

1. **Install dependencies:**
   ```bash
   cd library/tools/mcp_sqlite_server
   npm install
   ```

2. **Configure MCP in Cursor:**
   - Open Cursor Settings (`Ctrl+Shift+J` or `Cmd+,`)
   - Search for "MCP" or "Model Context Protocol"
   - Add the MCP server configuration (see Setup below)

## Setup with Cursor IDE

### Option 1: Use the provided config file

1. Open Cursor Settings
2. Navigate to **Features > MCP**
3. Click **"Add New MCP Server"**
4. Copy the contents of `mcp-config.json` into the MCP settings
5. Adjust the path in `args` if your workspace is in a different location

### Option 2: Manual configuration

In Cursor's MCP settings, add:

```json
{
  "mcpServers": {
    "resonance7-sqlite": {
      "command": "node",
      "args": [
        "d:\\Development\\Resonance7\\library\\tools\\mcp_sqlite_server\\src\\server.js"
      ],
      "env": {
        "KNOWLEDGE_BASE_DB_PATH": "d:\\Development\\Resonance7\\library\\resources\\wikis\\psdevwiki_ps3\\psdevwiki_ps3_knowledge_base.db"
      }
    }
  }
}
```

**Important**: Update the paths to match your actual workspace location.

## Available Tools

Once configured, agents can use these tools directly in Cursor:

### 1. `execute_query`

Execute a SQL query against the knowledge base database.

**Parameters:**
- `query` (required): SQL query string
- `database_path` (optional): Path to database file (defaults to configured knowledge base)

**Example:**
```
Use execute_query tool with:
- query: SELECT title FROM pages WHERE title LIKE 'XMBML%' LIMIT 10
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

### Query for specific pages:
```
Use execute_query tool with:
- query: SELECT title, namespace FROM pages WHERE title LIKE 'SC Communication%' LIMIT 5
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

The default database path is set in `mcp-config.json` via the `KNOWLEDGE_BASE_DB_PATH` environment variable. You can override this per-query using the `database_path` parameter.

## Security Considerations

- Database is opened in **read-only mode** - only SELECT queries are supported
- No write operations (INSERT, UPDATE, DELETE) are allowed
- Database path is configurable but defaults to the knowledge base location

## Troubleshooting

### MCP Server Not Appearing

1. Check that Node.js is in your PATH
2. Verify the path in `args` is correct and absolute
3. Restart Cursor after adding MCP configuration
4. Check Cursor's developer console for errors

### Database Not Found

1. Verify the database path in the `env` section of `mcp-config.json`
2. Use absolute paths (not relative)
3. Check file permissions

### Tools Not Working

1. Check Cursor's MCP server status (should show as "connected")
2. Verify Node.js version (18+ required)
3. Check that `better-sqlite3` installed correctly (may need to rebuild native modules)

### Database Files Not Visible to Agents

If agents cannot see knowledge base database files (`.db`, `.sqlite`, `.sqlite3`) in `library/resources/wikis/`, check `.cursorignore` patterns.

**Solution**: Add exceptions to the root-level `.cursorignore` file:

```gitignore
# Database files (if applicable)
*.db
*.sqlite
*.sqlite3

# Exception: Allow knowledge base databases in library directory
!library/**/*_knowledge_base.db
!library/**/*_knowledge_base.sqlite
!library/**/*_knowledge_base.sqlite3
```

**Important**: `.cursorignore` patterns are relative to the directory containing the file. If your workspace is at `projects/XMBMGMT/` but the database is at `library/...`, you must add the exception to the root-level `.cursorignore`, not the project-level one.

### Terminal Output Not Captured (Alternative Methods)

If you're using terminal-based queries instead of MCP and experiencing output capture issues:

1. **Use MCP Server** (recommended) - This bypasses all terminal output issues
2. **Enable Legacy Terminal Tool** in Cursor settings (Agents > Inline Editing & Terminal)
3. **Update Cursor** to version 1.7.17+ if using older versions
4. **Use file-based output** - Write results to a file, then read the file

For detailed troubleshooting, see the alternative methods section below.

## Alternative: SQLite Command-Line Tool

If MCP server isn't configured, you can use the SQLite command-line tool directly:

```bash
# Run a query
sqlite3 -header -column library/resources/wikis/psdevwiki_ps3/psdevwiki_ps3_knowledge_base.db "SELECT title FROM pages LIMIT 10;"
```

**Note**: Terminal output capture can be unreliable in Cursor. The MCP server is recommended to avoid these issues.

## Benefits Over Terminal-Based Queries

- ✅ **No terminal output capture issues** - Results returned directly through MCP
- ✅ **Structured JSON responses** - Easy for agents to parse
- ✅ **Native tool integration** - Works seamlessly with Cursor's tool system
- ✅ **No file creation needed** - Results returned in tool response
- ✅ **Type-safe** - Proper error handling and validation

## License

MIT License
