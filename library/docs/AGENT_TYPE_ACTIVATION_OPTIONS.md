# Agent Type Activation: Options and Recommendations

**Date**: 2025-12-01  
**Purpose**: Explore options for activating/selecting agent types (Initializer, Coder, Researcher)

## Current State

**No explicit agent type selection exists yet**. Agent types are defined but there's no mechanism to:
- Select which agent type to use
- Switch between agent types
- Persist agent type selection
- Load agent type-specific protocols

## Option 1: Single `/agents` Command (User's Suggestion)

### Implementation
```
/agents [type]
```

Where `type` is:
- `initializer` - Environment setup mode
- `coder` - Implementation mode  
- `researcher` - Knowledge gathering mode
- (no arg) - Interactive selection menu

### Pros
- ✅ Single command, easy to remember
- ✅ Interactive mode for discovery
- ✅ Can show current mode
- ✅ Can provide quick help for each type

### Cons
- ⚠️ Requires user to remember to use it
- ⚠️ No persistence (resets each session)
- ⚠️ Might be forgotten if not explicit

### Example Flow
```
User: /agents
Agent: Current mode: [none/default]
       Select agent type:
       1. Initializer - Set up project environment
       2. Coder - Implement features incrementally
       3. Researcher - Gather and organize knowledge
       4. Show current mode details
       
User: 2
Agent: [Switches to Coder mode, loads coder protocols]
       Coder mode active. I'll:
       - Read progress files and git history
       - Make incremental progress
       - Leave clean state with commits
       Ready to code!
```

## Option 2: Separate Commands

### Implementation
```
/initializer - Switch to initializer mode
/coder - Switch to coder mode
/researcher - Switch to researcher mode
/agent-mode - Show current mode
```

### Pros
- ✅ Explicit and clear
- ✅ Easy to discover (autocomplete shows all)
- ✅ Can have mode-specific help
- ✅ No ambiguity

### Cons
- ⚠️ More commands to remember
- ⚠️ No persistence
- ⚠️ Might clutter command list

## Option 3: Context-Aware Auto-Detection

### Implementation
Agent automatically detects which mode based on:
- Project state (new project → Initializer)
- Existing knowledge bases → Researcher might be needed
- Existing code → Coder mode
- User request ("gather information" → Researcher)

### Pros
- ✅ No user action needed
- ✅ Feels intelligent
- ✅ Reduces friction

### Cons
- ⚠️ Might guess wrong
- ⚠️ Less explicit control
- ⚠️ Harder to override

## Option 4: State File + Command

### Implementation
- Create `.agent-mode` file in project root
- `/agents [type]` writes to file
- Agent reads file on session start
- Persists across sessions

### Pros
- ✅ Persistence across sessions
- ✅ Project-specific (each project can have different mode)
- ✅ Can be version controlled
- ✅ Explicit and clear

### Cons
- ⚠️ Extra file to manage
- ⚠️ Might get out of sync

## Option 5: Hybrid Approach (RECOMMENDED)

### Implementation
Combine multiple approaches:

1. **State File for Persistence**
   - `.agent-mode` file in project root
   - Contains: `{"mode": "coder", "last_updated": "2025-12-01"}`

2. **Single `/agents` Command**
   - `/agents` - Show current mode and options
   - `/agents [type]` - Switch to type and persist
   - `/agents auto` - Auto-detect based on context

3. **Auto-Detection on Session Start**
   - Agent reads `.agent-mode` if exists
   - If not, auto-detects based on project state
   - Reports mode in session start message

4. **Mode Indicators**
   - Agent mentions current mode
   - Can show in session logs
   - Clear when mode changes

### Pros
- ✅ Best of all worlds
- ✅ Persistence when needed
- ✅ Auto-detection when helpful
- ✅ Explicit control when desired
- ✅ Project-specific

### Cons
- ⚠️ More complex to implement
- ⚠️ More to document

## Option 6: Project-Level Configuration

