# Session Tools

A comprehensive Python script for managing development sessions in the Resonance 7 development environment. This tool consolidates session creation, continuation, and maintenance into a single, user-friendly interface.

## Features

- **Create New Sessions**: Initialize new development sessions with unique identifiers
- **Continue Existing Sessions**: Resume work on previously created sessions
- **Session Maintenance**: Prune old sessions, create archives, and manage session lifecycle
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Dependency-Free**: Uses only Python standard library

## Quick Start

### Prerequisites
- Python 3.7 or higher
- Resonance 7 development environment

### Basic Usage

```bash
# Interactive mode (recommended)
python tools/session_tools.py

# Direct access to specific functions
python tools/session_tools.py --prune
python tools/session_tools.py --dry-run
```

## Menu Options

### Main Menu
```
1. New session (interactive)       # Create session with custom metadata
2. Auto create (all defaults)      # Create session with placeholder values
3. Continue existing session       # Resume work on previous session
4. Prune sessions                  # Manage session maintenance
5. Cancel                          # Exit
```

### Pruning Menu
```
1. Move old sessions (7+ days)     # Archive sessions older than 7 days
2. Create monthly archives         # Create YYYY-MM.zip archives
3. Cleanup old sessions (90+ days) # Remove very old sessions
4. Full maintenance (all steps)    # Run complete maintenance workflow
5. Cancel                          # Return to main menu
```

## Command Line Options

```bash
# Show help
python tools/session_tools.py --help

# Dry run mode (preview without changes)
python tools/session_tools.py --dry-run

# Direct to pruning menu
python tools/session_tools.py --prune

# Dry run with pruning
python tools/session_tools.py --prune --dry-run
```

## Session File Structure

Sessions are stored in `sessions/current/` with the format:
- **Filename**: `YYYYMMDD-NN.md` (e.g., `20251026-01.md`)
- **Continuations**: `YYYYMMDD-NN_pt2.md`, `YYYYMMDD-NN_pt3.md`, etc.
- **YAML Frontmatter**: Metadata including title, author, status, timestamps
- **Template Structure**: Standardized sections for tracking progress

## Directory Structure

```
sessions/
├── current/          # Active sessions
├── recent/           # Sessions 7+ days old
└── archived/         # Monthly zip archives (YYYY-MM.zip)
```

## Session Lifecycle

1. **Active**: New sessions start in "Active" status
2. **Handoff**: User requests finalization
3. **Completed**: Session marked as complete
4. **Archived**: Moved to `recent/` after 7 days
5. **Compressed**: Added to monthly archives
6. **Cleaned**: Old sessions removed after 90 days

## Examples

### Create a New Session
```bash
python tools/session_tools.py
# Select option 1: New session (interactive)
# Follow prompts to set title, author, description
```

### Continue Previous Session
```bash
python tools/session_tools.py
# Select option 3: Continue existing session
# Choose from recent sessions list
```

### Session Maintenance
```bash
python tools/session_tools.py --prune
# Select option 4: Full maintenance (all steps)
# This will: move old sessions → create archives → cleanup
```

### Preview Changes
```bash
python tools/session_tools.py --prune --dry-run
# See what would be done without making changes
```

## Troubleshooting

### Common Issues

**"Could not find sessions/current/ directory"**
- Ensure you're running from the Resonance 7 workspace root
- Check that `sessions/current/` directory exists

**Unicode/Emoji Display Issues**
- The script uses plain text for Windows compatibility
- All Unicode characters have been replaced with text equivalents

**Permission Errors**
- Ensure you have write access to the sessions directory
- On Linux/macOS, check file permissions with `ls -la sessions/`

### Getting Help

```bash
# Show detailed help
python tools/session_tools.py --help

# Check script version
python tools/session_tools.py --version
```

## Integration

This tool is designed to work with the Resonance 7 development environment:

- **Agent Foundation**: Uses `library/agent_foundation.json` for configuration
- **Session Templates**: References `library/session_template.md` for structure
- **Workspace Detection**: Automatically finds the development workspace root
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Additional Tools

This directory may contain additional development and maintenance tools as the project grows:

### Available Tools
- **`setup_workspace.py`** - Automated workspace setup for new projects
  - Create new project workspaces with proper structure and symlinks
  - Automatically includes `.gitignore`, `.cursorignore`, and `.agentignore` files
  - Regenerate workspace template: `python tools/setup_workspace.py --template`
  - If `library/workspace_template/` is missing, regenerate it using the command above

### Planned Tools
- **`maintenance/`** - Additional maintenance scripts
- **`deployment/`** - Deployment and build scripts

### Tool Organization
```
tools/
├── session_tools.py          # Session management (this tool)
├── setup_workspace.py        # Workspace setup (available)
├── maintenance/              # Maintenance scripts (planned)
├── deployment/               # Build/deploy scripts (planned)
└── README.md                 # This documentation
```

### Adding New Tools

When adding new tools to this directory:

1. **Follow Naming Conventions**: Use `snake_case.py` for Python scripts
2. **Include Documentation**: Add a docstring and help text
3. **Update This README**: Document new tools in this section
4. **Test Cross-Platform**: Ensure tools work on Windows, Linux, and macOS
5. **Use Standard Library**: Prefer built-in modules over external dependencies

### Tool Requirements

All tools in this directory should:
- Be dependency-free (use Python standard library)
- Include `--help` and `--version` flags
- Support `--dry-run` mode when applicable
- Work cross-platform (Windows/Linux/macOS)
- Follow the Resonance 7 development standards

## License

MIT License - Part of the Resonance 7 development framework.
