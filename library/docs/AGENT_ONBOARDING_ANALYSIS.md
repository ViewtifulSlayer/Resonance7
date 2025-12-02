# Agent Onboarding Analysis: Anthropic & GitHub Patterns

**Date**: 2025-12-01  
**Sources**: 
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [GitHub: How to Write a Great agents.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)

## Executive Summary

After analyzing both articles and comparing them to the current Resonance 7 framework, several key components are missing that would significantly improve agent effectiveness across multiple context windows. The primary gap is **project-specific agent guidance** separate from the framework-wide foundation.

## Key Findings

### 1. `agents.md` is Both a Pattern AND a File Name

**Answer to Question B**: `agents.md` (or `AGENTS.md`, `agent.md`) is a **convention/pattern** that has become a standard file name, similar to `README.md`. The GitHub article shows it's used across 2500+ repositories as a project-specific guidance file.

**Key Distinction**:
- **`agent_foundation.json`** (Resonance 7): Framework-wide, universal protocols
- **`agents.md`** (Project-specific): Project context, workflows, domain knowledge, project-specific rules

**Naming Variations Observed**:
- `agents.md` (most common)
- `AGENTS.md` (your existing example in `iog_relocalized`)
- `agent.md` (less common)
- `.github/agents.md` (GitHub-specific location)

### 2. Missing Components for Better Agent Onboarding

#### A. Project-Specific Agent Guidance File (`agents.md`)

**Current State**: 
- ✅ Framework foundation exists (`agent_foundation.json`)
- ✅ One example exists (`projects/iog_relocalized/AGENTS.md`)
- ❌ Not standardized across projects
- ❌ No template for creating new ones

**What It Should Contain** (based on GitHub article + Anthropic patterns):
- Project overview and goals
- Development environment setup
- Build system and tools
- Common workflows
- Project-specific conventions
- Known pitfalls and solutions
- Testing procedures
- File organization principles
- Domain-specific knowledge

**Recommendation**: Create `library/workspace_template/AGENTS.md` template that gets copied to new projects.

#### B. Initializer vs. Coding Agent Distinction

**Anthropic Finding**: The first agent session should have a **different prompt** that sets up the environment, while subsequent sessions focus on incremental progress.

**Current State**: 
- ❌ No distinction between first session and subsequent sessions
- ❌ No "environment setup" phase

**What's Missing**:
1. **Initializer Agent Prompt** (first session):
   - Create feature list (if complex project)
   - Set up progress tracking file
   - Create init scripts
   - Establish git structure
   - Document current state

2. **Coding Agent Prompt** (subsequent sessions):
   - Read progress files
   - Check git history
   - Verify current state
   - Make incremental progress
   - Leave clean state

**Recommendation**: Add to `agent_foundation.json` or create separate `initializer_prompt.md` and `coding_prompt.md` templates.

#### C. Feature List Tracking (for Complex Projects)

**Anthropic Finding**: For complex projects, maintain a JSON file listing all features with pass/fail status. Prevents agents from:
- Declaring victory too early
- Trying to one-shot the entire project
- Losing track of what's complete

**Current State**: 
- ❌ No feature tracking system
- ✅ Session logs track progress, but not in structured feature format

**Recommendation**: 
- Add optional `features.json` template for complex projects
- Include in `agents.md` when applicable
- Use JSON format (less likely to be corrupted by agents)

**Example Structure**:
```json
{
  "features": [
    {
      "category": "core",
      "description": "XML parsing and modification",
      "steps": ["Parse XMB XML", "Identify toggleable elements", "Apply comment-based toggles"],
      "passes": false
    }
  ]
}
```

#### D. Progress Tracking Files (Beyond Session Logs)

**Anthropic Finding**: A dedicated `claude-progress.txt` (or similar) file that agents read at session start provides quick context without parsing full session logs.

**Current State**: 
- ✅ Session logs exist (`sessions/current/YYYYMMDD-NN.md`)
- ❌ No lightweight progress file for quick context
- ❌ Agents must read full session logs to understand state

**Recommendation**: 
- Add optional `PROGRESS.md` or `progress.txt` in project root
- Updated by agents at end of each session
- Contains: last work done, current state, next steps, known issues
- Much shorter than full session log

#### E. Init Scripts and "Getting Up to Speed" Workflow

**Anthropic Finding**: Agents should start each session with:
1. Run `pwd` to see working directory
2. Read git logs and progress files
3. Read feature list (if exists)
4. Run init script to start dev environment
5. Test basic functionality before starting new work

**Current State**: 
- ❌ No standardized "getting up to speed" workflow
- ❌ No init scripts guidance
- ❌ No testing-before-starting protocol

**Recommendation**: 
- Add to `agents.md` template: "Getting Up to Speed" section
- Include init script examples (`init.sh`, `init.bat`)
- Document testing procedures

