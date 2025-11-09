# Resonance7 v1.1.0 - Enhanced Workspace Management

**Release Date:** November 9, 2025

This release enhances the Resonance7 framework with improved developer experience, streamlined agent interaction, and fixes for workspace template completeness.

## What's New

### Cursor Command System

- **Cursor command system** - New command interface for streamlined agent interaction:
  - `/foundation` - Load and apply Resonance7 foundation configuration
  - `/help` - Get succinct explanations of Resonance7 topics
  - `/start` - Initialize and verify workspace setup for first-time users
  - `/session` - Automatically create or update session logs from context

### Workspace Template Enhancements

- **Ignore file templates** - New `.cursorignore` and `.agentignore` templates included in workspace template
  - Automatically created for all new projects
  - Includes documentation on parent-level override patterns
  - Improves IDE performance and protects critical files

- **README files in template directories** - Added documentation to `docs/`, `src/`, and `tests/` directories
  - Ensures directories are tracked in Git
  - Provides context and best practices for each directory

- **README files in sessions subdirectories** - Added documentation to `current/`, `recent/`, and `archived/` directories
  - Explains session lifecycle and directory purposes
  - Improves discoverability and understanding

### Developer Experience Improvements

- **Batch file launchers** - Quick access to Python tools from any directory:
  - `session_tools.bat` - Launch session management tool
  - `setup_workspace.bat` - Launch workspace setup tool
  - No need to type full Python paths

- **Enhanced workspace setup** - `setup_workspace.py` improvements:
  - Automatically creates ignore files for new projects
  - Supports file symlinks (not just directories)
  - More robust cross-platform compatibility

### Changes

- **Simplified prerequisites** - Python is now the sole manual requirement
  - Git and IDE installation can be handled via planned app installer system
  - Clearer onboarding path for new users

### Fixes

- **Workspace template directories** - Fixed missing directories in v1.0.0
  - All template directories (`docs/`, `src/`, `tests/`) now tracked in Git
  - Complete template structure available in repository

## Getting Started

If you're upgrading from v1.0.0:

1. **Pull the latest changes:**
   ```bash
   git pull origin main
   ```

2. **Try the new Cursor commands:**
   - In Cursor chat, type `/foundation` to load the agent foundation
   - Use `/help` to learn about Resonance7 features
   - Use `/start` for guided workspace verification

3. **Use batch file launchers:**
   ```bash
   session_tools.bat
   setup_workspace.bat
   ```

If you're new to Resonance7, see the [v1.0.0 release notes](https://github.com/ViewtifulSlayer/Resonance7/releases/tag/v1.0.0) for initial setup instructions.

## Documentation

- **[README.md](README.md)** - Complete framework documentation
- **[CHANGELOG.md](CHANGELOG.md)** - Full changelog history
- **[Library Documentation](library/README.md)** - Core resources and agent foundation
- **[Session Management](sessions/README.md)** - Session logging and lifecycle
- **[Tools Documentation](tools/README.md)** - Available scripts and utilities

## Requirements

- Python 3.7 or higher (sole manual prerequisite)
- Git (can be installed via planned app installer system)
- A compatible IDE (Cursor recommended, but any IDE can be adapted)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Full Changelog:** [v1.0.0...v1.1.0](https://github.com/ViewtifulSlayer/Resonance7/compare/v1.0.0...v1.1.0)
