# Library - Shared Resonance 7 Resources

The `library/` directory contains the core configuration, templates, and shared resources that define the Resonance 7 framework. This directory is symlinked into all projects, making these resources accessible throughout the workspace.

## Core Files

### `agent_foundation.json`
The foundational configuration file that defines:
- Core philosophy and workspace architecture
- Essential agent behavior and ethical standards
- Communication protocols
- Development protocols (web-first, file safety, command execution)
- Session logging configuration

This file is automatically loaded by agents on session start via `.cursor/rules/agent_onboarding.mdc`.

### `session_template.md`
The template structure for session logs. Defines:
- YAML frontmatter format
- Session metadata rules
- Standard sections for tracking progress
- Lifecycle management guidelines

Referenced by `tools/session_tools.py` when creating new session logs.

### `workspace_template/`
Blueprint for new Resonance 7 projects. Contains:
- Standard project structure (src/, docs/, tests/)
- Template configuration files
- README and requirements.txt templates

Can be regenerated using `tools/setup_workspace.py --template` if missing.

## Documentation Modules

### `docs/`
Knowledge base and context modules for agents (see `docs/README.md` for details).

Modules are downloaded on-demand rather than included in the base repository to keep it lean. Organized by:
- `languages/` - Programming language documentation and examples
- `frameworks/` - Framework documentation (Godot, MonoGame, Unity, etc.)
- `hardware/` - Hardware documentation (game consoles, PC architecture, etc.)
- `tools/` - Development tool documentation (rom hacking suites, etc.)
- `subjects/` - Domain-specific knowledge modules

## Integration

The `library/` directory is automatically symlinked into all projects created via `tools/setup_workspace.py`, providing:
- Shared access to Resonance 7 configuration
- Consistent agent behavior across all projects
- Centralized template and resource management
- No duplication of core protocol files

## Purpose

This directory serves as the "brain" of Resonance 7 - containing the foundational rules, templates, and shared knowledge that enable consistent agent behavior and project structure across the entire workspace.

