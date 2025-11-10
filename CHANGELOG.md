# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/ViewtifulSlayer/Resonance7/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ViewtifulSlayer/Resonance7/releases/tag/v1.0.0

