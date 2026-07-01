#!/usr/bin/env node

/**
 * SQLite MCP Server for Resonance7 Knowledge Bases
 * 
 * Provides MCP tools for querying SQLite knowledge base databases.
 * Bypasses terminal output capture issues by exposing database access
 * directly through Cursor's MCP tool system.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import Database from "better-sqlite3";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import { existsSync, readdirSync } from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/** Workspace DB directory (library/tools/mcp_sqlite_server/src -> library/databases/db). */
const DB_DIR = join(__dirname, "../../../databases/db");

const DATABASE_PATH_HELP =
  "Optional: alias (filename stem under library/databases/db/, e.g. iog_disassembly), session_logs, or absolute path to a .db file. Default: session_logs.";

/** Fallback when no env override is set (library/tools/mcp_sqlite_server/src -> library/). */
const SESSION_LOGS_FALLBACK = join(DB_DIR, "session_logs.db");

/** Resolve session_logs / default DB from env (setup script sets DEFAULT_DB_PATH). */
function resolveSessionLogsPath() {
  return (
    process.env.SESSION_LOGS_DB_PATH ||
    process.env.DEFAULT_DB_PATH ||
    process.env.KNOWLEDGE_BASE_DB_PATH ||
    SESSION_LOGS_FALLBACK
  );
}

const DEFAULT_DB_PATH = resolveSessionLogsPath();

/** List *.db files in DB_DIR with alias = filename stem. */
function listWorkspaceDatabases() {
  if (!existsSync(DB_DIR)) {
    return [];
  }
  return readdirSync(DB_DIR)
    .filter((name) => name.endsWith(".db"))
    .map((name) => {
      const alias = name.slice(0, -3);
      const path = join(DB_DIR, name);
      return { alias, path };
    })
    .filter((entry) => existsSync(entry.path))
    .sort((a, b) => a.alias.localeCompare(b.alias));
}

/**
 * Resolve database_path: default, session_logs, db-dir stem alias, or absolute path.
 */
function resolveDatabasePath(input) {
  if (input === undefined || input === null || input === "" || input === "default") {
    return DEFAULT_DB_PATH;
  }
  const key = String(input).trim();
  if (key === "session_logs") {
    return resolveSessionLogsPath();
  }
  const stem = key.endsWith(".db") ? key.slice(0, -3) : key;
  const byStem = join(DB_DIR, `${stem}.db`);
  if (existsSync(byStem)) {
    return byStem;
  }
  if (existsSync(key)) {
    return key;
  }
  return key;
}

