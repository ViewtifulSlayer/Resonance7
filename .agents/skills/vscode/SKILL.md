---
name: vscode
description: VS Code as the host IDE for AI agents - MCP configuration locations and formats (.vscode/mcp.json vs .mcp.json vs user profile), Agent Host forwarding, Agent Skills and custom agent discovery, slash commands, trust and sandboxing, and the relevant settings. Use when configuring MCP servers, skills, or custom agents in VS Code, or debugging why VS Code does not see them.
license: MIT
metadata:
  category: tooling
  platform: vscode
---

# VS Code (IDE host for agents)

Use this skill when the task involves **VS Code's own agent customizations**: where it reads
MCP servers, skills, and custom agents, and how those differ from the Freebuff/Codebuff
project files.

- Freebuff's project files (`.agents/mcp.json`, `.agents/skills/`): use the **freebuff** skill.
- The Codebuff framework/CLI: use the **codebuff** skill.

## 1. MCP configuration locations

| Scope | File | Top-level key |
|-------|------|---------------|
| Workspace (VS Code format) | `.vscode/mcp.json` | `servers` |
| Workspace (portable) | `.mcp.json` at repo root | `mcpServers` |
| User profile | MCP: Open User Configuration -> user `mcp.json` | `servers` |
| Agent Host portable | `~/.copilot/mcp-config.json` | (Agent Host reads natively) |

Key gotcha: VS Code's `.vscode/mcp.json` uses a top-level **`servers`** object, while the
portable `.mcp.json` and Freebuff's `.agents/mcp.json` use **`mcpServers`**. Do not copy one
format into the other unchanged.

Agent Host sessions (for example Copilot) do **not** read `.vscode/mcp.json` directly; VS
Code forwards eligible servers, but only `.mcp.json` and the user `~/.copilot/mcp-config.json`
are read natively. For portable config, prefer `.mcp.json` or the user file.

Example `.vscode/mcp.json`:

```json
{
  "servers": {
    "Resonance7-sqlite": {
      "type": "stdio",
      "command": "C:\\Program Files\\nodejs\\node.exe",
      "args": ["C:\\path\\to\\repo\\library\\tools\\mcp_sqlite_server\\src\\server.js"]
    }
  }
}
```

## 2. Agent Skills in VS Code

Skill folders contain `SKILL.md` and are discovered from:

- Project: `.github/skills/`, `.claude/skills/`, `.agents/skills/`
- Personal: `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/`

So this repo's `.agents/skills/` are picked up by both Freebuff and VS Code. Skills become
slash commands (`/<name>`) and can auto-load when relevant.

Frontmatter for VS Code: `name` (must match the directory, lowercase/hyphens, max 64) and
`description` required; optional `argument-hint`, `user-invocable`, `disable-model-invocation`,
and experimental `context: fork`. Details in `reference.md`.

## 3. Custom agents

Custom agents are `.agent.md` Markdown files (YAML frontmatter + body):

- Workspace: `.github/agents/` (any `.md` here is treated as an agent), or `.claude/agents/`
- User: `~/.copilot/agents` or `~/.claude/agents`

Frontmatter can set `description`, `name`, `tools`, `agents` (subagents), `model`,
`user-invocable`, `disable-model-invocation`, `target`, `handoffs`, and preview `hooks`.

## 4. Slash commands and editor commands

| What | How |
|------|-----|
| Manage all customizations | Command Palette: `Chat: Open Customizations` |
| Skills menu | Type `/skills` in chat |
| Generate a skill | Type `/create-skill` (Local harness) |
| Generate an agent | Type `/create-agent` (Local harness) |
| Open user MCP config | Command Palette: `MCP: Open User Configuration` |
| List/stop/start MCP servers | Command Palette: `MCP: List Servers` |
| Add a server (guided) | Command Palette: `MCP: Add Server` |
| Add a server (CLI) | `code --add-mcp '{"name":"s","command":"...","args":[...]}'` |

## 5. Trust and sandboxing

- Workspace MCP servers inherit **Workspace Trust**. In restricted mode, `.vscode/mcp.json`
  and root `.mcp.json` servers do not start.
- Servers from other sources get a separate trust prompt; reset with `MCP: Reset Trust`.
- Sandboxing (`"sandboxEnabled": true`) is macOS/Linux only; **not available on Windows**.

## 6. This workspace

- `.vscode/` is **gitignored** (machine-local settings and MCP config).
- The project MCP server key is `Resonance7-sqlite`; default DB alias `session_logs`.
- There is no committed `.vscode/mcp.json`; generate Freebuff config with
  `python library/tools/scripts/setup_database.py`, and add a VS Code copy manually if
  Copilot also needs the server.

## 7. Sources

- MCP in VS Code: https://code.visualstudio.com/docs/agent-customization/mcp-servers
- Agent Skills: https://code.visualstudio.com/docs/agent-customization/agent-skills
- Custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