### Implementation
- Add to `AGENTS.md` or project config
- `agent_type: "coder"` in YAML frontmatter
- Agent reads on session start

### Pros
- ✅ Documented in project files
- ✅ Version controlled
- ✅ Part of project documentation

### Cons
- ⚠️ Less dynamic (requires file edit)
- ⚠️ Not as interactive

## Recommendation: Hybrid Approach (Option 5)

### Why This Works Best

1. **Flexibility**: Supports both explicit control and auto-detection
2. **Persistence**: Mode persists across sessions via state file
3. **Discovery**: `/agents` command helps users understand options
4. **Context-Aware**: Auto-detection when no explicit mode set
5. **Project-Specific**: Each project can have its own mode

### Implementation Details

#### 1. State File Structure
```json
{
  "mode": "coder",
  "last_updated": "2025-12-01T10:30:00Z",
  "set_by": "user",
  "context": "incremental development"
}
```

#### 2. `/agents` Command Behavior
```
/agents                    → Show current mode + options
/agents initializer        → Switch to initializer, persist
/agents coder              → Switch to coder, persist
/agents researcher         → Switch to researcher, persist
/agents auto               → Auto-detect and set
/agents status             → Show current mode details
```

#### 3. Auto-Detection Logic
```python
def detect_agent_mode(project_path):
    # Check for explicit mode file
    if exists('.agent-mode'):
        return read_mode_file()
    
    # Auto-detect based on project state
    if not exists('src/') and not exists('docs/knowledge_base/'):
        return "initializer"  # New project
    
    if exists('docs/knowledge_base/') and is_empty('src/'):
        return "researcher"  # Knowledge gathering phase
    
    if exists('src/') and has_code():
        return "coder"  # Implementation phase
    
    return "coder"  # Default
```

#### 4. Session Start Behavior
```
Agent on session start:
1. Check for .agent-mode file
2. If exists, load mode and protocols
3. If not, auto-detect based on project state
4. Report mode: "Resonance 7 Active - Coder Mode"
5. Load appropriate protocols
```

## Alternative: Simpler Single Command

If the hybrid is too complex, a simpler version:

### Simple `/agents` Command
- `/agents` - Interactive menu to select type
- `/agents [type]` - Direct selection
- No persistence (resets each session, but that's okay)
- Agent reports mode when activated

### Why Simpler Might Be Better
- ✅ Less to maintain
- ✅ No state file management
- ✅ User explicitly chooses each time
- ✅ Clearer intent

## Comparison Table

| Option | Complexity | Persistence | Auto-Detect | Explicit Control |
|--------|-----------|-------------|-------------|------------------|
| 1. Single `/agents` | Low | ❌ | ❌ | ✅ |
| 2. Separate commands | Low | ❌ | ❌ | ✅ |
| 3. Auto-detect only | Low | ❌ | ✅ | ❌ |
| 4. State file only | Medium | ✅ | ❌ | ✅ |
| 5. Hybrid (recommended) | High | ✅ | ✅ | ✅ |
| 6. Project config | Low | ✅ | ❌ | ⚠️ |

## Recommendation Summary

**Start Simple**: Implement Option 1 (single `/agents` command) first
- Easy to use
- Clear and explicit
- Can add persistence later if needed

**Evolve if Needed**: If persistence becomes important, add state file (Option 5)

**Why**: 
- YAGNI principle (You Aren't Gonna Need It)
- Can always add features later
- Simpler is better for initial implementation
- User feedback will guide evolution

## Implementation Priority

1. **Phase 1**: Single `/agents` command (Option 1)
   - Interactive selection
   - Mode-specific protocol loading
   - Clear mode reporting

2. **Phase 2** (if needed): Add persistence
   - `.agent-mode` state file
   - Auto-detection fallback
   - Session start mode loading

3. **Phase 3** (if needed): Advanced features
   - Mode-specific commands
   - Mode transitions
   - Mode history

