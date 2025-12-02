# Agent Type Selection

Select or view the current agent type mode (Initializer, Coder, or Researcher).

## Action

When this command is invoked:

**If no type specified (`/agents`):**
1. Check for existing agent mode (from `.agent-mode` file if exists, or auto-detect)
2. Display current mode and brief description
3. Show available agent types with descriptions
4. Offer to switch modes if user wants

**If type specified (`/agents [type]`):**
1. Validate the agent type (initializer, coder, researcher)
2. Load the appropriate protocol file:
   - Initializer: `library/workspace_template/INITIALIZER_AGENT.md` (if exists) or initializer protocols
   - Coder: Coder protocols (incremental development, progress tracking)
   - Researcher: `library/workspace_template/RESEARCHER_AGENT.md`
3. Optionally create/update `.agent-mode` file in project root for persistence
4. Acknowledge mode switch with summary of active protocols
5. Report what the agent will focus on in this mode

## Available Agent Types

### Initializer
- **Purpose**: First session setup, environment scaffolding
- **When to Use**: New project, setting up structure, creating feature lists
- **Focus**: Project structure, init scripts, feature lists, initial git setup
- **Output**: Project scaffolding, environment configuration

### Coder
- **Purpose**: Incremental feature development and implementation
- **When to Use**: Subsequent sessions, implementing features, fixing bugs
- **Focus**: Incremental progress, clean state, testing, git commits
- **Output**: Source code, features, bug fixes

### Researcher
- **Purpose**: Information gathering and knowledge base population
- **When to Use**: Populating knowledge bases, gathering domain knowledge, creating structured resources
- **Focus**: Information gathering, verification, organization, documentation
- **Output**: JSON knowledge bases, structured documentation, verified data

## Usage Examples

```
/agents
→ Shows current mode and available types

/agents coder
→ Switches to coder mode, loads protocols

/agents researcher
→ Switches to researcher mode, loads researcher protocols

/agents initializer
→ Switches to initializer mode, loads initializer protocols
```

## Mode-Specific Behaviors

### Initializer Mode
- Reads project state to determine what needs setup
- Creates feature lists (if complex project)
- Sets up progress tracking files
- Creates init scripts
- Establishes git structure
- Documents current state

### Coder Mode
- Reads progress files and git history
- Checks feature list (if exists)
- Verifies current state works
- Makes incremental progress
- Leaves clean state with commits
- Tests before starting new work

### Researcher Mode
- Identifies information needs
- Gathers from multiple sources with URLs
- Verifies through cross-referencing
- Organizes into structured formats (JSON)
- Creates knowledge base modules
- Documents sources and metadata

## Persistence

If `.agent-mode` file exists in project root:
- Agent reads it on session start
- Mode persists across sessions
- Can be version controlled
- Project-specific (each project can have different mode)

If no `.agent-mode` file:
- Agent auto-detects based on project state:
  - New project (no src/, no knowledge_base/) → Initializer
  - Has knowledge_base/ but no src/ → Researcher
  - Has src/ with code → Coder
  - Default → Coder

## When to Use

- **Start of session**: Select appropriate mode for the work ahead
- **Switching tasks**: Change mode when moving between research, setup, and coding
- **Checking mode**: Use `/agents` to see current mode and what it means
- **New project**: Use `/agents initializer` for first session

## Integration

- Works with `AGENTS.md` (project-specific guidance)
- Works with `PROGRESS.md` (quick context)
- Works with session logs (mode can be logged)
- Works with foundation (loads foundation first, then mode-specific protocols)

## Notes

- Mode selection is project-specific (stored in project root)
- Can switch modes mid-session if needed
- Foundation protocols always load first, then mode-specific protocols
- Mode affects agent behavior and focus, not core ethics/communication

