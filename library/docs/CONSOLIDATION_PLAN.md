# Documentation Consolidation Plan

**Date**: 2025-12-01  
**Purpose**: Identify redundancies and plan consolidation

## Current Files Analysis

### Core Documentation (Keep)

1. **AGENT_ONBOARDING_ANALYSIS.md** (10KB)
   - Comprehensive analysis of Anthropic & GitHub patterns
   - Missing components identification
   - Implementation recommendations
   - **Status**: ✅ **KEEP** - Primary comprehensive reference

2. **AGENT_ONBOARDING_SUMMARY.md** (5.7KB)
   - Quick reference version
   - Direct answers to questions
   - **Status**: ✅ **KEEP** - Useful quick reference, different purpose from analysis

3. **AGENT_TYPES_PROVENANCE.md** (8.2KB)
   - What came from articles vs. extensions
   - Supporting best practices
   - **Status**: ✅ **KEEP** - Important for understanding sources and credibility

4. **AGENT_TYPE_ACTIVATION_OPTIONS.md** (7.9KB)
   - Complete analysis of activation options
   - Pros/cons of each approach
   - **Status**: ✅ **KEEP** - Useful for future decisions

5. **AGENT_ACTIVATION_IMPLEMENTATION.md** (4.5KB)
   - Implementation guide for `/agents` command
   - Usage examples
   - **Status**: ✅ **KEEP** - Implementation reference

### Redundant Files (Consolidate or Remove)

6. **AGENT_TYPES_EXPANSION.md** (4.6KB)
   - Summary of Researcher agent type addition
   - **Overlap**: Covers same ground as RESEARCHER_AGENT_SUMMARY.md
   - **Status**: ⚠️ **CONSOLIDATE** - Merge key points into main analysis or remove

7. **RESEARCHER_AGENT_SUMMARY.md** (6.4KB)
   - Summary of Researcher agent type
   - **Overlap**: Redundant with RESEARCHER_AGENT.md protocol file
   - **Status**: ⚠️ **CONSOLIDATE** - Protocol file is authoritative, this is redundant

## Consolidation Strategy

### Option 1: Remove Redundant Summaries
- Delete `AGENT_TYPES_EXPANSION.md` (covered in main analysis)
- Delete `RESEARCHER_AGENT_SUMMARY.md` (protocol file is authoritative)
- **Result**: Cleaner, less redundant

### Option 2: Merge into Main Analysis
- Extract unique content from `AGENT_TYPES_EXPANSION.md`
- Add to `AGENT_ONBOARDING_ANALYSIS.md` if missing
- Delete redundant files
- **Result**: Single comprehensive source

### Option 3: Keep as Historical Record
- Mark as "Historical/Reference" in INDEX
- Don't actively maintain
- **Result**: Preserves context but reduces maintenance

## Recommendation: Option 1 (Remove Redundant)

**Rationale**:
- Protocol files (`RESEARCHER_AGENT.md`, `INITIALIZER_AGENT.md`) are authoritative
- Main analysis (`AGENT_ONBOARDING_ANALYSIS.md`) covers the expansion
- Summaries add little value beyond what's in protocol files
- Cleaner documentation is easier to maintain

**Action**:
1. Delete `AGENT_TYPES_EXPANSION.md` (covered in main analysis)
2. Delete `RESEARCHER_AGENT_SUMMARY.md` (protocol file is authoritative)
3. Update INDEX to reflect removal
4. Update README to reflect final structure

## Final Structure

After consolidation:

```
library/docs/
├── README.md                              # Overview and organization
├── INDEX.md                               # Navigation guide
├── AGENT_ONBOARDING_ANALYSIS.md          # Comprehensive analysis
├── AGENT_ONBOARDING_SUMMARY.md            # Quick reference
├── AGENT_TYPES_PROVENANCE.md              # Provenance documentation
├── AGENT_TYPE_ACTIVATION_OPTIONS.md       # Activation options analysis
├── AGENT_ACTIVATION_IMPLEMENTATION.md     # Implementation guide
└── CONSOLIDATION_PLAN.md                  # This file (can remove after consolidation)
```

**Total**: 7 files (down from 8, removing 2 redundant, adding INDEX)

## Related Files (Not in docs/)

Protocol files (authoritative sources):
- `library/workspace_template/INITIALIZER_AGENT.md`
- `library/workspace_template/RESEARCHER_AGENT.md`
- `library/workspace_template/AGENTS.md`

Commands:
- `.cursor/commands/agents.md`
- `.cursor/commands/foundation.md`
- `.cursor/commands/start.md`
- `.cursor/commands/help.md`
- `.cursor/commands/session.md`

## Next Steps

1. Review this plan
2. If approved, delete redundant files
3. Update INDEX.md
4. Update README.md
5. Remove this consolidation plan file (or keep as historical record)

