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
import { existsSync } from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Default database path (can be overridden via environment variable)
const DEFAULT_DB_PATH = process.env.KNOWLEDGE_BASE_DB_PATH || 
  join(__dirname, "../../../resources/wikis/psdevwiki_ps3/psdevwiki_ps3_knowledge_base.db");

let dbConnection = null;

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
        name: "execute_query",
        description: "Execute a SQL query against the knowledge base database and return results",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "SQL query to execute (SELECT, INSERT, UPDATE, DELETE, etc.)",
            },
            database_path: {
              type: "string",
              description: "Optional: Path to SQLite database file. If not provided, uses default knowledge base.",
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
              description: "Optional: Path to SQLite database file. If not provided, uses default knowledge base.",
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
              description: "Optional: Path to SQLite database file. If not provided, uses default knowledge base.",
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
              description: "Optional: Path to SQLite database file. If not provided, uses default knowledge base.",
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

  try {
    const dbPath = args.database_path || DEFAULT_DB_PATH;

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
        const query = args.query;
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
        const tableName = args.table_name;
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
