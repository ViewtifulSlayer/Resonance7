# Resonance 7 Framework Documentation Index

Quick navigation guide for framework documentation.

## Agent Onboarding & Types

### Core Analysis
- **[AGENT_ONBOARDING_ANALYSIS.md](AGENT_ONBOARDING_ANALYSIS.md)** - Comprehensive analysis of Anthropic & GitHub patterns
  - What components are missing
  - Implementation recommendations
  - File type summary

### Quick Reference
- **[AGENT_ONBOARDING_SUMMARY.md](AGENT_ONBOARDING_SUMMARY.md)** - Quick answers to common questions
  - What components are missing
  - Is agents.md a file or pattern?
  - What was created

### Provenance
- **[AGENT_TYPES_PROVENANCE.md](AGENT_TYPES_PROVENANCE.md)** - What came from articles vs. extensions
  - Directly from articles
  - Extensions and inferences
  - Supporting best practices

## Agent Type Activation

### Options Analysis
- **[AGENT_TYPE_ACTIVATION_OPTIONS.md](AGENT_TYPE_ACTIVATION_OPTIONS.md)** - Complete analysis of activation approaches
  - 6 different options evaluated
  - Pros/cons comparison
  - Recommendation: Hybrid approach

### Implementation
- **[AGENT_ACTIVATION_IMPLEMENTATION.md](AGENT_ACTIVATION_IMPLEMENTATION.md)** - Implementation guide
  - `/agents` command usage
  - Protocol loading
  - Auto-detection logic

## Related Documentation

### Agent Protocols
Located in `library/workspace_template/`:
- `INITIALIZER_AGENT.md` - Initializer agent protocol
- `RESEARCHER_AGENT.md` - Researcher agent protocol
- `AGENTS.md` - Project-specific agent guidance template
- `.agent-mode.example` - Template for agent mode persistence (⚠️ **Documentation only - not implemented**)

### Commands
Located in `.cursor/commands/`:
- `agents.md` - Agent type selection
- `foundation.md` - Foundation loading
- `start.md` - Workspace initialization
- `help.md` - Help system
- `session.md` - Session management

## Implementation Status Notes

### Agent Mode Persistence
**Status**: Documentation only, not implemented

The `.agent-mode` file persistence feature is **documentation only** - there's no actual code/tooling that implements it. Currently:
- `/agents [type]` command works (agent follows instructions manually)
- Mode is session-specific (doesn't persist automatically)
- `.agent-mode.example` is just a template showing structure
- No Python scripts or session hooks implement persistence

See `AGENT_MODE_IMPLEMENTATION_STATUS.md` for details.

## Reading Order

**For Understanding Agent Types:**
1. `AGENT_ONBOARDING_SUMMARY.md` - Quick overview
2. `AGENT_TYPES_PROVENANCE.md` - What's from articles vs. extensions
3. `AGENT_ONBOARDING_ANALYSIS.md` - Full analysis

**For Implementing Agent Selection:**
1. `AGENT_TYPE_ACTIVATION_OPTIONS.md` - Understand options
2. `AGENT_ACTIVATION_IMPLEMENTATION.md` - Implementation guide
3. `.cursor/commands/agents.md` - Command reference

**For Using Agent Types:**
1. `library/workspace_template/INITIALIZER_AGENT.md`
2. `library/workspace_template/RESEARCHER_AGENT.md`
3. `library/workspace_template/AGENTS.md`

## File Status

### Core Documentation (Active)
- ✅ `AGENT_ONBOARDING_ANALYSIS.md` - Comprehensive reference
- ✅ `AGENT_ONBOARDING_SUMMARY.md` - Quick reference
- ✅ `AGENT_TYPES_PROVENANCE.md` - Provenance documentation
- ✅ `AGENT_TYPE_ACTIVATION_OPTIONS.md` - Options analysis
- ✅ `AGENT_ACTIVATION_IMPLEMENTATION.md` - Implementation guide

### Marked for Removal (Redundant)
- ⚠️ `AGENT_TYPES_EXPANSION.md` - Covered in main analysis
- ⚠️ `RESEARCHER_AGENT_SUMMARY.md` - Protocol file is authoritative

**Note**: See `CONSOLIDATION_PLAN.md` for consolidation strategy. These files can be removed once consolidation is complete.

