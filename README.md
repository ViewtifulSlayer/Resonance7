# Resonance7

A comprehensive AI agent development framework and workspace management system designed for collaborative human-AI development. Resonance7 provides a structured environment for managing AI agent sessions, maintaining knowledge persistence, and organizing development projects with shared resources.

## 🌟 Features

- **Agent Foundation**: Core behavioral guidelines and protocols for AI agents
- **Session Management**: Structured logging and tracking of AI agent sessions
- **MCP Database Integration**: Support for sqlite databases for drastically enhanced knowledge-base
- **Workspace Templates**: Pre-configured project templates with shared resources
- **Knowledge Persistence**: Documentation libraries and session logs for knowledge accumulation
- **Cross-Platform Tools**: Python-based utilities that work on Windows, Linux, and macOS
- **IDE-Agnostic**: Works with any IDE that supports Cursor rules (or can be adapted)

## 📋 What's New

**v2.1.0** (2026-04-26)
- **`setup_mcp_sqlite.py`** - Writes a local **`.cursor/mcp.json`**, runs **`npm install`** in **`library/tools/mcp_sqlite_server`**; use the same Node for both (avoids `better-sqlite3` / **NODE_MODULE_VERSION** mismatches)
- **MCP config not in Git** - **`.cursor/mcp.json`** is gitignored; run the setup script after clone or use **`library/templates/configuration_templates/mcp.json.example`**
- **`/start`** - Expanded to require the SQLite MCP path/deps check (not only a description)
- **Ignore/attributes** - Tuned **`.gitignore`**, **`.agentignore`**, **`.cursorignore`**, **`.gitattributes`**

**v2.0.0** (2026-04-04)
- **Session MCP** - Ingest session markdown into **`session_logs.db`** for FTS search; optional **`sessions/INDEX.md`** template
- **Breaking** - New projects symlink **`library/`** and **`sessions/`** only; **`.cursor/`** stays at workspace root (no symlink into `projects/<name>/`)
- **Onboarding** - Stricter foundation load order, intent-vs-command guidance in `agent_foundation.json`, MDC onboarding rule
- **`project_tools.py`** - Renamed from `project_setup.py`; commands and docs updated
- **MCP SQLite server** - Defaults to `session_logs.db`; **`session_logs`** alias (see `library/resources/databases/workspace_mcp_servers.md`)

**v1.3.0** (2025-12-13)
- Enhanced agent foundation with action authorization policy
- Reorganized workspace structure (documentation and templates)
- Added knowledge base database support with MCP SQLite Server integration
- Improved template management and path references
- Fixed `.gitignore` patterns for better resource management

**v1.2.0** (2025-11-21)
- Reorganized tools structure: Universal tools moved to `library/tools/` (accessible via `library/` symlink)
- Projects now get independent `tools/` directories (not symlinked) for project-specific tools
- Enhanced agent foundation with improved behavior guidance and partnership model
- Strengthened file creation protocols and knowledge persistence philosophy
- Added timestamp accuracy requirements for session logging

**v1.1.0** (2025-11-09)
- Added Cursor command system for streamlined agent interaction (`/foundation`, `/help`, `/start`, `/session`)
- Enhanced workspace template with `.cursorignore` and `.agentignore` templates
- Fixed missing directories in workspace template (now tracked in Git)