const server = new Server(
  {
    name: "resonance7-sqlite-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "list_databases",
        description:
          "List workspace SQLite databases (alias and path) from library/databases/db/",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "execute_query",
        description: "Execute a SQL query against the knowledge base database and return results",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "SQL query to execute (SELECT only; database is opened read-only)",
            },
            database_path: {
              type: "string",
              description: DATABASE_PATH_HELP,
            },
          },
          required: ["query"],
        },
      },
      {
        name: "get_tables",
        description: "List all tables in the knowledge base database",
        inputSchema: {
          type: "object",
          properties: {
            database_path: {
              type: "string",
              description: DATABASE_PATH_HELP,
            },
          },
        },
      },
      {
        name: "get_table_schema",
        description: "Get the schema information for a specific table",
        inputSchema: {
          type: "object",
          properties: {
            table_name: {
              type: "string",
              description: "Name of the table to get schema for",
            },
            database_path: {
              type: "string",
              description: DATABASE_PATH_HELP,
            },
          },
          required: ["table_name"],
        },
      },
      {
        name: "get_database_info",
        description: "Get information about the database (size, page count, etc.)",
        inputSchema: {
          type: "object",
          properties: {
            database_path: {
              type: "string",
              description: DATABASE_PATH_HELP,
            },
          },
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const toolArgs = args ?? {};

  try {
    if (name === "list_databases") {
      const databases = listWorkspaceDatabases();
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                db_dir: DB_DIR,
                default_alias: "session_logs",
                databases,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    const dbPath = resolveDatabasePath(toolArgs.database_path);

    // Verify database exists
    if (!existsSync(dbPath)) {
      return {
        content: [
          {
            type: "text",
            text: `Error: Database not found at ${dbPath}`,
          },
        ],
        isError: true,
      };
    }

    switch (name) {
      case "execute_query": {
        const query = toolArgs.query;
        if (!query) {
          return {
            content: [
              {
                type: "text",
                text: "Error: Query parameter is required",
              },
            ],
            isError: true,
          };
        }

        const db = new Database(dbPath, { readonly: true });
        try {
          const queryUpper = query.trim().toUpperCase();
          const isSelect = queryUpper.startsWith("SELECT");

          if (isSelect) {
            const stmt = db.prepare(query);
            const rows = stmt.all();
            
            // Convert to JSON-serializable format
            const results = rows.map(row => {
              const obj = {};
              for (const key in row) {
                obj[key] = row[key];
              }
              return obj;
            });

            return {
              content: [
                {
                  type: "text",
                  text: JSON.stringify({
                    success: true,
                    query: query,
                    results: results,
                    count: results.length,
                  }, null, 2),
                },
              ],
            };
          } else {
            // For non-SELECT queries, we'd need write access
            return {
              content: [
                {
                  type: "text",
                  text: "Error: Only SELECT queries are supported. Database is opened in read-only mode.",
                },
              ],
              isError: true,
            };
          }
        } catch (error) {
          return {
            content: [
              {
                type: "text",
                text: `Database error: ${error.message}`,
              },
            ],
            isError: true,
          };
        } finally {
          db.close();
        }
      }

      case "get_tables": {
        const db = new Database(dbPath, { readonly: true });
        try {
          const tables = db
            .prepare(
              "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            .all()
            .map((row) => row.name);

          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ tables: tables }, null, 2),
              },
            ],
          };
        } catch (error) {
          return {
            content: [
              {
                type: "text",
                text: `Error: ${error.message}`,
              },
            ],
            isError: true,
          };
        } finally {
          db.close();
        }
      }

      case "get_table_schema": {
        const tableName = toolArgs.table_name;
        if (!tableName) {
          return {
            content: [
              {
                type: "text",
                text: "Error: table_name parameter is required",
              },
            ],
            isError: true,
          };
        }

        const db = new Database(dbPath, { readonly: true });
        try {
          const schema = db
            .prepare(`PRAGMA table_info(${tableName})`)
            .all();

          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ table: tableName, schema: schema }, null, 2),
              },
            ],
          };
        } catch (error) {
          return {
            content: [
              {
                type: "text",
                text: `Error: ${error.message}`,
              },
            ],
            isError: true,
          };
        } finally {
          db.close();
        }
      }

      case "get_database_info": {
        const db = new Database(dbPath, { readonly: true });
        try {
          const pageCount = db.prepare("PRAGMA page_count").get();
          const pageSize = db.prepare("PRAGMA page_size").get();
          const tableCount = db
            .prepare(
              "SELECT COUNT(*) as count FROM sqlite_master WHERE type='table'"
            )
            .get();

          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(
                  {
                    path: dbPath,
                    page_count: pageCount.page_count,
                    page_size: pageSize.page_size,
                    approximate_size_mb: (
                      (pageCount.page_count * pageSize.page_size) /
                      (1024 * 1024)
                    ).toFixed(2),
                    table_count: tableCount.count,
                  },
                  null,
                  2
                ),
              },
            ],
          };
        } catch (error) {
          return {
            content: [
              {
                type: "text",
                text: `Error: ${error.message}`,
              },
            ],
            isError: true,
          };
        } finally {
          db.close();
        }
      }

      default:
        return {
          content: [
            {
              type: "text",
              text: `Error: Unknown tool: ${name}`,
            },
          ],
          isError: true,
        };
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Resonance7 SQLite MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
