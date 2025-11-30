# Resonance 7 Workspace Template

This template provides the standard structure for new Resonance7 projects.

## Usage

1. Copy this template to create a new project
2. Rename the directory to your project name
3. Update the README.md and requirements.txt files
4. Start developing!

## Structure

- `src/` - Source code
- `docs/` - Documentation  
- `tests/` - Test files
- `tools/` - Project-specific tools (independent, not symlinked)
- `.gitignore` - Git ignore rules
- `.cursorignore` - Cursor IDE ignore rules
- `.agentignore` - Agent file modification protection rules
- `README.md` - Project documentation
- `requirements.txt` - Python dependencies

## Resonance 7 Integration

This template includes symlinks to shared Resonance7 resources:
- `library/` - Shared Resonance7 resources (including universal tools in `library/tools/`)
- `sessions/` - Shared session management
- `tools/` - Project-specific tools directory (independent, not symlinked)

Universal tools accessible via `library/` symlink:
- `library/tools/session_tools.py` - Session creation and management
- `library/tools/setup_workspace.py` - Workspace setup utility
- `library/tools/session_tools.bat` - Quick launcher for session management
- `library/tools/setup_workspace.bat` - Quick launcher for workspace setup

The `.cursor` configuration is shared from the workspace root level.

## Location

This template is stored in `library/workspace_template/` and serves as the master blueprint for all new Resonance7 projects.
