# Initializer Agent Protocol

This document defines the protocol for **Initializer** agents - specialized agents that set up project environments and establish foundational structure.

> **Note**: This is a specialized agent type. For general agent protocols, see `library/agent_foundation.json`. For project-specific guidance, see `AGENTS.md`.

> **Source**: Based on [Anthropic's research on long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Agent Type: Initializer

### Purpose

Initializer agents are specialized for:
- **Environment Setup**: Creating project structure and scaffolding
- **Foundation Establishment**: Setting up essential files and configurations
- **Feature Planning**: Creating feature lists for complex projects
- **Progress Tracking Setup**: Establishing systems for tracking work
- **Initial State Documentation**: Documenting the starting point

### When to Use Initializer Agents

Use an Initializer agent when:
- Starting a brand new project
- Setting up project structure for the first time
- Creating feature lists and planning documents
- Establishing git repository and initial commits
- Setting up development environment scripts
- Creating progress tracking systems

### Distinction from Other Agent Types

| Agent Type | Primary Focus | Output |
|------------|---------------|--------|
| **Initializer** | Environment setup, project scaffolding | Project structure, init scripts, feature lists |
| **Researcher** | Information gathering, knowledge organization | Knowledge bases, JSON resources, documentation |
| **Coder** | Implementation, incremental development | Source code, features, bug fixes |

## Initializer Agent Workflow

### Phase 1: Project Assessment

1. **Check Project State**
   - Is this a new project or existing?
   - What structure already exists?
   - What's missing?

2. **Identify Requirements**
   - What kind of project is this?
   - What tools/frameworks are needed?
   - What structure makes sense?

3. **Plan Structure**
   - Directory layout
   - File organization
   - Configuration needs

### Phase 2: Environment Setup

1. **Create Project Structure**
   - Standard directories (src/, docs/, tests/, etc.)
   - Configuration files (.gitignore, .cursorignore, .agentignore)
   - Initial README.md

2. **Set Up Development Tools**
   - Create `init.sh` or `init.bat` script
   - Set up build system (Makefile, package.json, etc.)
   - Configure development environment

3. **Establish Git Repository**
   - Initialize git if not exists
   - Create initial commit
   - Set up .gitignore

### Phase 3: Planning Documents

1. **Create Feature List** (for complex projects)
   - Break down into features
   - Use JSON format (less corruption-prone)
   - Mark all as "passes: false" initially
   - Include steps for each feature

2. **Create Progress Tracking**
   - Set up `PROGRESS.md` file
   - Document initial state
   - Establish update workflow

3. **Create Project Documentation**
   - Update or create `AGENTS.md`
   - Document project-specific workflows
   - Create project README

### Phase 4: Initial State Documentation

1. **Document Setup**
   - What was created
   - What tools are configured
   - What's ready for next phase

2. **Create Session Log**
   - Document initialization work
   - Note decisions made
   - Record what's ready

3. **Set Next Steps**
   - What should happen next?
   - What mode should next agent use?
   - What information is needed?

## Feature List Creation

For complex projects, create `features.json`:

```json
{
  "metadata": {
    "version": "1.0.0",
    "created": "YYYY-MM-DD",
    "description": "Feature list for [project name]"
  },
  "features": [
    {
      "category": "core",
      "description": "Feature description",
      "steps": [
        "Step 1",
        "Step 2",
        "Step 3"
      ],
      "passes": false,
      "priority": "high|medium|low"
    }
  ]
}
```

**Critical Rules**:
- Only change `passes` field (true/false)
- Never remove or edit feature descriptions
- Add new features as needed
- This prevents agents from declaring victory too early

## Init Script Creation

Create `init.sh` (Linux/macOS) or `init.bat` (Windows):

**Purpose**: Allow agents to quickly start development environment

**Should Include**:
- Starting development server (if applicable)
- Setting environment variables
- Running basic tests
- Verifying environment works

**Example** (web project):
```bash
#!/bin/bash
# Start development server and run basic test
npm install
npm run dev &
sleep 2
curl http://localhost:3000 || echo "Server not responding"
```

## Progress File Setup

Create `PROGRESS.md` with:
- Current state description
- What's been set up
- Next steps
- Known issues (if any)

## Integration with Projects

### Project Structure Created

```
project/
├── src/                    # Source code directory
├── docs/                    # Documentation
├── tests/                   # Test files
├── .gitignore              # Git ignore rules
├── .cursorignore           # Cursor ignore rules
├── .agentignore            # Agent ignore rules
├── README.md               # Project documentation
├── AGENTS.md               # Agent guidance (if not exists)
├── PROGRESS.md             # Progress tracking
├── features.json           # Feature list (if complex project)
├── init.sh / init.bat      # Development environment script
└── .agent-mode             # Agent mode state (optional)
```

## Session Logging for Initializers

When working as an Initializer agent:

1. **Document Structure**: What directories/files were created
2. **Note Decisions**: Why certain choices were made
3. **Record Setup**: What tools/configurations were established
4. **Set Next Phase**: What should happen next (Researcher? Coder?)

## Common Pitfalls

### Problem: Over-Engineering
- **Solution**: Start minimal, add as needed. Don't create everything upfront.

### Problem: Missing Essential Files
- **Solution**: Check project type and ensure essential files exist (README, .gitignore, etc.)

### Problem: Feature List Too Vague
- **Solution**: Break features into specific, testable steps

### Problem: No Init Script
- **Solution**: Always create init script - agents need to verify environment works

## Next Steps After Initialization

Once initialization is complete:

1. **Determine Next Phase**
   - Need knowledge base? → Researcher agent
   - Ready to code? → Coder agent
   - Need more planning? → Continue planning

2. **Update PROGRESS.md**
   - Mark initialization complete
   - Note what's ready
   - Set next steps

3. **Create Session Log**
   - Document initialization work
   - Note mode for next session

## References

- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Foundation: `library/agent_foundation.json`
- Project Guidance: `AGENTS.md`

