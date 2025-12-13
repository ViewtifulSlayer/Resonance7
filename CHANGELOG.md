# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2025-12-13

### Changed
- Renamed `library/tools/setup_project.py` to `library/tools/project_setup.py` for better naming consistency
- Reorganized documentation structure:
  - Moved `library/docs/` to `library/resources/docs/` for better resource grouping
  - Updated all references to documentation modules to reflect new location
- Updated project template generation:
  - Template generation now acts as failsafe only (template tracked in git)
  - Function checks if template exists before generating
- Updated command files:
  - Fixed session template path in `.cursor/commands/session.md` to point to `library/templates/documentation_templates/session_template.md`
- Enhanced ignore file patterns:
  - Updated `.cursorignore` to properly handle `library/resources/docs/` and `library/resources/wikis/`
  - Updated `.gitignore` to exclude knowledge base databases while preserving index files
  - Refined patterns to allow markdown index files for discoverability
  - Added exception for `library/resources/README.md` to allow tracking of resources directory README
- Refined agent foundation:
  - Consolidated timestamp format specification (removed redundancy between format and timestamp_accuracy fields)
  - Updated session logging tool reference to correct path

### Added
- Knowledge base database support:
  - Added `library/resources/wikis/` directory for knowledge base databases
  - Created `library/resources/wikis/README.md` with database access documentation
  - Added MCP SQLite Server integration documentation
  - Created `knowledge_base_index.md` template for knowledge base navigation
- Resource organization:
  - Created `library/resources/README.md` as index for shared resources
  - Organized templates into `library/templates/documentation_templates/` and `library/templates/project_template/`
  - Renamed README templates to lowercase (`readme_project.md`, `readme_library.md`, `readme_minimal.md`)
- Minimal READMEs for empty documentation subdirectories (`dev_tools/`, `frameworks/`, `languages/`, `hardware/`)
- Enhanced agent foundation:
  - Added `action_authorization_policy` to distinguish information requests ("check", "review", "could we") from action requests
  - Policy prevents agents from taking unauthorized actions on information-gathering requests

### Fixed
- Fixed template path references in `session_tools.py` to point to correct template location
- Fixed project setup tool to properly reference `project_template` directory
- Fixed all path references to use correct documentation and template locations
- Fixed `.gitignore` to properly exclude knowledge base database files (`.db`, `.sqlite`, `.sqlite3`) from being tracked
- Fixed `.gitignore` to allow `library/resources/README.md` to be tracked (added exception rule)

## [1.2.0] - 2025-11-21

### Added
- `ARCHITECTURE.md` template in workspace template (`library/workspace_template/docs/ARCHITECTURE.md`) - Generic architecture documentation template for future projects with sections for system architecture, data architecture, repository setup, and technical stack documentation

### Changed
- Enhanced `agent_foundation.json` with improved agent behavior guidance:
  - Added `mutual_respect` to core_philosophy - establishes partnership model with complementary strengths
  - Strengthened file creation prohibition - explicitly includes documentation files, analysis files, summary files with only session logs as exception
  - Refined `knowledge_persistence` philosophy - clarified it means using existing resources, not creating new files
  - Enhanced critical friend guidance - added specific criteria for when to challenge (safety, best practices, factual errors) vs. when to follow (preference, style, non-critical)
  - Added confidence language - encourages agents to work confidently within capabilities while maintaining humility
  - Added "When to challenge vs. when to follow" guidance to communication rules
  - Split long documentation rule into separate items for better readability
  - Removed redundant `documentation_principle` from development_protocols (covered in communication rules)
  - Added `timestamp_accuracy` rule to session_logging metadata_rules - explicitly requires getting actual current time via command, prohibits rounding to quarter hours
- Reorganized tools structure for better separation of concerns:
  - Moved universal tools (`session_tools.py`, `setup_workspace.py`) to `library/tools/` - now accessible via `library/` symlink
  - Moved batch launchers (`session_tools.bat`, `setup_workspace.bat`) to `library/tools/` for consistency
  - Projects now get independent `tools/` directories (not symlinked) for project-specific tools
  - Removed `tools/` symlink from shared resources - projects create their own `tools/` directories
  - Root `tools/` directory remains for user-specific tools (excluded from repository via `.git/info/exclude`)
  - Updated `setup_workspace.py` to create independent `tools/` directories in new projects
  - Updated workspace template to include `tools/` directory structure
  - Enhanced template regeneration to preserve `ARCHITECTURE.md` during regeneration
  - Updated workspace template `.gitignore` with symlink notes for clarity
- Updated LICENSE copyright to ViewtifulSlayer

### Fixed
- Fixed typos in `agent_foundation.json`: "collobration" → "collaboration", "well-stuctured" → "well-structured"
- Fixed JSON syntax error in communication array (nested array converted to separate string items)

## [1.1.1] - 2025-11-10

### Added
- README.md for projects directory documenting project creation, structure, and best practices

### Changed
- Removed `projects/.gitkeep` as it's been replaced by README.md

## [1.1.0] - 2025-11-09

### Added
- `.cursorignore` and `.agentignore` templates in workspace template
- Cursor command system (`/foundation`, `/help`, `/start`, `/session`)
- Batch file launchers for Python tools (`session_tools.bat`, `setup_workspace.bat`)
- README.md files in workspace template directories (`docs/`, `src/`, `tests/`)
- README.md files in sessions subdirectories (`current/`, `recent/`, `archived/`)

### Changed
- Enhanced `setup_workspace.py` to automatically create ignore files
- Updated prerequisites to make Python the sole manual requirement
- Improved workspace setup to support file symlinks (not just directories)

### Fixed
- Workspace template directories now tracked in Git (v1.0.0 had missing folders)

## [1.0.0] - 2025-11-09

### Added
- Initial release of Resonance7 framework
- Core workspace template system
- Session management tools (`session_tools.py`)
- Foundation configuration system (`agent_foundation.json`)
- Workspace setup automation (`setup_workspace.py`)
- Shared resource symlinking for projects
- Session lifecycle management (current → recent → archived)
- Cross-platform Python tooling

[Unreleased]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ViewtifulSlayer/Resonance7/releases/tag/v1.0.0

