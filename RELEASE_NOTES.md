# Resonance7 v1.3.0 - Enhanced Foundation & Framework Improvements

**Release Date:** December 13, 2025

This release focuses on enhancing the core agent foundation, reorganizing workspace structure, and improving framework documentation and resource management.

## What's New

### Enhanced Agent Foundation

- Added action authorization policy to distinguish information requests from action requests
- Improved agent behavior guidance and partnership model
- Strengthened file creation protocols and knowledge persistence philosophy
- Enhanced development workflows and best practices

### Workspace Reorganization

- **Documentation Structure**: Moved `library/docs/` to `library/resources/docs/` for better resource grouping
- **Knowledge Base Support**: Added `library/resources/wikis/` for knowledge base databases with MCP SQLite Server integration
- **Template Organization**: Organized templates into `library/templates/documentation_templates/` and `library/templates/project_template/`
- **Tool Naming**: Renamed `setup_project.py` to `project_setup.py` for better consistency

### Resource Management

- Enhanced `.cursorignore` and `.gitignore` patterns for better resource management
- Knowledge base databases excluded from indexing while preserving markdown index files for discoverability
- Fixed `.gitignore` to properly exclude knowledge base database files (`.db`, `.sqlite`, `.sqlite3`) from git tracking
- Fixed `.gitignore` to allow `library/resources/README.md` to be tracked (added exception rule)
- Improved template generation (failsafe only, template tracked in git)

## Implementation Status

### Fully Implemented
- ✅ Enhanced agent foundation with action authorization policy
- ✅ Workspace reorganization and resource structure improvements
- ✅ Knowledge base database support with MCP SQLite Server integration
- ✅ Template organization and path fixes
- ✅ Updated command system with correct template paths
- ✅ Fixed `.gitignore` patterns for knowledge base databases

## Key Features

- Enhanced agent foundation with action authorization policy
- Reorganized resource structure for better organization
- Knowledge base database support
- Improved template management
- Better ignore file patterns for resource management

## Changes

- Enhanced agent foundation with action authorization policy
- Reorganized documentation and resource structure
- Added knowledge base database support
- Improved project template structure and generation
- Updated tool naming and path references
- Fixed `.gitignore` to properly exclude knowledge base databases and allow README tracking

## Getting Started

### For New Projects

1. **Create project**: `python library/tools/project_setup.py --project my-project`
2. **Start working**: Agents follow the universal foundation protocols

### For Existing Projects

Continue using the enhanced agent foundation for consistent behavior across all projects.

## Documentation

- **[Library Documentation](library/README.md)** - Core resources and agent foundation
- **[Documentation Modules](library/resources/docs/README.md)** - Knowledge base organization
- **[Knowledge Bases](library/resources/wikis/README.md)** - Database access and knowledge bases

## Requirements

- Python 3.7 or higher
- Git
- A compatible IDE (Cursor recommended, but any IDE can be adapted)

## Testing

This release is being tested as a branch diverging from main. Enhanced foundation features are ready for testing.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Full Changelog:** [v1.2.0...v1.3.0](https://github.com/ViewtifulSlayer/Resonance7/compare/v1.2.0...v1.3.0)
