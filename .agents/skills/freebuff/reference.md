# Freebuff reference

Companion detail for the **freebuff** skill. Verified against the sources listed at the
bottom; platform facts change, so re-check before relying on volatile items (models, limits).

## Discovery order: skills (Codebuff/Freebuff)

Later entries override earlier ones with the same `name`:

1. `~/.claude/skills/` (global, Claude Code compatible)
2. `~/.agents/skills/` (global)
3. `.claude/skills/` (project, Claude Code compatible)
4. `.agents/skills/` (project, highest priority)

VS Code adds its own locations (see the **vscode** skill): `.github/skills/`,
`~/.copilot/skills/`.

## Discovery order: knowledge / context files (home directory)

Only the first file found is used; matching is case-insensitive:

1. `~/.knowledge.md` (highest)
2. `~/.AGENTS.md`
3. `~/.CLAUDE.md`

Project-side context files: `knowledge.md` at the repo root, plus optional `knowledge.md`
files in subdirectories. `AGENTS.md` and `CLAUDE.md` at the project root are also read.
Project knowledge adds to, and can override, home preferences.

## SKILL.md frontmatter

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | 1-64 chars, lowercase letters/digits/hyphens, must match directory, no leading/trailing/consecutive hyphens |
| `description` | Yes | 1-1024 chars; shown when browsing and used for auto-load matching |
| `license` | No | e.g. `MIT` |
| `metadata` | No | Free-form key/value pairs for categorization |

Valid names: `git-release`, `api-design`, `review2`, `deploy-prod`.
Invalid names: `Git-Release`, `my--skill`, `-skill`, `skill-`.

Minimal example:

```markdown
---
name: my-skill
description: What it does and when to invoke it
---

# My Skill
Instructions go here.
```

## Freebuff vs Codebuff config paths (Windows)

| Item | Path |
|------|------|
| Freebuff binary/config | `C:\Users\<you>\.config\manicode\freebuff.exe` |
| Codebuff binary | `~/.config/manicode/codebuff` |
| Global project MCP | `~/.agents/mcp.json` |
| Global project skills | `~/.agents/skills/` |
| Trusted `.agents` dirs | `C:\Users\<you>\.config\manicode\trusted-agent-dirs.json` |

The `.agents/mcp.json` search paths and merge behavior were confirmed directly in the
Freebuff binary during session `20260922-01`.

## This workspace's MCP entry

`.agents/mcp.json` (gitignored) holds one managed server:

```json
{
  "mcpServers": {
    "Resonance7-sqlite": {
      "command": "<abs path to node.exe>",
      "args": ["<abs path>\\library\\tools\\mcp_sqlite_server\\src\\server.js"],
      "env": { "DEFAULT_DB_PATH": "<abs path>\\library\\databases\\db\\session_logs.db" }
    }
  }
}
```

`setup_database.py` owns only the `Resonance7-sqlite` key and preserves other server
blocks. Rerun it after changing Node paths or moving the repo.

## `--global-agents` semantics

- Walks the workspace `.agents/` tree (excluding the workspace `mcp.json`).
- Copies files that do not exist under `~/.agents/`.
- If a destination exists, it is preserved and a warning is printed (counted as a conflict).
- An existing global `mcp.json` is always preserved, never overwritten.

## Capability snapshot (dated, volatile)

- Freebuff products: CLI, Desktop, Web, Cloud, Chat.
- Access tiers and the model catalog change frequently; see the Freebuff repo/model docs.
- The Freebuff binary is model-agnostic; the active model is selected per session.
- Session/credit limits depend on tier and region.

Do not encode specific model names or daily session counts into repository docs.

## Common failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Skill absent from `/skill:` menu | Wrong directory depth, name mismatch, or invalid name | Fix path/name; restart Freebuff |
| Skill present but never auto-loads | Vague `description` | Make the description name the task and trigger |
| MCP server absent | Not launched from repo root; malformed JSON; missing `mcpServers` key | Start from root; validate JSON; restart |
| MCP tools work but wrong data | Default DB guess | Pass `database_path` explicitly |
| Global config overwritten | A tool used copy (not copy-if-missing) | Use `--global-agents`, which never overwrites |

## Sources

- https://www.codebuff.com/docs/tips/skills - skill directories, frontmatter, name rules, discovery order
- https://www.codebuff.com/docs/tips/knowledge-files - knowledge files and home precedence
- https://github.com/CodebuffAI/freebuff - product overview, models, access
- https://freebuff.com/ - product site
- https://github.com/CodebuffAI/freebuff/issues/957 - MCP config loaded once at boot from `process.cwd()`
- Session `20260922-01` - loader schema and `.agents/mcp.json` search paths confirmed in the binary
