# Resonance7 v1.3.0 - Agent Type System & Enhanced Onboarding

**Release Date:** December 1, 2025

This release introduces a comprehensive agent type system based on research from Anthropic and GitHub, adding specialized agent types, project-specific guidance, and enhanced onboarding capabilities. The framework now supports Initializer, Coder, and Researcher agent types with dedicated protocols and workflows.

## What's New

### Agent Type System

- **Three Specialized Agent Types**:
  - **Initializer Agent** - Sets up project environment, creates scaffolding, establishes feature lists (based on [Anthropic's research](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents))
  - **Coder Agent** - Makes incremental progress, implements features, maintains clean state
  - **Researcher Agent** - Gathers information, verifies data, populates knowledge bases (extension based on best practices)

- **Agent Type Selection**:
  - `/agents` command for interactive agent type selection
  - `/agents [type]` for direct mode switching (initializer, coder, researcher)
  - Auto-detection based on project state (new project → Initializer, has knowledge_base/ → Researcher, has src/ → Coder)
  - Mode-specific protocol loading

### Project-Specific Agent Guidance

- **`AGENTS.md` Template** - Project-specific agent guidance file:
  - Based on [GitHub's agents.md pattern](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
  - Includes project overview, development environment, workflows, and domain knowledge
  - Template automatically copied to new projects
  - Distinguishes from framework-wide `agent_foundation.json`

- **`PROGRESS.md` Template** - Lightweight quick-context tracking:
  - Faster than parsing full session logs
  - Updated at end of each session
  - Provides quick state understanding for agents

### Agent Protocols

- **`INITIALIZER_AGENT.md`** - Complete protocol for initializer agents:
  - Environment setup workflow
  - Feature list creation
  - Init script creation
  - Project scaffolding

- **`CODER_AGENT.md`** - Complete protocol for coder agents:
  - "Getting Up to Speed" workflow (8-step process)
  - Testing protocols (before, during, after)
  - Incremental progress principles
  - Feature list integration
  - Clean state requirements

- **`RESEARCHER_AGENT.md`** - Complete protocol for researcher agents:
  - Information gathering workflow
  - Verification standards
  - Knowledge base organization
  - Source attribution requirements

### Knowledge Base Templates

- **`knowledge_base_template.json`** - Template for structured knowledge bases:
  - Metadata structure
  - Content organization patterns
  - Based on XMBMGMT's excellent knowledge base structure

- **`KNOWLEDGE_BASE_INDEX_TEMPLATE.md`** - Template for knowledge base navigation:
  - Quick reference guides
  - File relationship documentation
  - "I want to..." workflows

### Framework Documentation

Comprehensive documentation added to `library/docs/`:

- **`AGENT_ONBOARDING_ANALYSIS.md`** - Complete analysis of Anthropic & GitHub patterns
- **`AGENT_ONBOARDING_SUMMARY.md`** - Quick reference guide
- **`AGENT_TYPES_PROVENANCE.md`** - What came from articles vs. extensions, with supporting best practices
- **`AGENT_TYPE_ACTIVATION_OPTIONS.md`** - Analysis of 6 different activation approaches
- **`AGENT_ACTIVATION_IMPLEMENTATION.md`** - Implementation guide for `/agents` command
- **`INDEX.md`** - Navigation guide for all framework documentation

## Implementation Status

### Fully Implemented
- ✅ Agent type protocols and documentation (Initializer, Coder, Researcher)
- ✅ `/agents` command (agent follows instructions manually)
- ✅ `AGENTS.md` and `PROGRESS.md` templates
- ✅ Knowledge base templates
- ✅ Auto-detection logic (documented)
- ✅ Comprehensive framework documentation
- ✅ Foundation refactored for universality (workflow-specific elements moved to protocols)

### Documentation Only (Not Yet Implemented)
- ⚠️ `.agent-mode` file persistence - Documented but no automated tooling
- ⚠️ Session start mode loading - Would require Python scripts/session hooks
- ⚠️ Automatic file creation - Currently manual (agent follows instructions)

**Note**: The agent type system works via agents following documented protocols. There's no automated tooling yet - agents read the documentation and follow the instructions manually. This is intentional for Phase 1; automated persistence can be added in Phase 2 if needed.

## Key Features

### Based on Research

- **Anthropic's Findings**: Initializer vs. Coder distinction, feature lists, progress tracking, incremental development
- **GitHub's Pattern**: `agents.md` as project-specific guidance (used in 2500+ repositories)
- **Best Practices**: Knowledge engineering, information architecture, agent specialization

### Extensions

- **Researcher Agent Type**: Extension based on knowledge engineering best practices and the need for systematic knowledge base population
- **Knowledge Base Templates**: Based on XMBMGMT's excellent knowledge base structure
- **Verification Protocols**: Source quality hierarchy and verification standards

## Changes

- Enhanced workspace template with agent guidance files
- Updated command system with `/agents` command
- Added comprehensive framework documentation
- Created agent protocol files for each agent type

## Getting Started

### For New Projects

1. **Create project**: `python library/tools/setup_workspace.py --project my-project`
2. **Customize `AGENTS.md`**: Add project-specific guidance
3. **Select agent type**: Use `/agents [type]` or let auto-detection choose
4. **Start working**: Agent follows appropriate protocols

### For Existing Projects

1. **Add `AGENTS.md`**: Copy from template and customize
2. **Add `PROGRESS.md`**: Create for quick context tracking
3. **Use `/agents` command**: Select appropriate agent type for your work

### Agent Type Selection

```
/agents                    # Show current mode and options
/agents initializer        # Switch to initializer mode
/agents coder              # Switch to coder mode
/agents researcher         # Switch to researcher mode
```

## Documentation

- **[Framework Documentation Index](library/docs/INDEX.md)** - Navigation guide
- **[Agent Onboarding Analysis](library/docs/AGENT_ONBOARDING_ANALYSIS.md)** - Complete analysis
- **[Agent Protocols](library/workspace_template/)** - Initializer, Researcher, and project guidance templates
- **[Commands](.cursor/commands/agents.md)** - Agent type selection command

## Requirements

- Python 3.7 or higher
- Git
- A compatible IDE (Cursor recommended, but any IDE can be adapted)

## Testing

This release is being tested as a branch diverging from main. The agent type system and `AGENTS.md` features are ready for testing. Feedback will guide Phase 2 enhancements (automated persistence, session hooks, etc.).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Full Changelog:** [v1.2.0...v1.3.0](https://github.com/ViewtifulSlayer/Resonance7/compare/v1.2.0...v1.3.0)
