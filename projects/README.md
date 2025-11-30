# Projects - User Development Workspaces

The `projects/` directory contains individual development projects created within the Resonance7 framework. Each project is a self-contained workspace that shares access to Resonance7 resources through symlinks, enabling consistent development practices across all projects.

## Purpose

This directory serves as the workspace for your development projects. Projects created here:
- Follow a standardized structure based on the Resonance7 template
- Have automatic access to shared Resonance7 resources via symlinks
- Maintain project-specific configuration while benefiting from framework-wide standards
- Are isolated workspaces that can be developed independently

## Creating a New Project

Use the `setup_workspace.py` tool to create new projects:

```bash
# Interactive mode (recommended)
python tools/setup_workspace.py

# Direct project creation
python tools/setup_workspace.py --project my-project-name

# Preview changes without creating
python tools/setup_workspace.py --project my-project-name --dry-run
```

The tool will:
1. Create the project directory structure (`src/`, `docs/`, `tests/`)
2. Set up symlinks to shared Resonance7 resources
3. Generate project-specific configuration files
4. Create a README.md template for your project

## Project Structure

Each project follows this standard structure:

```
projects/
└── [project-name]/
    ├── src/                    # Project source code
    ├── docs/                   # Project documentation
    ├── tests/                  # Project test files
    ├── .gitignore              # Project-specific git ignore rules
    ├── .cursorignore           # Project-specific Cursor IDE ignore rules
    ├── .agentignore            # Project-specific agent file protection rules
    ├── README.md               # Project documentation
    ├── requirements.txt        # Python dependencies
    │
    ├── library/                # Symlink → Shared Resonance7 resources (includes universal tools)
    ├── sessions/               # Symlink → Shared session management
    ├── tools/                  # Independent directory → Project-specific tools (not symlinked)
    ├── .cursor/                # Symlink → Shared Cursor configuration
    │
    │   # Universal tools accessible via library/ symlink:
    │   # - library/tools/session_tools.py
    │   # - library/tools/setup_workspace.py
    │   # - library/tools/session_tools.bat
    │   # - library/tools/setup_workspace.bat
```

## Shared Resources

All projects automatically receive symlinks to shared Resonance7 resources:

### `library/` → Shared Resonance7 Resources
- `agent_foundation.json` - Core agent behavior and protocols
- `session_template.md` - Session logging template
- `workspace_template/` - Project template blueprint
- `docs/` - Knowledge base modules (on-demand)

### `sessions/` → Session Management
- `current/` - Active development sessions
- `recent/` - Older sessions (7+ days)
- `archived/` - Monthly session archives

### `tools/` → Project-Specific Tools
- **Independent directory** (not symlinked) for project-specific tools
- Universal tools are in `library/tools/` and accessible via `library/` symlink:
  - `library/tools/session_tools.py` - Session creation and management
  - `library/tools/setup_workspace.py` - Workspace setup utility

### `.cursor/` → Cursor Configuration
- Shared Cursor IDE rules and configuration
- Agent onboarding protocols

### Batch Launchers
- `tools/` - Universal development tools directory (accessible via library/ symlink)
  - `session_tools.py` - Session creation and management
  - `setup_workspace.py` - Workspace setup utility
  - `session_tools.bat` - Quick launcher for session management
  - `setup_workspace.bat` - Quick launcher for workspace setup

## Project Configuration Files

Each project includes three ignore/protection files:

### `.gitignore`
Project-specific Git ignore rules. Excludes build artifacts, virtual environments, IDE files, and other project-specific patterns.

### `.cursorignore`
Tells Cursor IDE which files to ignore when indexing and searching. Can override parent-level patterns using the `!` negation operator.

### `.agentignore`
Protects files from automatic agent modification. Referenced by the `file_safety` protocol in `agent_foundation.json`. Can override parent-level patterns using the `!` negation operator.

## Project Isolation

