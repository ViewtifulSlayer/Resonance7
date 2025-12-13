# Session Management

Create or update a Resonance 7 session log automatically based on current context.

## Action

When this command is invoked:

**If no session exists:**
1. Find the sessions directory: `sessions/current/`
2. Calculate next session ID (YYYYMMDD-NN format)
3. Create new session file with:
   - **Metadata auto-filled from context:**
     - Title: Based on current work/topic discussed
     - Author: "Resonance 7 Agent"
     - Model: "[model]" (auto-detected)
     - Status: "Active"
     - Description: Brief summary of session focus based on conversation
     - Timestamps: Current UTC time
   - **Template sections populated:**
     - Summary: Key accomplishments and insights from conversation
     - Key Decisions: Important decisions made
     - Deliverables: Files created, features implemented
     - Implementation Highlights: Notable techniques, patterns used
     - Next Work Items: Tasks identified or remaining work

**If session exists (most recent in sessions/current/):**
1. Read the existing session file
2. Update `last_updated` timestamp
3. **Add/update sections based on new work:**
   - Update Summary with new accomplishments
   - Add new Key Decisions if any
   - Add new Deliverables (files created/modified)
   - Add Implementation Highlights from recent work
   - Update Next Work Items with new tasks or completed items
   - Update Context Snapshot with current state
   - Add Sources (web/local) if referenced
4. Preserve existing content, append new information

## Context Gathering

Extract from current conversation:
- Files created/modified
- Features implemented
- Decisions made
- Challenges encountered
- URLs/web sources referenced
- Tools/commands used
- User preferences or feedback
- Remaining tasks or next steps

## Session File Structure

Follow the template from `library/templates/documentation_templates/session_template.md`:
- YAML frontmatter (metadata)
- Summary section
- Key Decisions & Rationale
- Deliverables & Metrics
- Implementation Highlights
- Challenges, Failures & Lessons
- Next Work Items (High/Medium/Low Priority)
- Context Snapshot
- Sources (Web and Local)
- Related Sessions
- Notes (User Feedback, Process Insights, Ready State)

## Metadata Rules

- `created`: NEVER modify after initial creation
- `last_updated`: Update ONLY when adding sections, completing work, adding files. NOT for typos, formatting, grammar fixes
- `status`: Active (work in progress) → Handoff (ready for next agent) → Completed (finished)

## When to Use

- At the start of a work session (creates new session)
- During a session to capture progress (updates existing)
- After completing significant work (updates with deliverables)
- When transitioning between major tasks (updates context)
- Before ending a session (final update with complete state)

