# AGENTS.md

This file provides context and instructions for AI coding agents working on this project.

> **Note**: This file is project-specific guidance. For framework-wide protocols, see `library/agent_foundation.json`.

## Project Overview

[Brief description of what this project does, its goals, and key technologies]

**Key Repository/Resources**: [URLs or paths to important resources]

## Development Environment

### Workspace Structure

[Describe the project directory structure and where key files are located]

### Prerequisites

- [List required tools, SDKs, libraries, etc.]
- [Version requirements if applicable]

### Build System

[Describe how to build the project]
- **Build Command**: [e.g., `make`, `npm build`, `python setup.py`]
- **Output Location**: [Where built artifacts go]
- **Dependencies**: [How to install dependencies]

### Development Setup

1. [Step-by-step setup instructions]
2. [Environment variables needed]
3. [Configuration files to create/modify]

## Agent Types

This project may use different agent types depending on the task:

- **Initializer Agent**: First session - sets up environment, creates feature lists, establishes project structure
- **Researcher Agent**: Information gathering - populates knowledge bases, creates structured resources (see `library/workspace_template/RESEARCHER_AGENT.md`)
- **Coder Agent**: Implementation - makes incremental progress, implements features, fixes bugs

## Getting Up to Speed (For Agents)

When starting a new session, follow these steps to understand the current state:

1. **Check Working Directory**: Run `pwd` to see where you are
2. **Read Progress File**: Read `PROGRESS.md` (if it exists) for quick context
3. **Read Recent Session Logs**: Check `sessions/current/` for recent work
4. **Check Git History**: Run `git log --oneline -20` to see recent commits
5. **Read Feature List**: If `features.json` exists, review what's complete/incomplete
6. **Check Knowledge Bases**: If `docs/knowledge_base/` exists, review for domain knowledge
7. **Initialize Environment**: Run init script (`init.sh` or `init.bat`) if available
8. **Test Current State**: Verify existing functionality works before adding new features

## Collaborative Workflow

### Core Principles

1. [Project-specific principle 1]
2. [Project-specific principle 2]
3. [User preferences or working style]

### User Preferences

- [Document any specific user preferences for this project]
- [Communication style, documentation preferences, etc.]

## Development Methodology

### [Domain-Specific Methodology]

[Describe any specific approaches, patterns, or methodologies used in this project]

### Common Patterns

[Document common code patterns, conventions, or idioms used in this project]

## File Organization

### Key Directories

- `src/` - [Purpose]
- `docs/` - [Purpose]
- `tests/` - [Purpose]
- `tools/` - [Purpose]

### Important Files

- [List key files and their purposes]

## Common Pitfalls & Solutions

### Problem: [Common Issue]
- **Cause**: [Why it happens]
- **Solution**: [How to fix it]

### Problem: [Another Common Issue]
- **Cause**: [Why it happens]
- **Solution**: [How to fix it]

## Testing & Validation

### Build Testing

1. [How to test builds]
2. [What to check for]

### Functional Testing

1. [How to test functionality]
2. [Test procedures]

### End-to-End Testing

1. [How to verify complete workflows]
2. [Integration testing procedures]

## Workflow Tips

1. [Tip 1]
2. [Tip 2]
3. [Tip 3]

## Session Logging

- **Location**: `sessions/current/YYYYMMDD-NN.md`
- **Update When**: Adding sections, completing work, adding files
- **Don't Update For**: Typos, formatting, grammar fixes
- **Tool**: Use `library/tools/session_tools.py` or update manually

## Key Resources

- [Resource 1] - [Description]
- [Resource 2] - [Description]
- [External documentation or references]

## Feature Tracking (If Applicable)

For complex projects, see `features.json` for a structured list of features and their completion status. Only update the `passes` field - do not remove or edit feature descriptions.