Projects are:
- **Self-contained**: Each project has its own source code, documentation, and tests
- **Independently developed**: Work on projects separately without affecting others
- **User-specific**: Projects are excluded from version control (per root `.gitignore`)
- **Resource-shared**: Access shared Resonance7 resources via symlinks without duplication

## Integration with Resonance7

Projects benefit from Resonance7's framework features:

### Agent Foundation
- All projects use the same agent behavioral guidelines from `library/agent_foundation.json`
- Consistent development protocols across all projects
- Shared ethical standards and communication protocols

### Session Management
- Track development sessions across all projects
- Maintain context and history through session logs
- Access session tools from any project directory

### Knowledge Persistence
- Access shared documentation modules from `library/docs/`
- Reference session logs for context and decisions
- Maintain consistent documentation standards

### Development Tools
- Use shared tools from any project directory
- Access workspace setup utilities for creating additional projects
- Benefit from framework-wide tool improvements

## Best Practices

### Project Naming
- Use descriptive, clear project names
- Follow naming conventions appropriate for your platform
- Avoid special characters that might cause issues with symlinks

### Project Organization
- Keep project-specific code in `src/`
- Maintain documentation in `docs/`
- Write tests in `tests/`
- Update `README.md` with project-specific information

### Configuration Management
- Customize `.gitignore`, `.cursorignore`, and `.agentignore` as needed
- Use `!` negation in ignore files to override parent-level patterns when necessary
- Protect critical files by adding them to `.agentignore`

### Shared Resources
- **Do not modify** symlinked directories (`library/`, `sessions/`, `tools/`, `.cursor/`)
- Changes to shared resources affect all projects
- Use project-specific directories for project-specific work

### Version Control
- Projects are excluded from the main Resonance7 repository (user-specific)
- Each project can have its own Git repository if needed
- Use project-level `.gitignore` to control what gets committed

## Working with Projects

### Starting Development
1. Create a new project: `python tools/setup_workspace.py --project my-project`
2. Navigate to the project: `cd projects/my-project`
3. Set up virtual environment: `python -m venv .venv`
4. Activate virtual environment: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Start coding in `src/`

### Accessing Shared Resources
From any project directory:
- Access agent foundation: `library/agent_foundation.json`
- Create sessions: `python tools/session_tools.py` or `session_tools.bat`
- Use workspace tools: `python tools/setup_workspace.py` or `setup_workspace.bat`
- Reference session logs: `sessions/current/`

### Project Maintenance
- Keep project structure organized
- Update `README.md` as the project evolves
- Maintain `requirements.txt` with current dependencies
- Run session maintenance tools periodically

## Troubleshooting

### Symlink Issues
If symlinks don't work on your platform:
- **Windows**: The tool will attempt directory junctions as a fallback
- **Linux/macOS**: Ensure you have permission to create symlinks
- **Manual fix**: See `tools/setup_workspace.py` for symlink creation logic

### Missing Shared Resources
If shared resources are missing:
- Verify you're in a Resonance7 workspace (look for `.cursor/rules/agent_onboarding.mdc`)
- Recreate symlinks: `python tools/setup_workspace.py --project [project-name]` (will prompt about existing project)

### Project Already Exists
If a project with the same name exists:
- The tool will prompt to overwrite
- Choose a different name, or confirm overwrite to replace the existing project

## Related Documentation

- **[Library Documentation](../library/README.md)** - Shared Resonance7 resources
- **[Session Management](../sessions/README.md)** - Session logging and lifecycle
- **[Tools Documentation](../tools/README.md)** - Available scripts and utilities
- **[Workspace Template](../library/workspace_template/README.md)** - Project template structure
- **[Root README](../README.md)** - Framework overview and quick start

## Purpose in Resonance7 Architecture

The `projects/` directory embodies the Resonance7 principle of **Knowledge Persistence** by:
- Providing isolated workspaces for focused development
- Enabling shared access to accumulated knowledge and resources
- Maintaining consistent structure and standards across projects
- Supporting the human-AI collaborative development model

Each project is both independent and connected, allowing you to work on multiple projects while benefiting from the shared knowledge and tools of the Resonance7 framework.

