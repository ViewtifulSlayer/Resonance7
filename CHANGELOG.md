# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2025-12-01

### Added
- Agent type system with three specialized agent types:
  - **Initializer Agent** - Environment setup and project scaffolding (based on Anthropic research)
  - **Coder Agent** - Incremental feature development and implementation
  - **Researcher Agent** - Information gathering and knowledge base population
- `/agents` command for agent type selection and mode switching
- Project-specific agent guidance system:
  - `AGENTS.md` template in workspace template for project-specific agent guidance
  - `PROGRESS.md` template for lightweight quick-context tracking
  - Agent protocols: `INITIALIZER_AGENT.md` and `RESEARCHER_AGENT.md`
- Knowledge base templates:
  - `knowledge_base_template.json` - Template for structured knowledge bases
  - `KNOWLEDGE_BASE_INDEX_TEMPLATE.md` - Template for knowledge base navigation
- Framework documentation in `library/docs/`:
  - `AGENT_ONBOARDING_ANALYSIS.md` - Comprehensive analysis of Anthropic & GitHub patterns
  - `AGENT_ONBOARDING_SUMMARY.md` - Quick reference guide
  - `AGENT_TYPES_PROVENANCE.md` - Documentation of sources and best practices
  - `AGENT_TYPE_ACTIVATION_OPTIONS.md` - Analysis of activation approaches
  - `AGENT_ACTIVATION_IMPLEMENTATION.md` - Implementation guide
  - `INDEX.md` - Navigation guide for framework documentation
- Auto-detection of agent mode based on project state (new project → Initializer, has knowledge_base/ → Researcher, has src/ → Coder)

### Changed
- Enhanced workspace template with agent guidance files:
  - `AGENTS.md` template includes agent type information and "Getting Up to Speed" workflow
  - `PROGRESS.md` template for quick context tracking
  - `.agent-mode.example` template (documentation only - persistence not yet implemented)
- Updated command system with agent type selection capability

### Documentation
- Added comprehensive documentation of agent onboarding patterns from Anthropic and GitHub articles
- Documented what features came from articles vs. extensions
- Created implementation guides for agent type activation
- Added provenance documentation with supporting best practices

### Notes
- Agent mode persistence (`.agent-mode` file) is documented but not yet implemented - currently session-specific
- `/agents` command works via agent following instructions manually (no automated tooling yet)
- All agent type protocols are documentation/guidelines, not automated systems

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

