# Agent Types Expansion: Researcher Agent

**Date**: 2025-12-01  
**Context**: Expansion of agent types to include Researcher/Knowledge Engineer

## Summary

Added a third agent type to the Resonance 7 framework: **Researcher** (or **Knowledge Engineer**) agents, specialized for information gathering, verification, and knowledge base population.

## The Three Agent Types

### 1. Initializer Agent
- **Purpose**: First session setup
- **Focus**: Environment setup, project scaffolding
- **Output**: Project structure, init scripts, feature lists

### 2. Researcher Agent (NEW)
- **Purpose**: Information gathering and organization
- **Focus**: Populating knowledge bases, creating structured resources
- **Output**: JSON knowledge bases, structured documentation, verified data

### 3. Coder Agent
- **Purpose**: Implementation and development
- **Focus**: Incremental feature development
- **Output**: Source code, bug fixes, incremental progress

## Why Researcher Agents?

Projects like XMBMGMT require extensive knowledge bases with:
- Structured, verifiable data (JSON format)
- Cross-referenced modules
- Source attribution with URLs
- Organized for easy reference

This work is distinct from coding and initialization, requiring specialized protocols.

## What Was Created

### 1. Researcher Agent Protocol
- **File**: `library/workspace_template/RESEARCHER_AGENT.md`
- **Contents**: Complete workflow, verification standards, best practices
- **Purpose**: Guide agents in information gathering and knowledge base creation

### 2. Knowledge Base Templates
- **`knowledge_base_template.json`**: Template for main knowledge base structure
- **`KNOWLEDGE_BASE_INDEX_TEMPLATE.md`**: Template for index/navigation file
- **Based on**: XMBMGMT's excellent knowledge base structure

### 3. Updated Documentation
- Updated `AGENTS.md` template to mention agent types
- Updated `AGENTS.md` for XMBMGMT to reference knowledge base
- Updated analysis documents to include Researcher agent type

## Researcher Agent Workflow

### Phase 1: Information Gathering
- Identify information needs
- Source identification (primary > secondary > tertiary)
- Information collection with source URLs

### Phase 2: Verification & Validation
- Cross-reference multiple sources
- Verify accuracy (test when possible)
- Document uncertainties clearly

### Phase 3: Organization & Structuring
- Choose format (JSON for structured data, Markdown for guides)
- Create knowledge base structure (main + specialized modules)
- Organize by purpose

### Phase 4: Documentation & Metadata
- Add metadata (version, dates, sources)
- Create index file for navigation
- Document all sources with URLs

## Knowledge Base Structure

Based on XMBMGMT's example:

```
docs/knowledge_base/
├── main_knowledge_base.json      # Core knowledge, overview
├── specialized_module1.json       # Focused topic 1
├── specialized_module2.json       # Focused topic 2
├── examples.json                  # Practical examples
└── KNOWLEDGE_BASE_INDEX.md        # Navigation guide
```

## Integration

### With Projects
- Knowledge bases live in `projects/{project}/docs/knowledge_base/`
- Created by Researcher agents
- Referenced in `AGENTS.md`
- Used by Coder agents for implementation

### With Framework
- Templates in `library/workspace_template/`
- Protocol in `RESEARCHER_AGENT.md`
- Accessible to all projects via symlink

## Example: XMBMGMT

XMBMGMT demonstrates excellent knowledge base structure:
- Main knowledge base with overview
- Specialized modules (query protocols, attributes, RCO objects, examples)
- Index file for navigation
- All with metadata, sources, and cross-references

This structure enables:
- Quick reference during development
- Verified, structured data
- Easy maintenance and updates
- Clear source attribution

## Next Steps

1. **Review**: Check `RESEARCHER_AGENT.md` protocol
2. **Test**: Use Researcher workflow for knowledge base creation
3. **Iterate**: Refine based on what works
4. **Document**: Add Researcher guidance to project `AGENTS.md` files

## Files Created

- `library/workspace_template/RESEARCHER_AGENT.md` - Complete protocol
- `library/workspace_template/knowledge_base_template.json` - Knowledge base template
- `library/workspace_template/KNOWLEDGE_BASE_INDEX_TEMPLATE.md` - Index template
- `projects/XMBMGMT/docs/analysis/RESEARCHER_AGENT_SUMMARY.md` - This summary

## References

- Researcher Protocol: `library/workspace_template/RESEARCHER_AGENT.md`
- Knowledge Base Templates: `library/workspace_template/`
- Example Knowledge Base: `projects/XMBMGMT/docs/knowledge_base/`

