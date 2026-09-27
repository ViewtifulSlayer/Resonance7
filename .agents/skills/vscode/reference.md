# VS Code reference

Companion detail for the **vscode** skill.

## MCP config: formats and keys

| Location | Key | Notes |
|----------|-----|-------|
| `.vscode/mcp.json` | `servers` | VS Code workspace format; per-workspace |
| `.mcp.json` (repo root) | `mcpServers` | Portable; works across compatible tools |
| User profile `mcp.json` | `servers` | Via `MCP: Open User Configuration` |
| `~/.copilot/mcp-config.json` | vendor format | Read natively by Agent Host |
| `devcontainer.json` | `customizations.vscode.mcp.servers` | Dev Containers |

Server fields include `type` (`stdio`, `http`), `command`, `args`, `env`, and
`sandboxEnabled`. Remote servers use `type: "http"` with `url`.

## Skills locations (VS Code)

| Scope | Locations |
|-------|-----------|
| Project | `.github/skills/`, `.claude/skills/`, `.agents/skills/` |
| Personal | `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/` |

VS Code skill frontmatter:

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | lowercase letters/digits/hyphens, must match directory, max 64 |
| `description` | Yes | max 1024; drives relevance matching |
| `argument-hint` | No | hint shown for the slash command |
| `user-invocable` | No | default true; set false to hide from `/` menu |
| `disable-model-invocation` | No | default false; set true for on-demand only |
| `context` | No | experimental; `fork` runs the skill in a subagent context |

Loading is progressive: (1) name and description, (2) SKILL.md body on match or slash
invocation, (3) referenced resource files only as needed. Reference extra files with
relative Markdown links or `#file:./name` so they are picked up.

## Custom agents (VS Code)

| Scope | Locations |
|-------|-----------|
| Workspace | `.github/agents/`, `.claude/agents/` |
| User | `~/.copilot/agents`, `~/.claude/agents` |

Frontmatter fields include `description`, `name`, `argument-hint`, `tools`, `agents`,
`model`, `user-invocable`, `disable-model-invocation`, `target`, `mcp-servers`, `handoffs`,
and preview `hooks`.

## Relevant settings

| Setting | Purpose |
|---------|---------|
| `chat.mcp.autostart` | `never` / `onlyNew` / `newAndOutdated` (default) - when VS Code starts MCP servers |
| `chat.mcp.discovery.enabled` | Reuse MCP config from Claude Desktop, Copilot CLI, Cursor, Windsurf |
| `chat.useCustomizationsInParentRepositories` | Discover skills/agents from a parent repo in a monorepo |
| `chat.agentSkillsLocations` | Deprecated; use supported default locations |
| `github.copilot.chat.skillTool.enabled` | Required to run skills in a forked context |

## Trust and behavior notes

- Workspace MCP servers inherit **Workspace Trust**; restricted mode blocks them.
- Agent Host does not read `.vscode/mcp.json` directly; it reads `.mcp.json` and
  `~/.copilot/mcp-config.json` and receives forwarded config from VS Code.
- Sandboxing local stdio servers requires macOS/Linux; **Windows is unsupported**.
- `MCP: Reset Trust` clears separate MCP trust decisions (does not change Workspace Trust).

## Cross-check with this repo

- `.agents/mcp.json` uses `mcpServers`; a VS Code `.vscode/mcp.json` would use `servers`.
- `.vscode/` is gitignored here, so any VS Code MCP/settings file is machine-local.
- `.agents/skills/` is read by both Freebuff and VS Code (shared location).

## Sources

- https://code.visualstudio.com/docs/agent-customization/mcp-servers - config locations, formats, trust, sandbox, settings
- https://code.visualstudio.com/docs/agent-customization/agent-skills - skill locations, frontmatter, loading, commands
- https://code.visualstudio.com/docs/agent-customization/custom-agents - `.agent.md` locations and frontmatter
