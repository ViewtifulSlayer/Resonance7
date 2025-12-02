# Agent Types: Provenance and Best Practices

**Date**: 2025-12-01  
**Purpose**: Document what came from articles vs. extensions, and supporting best practices

## Directly from Articles

### Initializer vs. Coder Agent Distinction

**Source**: [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**What the Article Says**:
> "We developed a two-fold solution to enable the Claude Agent SDK to work effectively across many context windows: an **initializer agent** that sets up the environment on the first run, and a **coding agent** that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session."

**Anthropic's Implementation**:
- **Initializer Agent**: First session uses specialized prompt to:
  - Set up `init.sh` script
  - Create `claude-progress.txt` file
  - Create feature list file
  - Make initial git commit

- **Coding Agent**: Subsequent sessions:
  - Read progress files and git history
  - Make incremental progress
  - Leave structured updates
  - Test before starting new work

**Our Implementation**: Directly based on Anthropic's findings, adapted to Resonance 7 structure.

## Extensions and Inferences

### Researcher Agent Type

**Source**: **NOT directly from articles** - This was an extension/inference based on:
1. User's observation about XMBMGMT's extensive JSON knowledge bases
2. Need for information gathering and organization workflows
3. General software engineering principles

**Rationale**:
- XMBMGMT has extensive knowledge bases that required systematic information gathering
- This work is distinct from initialization (setup) and coding (implementation)
- Knowledge engineering is a recognized discipline with established practices

**Supporting Best Practices** (from web research):

1. **Hierarchical Task Decomposition**
   - Source: [Google Cloud: Agentic AI System Design Patterns](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
   - Principle: Break complex tasks into specialized sub-tasks assigned to specialized agents
   - Application: Researcher agent handles information gathering, separate from coding

2. **Modular and Scalable Architecture**
   - Source: [Leanware: AI Agent Architecture](https://www.leanware.co/insights/ai-agent-architecture)
   - Principle: Design agents with modular components for independent development
   - Application: Researcher agent is a specialized module for knowledge work

3. **Data Quality Assurance**
   - Source: [Leanware: AI Agent Architecture](https://www.leanware.co/insights/ai-agent-architecture)
   - Principle: Implement validation processes to verify information accuracy, completeness, and relevance
   - Application: Researcher agent's verification phase (cross-referencing, source hierarchy)

4. **Effective Memory Management**
   - Source: [Leanware: AI Agent Architecture](https://www.leanware.co/insights/ai-agent-architecture)
   - Principle: Maintain both short-term and long-term memory systems
   - Application: Knowledge bases serve as long-term memory, progress files as short-term

## Established Patterns Supporting Researcher Agent

### Knowledge Engineering

**Established Discipline**: Knowledge engineering has been a recognized field since the 1980s, focusing on:
- Extracting knowledge from experts
- Structuring knowledge for reuse
- Creating knowledge bases and ontologies
- Verification and validation of knowledge

**Application**: Researcher agent follows knowledge engineering principles:
- Information gathering (extraction)
- Verification (validation)
- Structuring (organization)
- Documentation (knowledge base creation)

### Information Architecture

**Established Discipline**: Information architecture principles include:
- Organizing information for findability
- Creating clear hierarchies
- Enabling cross-referencing
- Providing navigation aids

**Application**: Knowledge base structure (main + modules + index) follows information architecture best practices.

### Software Engineering: Separation of Concerns

**Established Principle**: Different tasks require different approaches:
- Setup/initialization (Initializer)
- Information gathering (Researcher)
- Implementation (Coder)

**Application**: Each agent type has distinct responsibilities, reducing cognitive load and improving focus.

## What's Directly Supported vs. Extension

| Component | Source | Support Level |
|-----------|--------|---------------|
| **Initializer Agent** | Anthropic article | ✅ Directly from article |
| **Coder Agent** | Anthropic article | ✅ Directly from article |
| **Researcher Agent** | Extension/inference | ⚠️ Supported by best practices, not directly from articles |
| **Feature List Tracking** | Anthropic article | ✅ Directly from article |
| **Progress Files** | Anthropic article | ✅ Directly from article |
| **Knowledge Base Structure** | Extension | ⚠️ Based on XMBMGMT example + information architecture principles |
| **Verification Protocols** | Extension | ⚠️ Based on knowledge engineering + data quality best practices |

## Best Practices That Support the Design

### 1. Specialization and Role Separation
- **Principle**: Different tasks benefit from specialized approaches
- **Support**: [Google Cloud: Agentic AI Patterns](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
- **Application**: Three distinct agent types for different phases

### 2. Structured Knowledge Representation
- **Principle**: Knowledge should be structured for reuse and verification
- **Support**: Knowledge engineering discipline (established field)
- **Application**: JSON knowledge bases with metadata and cross-references

### 3. Verification and Quality Assurance
- **Principle**: Information must be verified before use
- **Support**: [Leanware: Data Quality Assurance](https://www.leanware.co/insights/ai-agent-architecture)
- **Application**: Researcher agent's verification phase with source hierarchy

### 4. Incremental Progress
- **Principle**: Complex tasks should be broken into incremental steps
- **Support**: Anthropic article (coding agent makes incremental progress)
- **Application**: Coder agent workflow

### 5. Context Preservation
- **Principle**: Agents need context to work effectively across sessions
- **Support**: Anthropic article (progress files, git history)
- **Application**: Progress files, session logs, knowledge bases

## Conclusion

### Directly from Articles
- ✅ Initializer vs. Coder distinction
- ✅ Feature list tracking
- ✅ Progress files
- ✅ "Getting up to speed" workflow

### Extensions (Supported by Best Practices)
- ⚠️ Researcher agent type (supported by knowledge engineering, information architecture, and agent specialization principles)
- ⚠️ Knowledge base structure (based on XMBMGMT example + information architecture)
- ⚠️ Verification protocols (based on data quality and knowledge engineering practices)

### Recommendation

The Researcher agent type, while not directly from the articles, is:
1. **Necessary**: Addresses real need (knowledge base population)
2. **Supported**: Aligns with established best practices
3. **Practical**: Based on working example (XMBMGMT)
4. **Consistent**: Follows same pattern as Initializer/Coder distinction

However, it should be considered an **extension** rather than a direct implementation of the articles' findings.

## References

### Articles Referenced
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [GitHub: How to Write a Great agents.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)

### Best Practices Supporting Extensions
- [Google Cloud: Agentic AI System Design Patterns](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
- [Leanware: AI Agent Architecture](https://www.leanware.co/insights/ai-agent-architecture)
- Knowledge Engineering (established discipline, 1980s-present)
- Information Architecture (established discipline)

