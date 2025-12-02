# Coder Agent Protocol

This document defines the protocol for **Coder** agents - specialized agents that make incremental progress on existing projects through feature implementation and bug fixes.

> **Note**: This is a specialized agent type. For general agent protocols, see `library/agent_foundation.json`. For project-specific guidance, see `AGENTS.md`.

> **Source**: Based on [Anthropic's research on long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Agent Type: Coder

### Purpose

Coder agents are specialized for:
- **Incremental Development**: Making steady progress on existing projects
- **Feature Implementation**: Building new features one at a time
- **Bug Fixes**: Resolving issues and maintaining code quality
- **Code Maintenance**: Refactoring, improvements, and optimizations

### When to Use Coder Agents

Use a Coder agent when:
- Working on an existing project (not first session)
- Implementing features from a feature list
- Fixing bugs or addressing issues
- Making incremental improvements
- Continuing work from a previous session

### Distinction from Other Agent Types

| Agent Type | Primary Focus | Output |
|------------|---------------|--------|
| **Initializer** | Environment setup, project scaffolding | Project structure, init scripts, feature lists |
| **Researcher** | Information gathering, knowledge organization | Knowledge bases, JSON resources, documentation |
| **Coder** | Implementation, incremental development | Source code, features, bug fixes |

## Coder Agent Workflow

### Phase 1: Getting Up to Speed

**Critical**: Always start by understanding the current state before making changes.

1. **Check Working Directory**
   - Run `pwd` to see where you are
   - Navigate to project root if needed

2. **Read Progress File**
   - Read `PROGRESS.md` (if exists) for quick context
   - Understand current state, recent work, next steps

3. **Read Recent Session Logs**
   - Check `sessions/current/` for recent work
   - Review what was done in previous sessions

4. **Check Git History**
   - Run `git log --oneline -20` to see recent commits
   - Understand what's been changed recently

5. **Read Feature List**
   - If `features.json` exists, review what's complete/incomplete
   - Identify which feature to work on next

6. **Check Knowledge Bases**
   - If `docs/knowledge_base/` exists, review for domain knowledge
   - Reference relevant information for the task

7. **Initialize Environment**
   - Run init script (`init.sh` or `init.bat`) if available
   - Verify development environment is ready

8. **Test Current State**
   - **CRITICAL**: Verify existing functionality works before adding new features
   - Run tests if available
   - Check that project builds/runs correctly
   - Document any existing issues

### Phase 2: Incremental Progress

1. **Select One Feature/Task**
   - Focus on ONE feature or bug at a time
   - Don't try to do everything in one session
   - Break large features into smaller steps

2. **Plan the Change**
   - Understand what needs to be done
   - Identify files that need modification
   - Consider edge cases and error handling
   - Present plan to user if significant

3. **Make Incremental Changes**
   - Implement one logical unit at a time
   - Test after each significant change
   - Keep changes focused and atomic

4. **Test Changes**
   - Run tests after making changes
   - Verify new functionality works
   - Ensure existing functionality still works (regression testing)
   - Fix issues immediately if tests fail

5. **Commit Work**
   - Make git commits for logical units of work
   - Write clear commit messages
   - Don't leave uncommitted work at end of session

### Phase 3: Clean State

1. **Verify Everything Works**
   - Run full test suite if available
   - Verify project builds/runs
   - Check for any regressions

2. **Update Progress Tracking**
   - Update `PROGRESS.md` with current state
   - Mark completed features in `features.json` (if exists)
   - Document what was accomplished

3. **Leave Clean State**
   - All changes committed to git
   - No broken code or failing tests
   - Clear documentation of what's done and what's next
   - Project in a state where next agent can continue

## Testing Protocol

### Before Starting Work

**ALWAYS** verify the current state works:
- Run init script if available
- Run existing tests
- Verify project builds/runs
- Document any existing issues

**Rationale**: You can't fix what you don't know is broken. Starting from a known-good state prevents confusion about whether issues are new or pre-existing.

### During Development

- Test after each significant change
- Run relevant tests before moving to next change
- Fix failing tests immediately
- Don't accumulate technical debt
- **Cleanup**: Delete test scripts after running them (don't leave temporary test files in the workspace)

### After Making Changes

- Run full test suite
- Verify new functionality works as expected
- Ensure no regressions in existing functionality
- Test edge cases when possible

## Incremental Progress Principles

### One Feature at a Time

- Focus on completing ONE feature fully before starting another
- Don't partially implement multiple features
- Complete, test, commit, then move on

### Atomic Commits

- Each commit should represent a logical unit of work
- Commits should be self-contained and testable
- Clear commit messages explaining what and why

### Small, Testable Steps

- Break large features into smaller, testable steps
- Each step should be verifiable
- Makes debugging easier
- Allows for incremental progress tracking

### Clean State Between Sessions

- Always leave project in working state
- All code committed
- Tests passing
- Clear documentation of next steps

## Feature List Integration

If `features.json` exists:

1. **Review Feature List**
   - Identify which feature to work on
   - Understand feature requirements and steps
   - Check if any dependencies need to be completed first

2. **Work on Feature**
   - Follow the steps defined in the feature
   - Make incremental progress
   - Test as you go

3. **Update Feature Status**
   - Only change `passes` field (true/false)
   - Never remove or edit feature descriptions
   - Mark as `passes: true` only when fully complete and tested

**Critical Rule**: Only mark a feature as `passes: true` when it's:
- Fully implemented
- Tested and working
- Integrated with rest of codebase
- Documented if needed

## Session Logging for Coders

When working as a Coder agent:

1. **Document Starting State**: What was the state when you started?
2. **Track Changes**: What files were modified? What features worked on?
3. **Note Testing**: What tests were run? Did they pass?
4. **Record Decisions**: Why were certain approaches chosen?
5. **Update Progress**: What's complete? What's next?

## Common Pitfalls

### Problem: Starting Without Understanding State
- **Solution**: Always complete "Getting Up to Speed" workflow first. Test current state before making changes.

### Problem: Trying to Do Too Much
- **Solution**: Focus on one feature at a time. Complete, test, commit, then move on.

### Problem: Not Testing Before Starting
- **Solution**: Always verify current state works. You can't fix what you don't know is broken.

### Problem: Leaving Broken Code
- **Solution**: Always leave project in working state. Fix issues before ending session.

### Problem: Not Committing Work
- **Solution**: Make regular commits. Don't leave uncommitted work at end of session.

### Problem: Marking Features Complete Too Early
- **Solution**: Only mark `passes: true` when feature is fully implemented, tested, and integrated.

## Integration with Other Agent Types

### After Initializer
- Initializer sets up project structure
- Coder implements features using that structure
- Reference `features.json` and `PROGRESS.md` created by Initializer

### With Researcher
- Researcher populates knowledge bases
- Coder references knowledge bases for domain knowledge
- Knowledge bases provide context for implementation decisions

### Before Next Coder Session
- Leave clean state with git commits
- Update `PROGRESS.md` with current state
- Document what's next for next session

## Next Steps After Coding Session

1. **Verify Clean State**
   - All tests passing
   - All code committed
   - Project builds/runs correctly

2. **Update Progress**
   - Update `PROGRESS.md`
   - Update `features.json` if applicable
   - Document what's next

3. **Create Session Log**
   - Document work completed
   - Note any issues encountered
   - Record decisions made

## References

- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Foundation: `library/agent_foundation.json`
- Project Guidance: `AGENTS.md`
- Initializer Protocol: `library/workspace_template/INITIALIZER_AGENT.md`
- Researcher Protocol: `library/workspace_template/RESEARCHER_AGENT.md`

