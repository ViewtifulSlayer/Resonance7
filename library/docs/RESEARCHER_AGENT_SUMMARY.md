# Researcher Agent Type: Summary

**Date**: 2025-12-01  
**Context**: Expansion of agent types beyond Initializer and Coder

## Overview

The **Researcher** (or **Knowledge Engineer**) agent type is specialized for information gathering, verification, and knowledge base population. This addresses the need for agents that can systematically collect, verify, and organize domain knowledge into structured, reusable formats.

## Why Researcher Agents?

### The Problem

Projects like XMBMGMT require extensive knowledge bases with structured, verifiable data:
- JSON knowledge bases with metadata
- Cross-referenced modules
- Verified information with source attribution
- Organized for easy reference

This work is distinct from:
- **Initializer**: Sets up project structure
- **Coder**: Implements features incrementally

### The Solution

A specialized **Researcher** agent type that:
1. **Gathers** information from multiple sources
2. **Verifies** accuracy through cross-referencing
3. **Organizes** into structured formats (JSON, knowledge bases)
4. **Documents** with proper attribution and metadata

## Agent Type Comparison

| Agent Type | Primary Focus | When to Use | Output |
|------------|---------------|-------------|--------|
| **Initializer** | Environment setup | First session of new project | Project structure, init scripts, feature lists |
| **Researcher** | Information gathering | Need to populate knowledge bases | JSON knowledge bases, structured documentation |
| **Coder** | Implementation | Subsequent sessions, feature development | Source code, bug fixes, incremental progress |

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

Based on XMBMGMT's excellent example:

```
docs/knowledge_base/
├── main_knowledge_base.json      # Core knowledge, overview
├── specialized_module1.json       # Focused topic 1
├── specialized_module2.json       # Focused topic 2
├── examples.json                  # Practical examples
└── KNOWLEDGE_BASE_INDEX.md        # Navigation guide
```

### Key Principles

1. **Modular**: Break into specialized modules, not one large file
2. **Verifiable**: Only include information that can be verified
3. **Attributed**: Always cite sources with URLs
4. **Versioned**: Include version numbers and update dates
5. **Indexed**: Create index file for easy navigation

## Templates Created

1. **`RESEARCHER_AGENT.md`** - Complete protocol for researcher agents
   - Workflow phases
   - Verification standards
   - Best practices
   - Integration guidelines

2. **`knowledge_base_template.json`** - Template for main knowledge base
   - Metadata structure
   - Content organization
   - Example patterns

3. **`KNOWLEDGE_BASE_INDEX_TEMPLATE.md`** - Template for index file
   - Navigation structure
   - Quick reference guide
   - File relationships

## Integration with Projects

### Project Knowledge Bases
- Location: `projects/{project}/docs/knowledge_base/`
- Created by Researcher agents
- Referenced in `AGENTS.md`
- Used by Coder agents for implementation

### Shared Knowledge Modules
- Location: `library/docs/{category}/`
- Categories: languages, frameworks, hardware, tools, subjects
- Can be populated by Researcher agents
- Accessible to all projects via symlink

## Example: XMBMGMT Knowledge Base

XMBMGMT demonstrates excellent knowledge base structure:

- **Main**: `ps3_xmb_knowledge_base.json` - Core XMB knowledge
- **Modules**:
  - `xmbml_query_protocols.json` - Query types and URL patterns
  - `xmbml_attribute_definitions.json` - Attribute definitions
  - `rco_object_attributes.json` - RCO object types
  - `xmb_modification_examples.json` - Practical examples
- **Index**: `KNOWLEDGE_BASE_INDEX.md` - Navigation guide

Each module:
- Has metadata with version and sources
- Contains structured, verifiable data
- Cross-references related modules
- Includes practical examples

## Verification Standards

### Source Quality Hierarchy

1. **Primary Sources** (Highest Priority)
   - Official documentation
   - Source code analysis
   - Authoritative references

2. **Secondary Sources** (Good)
   - Community wikis (well-maintained)
   - Expert forums (verified information)
   - Reputable tutorials

3. **Tertiary Sources** (Use with Caution)
   - Personal blogs
   - Unverified forum posts
   - Outdated documentation

### Verification Checklist

- [ ] Information appears in multiple sources
- [ ] Primary source confirms information
- [ ] Examples tested (when applicable)
- [ ] Version/context dependencies documented
- [ ] Uncertainties clearly marked
- [ ] All sources cited with URLs

## When to Use Researcher Agents

Use a Researcher agent when:

1. **Starting New Project**
   - Need to gather domain knowledge
   - Building knowledge base from scratch

2. **Populating Resources**
   - Creating JSON knowledge bases
   - Extracting structured data from documentation
   - Building reference materials

3. **Knowledge Gaps**
   - Missing information for implementation
   - Need verified, structured data
   - Building documentation library

4. **Project Evolution**
   - New domain knowledge discovered
   - Need to update knowledge bases
   - Expanding resource libraries

## Next Steps

1. **Review Templates**: Check `RESEARCHER_AGENT.md` and knowledge base templates
2. **Test Workflow**: Use Researcher protocol for a knowledge base creation task
3. **Iterate**: Refine based on what works
4. **Document**: Add Researcher agent guidance to `AGENTS.md` templates

## References

- XMBMGMT Knowledge Base: `projects/XMBMGMT/docs/knowledge_base/`
- Researcher Protocol: `library/workspace_template/RESEARCHER_AGENT.md`
- Knowledge Base Templates: `library/workspace_template/knowledge_base_template.json`

