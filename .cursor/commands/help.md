# Resonance 7 Help

Provide succinct and clear explanations of Resonance7 topics and features.

## Action

When this command is invoked:
1. Ask the user what Resonance7 topic they need help with, OR
2. If a specific topic is mentioned, provide a clear, concise explanation

Be ready to explain:
- Workspace structure and architecture
- Foundation repo vs external projects
- Available tools and their usage
- Session management system
- Setup scripts
- Ignore files (.gitignore, .cursorignore, .agentignore)
- Any other Resonance7 concepts

## Explanation Style

- **Succinct**: Get to the point quickly
- **Clear**: Use simple, direct language
- **Practical**: Focus on what users need to know to use the feature
- **Contextual**: Reference actual files and paths in the workspace
- **Examples**: Include brief usage examples when helpful

## Common Topics

**Workspace Structure:**
- Foundation repo: `library/`, `.cursor/`, `projects/` (pairing files), `tests/`
- Session logs: `library/sessions/{current,recent,archived}/`
- External project code: separate folder, linked via `projects/*.code-workspace`

**Tools (`library/tools/scripts/`):**
- `setup_workspace.py` - Bootstrap dirs; pair external projects
- `setup_database.py` - MCP config and `npm install`
- `session_tools.py` - Session log create, prune, ingest (when ingest script exists)

**Session Management:**
- Lifecycle: current -> recent -> archived
- Naming: `YYYYMMDD-NN.md`
- Template: `library/templates/session_template.md`

**Configuration Files:**
- `.gitignore` - Git exclusions (session payloads, local MCP, pairing files)
- `.cursorignore` - Cursor indexing exclusions
- `.agentignore` - Agent file modification protection
- `library/.workspace_setup_required` - First-run marker (removed after bootstrap)

**First-Time Setup:**
1. `python library/tools/scripts/setup_workspace.py`
2. `python library/tools/scripts/setup_database.py`
3. Reload editor

## When to Use

- When users ask "How does X work?" about Resonance7
- When explaining workspace concepts
- When users need clarification on tools or features
- When onboarding new users to the framework
