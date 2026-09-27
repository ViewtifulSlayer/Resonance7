# Resonance7 - Agent Guidance (AGENTS.md)

This file is auto-read by Freebuff/Codebuff at session start. It is the thin, always-on layer; the full protocol contract lives in `library/agent_foundation.json` (read it as part of onboarding below).

## 1. Agent Onboarding (Mandatory)

AT THE BEGINNING OF A CHAT, DO NOT PROCEED WITH ANY USER REQUESTS BEFORE COMPLETING THESE STEPS:

1. Have you read [**`Resonance7/library/agent_foundation.json`**] at least once this session? 
  - If yes, proceed to step 3.
  - If no, proceed to step 2.

2. Carefully read [**`Resonance7/library/agent_foundation.json`**] and commit it to memory. It is your core foundation and should not be combined with other tasks.
  - Verify step 2 is complete by summarizing the foundation and stating "Resonance 7 Active - Foundation Loaded."
  - Proceed to step 4.

3. Has [**`Resonance7/library/agent_foundation.json`**] been pushed out of your context window or has it been about a dozen messages since the last foundation-read?
  - If yes to either, proceed to step 2.
  - If no to both, proceed to step 4.

4. Proceed with user request only at this point.

## 2. Capability Availability

When the preferred or required capability is missing, disabled, disconnected, or out of context, **stop and ask** before substituting a weaker path. Silent workarounds waste time the user could fix quickly.

- Name what is missing, one clause on why it matters for this task, and the shortest steps for the user to enable or fix it.
- Ask: wait for enablement, or explicitly proceed with a **named** fallback.
- Do not guess from files when live inspection was the intended path. Do not chain alternate approaches after the first unavailable signal without user input.
- Allowed without asking: documented peer fallbacks already in the foundation, one brief retry after a transient failure, user-authorized best-effort mode,   and permanently impossible capabilities (state that, then offer options).

## 3. MCP (SQLite)

Freebuff loads MCP servers from `.agents/mcp.json` (gitignored, machine-local).
Regenerate it with:

```bash
python library/tools/scripts/setup_database.py
```

- Server key: `Resonance7-sqlite`.
- Default DB: `library/databases/db/session_logs.db` (alias `session_logs`).
- Any `library/databases/db/<stem>.db` is reachable as alias `<stem>`; discover
  via the MCP `list_databases` tool.
- MCP tools are SELECT-only; schema/data changes go through ingest scripts.
- Never run session log ingest (`session_logs.db`) without explicit user
  permission.

## 4. Session logging

Session logs live in `library/sessions/current/` (lifecycle: current -> recent
-> archived). Create/update them per `library/templates/session_template.md`
and the `session_logging` rules in `library/agent_foundation.json`.

## 5. Skills

Loadable on demand from `.agents/skills/`:

- `database-specialist` - schema design, ingest/compile/verify workflows
- `mcp-sqlite` - MCP + SQLite server config, querying workspace DBs
- `markdown-punctuation` - ASCII-only punctuation in markdown
- `python-expert` - Python edge cases and OS-specific gotchas
- `freebuff` - working inside Freebuff: AGENTS.md context, `.agents/` skills + MCP, global `~/.agents`
- `codebuff` - the Codebuff framework/CLI behind Freebuff (knowledge.md, `/init`, custom agents, SDK)
- `vscode` - VS Code agent config: MCP (`servers` vs `mcpServers`), Agent Skills, custom agents
- `skill-authoring` - how to write and review a skill (SKILL.md + reference.md)
- `ghidra-expert` - Ghidra / SNES 65816 reverse engineering

For explanations of Resonance7 topics (workspace structure, tools, sessions,
ignore files), ask the agent - the knowledge lives in the foundation file,
this AGENTS.md, and the skills above.

## 6. File safety and approval

- Check `.agentignore` before ANY file modification; do not modify listed
  files/directories unless the user explicitly requests it.
- **Default to assess-and-ask:** do not edit files, create files (except
  session logs), or run state-changing commands until the user explicitly
  approves that specific work. Questions, assessments, and lookahead plans are
  not permission to implement. Full policy:
  `library/agent_foundation.json` (`command_authorization_policy`).
- Prefer the chat window for communication. Do not create `.md` files without
  explicit permission (session logs are the exception: update them at your
  discretion and inform the user).