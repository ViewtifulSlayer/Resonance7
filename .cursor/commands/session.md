# Session Management

Create or update a Resonance 7 session log automatically based on current context.

## What This Command Does

When you invoke `/session`, the agent **creates or updates the session markdown file** in `sessions/current/` (or updates the most recent one). A **session logs database** (`session_logs.db`) provides queryable recall (e.g. via MCP); the user runs ingest when they want the database updated. **Never run session log ingest without explicit user permission.**

## Action

When this command is invoked:

**If you have already created a session log:** Regardless of whether the date has changed or not (e.g. past midnight UTC), keep using your current session log; the "last_updated" timestamp doesn't have to match the "created" timestamp. Then:
1. Read the existing session file
2. **If (and only if) substantive content is added/updated**, update `last_updated` timestamp
3. **Add/update sections based on new work:**
   - Update Summary with new accomplishments
   - Add new Key Decisions if any
   - Add new Deliverables (files created/modified)
   - Add Implementation Highlights from recent work
   - Update Next Work Items with new tasks or completed items
   - Update Context Snapshot with current state
   - Add Sources (web/local) if referenced
4. Preserve existing content, append new information

**If you have not created or updated a session log:**
1. In `sessions/current/`: if the most recent session has status **Handoff**, set its `status` to **Completed** (status only).
2. Calculate next session ID (YYYYMMDD-NN format).
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
- `status`: Active → Handoff → Completed. When creating a new log, if the previous session is Handoff, set it to Completed first (status only).

## When to Use

- At the start of a **new** work session (creates new session only when no session exists or user explicitly starts one)
- During a session to capture progress (prefer updating existing)
- After completing significant work (updates existing with deliverables)
- When transitioning between major tasks (updates existing context)
- Before ending a session (final update with complete state)

