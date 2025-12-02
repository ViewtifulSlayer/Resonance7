# Researcher Agent Protocol

This document defines the protocol for **Researcher** or **Knowledge Engineer** agents - specialized agents that gather, verify, organize, and populate knowledge bases and resource libraries.

> **Note**: This is a specialized agent type. For general agent protocols, see `library/agent_foundation.json`. For project-specific guidance, see `AGENTS.md`.

> **Provenance Note**: The Initializer and Coder agent types are directly from [Anthropic's research](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents). The Researcher agent type is an extension based on knowledge engineering best practices and the need for systematic knowledge base population. See `projects/XMBMGMT/docs/analysis/AGENT_TYPES_PROVENANCE.md` for details.

## Agent Type: Researcher / Knowledge Engineer

### Purpose

Researcher agents are specialized for:
- **Information Gathering**: Collecting data from multiple sources (web, documentation, code analysis)
- **Data Verification**: Ensuring accuracy and verifiability of information
- **Knowledge Organization**: Structuring information into reusable formats (JSON, knowledge bases)
- **Resource Population**: Creating and maintaining project knowledge bases and documentation libraries

### When to Use Researcher Agents

Use a Researcher agent when:
- Starting a new project and need to gather domain knowledge
- Populating knowledge bases with structured, verifiable data
- Creating resource libraries (like XMBMGMT's JSON knowledge bases)
- Analyzing documentation to extract structured information
- Building reference materials for future development

### Distinction from Other Agent Types

| Agent Type | Primary Focus | Output |
|------------|---------------|--------|
| **Initializer** | Environment setup, project scaffolding | Project structure, init scripts, feature lists |
| **Researcher** | Information gathering, knowledge organization | Knowledge bases, JSON resources, documentation |
| **Coder** | Implementation, incremental development | Source code, features, bug fixes |

## Researcher Agent Workflow

### Phase 1: Information Gathering

1. **Identify Information Needs**
   - What knowledge is required for the project?
   - What questions need answering?
   - What data structures are needed?

2. **Source Identification**
   - Official documentation (always prefer primary sources)
   - Community resources (forums, wikis)
   - Code analysis (if applicable)
   - Expert knowledge (user input)

3. **Information Collection**
   - Gather from multiple sources for verification
   - Document sources with URLs (critical for reproducibility)
   - Note any conflicts or ambiguities
   - Capture examples and patterns

### Phase 2: Verification & Validation

1. **Cross-Reference Sources**
   - Compare information across multiple sources
   - Identify consensus vs. conflicting information
   - Note version differences or context-specific variations

2. **Verify Accuracy**
   - Test information when possible (code examples, commands)
   - Check against official documentation
   - Validate with user when uncertain

3. **Document Uncertainties**
   - Clearly mark assumptions or uncertain information
   - Note when information is context-specific
   - Document version dependencies

### Phase 3: Organization & Structuring

1. **Choose Structure Format**
   - **JSON**: For structured data, attributes, protocols, examples
   - **Markdown**: For guides, explanations, workflows
   - **Hybrid**: JSON data + Markdown index (like XMBMGMT)

2. **Create Knowledge Base Structure**
   - Main knowledge base file (overview/index)
   - Specialized modules (by topic/domain)
   - Index file (KNOWLEDGE_BASE_INDEX.md) for navigation

3. **Organize by Purpose**
   - Group related information together
   - Create clear hierarchies
   - Enable easy cross-referencing

### Phase 4: Documentation & Metadata

1. **Add Metadata**
   - Version number
   - Last updated date
   - Source attribution
   - Related files references

2. **Create Index**
   - Navigation guide
   - Quick reference sections
   - "I want to..." workflows

3. **Document Sources**
   - All URLs used
   - Attribution for community resources
   - Version information for documentation

## Knowledge Base Structure Template

### Main Knowledge Base (JSON)

```json
{
  "metadata": {
    "version": "1.0.0",
    "last_updated": "YYYY-MM-DD",
    "source": "Primary sources with URLs",
    "description": "Brief description of knowledge base purpose",
    "related_files": {
      "module1": "filename1.json",
      "module2": "filename2.json"
    }
  },
  "main_topic": {
    "description": "Overview of main topic",
    "subtopics": {
      "subtopic1": {
        "description": "Details",
        "attributes": {},
        "examples": []
      }
    }
  }
}
```

### Specialized Module (JSON)

```json
{
  "metadata": {
    "version": "1.0.0",
    "description": "Specific module purpose",
    "source": "Sources with URLs"
  },
  "module_data": {
    "item1": {
      "description": "Details",
      "usage": "When to use",
      "examples": []
    }
  }
}
```

### Index File (Markdown)

```markdown
# Knowledge Base Index

## Main Knowledge Base
**`main_knowledge_base.json`** - Core knowledge base
- Overview
- Key concepts
- Links to specialized modules

## Specialized Modules
**`module1.json`** - [Purpose]
- [What it contains]
- **Use when:** [When to reference]

## Quick Reference Guide
### I want to...
[Common workflows and which files to check]
```

## Verification Standards

### Source Quality Hierarchy

1. **Primary Sources** (Highest Priority)
   - Official documentation
   - Source code (when analyzing)
   - Authoritative references

2. **Secondary Sources** (Good)
   - Community wikis (well-maintained)
   - Expert forums (verified information)
   - Tutorials from reputable sources

3. **Tertiary Sources** (Use with Caution)
   - Personal blogs
   - Unverified forum posts
   - Outdated documentation

### Verification Checklist

- [ ] Information appears in multiple sources
- [ ] Primary source confirms information
- [ ] Examples have been tested (when applicable)
- [ ] Version/context dependencies are documented
- [ ] Uncertainties are clearly marked
- [ ] All sources are cited with URLs

## Knowledge Base Best Practices

### Organization

1. **Modular Structure**: Break into specialized modules rather than one large file
2. **Clear Naming**: Use descriptive, consistent file names
3. **Cross-References**: Link related information across modules
4. **Index File**: Always create an index for navigation

### Content Quality

1. **Verifiable Data**: Only include information that can be verified
2. **Source Attribution**: Always cite sources with URLs
3. **Version Tracking**: Include version numbers and update dates
4. **Examples**: Include practical examples when possible
5. **Common Pitfalls**: Document known issues or gotchas

### Maintenance

1. **Update Dates**: Keep `last_updated` current
2. **Version Numbers**: Increment when making significant changes
3. **Cross-Reference Updates**: Update related files when changing information
4. **Deprecation**: Mark outdated information clearly

## Integration with Projects

### Project Knowledge Bases

Location: `projects/{project}/docs/knowledge_base/`

Structure:
- Main knowledge base JSON
- Specialized module JSONs
- Index Markdown file

### Shared Knowledge Modules

Location: `library/docs/{category}/`

Categories:
- `languages/` - Programming language documentation
- `frameworks/` - Framework documentation
- `hardware/` - Hardware documentation
- `tools/` - Development tool documentation
- `subjects/` - Domain-specific knowledge

## Example: XMBMGMT Knowledge Base

The XMBMGMT project demonstrates excellent knowledge base structure:

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

## Session Logging for Researchers

When working as a Researcher agent:

1. **Document Sources**: List all URLs and resources consulted
2. **Note Verification**: Document how information was verified
3. **Track Organization**: Document structure decisions and rationale
4. **Record Uncertainties**: Note any assumptions or uncertain information
5. **Update Progress**: Mark knowledge bases created/updated

## Common Pitfalls

### Problem: Information Without Sources
- **Solution**: Always include source URLs, even if it's "user knowledge" or "code analysis"

### Problem: Unverified Information
- **Solution**: Cross-reference multiple sources, test when possible, mark uncertainties

### Problem: Overly Large Files
- **Solution**: Break into specialized modules, use index file for navigation

### Problem: Outdated Information
- **Solution**: Include version numbers, update dates, document deprecation

### Problem: Poor Organization
- **Solution**: Use clear structure, create index file, enable cross-referencing

## Next Steps After Research

Once knowledge base is populated:

1. **Review with User**: Ensure accuracy and completeness
2. **Update AGENTS.md**: Reference knowledge base in project guidance
3. **Document Usage**: Explain how to use knowledge base in development
4. **Maintain**: Keep updated as project evolves

