# .agent-mode File Explanation

## Current Status

**Important**: The `.agent-mode` file persistence feature is **not yet implemented**. It's planned for "Phase 2" if needed.

## How It Works (When Implemented)

### `.agent-mode.example` vs `.agent-mode`

- **`.agent-mode.example`** - Just a template file showing the structure. **Does nothing by itself.**
- **`.agent-mode`** (without `.example`) - The actual file that would be read by agents (when implemented)

### Current Behavior

**Right now**:
- No `.agent-mode` file is read automatically
- Agents auto-detect mode based on project state (if no explicit mode set)
- You use `/agents [type]` command to switch modes
- The command can optionally create `.agent-mode` file for persistence (not yet implemented)

### Auto-Detection (Current Default)

If no `.agent-mode` file exists, agents auto-detect:
- New project (no `src/`, no `knowledge_base/`) → **Initializer**
- Has `knowledge_base/` but no `src/` → **Researcher**
- Has `src/` with code → **Coder**
- Default → **Coder**

## What `.agent-mode.example` Is For

The `.example` file is just a **template** showing:
- What the file structure looks like
- What fields it contains
- Example values

**It does NOT set a default mode.** It's just documentation.

## If You Want a Default Mode

To actually set a default mode (when persistence is implemented), you would:

1. **Rename the file**: `mv .agent-mode.example .agent-mode`
2. **Edit the mode**: Change `"mode": "coder"` to your desired default
3. **Commit it**: Add to git so it's project-specific

But again, **this feature isn't implemented yet** - it's planned for Phase 2.

## Recommendation

Since persistence isn't implemented yet, we could:

1. **Remove `.agent-mode.example`** - It's confusing without the feature
2. **Keep it** - As documentation of future feature
3. **Add note** - Clarify it's for future use

## Current Workflow

**Right now, to set agent mode:**
```
/agents coder        # Sets mode for this session
/agents researcher    # Sets mode for this session
/agents initializer   # Sets mode for this session
```

Mode is **session-specific** until persistence is implemented.

