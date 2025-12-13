# Library - Shared Resonance 7 Resources

The `library/` directory contains the core configuration, templates, and shared resources that define the Resonance 7 framework. This directory is symlinked into all projects, making these resources accessible throughout the workspace.

## Core Files

### `agent_foundation.json`
The foundational configuration file that defines:
- Core philosophy and workspace architecture
- Essential agent behavior and ethical standards
- Communication protocols
- Development protocols (web-first, file safety, command execution)
- Session logging configuration

This file is automatically loaded by agents on session start via `.cursor/rules/agent_onboarding.mdc`.

### `session_template.md`
The template structure for session logs. Defines:
- YAML frontmatter format
- Session metadata rules
- Standard sections for tracking progress
- Lifecycle management guidelines

Referenced by `tools/session_tools.py` when creating new session logs.

### `templates/project_template/`
Blueprint for new Resonance 7 projects. Contains:
- Standard project structure (src/, docs/, tests/)
- Template configuration files
- README and requirements.txt templates

Can be regenerated using `tools/project_setup.py --template` if missing.

## Database Access

### Knowledge Base Databases

Knowledge base databases are located in `resources/wikis/` and provide structured access to wiki content via SQLite.

**Recommended Method**: Use the **MCP SQLite Server** for direct database access through Cursor's tool system.

**Quick Setup:**
1. Install: `cd library/tools/mcp_sqlite_server && npm install`
2. Configure in Cursor: See `library/tools/mcp_sqlite_server/SETUP.md`
3. Restart Cursor

**Usage:**
```
Use execute_query tool with:
- query: SELECT title FROM pages WHERE title LIKE 'XMBML%' LIMIT 10
```

For detailed setup, troubleshooting, and alternative methods, see `library/tools/mcp_sqlite_server/README.md`.

**Note**: If databases aren't visible to agents, check `.cursorignore` patterns. The root `.cursorignore` should include exceptions for knowledge base databases:
```gitignore
*.db
*.sqlite
*.sqlite3
!library/**/*_knowledge_base.db
!library/**/*_knowledge_base.sqlite
!library/**/*_knowledge_base.sqlite3
```

## Resources

### `resources/docs/`
Knowledge base and context modules for agents (see `resources/docs/README.md` for details).

Modules are downloaded on-demand rather than included in the base repository to keep it lean. Organized by:
- `languages/` - Programming language documentation and examples
- `frameworks/` - Framework documentation (Godot, MonoGame, Unity, etc.)
- `hardware/` - Hardware documentation (game consoles, PC architecture, etc.)
- `tools/` - Development tool documentation (rom hacking suites, etc.)

### `resources/wikis/`
Knowledge base databases extracted from wikis. See `resources/wikis/README.md` for details.

## Integration

The `library/` directory is automatically symlinked into all projects created via `library/tools/project_setup.py`, providing:
- Shared access to Resonance 7 configuration
- Consistent agent behavior across all projects
- Centralized template and resource management
- No duplication of core protocol files

## Purpose

This directory serves as the "brain" of Resonance 7 - containing the foundational rules, templates, and shared knowledge that enable consistent agent behavior and project structure across the entire workspace.

