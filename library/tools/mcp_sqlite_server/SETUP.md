# MCP SQLite Server Setup Guide

Quick setup instructions for configuring the SQLite MCP server in Cursor IDE.

## Step 1: Install Dependencies

```bash
cd library/tools/mcp_sqlite_server
npm install
```

This installs:
- `@modelcontextprotocol/sdk` - MCP protocol implementation
- `better-sqlite3` - Fast SQLite3 library for Node.js

## Step 2: Configure Cursor MCP Settings

1. **Open Cursor Settings:**
   - Press `Ctrl+Shift+J` (Windows/Linux) or `Cmd+,` (Mac)
   - Or: File → Preferences → Settings

2. **Navigate to MCP Settings:**
   - Search for "MCP" or "Model Context Protocol"
   - Or go to: **Features > MCP**

3. **Add MCP Server Configuration:**
   
   Click "Add New MCP Server" or edit the MCP settings JSON directly.

   **Copy this configuration** (update paths if your workspace is different):

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

   **Important**: 
   - Use **absolute paths** (not relative)
   - Use **double backslashes** (`\\`) in Windows paths
   - Update paths to match your actual workspace location

4. **Restart Cursor:**
   - Close and reopen Cursor for MCP server to connect

## Step 3: Verify Installation

After restarting Cursor:

1. Open a chat with an agent
2. The agent should now have access to these tools:
   - `execute_query` - Run SQL queries
   - `get_tables` - List database tables
   - `get_table_schema` - Get table structure
   - `get_database_info` - Get database statistics

3. **Test it:**
   ```
   Use get_tables tool to list all tables in the knowledge base
   ```

## Troubleshooting

### MCP Server Not Connecting

- **Check Node.js**: Ensure Node.js 18+ is installed and in PATH
  ```bash
  node --version
  ```

- **Check Paths**: Verify all paths in the MCP config are correct and absolute
- **Check Permissions**: Ensure the database file is readable
- **Check Cursor Logs**: View → Output → Select "MCP" to see connection logs

### "Command not found: node"

- Install Node.js from [nodejs.org](https://nodejs.org/)
- Or ensure Node.js is in your system PATH
- Restart Cursor after installing Node.js

### Database Not Found

- Verify the database path in the `env.KNOWLEDGE_BASE_DB_PATH` setting
- Use absolute paths (full path from drive letter)
- Check that the database file exists at that location

### Native Module Build Errors

If `better-sqlite3` fails to install:

```bash
# Windows (may need Visual Studio Build Tools)
npm install --build-from-source better-sqlite3

# Or use prebuilt binaries
npm install better-sqlite3
```

## Alternative: Use Relative Paths (Advanced)

If you want the server to work across different machines, you can modify `server.js` to resolve paths relative to the workspace root, but absolute paths are more reliable for MCP configuration.

## Next Steps

Once configured, agents can query the database directly:

```
Use execute_query tool with:
- query: SELECT title FROM pages WHERE title LIKE 'XMBML%' LIMIT 10
```

No terminal output capture needed - results come directly through MCP tools!