#### F. Testing and Verification Protocols

**Anthropic Finding**: Agents often mark features complete without proper end-to-end testing. Explicit testing protocols dramatically improve quality.

**Current State**: 
- ❌ No explicit testing requirements in foundation
- ❌ No verification protocols

**Recommendation**: 
- Add testing section to `agents.md` template
- Include: build testing, functional testing, end-to-end verification
- Require agents to verify existing functionality before adding new features

## Recommended Implementation Plan

### Phase 1: Project-Specific Agent Files

1. **Create `library/workspace_template/AGENTS.md`** template
   - Based on GitHub article best practices
   - Include sections from Anthropic findings
   - Project-agnostic structure

2. **Update `setup_workspace.py`**
   - Copy `AGENTS.md` template to new projects
   - Pre-populate with project name and basic structure

3. **Create `XMBMGMT/AGENTS.md`**
   - Use template as starting point
   - Document XMB-specific workflows
   - Include PSDK3v2 setup
   - Document XML modification patterns

### Phase 1.5: Researcher Agent Type (NEW)

1. **Create `library/workspace_template/RESEARCHER_AGENT.md`** protocol
   - Define Researcher/Knowledge Engineer agent type
   - Information gathering and verification protocols
   - Knowledge base structure templates
   - Integration with project knowledge bases

2. **Create Knowledge Base Templates**
   - `knowledge_base_template.json` - Main knowledge base structure
   - `KNOWLEDGE_BASE_INDEX_TEMPLATE.md` - Index file template
   - Based on XMBMGMT's excellent knowledge base structure

3. **Document Researcher Workflow**
   - Phase 1: Information Gathering
   - Phase 2: Verification & Validation
   - Phase 3: Organization & Structuring
   - Phase 4: Documentation & Metadata

### Phase 2: Enhanced Onboarding Workflow

1. **Add "Getting Up to Speed" Protocol**
   - Document in `agent_foundation.json` or `AGENTS.md` template
   - Standard steps: pwd, read progress, read features, init, test

2. **Create Progress Tracking File Template**
   - `PROGRESS.md` template
   - Lightweight format for quick context

3. **Add Agent Type Distinctions**
   - **Initializer**: First session, environment setup
   - **Researcher**: Information gathering, knowledge base population
   - **Coder**: Subsequent sessions, incremental development
   - Document in foundation or separate protocol files

### Phase 3: Feature Tracking (Optional, for Complex Projects)

1. **Create `features.json` Template**
   - For projects with multiple features/components
   - JSON format (less corruption-prone)
   - Include in `AGENTS.md` when applicable

2. **Document Feature Tracking Workflow**
   - When to create feature list
   - How to update (only change `passes` field)
   - Integration with session logs

## File Type Summary

| File Type | Purpose | Scope | Location |
|-----------|----------|-------|----------|
| `agent_foundation.json` | Framework-wide protocols | All projects | `library/` |
| `agents.md` | Project-specific guidance | Single project | `projects/{project}/` |
| `PROGRESS.md` | Quick context for agents | Single project | `projects/{project}/` |
| `features.json` | Feature tracking (optional) | Complex projects | `projects/{project}/` |
| `init.sh` / `init.bat` | Environment setup | Single project | `projects/{project}/` |
| `RESEARCHER_AGENT.md` | Researcher agent protocol | All projects | `library/workspace_template/` |
| Knowledge base JSONs | Structured domain knowledge | Single project | `projects/{project}/docs/knowledge_base/` |
| Session logs | Detailed work history | All projects | `sessions/current/` |

## Integration with Existing Resonance 7

### What Already Works Well

1. ✅ **Session Logging System**: Comprehensive, well-structured
2. ✅ **Foundation JSON**: Solid framework-wide protocols
3. ✅ **Command System**: Good user-triggered commands
4. ✅ **Auto-loading Rules**: `.cursor/rules/agent_onboarding.mdc` works

### What Needs Enhancement

1. ⚠️ **Project-Specific Context**: Add `AGENTS.md` per project
2. ⚠️ **Quick Context**: Add lightweight `PROGRESS.md` files
3. ⚠️ **Session Start Workflow**: Standardize "getting up to speed" steps
4. ⚠️ **Initializer Phase**: Distinguish first session from subsequent

## Next Steps

1. **Immediate**: Create `XMBMGMT/AGENTS.md` for this project
2. **Short-term**: Create `library/workspace_template/AGENTS.md` template
3. **Medium-term**: Add progress tracking and init script guidance
4. **Long-term**: Consider feature tracking for complex projects

## References

- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [GitHub: How to Write a Great agents.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- Existing example: `projects/iog_relocalized/AGENTS.md`

