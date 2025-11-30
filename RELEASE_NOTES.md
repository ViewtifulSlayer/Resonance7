# Resonance7 v1.2.0 - Tools Reorganization & Enhanced Foundation

**Release Date:** November 30, 2025

This release introduces a major reorganization of the tools structure for better separation of concerns, enhances the agent foundation with improved behavior guidance, and adds architecture documentation templates. The framework is now more modular and maintainable.

## What's New

### Tools Structure Reorganization

- **Universal tools moved to `library/tools/`** - Framework tools are now centralized:
  - `session_tools.py` - Session creation and management
  - `setup_workspace.py` - Workspace setup and template management
  - `session_tools.bat` - Quick launcher for session management
  - `setup_workspace.bat` - Quick launcher for workspace setup
  - All accessible via the `library/` symlink in projects

- **Independent project tools directories** - Projects now get their own `tools/` directories:
  - No longer symlinked to root `tools/`
  - Each project can have project-specific tools and scripts
  - Better separation between framework tools and project tools
  - Universal tools remain accessible via `library/tools/`

- **Migration support** - Existing projects can be migrated using the migration script (now removed after migration completion)

### Architecture Documentation Template

- **`ARCHITECTURE.md` template** - New template in workspace template (`library/workspace_template/docs/ARCHITECTURE.md`):
  - Generic architecture documentation template for future projects
  - Sections for system architecture, data architecture, repository setup, and technical stack
  - Automatically preserved during template regeneration
  - Helps maintain consistent architecture documentation across projects

### Enhanced Agent Foundation

- **Improved behavior guidance** - Enhanced `agent_foundation.json` with:
  - **Mutual respect partnership model** - Establishes complementary strengths between human and AI
  - **Strengthened file creation protocols** - Explicitly prohibits documentation, analysis, and summary files (session logs remain exception)
  - **Refined knowledge persistence** - Clarified to mean using existing resources, not creating new files
  - **Enhanced critical friend guidance** - Specific criteria for when to challenge (safety, best practices, factual errors) vs. when to follow (preference, style, non-critical)
  - **Confidence language** - Encourages agents to work confidently within capabilities while maintaining humility
  - **Timestamp accuracy requirements** - Explicitly requires getting actual current time via command, prohibits rounding to quarter hours

### Workspace Template Completeness

- **Complete template structure** - Workspace template now includes full directory structure with READMEs:
  - `src/README.md` - Source code directory documentation
  - `tests/README.md` - Test directory documentation
  - `tools/README.md` - Project-specific tools documentation
  - All directories preserved in repository (no regeneration needed)
  - Template regeneration preserves all READMEs and `ARCHITECTURE.md`

### Session Directory Documentation

- **README files in session directories** - Added documentation to preserve empty directories:
  - `sessions/current/README.md` - Active sessions documentation
  - `sessions/recent/README.md` - Recent sessions documentation
  - `sessions/archived/README.md` - Archived sessions documentation (already existed)
  - Directories now tracked in Git with functional documentation (better than `.gitkeep` files)

## Changes

- **Updated LICENSE copyright** - Changed to ViewtifulSlayer
- **Updated `.gitignore`** - Fixed patterns to preserve README files in session directories
- **Enhanced `setup_workspace.py`** - Now preserves directory READMEs and `ARCHITECTURE.md` during template regeneration
- **Updated workspace template** - Version marked as 1.2.0 in template README

## Fixes

- **Fixed typos in `agent_foundation.json`**:
  - "collobration" → "collaboration"
  - "well-stuctured" → "well-structured"
- **Fixed JSON syntax error** - Nested array in communication rules converted to separate string items

## Getting Started

If you're upgrading from v1.1.x:

1. **Pull the latest changes:**
   ```bash
   git pull origin main
   ```

2. **Update tool paths** - Universal tools are now in `library/tools/`:
   ```bash
   # Old (still works via symlink, but direct path is clearer)
   python tools/session_tools.py
   
   # New (recommended)
   python library/tools/session_tools.py
   ```

3. **Migrate existing projects** (if needed):
   - Existing projects with symlinked `tools/` directories should be migrated
   - Migration script was available but has been removed after completion
   - Manual migration: Remove symlink, create independent `tools/` directory
   - Copy project-specific files from root `tools/` to project `tools/` as needed

4. **Use the new architecture template**:
   - New projects include `ARCHITECTURE.md` template in `docs/`
   - Customize it for your project's architecture documentation needs

If you're new to Resonance7, see the [v1.0.0 release notes](https://github.com/ViewtifulSlayer/Resonance7/releases/tag/v1.0.0) for initial setup instructions.

## Documentation

- **[README.md](README.md)** - Complete framework documentation
- **[CHANGELOG.md](CHANGELOG.md)** - Full changelog history
- **[Library Documentation](library/README.md)** - Core resources and agent foundation
- **[Session Management](sessions/README.md)** - Session logging and lifecycle
- **[Tools Documentation](library/tools/README.md)** - Available scripts and utilities
- **[Workspace Template](library/workspace_template/README.md)** - Project template structure

## Requirements

- Python 3.7 or higher
- Git
- A compatible IDE (Cursor recommended, but any IDE can be adapted)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Full Changelog:** [v1.1.1...v1.2.0](https://github.com/ViewtifulSlayer/Resonance7/compare/v1.1.1...v1.2.0)
