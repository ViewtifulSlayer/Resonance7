# Resonance 7 Agent System: Complete Reference

**Single source of truth for agent types, onboarding, and activation**

**Sources**: 
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [GitHub: How to Write a Great agents.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)

---

## Executive Summary

Resonance 7 implements a three-agent-type system based on Anthropic's research and GitHub's agents.md pattern. The framework supports **Initializer**, **Coder**, and **Researcher** agent types with project-specific guidance via `AGENTS.md` files.

**Key Components**:
- Framework-wide foundation: `agent_foundation.json`
- Project-specific guidance: `AGENTS.md` (per project)
- Quick context: `PROGRESS.md` (per project)
- Agent type selection: `/agents` command
- Specialized protocols: `INITIALIZER_AGENT.md`, `RESEARCHER_AGENT.md`

---

## Agent Types

### Initializer Agent
**Source**: Directly from Anthropic article

**Purpose**: First session setup, environment scaffolding

**When to Use**: New project, setting up structure, creating feature lists

**Workflow**:
1. Assess project state and requirements
2. Create project structure (src/, docs/, tests/, etc.)
3. Set up development tools (init scripts, build system)
4. Create feature list (if complex project)
5. Set up progress tracking (`PROGRESS.md`)
6. Establish git structure and initial commit
7. Document current state

**Output**: Project scaffolding, init scripts, feature lists, initial git setup

**Protocol File**: `library/workspace_template/INITIALIZER_AGENT.md`

### Coder Agent
**Source**: Directly from Anthropic article

**Purpose**: Incremental feature development and implementation

**When to Use**: Subsequent sessions, implementing features, fixing bugs

**Workflow**:
1. Read progress files and git history
2. Check feature list (if exists)
3. Verify current state works (run init script, test)
4. Make incremental progress on one feature
5. Test changes
6. Leave clean state with git commits
7. Update progress file

**Output**: Source code, features, bug fixes, incremental progress

**Protocol**: Documented in Anthropic article patterns (incremental development, progress tracking)

### Researcher Agent
**Source**: Extension based on best practices (not directly from articles)

**Purpose**: Information gathering and knowledge base population

**When to Use**: Populating knowledge bases, gathering domain knowledge, creating structured resources

**Workflow**:
1. **Information Gathering**: Identify needs, collect from multiple sources with URLs
2. **Verification**: Cross-reference sources, verify accuracy, document uncertainties
3. **Organization**: Structure into JSON knowledge bases (main + specialized modules)
4. **Documentation**: Add metadata, create index file, document all sources

**Output**: JSON knowledge bases, structured documentation, verified data

**Protocol File**: `library/workspace_template/RESEARCHER_AGENT.md`

**Supporting Best Practices**:
- Knowledge engineering (established discipline)
- Information architecture principles
- Data quality assurance
- Hierarchical task decomposition

---

## Project-Specific Guidance: AGENTS.md

**Pattern**: Based on GitHub's agents.md (used in 2500+ repositories)

**Purpose**: Project context, workflows, domain knowledge (separate from framework-wide foundation)

**Key Distinction**:
- `agent_foundation.json` = Framework-wide, universal protocols
- `AGENTS.md` = Project-specific guidance

**What It Contains**:
- Project overview and goals
- Development environment setup
- Build system and tools
- Common workflows
- Project-specific conventions
- Known pitfalls and solutions
- Testing procedures
- File organization principles
- Domain-specific knowledge
- "Getting Up to Speed" workflow

**Template**: `library/workspace_template/AGENTS.md`

**Naming Variations**: `agents.md`, `AGENTS.md`, `agent.md` (all valid)

---

## Agent Type Activation

### `/agents` Command

**Location**: `.cursor/commands/agents.md`

**Usage**:
```
/agents                    # Show current mode and options
/agents initializer        # Switch to initializer mode
/agents coder              # Switch to coder mode
/agents researcher         # Switch to researcher mode
```

**Behavior**:
- If no type specified: Shows current mode and available types
- If type specified: Loads appropriate protocol file and switches mode
- Auto-detects mode if no explicit selection

### Auto-Detection Logic

If no explicit mode set:
- New project (no `src/`, no `knowledge_base/`) → **Initializer**
- Has `knowledge_base/` but no `src/` → **Researcher**
- Has `src/` with code → **Coder**
- Default → **Coder**

### Implementation Status

