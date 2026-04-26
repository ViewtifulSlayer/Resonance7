# Resonance 7 Start

Initialize and verify Resonance7 workspace setup for first-time or returning users.

## Action

When this command is invoked:
1. Load the foundation (same as `/foundation`)
2. Check workspace state and verify setup
3. **Run the [MCP Setup Check (SQLite)](#mcp-setup-check-sqlite) below** (config, path validation, and Node dependencies). This is not optional for `/start` - actually perform the checks and `npm install`, do not only describe them.
4. Provide a personalized onboarding checklist based on current state
5. Guide user to next steps

## Verification Checks

Check for:
- Python installation and version
- Workspace structure (library/, sessions/, tools/, projects/)
- Existing sessions (if any)
- Existing projects (if any)
- Shared resource symlinks (in current project if applicable)
- **SQLite MCP:** `.cursor/mcp.json` valid paths, and `node_modules` for `library/tools/mcp_sqlite_server` (see MCP section)

## Onboarding Checklist

**For First-Time Users:**
- [x] Python 3.7+ installed ([Download if needed](https://www.python.org/downloads/))
- [ ] Workspace cloned/downloaded
- [ ] Configure SQLite MCP: `python library/tools/setup_mcp_sqlite.py`, then reload Cursor ([MCP Setup Check (SQLite)](#mcp-setup-check-sqlite))
- [ ] Agent foundation loaded (done automatically)
- [ ] Create first session: `python library/tools/session_tools.py`
- [ ] Create first project: `python library/tools/project_tools.py --project my-project`
- [ ] Explore available commands: `/help` for explanations

**For Returning Users:**
- Verify workspace structure is intact
- Check for recent sessions
- List available projects
- Suggest next actions based on current state

## Next Steps Guidance

Based on workspace state, suggest:
- **No sessions yet?** -> Create your first session to start tracking work
- **No projects yet?** -> Create a project workspace to begin development
- **Has sessions/projects?** -> Continue existing work or start new tasks
- **Questions?** -> Use `/help` to learn about specific topics

## Available Commands

- `/foundation` - Load core protocols and guidelines
- `/help` - Get explanations of Resonance7 topics
- `/start` - This command (workspace initialization)

## Quick Access

- `library/tools/session_tools.py` - Session management
- `library/tools/project_tools.py` - Create new projects
- `library/tools/setup_mcp_sqlite.py` - Write `.cursor/mcp.json` and run `npm install` for the SQLite MCP (see [MCP Setup Check (SQLite)](#mcp-setup-check-sqlite))
- Or use Python scripts directly: `python library/tools/session_tools.py`

## When to Use

- First time setting up Resonance7
- Returning after a break (refresh understanding)
- Verifying workspace is properly configured
- Getting oriented in a new workspace

## MCP Setup Check (SQLite)

**Agents:** perform this block every time `/start` runs. Use the tools and shell to read files, run the automated setup when needed, then validate paths. If you only summarize these steps without executing them, you have not completed `/start`.

### Automated setup (preferred)

From the **workspace root**, run the helper so one Node is used for both `npm install` and `mcp.json` (avoids `better-sqlite3` / NODE_MODULE_VERSION issues):

1. `python library/tools/setup_mcp_sqlite.py`  
   - Writes `.cursor/mcp.json` with absolute paths, runs `npm install` in `library/tools/mcp_sqlite_server`, then runs `npm audit fix` (compatible security updates). Use `--skip-audit-fix` to skip the audit step.
   - Optional: `python library/tools/setup_mcp_sqlite.py --dry-run` to print what would be written (no file write, no `npm install` or audit).
   - If Node is missing, the script prints how to install Node 18+ and exit instructions.
2. If the user cannot run Python, they may hand-edit using the **committed template shape**: `library/templates/configuration_templates/mcp.json.example` (placeholders; copy into `.cursor/mcp.json` and substitute), then run `npm install` in `library/tools/mcp_sqlite_server` with the **same** `node.exe` you put in `command`.

**After** a successful `setup_mcp_sqlite.py` run, remind the user: **reload the Cursor window** so MCP servers pick up the config.

If `.cursor/mcp.json` is already present with **no** placeholders and `node_modules` is installed, you can skip the script and go straight to validation below (unless the user reports MCP errors, in which case re-run the script or `npm install` with the same Node as in `command`).

### Check `.cursor/mcp.json`

1. Confirm file exists at `.cursor/mcp.json` (or run the automated setup above if missing)
2. Confirm a server entry exists (example key: `Resonance7-sqlite`)
3. Read the resolved values and validate required fields:
   - `command` (Node executable)
   - `args[0]` (path to `library/tools/mcp_sqlite_server/src/server.js`)
   - `env.DEFAULT_DB_PATH` if set (else the server uses its own default under `library/resources/...` - still confirm the DB file exists if you rely on it)

### Placeholder detection

If any value still contains placeholders (examples: `<ABSOLUTE_PATH_TO_NODE_EXE>`, `<ABSOLUTE_PATH_TO_WORKSPACE>`), do **not** only ask the user to hand-edit: run `python library/tools/setup_mcp_sqlite.py` from the workspace root (unless the user opts out), then re-check the file.

If the user will edit manually, minimum substitutions are:
- `command` -> absolute path to `node.exe` (e.g. `C:\Program Files\nodejs\node.exe` on Windows when a full install exists)
- `args[0]` -> absolute path to `library/tools/mcp_sqlite_server/src/server.js`
- `env.DEFAULT_DB_PATH` -> absolute path to `library/resources/databases/db/session_logs.db` (on Windows the drive letter must be valid, e.g. `E:\Resonance7\...`, not `E:Resonance7\...`)

### Node dependencies (MCP SQLite server)

The MCP process loads `better-sqlite3` and `@modelcontextprotocol/sdk`. If you did not use `setup_mcp_sqlite.py`, ensure packages are installed:

1. Working directory: `library/tools/mcp_sqlite_server` (under the workspace root)
2. Run: `npm install` (use the same Node as in `mcp.json` if multiple installs exist, e.g. `& "C:\Program Files\nodejs\npm.cmd" install` in that folder on Windows)
3. If the command fails, report the error. Native modules need a matching Node version (see `engines` in that folder's `package.json`)

### Path validation (Windows)

Run and report results (substitute the actual strings from `mcp.json`):

- `Test-Path -LiteralPath "<command path>"`
- `Test-Path -LiteralPath "<args[0] path>"`
- `Test-Path -LiteralPath "<DEFAULT_DB_PATH or default DB file path>"` when applicable

If any are `False`, report exactly which path failed and how to fix it.

On non-Windows, verify the same three files exist with the platform equivalent (e.g. `test -f`).

### Optional quick import check

If path validation passed, you may run a one-shot check from `library/tools/mcp_sqlite_server` that the same imports as `src/server.js` load (e.g. `import` from `@modelcontextprotocol/sdk/...` and `better-sqlite3`). If this fails after `npm install`, report the error.

### Final step

- If `mcp.json` or `node_modules` was fixed during this run, remind the user: **reload the Cursor window** so MCP servers restart.
- If the config was already valid and `npm install` was up to date, a reload is not strictly required but safe after any MCP change.
