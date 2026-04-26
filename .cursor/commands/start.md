# Resonance 7 Start

Initialize and verify Resonance7 workspace setup for first-time or returning users.

## Action

When this command is invoked:
1. Load the foundation (same as `/foundation`)
2. Check workspace state and verify setup
3. Provide a personalized onboarding checklist based on current state
4. Guide user to next steps

## Verification Checks

Check for:
- Python installation and version
- Workspace structure (library/, sessions/, tools/, projects/)
- Existing sessions (if any)
- Existing projects (if any)
- Shared resource symlinks (in current project if applicable)

## Onboarding Checklist

**For First-Time Users:**
- [x] Python 3.7+ installed ([Download if needed](https://www.python.org/downloads/))
- [ ] Workspace cloned/downloaded
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
- Or use Python scripts directly: `python library/tools/session_tools.py`

## When to Use

- First time setting up Resonance7
- Returning after a break (refresh understanding)
- Verifying workspace is properly configured
- Getting oriented in a new workspace

## MCP Setup Check (SQLite)

During `/start`, verify MCP config is usable for this workspace.

### Check `.cursor/mcp.json`

1. Confirm file exists at `.cursor/mcp.json`
2. Confirm server entry exists (example key: `Resonance7-sqlite`)
3. Validate required fields:
   - `command`
   - `args[0]`
   - `env.DEFAULT_DB_PATH` (optional only if your server supports no default)

### Placeholder Detection

If any value contains placeholders (examples: `<ABSOLUTE_PATH_TO_NODE_EXE>`, `<ABSOLUTE_PATH_TO_WORKSPACE>`), pause and ask the user to replace them with real paths.

Minimum substitutions:
- `command` -> absolute path to `node.exe`
- `args[0]` -> absolute path to `library/tools/mcp_sqlite_server/src/server.js`
- `env.DEFAULT_DB_PATH` -> absolute path to `library/resources/databases/db/session_logs.db`

### Path Validation (Windows)

Run checks:
- `Test-Path -LiteralPath "<command path>"`
- `Test-Path -LiteralPath "<args[0] path>"`
- `Test-Path -LiteralPath "<DEFAULT_DB_PATH path>"`

If any are `False`, report exactly which path failed and ask user to fix it.

### Final Step

After edits to MCP config, remind user:
- Reload Cursor window so MCP servers restart.
