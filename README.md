# Resonance7

A comprehensive AI agent development framework and workspace management system designed for collaborative human-AI development. Resonance7 provides a structured environment for managing AI agent sessions, maintaining knowledge persistence, and organizing development projects with shared resources.

## 🌟 Features

- **Agent Foundation**: Core behavioral guidelines and protocols for AI agents
- **Session Management**: Structured logging and tracking of AI agent sessions
- **Workspace Templates**: Pre-configured project templates with shared resources
- **Knowledge Persistence**: Documentation libraries and session logs for knowledge accumulation
- **Cross-Platform Tools**: Python-based utilities that work on Windows, Linux, and macOS
- **IDE-Agnostic**: Works with any IDE that supports Cursor rules (or can be adapted)

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Git
- A compatible IDE (Cursor recommended, but any IDE can be adapted)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ViewtifulSlayer/Resonance7.git
   cd Resonance7
   ```

2. **Set up your IDE:**
   - If using Cursor, the `.cursor/rules/agent_onboarding.mdc` will be automatically loaded
   - For other IDEs, copy the agent foundation rules to your IDE's configuration

3. **Verify installation:**
   - Check that `library/agent_foundation.json` exists
   - Verify `tools/session_tools.py` is executable
   - Test with: `python tools/session_tools.py --help`

### First Steps

1. **Create a new session:**
   ```bash
   python tools/session_tools.py
   ```
   Follow the interactive prompts to create your first session log.

2. **Set up a new project:**
   ```bash
   python tools/setup_workspace.py --project my-project
   ```
   This creates a new project workspace with shared resources symlinked.

## 📁 Directory Structure

```
Resonance7/                         # Main workspace
├── .cursor/                         # Shared Cursor configuration
│   └── rules/  
│       └── agent_onboarding.mdc     # Shared Cursor rules (IDE-agnostic protocol)
├── library/                         # Shared Resonance 7 resources
│   ├── docs/                        # Knowledge base modules (see docs/README.md)
│   ├── agent_foundation.json         # Core Resonance 7 Agent foundation
│   ├── session_template.md           # Session logging template
│   ├── workspace_template/           # Project template (see workspace_template/README.md)
│   └── README.md                     # Documentation for library directory
├── sessions/                         # Shared session management
│   ├── current/                      # Current sessions (last 7 days)
│   ├── recent/                       # Sessions 7+ days old
│   ├── archived/                     # Monthly zip archives (YYYY-MM.zip)
│   └── README.md                     # Documentation for sessions directory
├── tools/                            # Shared scripts and tools
│   ├── session_tools.py              # Script for session log management
│   ├── setup_workspace.py            # Workspace setup and template management
│   └── README.md                     # Documentation for session tools
├── projects/                         # Project-specific workspaces
│   └── [project-name]/               # Individual user projects
│       ├── src/                      # Project source code
│       ├── docs/                     # Project documentation
│       ├── tests/                    # Project tests
│       ├── .gitignore                # Project-level git ignore
│       ├── .cursorignore             # Project-level Cursor IDE ignore
│       ├── .agentignore              # Project-level agent ignore
│       └── README.md                 # Project README
│       # Note: library/, sessions/, tools/, .cursor/ are symlinked into projects
├── .cursorignore                     # Root-level Cursor ignore file
├── .agentignore                      # Root-level agent ignore file
├── .gitignore                        # Root-level git ignore file
├── .gitattributes                    # Git attributes for line endings
├── LICENSE                           # MIT License
└── README.md                         # Root-level README file
```

## 📚 Documentation

- **[Library Documentation](library/README.md)** - Core resources and agent foundation
- **[Session Management](sessions/README.md)** - Session logging and lifecycle
- **[Tools Documentation](tools/README.md)** - Available scripts and utilities
- **[Workspace Template](library/workspace_template/README.md)** - Project template structure
- **[Documentation Modules](library/docs/README.md)** - Knowledge base organization

## 🛠️ Usage

### Creating Sessions

Sessions track your work with AI agents, maintaining context and history:

```bash
# Interactive mode
python tools/session_tools.py

# Quick session creation
python tools/session_tools.py  # Follow prompts

# Session maintenance
python tools/session_tools.py --prune
```

### Managing Projects

Create new project workspaces with shared resources:

```bash
# Interactive mode
python tools/setup_workspace.py

# Direct project creation
python tools/setup_workspace.py --project my-app

# Regenerate workspace template
python tools/setup_workspace.py --template
```

### Agent Foundation

The core agent behavior is defined in `library/agent_foundation.json`. This file establishes:
- Ethical standards and communication protocols
- Development workflows and best practices
- Session logging requirements
- Knowledge persistence strategies

## 🎯 Philosophy

Resonance7 is built on two core principles:

1. **Human-AI Collaborative Synergy**: Human wisdom and AI intelligence complement each other—together, our combined capabilities achieve what neither could alone.

2. **Knowledge Persistence**: The framework enables knowledge accumulation and retrieval across shared documentation libraries and regularly maintained session logs.

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
- Project workspaces symlink shared resources for consistency
- Documentation modules can be downloaded on-demand in `library/docs/`

---

**Ready to get started?** Clone the repository and run `python tools/session_tools.py` to create your first session!
