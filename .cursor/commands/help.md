# Resonance 7 Help

Provide succinct and clear explanations of Resonance7 topics and features.

## Action

When this command is invoked:
1. Ask the user what Resonance7 topic they need help with, OR
2. If a specific topic is mentioned, provide a clear, concise explanation

Be ready to explain:
- Workspace structure and architecture
- How symlinks work in projects
- Available tools and their usage
- Session management system
- Installer scripts (when implemented)
- Ignore files (.gitignore, .cursorignore, .agentignore)
- Project creation and setup
- Any other Resonance7 concepts

## Explanation Style

- **Succinct**: Get to the point quickly
- **Clear**: Use simple, direct language
- **Practical**: Focus on what users need to know to use the feature
- **Contextual**: Reference actual files and paths in the workspace
- **Examples**: Include brief usage examples when helpful

## Common Topics

**Workspace Structure:**
- Explain the directory layout (library/, sessions/, tools/, projects/)
- How shared resources are organized
- Project workspace structure

**Symlinks:**
- How symlinks connect projects to shared resources
- What gets symlinked (library, sessions, tools, .cursor, batch files)
- Platform differences (Windows vs Linux/macOS)
- Why symlinks are used (single source of truth, consistency)

**Tools:**
- `session_tools.py` - Session management and logging
- `project_setup.py` - Project workspace creation
- How to run tools from any project directory

**Session Management:**
- How sessions are created and tracked
- Session lifecycle (current → recent → archived)
- Session file naming and structure
- Pruning and maintenance

**Configuration Files:**
- `.gitignore` - Git version control exclusions
- `.cursorignore` - Cursor IDE indexing exclusions
- `.agentignore` - Agent file modification protection
- How ignore patterns cascade from parent directories
- Using `!` to override parent-level ignores

**Project Setup:**
- Creating new projects with `project_setup.py`
- What gets created automatically
- Shared resource symlinking
- Configuration file generation

## When to Use

- When users ask "How does X work?" about Resonance7
- When explaining workspace concepts
- When users need clarification on tools or features
- When onboarding new users to the framework