[View full changelog →](CHANGELOG.md)

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Git
- A compatible IDE (Cursor recommended, but any IDE can be adapted)
- **Node.js 18+** (optional) - only if you use the **Cursor SQLite MCP** server in **`library/tools/mcp_sqlite_server`**; use one Node install for both **`mcp.json`** and **`npm install`**

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ViewtifulSlayer/Resonance7.git
   cd Resonance7
   ```

2. **Set up your IDE:**
   - If using Cursor, the `.cursor/rules/agent_onboarding.mdc` will be automatically loaded
   - For other IDEs, copy the agent foundation rules to your IDE's configuration

3. **SQLite MCP (optional, Cursor):** To query **`session_logs.db`** and related SQLite DBs from the MCP server, from the repo root run:
   ```bash
   python library/tools/setup_mcp_sqlite.py
   ```
   Then **reload the Cursor window** so MCP picks up **`.cursor/mcp.json`**. To hand-edit instead, start from **`library/templates/configuration_templates/mcp.json.example`**, run **`npm install`** in **`library/tools/mcp_sqlite_server`**, and reload.

4. **Verify installation:**
   - Check that `library/agent_foundation.json` exists
   - Verify `library/tools/session_tools.py` is executable
   - Test with: `python library/tools/session_tools.py --help`
   - If you use MCP: confirm **`library/tools/mcp_sqlite_server/node_modules`** exists (created by the setup script or **`npm install`**)

### First Steps

1. **Create a new session:**
   ```bash
   python library/tools/session_tools.py
   ```
   Follow the interactive prompts to create your first session log.

2. **Set up a new project:**
   ```bash
   python library/tools/project_tools.py --project my-project
   ```
   This creates a new project workspace with shared resources symlinked.

## 📁 Directory Structure

```
Resonance7/                          # Main workspace
├── .cursor/                         # Cursor configuration
│   ├── commands/                    # Cursor commands
│   ├── rules/                       # Shared Cursor rules
│   │   └── agent_onboarding.mdc     # Shared Onboarding rule (IDE-agnostic protocol)
│   ├── skills/                      # Cursor skills
│   └── mcp.json                     # Local Cursor MCP (gitignored; generate via setup_mcp_sqlite.py)
├── library/                         # Shared Resonance 7 resources
│   ├── resources/                   # Shared resources
│   │   ├── db/                      # SQLite databases (downloaded/built on-demand)
│   │   ├── docs/                    # Documentation modules (downloaded on-demand)
│   │   └── wikis/                   # Knowledge base indexes extracted from wikis
│   ├── templates/                   # Project and documentation templates
│   │   ├── documentation_templates/ # Documentation file templates
│   │   └── project_template/        # Project workspace template
│   ├── tools/                       # Universal development tools
│   │   ├── mcp_sqlite_server/       # MCP SQLite Server for database access
│   │   ├── session_tools.py         # Script for session log management
│   │   └── project_tools.py         # Project setup and template management
│   ├── agent_foundation.json        # Core Resonance 7 Agent foundation
│   └── README.md                    # Documentation for library directory
├── sessions/                        # Shared session management
│   ├── current/                     # Current sessions (last 7 days)
│   ├── recent/                      # Sessions 7+ days old
│   ├── archived/                    # Monthly zip archives (YYYY-MM.zip)
│   ├── INDEX.md                     # Topic-based index of sessions
│   └── README.md                    # Documentation for sessions directory
├── projects/                        # Project-specific workspaces
│    └─ [project-name]/
│       ├── docs/                    # Project-specific resources
│       ├── library/                 # Symlink → Shared Resonance7 resources (includes universal tools)
│       ├── sessions/                # Symlink → Shared session management
│       ├── src/                     # Project source code
│       ├── tests/                   # Project test files
│       ├── tools/                   # Project-specific tools (independent, not symlinked)
│       ├── .agentignore             # Project-level agent ignore
│       ├── .cursorignore            # Project-level Cursor IDE ignore
│       ├── .gitignore               # Project-level git ignore
│       ├── README.md                # Project documentation
│       └── requirements.txt         # Python dependencies
│           # Note: library/ and sessions/ are symlinked into projects; .cursor/ stays at workspace root only
├── .cursorignore                    # Root-level Cursor ignore file
├── .agentignore                     # Root-level agent ignore file
├── .gitignore                       # Root-level git ignore file
├── .gitattributes                   # Git attributes for line endings
├── CHANGELOG.md                     # Change log
├── LICENSE                          # MIT License
├── README.md                        # Root-level README file
└── RELEASE_NOTES.md                 # Release notes
```

## 📚 Documentation

- **[Library Documentation](library/README.md)** - Core resources and agent foundation
- **[Session Management](sessions/README.md)** - Session logging and lifecycle
- **[Tools Documentation](library/tools/README.md)** - Available scripts and utilities
- **[Project Template](library/templates/project_template/README.md)** - Project template structure
- **[Documentation Modules](library/resources/docs/README.md)** - Knowledge base organization
- **[Knowledge Bases](library/resources/wikis/README.md)** - Database access and knowledge bases
- **[Release Notes](RELEASE_NOTES.md)** - Detailed release information
- **[Changelog](CHANGELOG.md)** - Complete change history

## 🛠️ Usage

### Creating Sessions

Sessions track your work with AI agents, maintaining context and history:

```bash
# Interactive mode
python library/tools/session_tools.py