**Current**: Documentation only - agents follow instructions manually
- `/agents` command works (agent reads documentation)
- Mode is session-specific (doesn't persist automatically)
- No automated tooling yet

**Future (Phase 2)**: Optional persistence via `.agent-mode` file
- `.agent-mode.example` template exists (documentation only)
- Would require Python scripts/session hooks to implement
- Not yet implemented

---

## Supporting Files

### PROGRESS.md
**Purpose**: Lightweight quick-context file (faster than parsing full session logs)

**Contains**: Last work done, current state, next steps, known issues

**Location**: Project root (`projects/{project}/PROGRESS.md`)

**Template**: `library/workspace_template/PROGRESS.md`

### features.json (Optional)
**Purpose**: Feature tracking for complex projects

**Prevents**: Agents declaring victory too early, losing track of progress

**Format**: JSON with `passes` field (true/false)

**Rule**: Only change `passes` field - never remove or edit feature descriptions

**Location**: Project root (optional, for complex projects)

### init.sh / init.bat
**Purpose**: Start development environment quickly

**Contains**: Commands to start dev server, set environment variables, run basic tests

**Location**: Project root

---

## Knowledge Base System

### Structure (Based on XMBMGMT Example)

```
docs/knowledge_base/
├── main_knowledge_base.json      # Core knowledge, overview
├── specialized_module1.json      # Focused topic 1
├── specialized_module2.json      # Focused topic 2
├── examples.json                 # Practical examples
└── KNOWLEDGE_BASE_INDEX.md       # Navigation guide
```

### Templates
- `knowledge_base_template.json` - Main knowledge base structure
- `KNOWLEDGE_BASE_INDEX_TEMPLATE.md` - Index file template

### Principles
1. **Modular**: Break into specialized modules, not one large file
2. **Verifiable**: Only include information that can be verified
3. **Attributed**: Always cite sources with URLs
4. **Versioned**: Include version numbers and update dates
5. **Indexed**: Create index file for easy navigation

---

## Provenance: What Came From Where

### Directly from Articles

**Anthropic Article**:
- ✅ Initializer vs. Coder distinction
- ✅ Feature list tracking
- ✅ Progress files (`claude-progress.txt` pattern)
- ✅ "Getting up to speed" workflow
- ✅ Incremental development approach
- ✅ Testing protocols

**GitHub Article**:
- ✅ `agents.md` as project-specific guidance pattern
- ✅ Structure and content recommendations
- ✅ Best practices from 2500+ repositories

### Extensions (Supported by Best Practices)

**Researcher Agent Type**:
- ⚠️ Extension based on knowledge engineering principles
- ⚠️ Supported by: Hierarchical task decomposition, modular architecture, data quality assurance
- ⚠️ Practical need: XMBMGMT's knowledge base population

**Knowledge Base Structure**:
- ⚠️ Based on XMBMGMT example + information architecture principles
- ⚠️ Modular organization, cross-referencing, indexing

**Verification Protocols**:
- ⚠️ Based on knowledge engineering + data quality best practices
- ⚠️ Source hierarchy (primary > secondary > tertiary)

---

## File Type Summary

| File Type | Purpose | Scope | Location |
|-----------|---------|-------|----------|
| `agent_foundation.json` | Framework-wide protocols | All projects | `library/` |
| `AGENTS.md` | Project-specific guidance | Single project | `projects/{project}/` |
| `PROGRESS.md` | Quick context for agents | Single project | `projects/{project}/` |
| `features.json` | Feature tracking (optional) | Complex projects | `projects/{project}/` |
| `init.sh` / `init.bat` | Environment setup | Single project | `projects/{project}/` |
| `INITIALIZER_AGENT.md` | Initializer protocol | All projects | `library/workspace_template/` |
| `RESEARCHER_AGENT.md` | Researcher protocol | All projects | `library/workspace_template/` |
| Knowledge base JSONs | Structured domain knowledge | Single project | `projects/{project}/docs/knowledge_base/` |
| Session logs | Detailed work history | All projects | `sessions/current/` |

---

## "Getting Up to Speed" Workflow

Agents should start each session with:

1. **Check Working Directory**: Run `pwd` to see where you are
2. **Read Progress File**: Read `PROGRESS.md` (if exists) for quick context
3. **Read Recent Session Logs**: Check `sessions/current/` for recent work
4. **Check Git History**: Run `git log --oneline -20` to see recent commits
5. **Read Feature List**: If `features.json` exists, review what's complete/incomplete
6. **Check Knowledge Bases**: If `docs/knowledge_base/` exists, review for domain knowledge
7. **Initialize Environment**: Run init script (`init.sh` or `init.bat`) if available
8. **Test Current State**: Verify existing functionality works before adding new features

---

## Implementation Status

### Fully Implemented
- ✅ Agent type protocols and documentation
- ✅ `/agents` command (agent follows instructions manually)
- ✅ `AGENTS.md` and `PROGRESS.md` templates
- ✅ Knowledge base templates
- ✅ Auto-detection logic (documented)
- ✅ Comprehensive framework documentation

### Documentation Only (Not Yet Implemented)
- ⚠️ `.agent-mode` file persistence - Documented but no automated tooling
- ⚠️ Session start mode loading - Would require Python scripts/session hooks
- ⚠️ Automatic file creation - Currently manual (agent follows instructions)

**Note**: The agent type system works via agents following documented protocols. There's no automated tooling yet - agents read the documentation and follow the instructions manually. This is intentional for Phase 1; automated persistence can be added in Phase 2 if needed.

---

## References

### Articles
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [GitHub: How to Write a Great agents.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)

### Best Practices Supporting Extensions
- [Google Cloud: Agentic AI System Design Patterns](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
- [Leanware: AI Agent Architecture](https://www.leanware.co/insights/ai-agent-architecture)
- Knowledge Engineering (established discipline, 1980s-present)
- Information Architecture (established discipline)

---

## Quick Reference

**Select Agent Type**: `/agents [type]` (initializer, coder, researcher)

**Project Guidance**: Create `AGENTS.md` in project root

**Quick Context**: Create `PROGRESS.md` in project root

**Protocol Files**: `library/workspace_template/INITIALIZER_AGENT.md`, `RESEARCHER_AGENT.md`

**Command Reference**: `.cursor/commands/agents.md`