# Quick session creation
python library/tools/session_tools.py  # Follow prompts

# Session maintenance
python library/tools/session_tools.py --prune
```

### Managing Projects

Create new project workspaces with shared resources:

```bash
# Interactive mode
python library/tools/project_tools.py

# Direct project creation
python library/tools/project_tools.py --project my-app

# Regenerate project template
python library/tools/project_tools.py --template
```

### Agent Foundation

The core agent behavior is defined in `library/agent_foundation.json`, which provides universal protocols for all agents working in Resonance7 projects. This file establishes:
- Ethical standards and communication protocols
- Development workflows and best practices
- Session logging requirements
- Knowledge persistence strategies

## 🎯 Philosophy

Resonance7 is built on two core principles:

1. **Mutual Respect**: The user and agent are partners with complementary strengths. The user provides direction and domain expertise; the agent provides technical knowledge and execution. Both perspectives are valuable and should be expressed respectfully.

2. **Knowledge Persistence**: The framework enables knowledge accumulation and enhanced context retrieval through regularly maintained session logs, the user-curated documentation library, and a well-structured workspace. MCP-queryable databases (e.g. session_logs, workspace DBs) extend this with persistent recall and lookup when configured.

## 🔧 Configuration

### Agent Ignore

Add files or directories to `.agentignore` to prevent AI agents from modifying them:

```
# Protect core protocol files
library/agent_foundation.json

# Protect archived sessions
sessions/archived/
```

### Cursor Ignore

The `.cursorignore` file tells Cursor IDE which files and directories to ignore when indexing and searching. This improves IDE performance and reduces noise in search results. Project-level `.cursorignore` files can override parent-level patterns using the `!` negation operator.

### Git Ignore

The `.gitignore` file excludes user-specific content (sessions, projects, documentation modules) while preserving the framework structure. Your personal work remains local while the framework is version-controlled.

**Note**: Universal tools are in `library/tools/` and accessible via the `library/` symlink in projects. Projects get their own independent `tools/` directories for project-specific tools.

### Cursor SQLite MCP

**`.cursor/mcp.json`** is not committed. After clone or on a new machine, run **`python library/tools/setup_mcp_sqlite.py`** from the workspace root, then reload Cursor. The script writes absolute paths to your Node binary and the MCP server entrypoint, sets **`DEFAULT_DB_PATH`** for **`session_logs.db`**, and installs npm dependencies under **`library/tools/mcp_sqlite_server`**. See **`library/tools/mcp_sqlite_server/README.md`** and **`library/tools/mcp_sqlite_server/SETUP.md`** for details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests
- Share your use cases and experiences

## 🔮 Future Considerations

### GitHub Actions Workflows

Potential CI/CD workflows for:
- Validate session log YAML frontmatter
- Check session chain integrity
- Generate session statistics and reports
- Automated testing and quality checks

## 📖 Additional Resources

- Session logs are stored in `sessions/current/` (automatically archived after 7 days)
- Project workspaces symlink **`library/`** and **`sessions/`** to the workspace root for consistency (`.cursor/` is not symlinked into projects)
- Documentation modules are available in `library/resources/docs/`
- Knowledge base databases are accessible via MCP SQLite Server (see `library/tools/mcp_sqlite_server/README.md`)

---

**Ready to get started?** Clone the repository and run `python library/tools/session_tools.py` to create your first session!
