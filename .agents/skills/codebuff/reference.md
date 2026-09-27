# Codebuff reference

Companion detail for the **codebuff** skill. Codebuff is the open multi-agent framework
behind Freebuff.

## Command and config quick reference

| Item | Value |
|------|-------|
| Install | `npm install -g codebuff` |
| Run | `codebuff` (from the project directory) |
| Scaffold | `/init` inside the CLI (creates `.agents/` and `knowledge.md`) |
| Modes | Free, Max, Plan |
| CLI binary cache | `~/.config/manicode/codebuff` (Windows: `%USERPROFILE%\.config\manicode\codebuff`) |
| SDK | `@codebuff/sdk` (embedding custom agents) |

## Context file precedence (home directory)

Only the first file found is used; matching is case-insensitive:

1. `~/.knowledge.md`
2. `~/.AGENTS.md`
3. `~/.CLAUDE.md`

Project context: root `knowledge.md`, optional subdirectory `knowledge.md`, plus root
`AGENTS.md` / `CLAUDE.md`.

## Skill discovery order

Later entries override earlier ones with the same `name`:

1. `~/.claude/skills/`
2. `~/.agents/skills/`
3. `.claude/skills/`
4. `.agents/skills/` (project, highest)

## SKILL.md frontmatter (shared spec)

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | 1-64 chars, lowercase letters/digits/hyphens, must match the directory name, no leading/trailing/consecutive hyphens |
| `description` | Yes | 1-1024 chars; drives browsing and auto-load matching |
| `license` | No | e.g. `MIT` |
| `metadata` | No | key/value categorization (e.g. `category`, `language`) |

## Relationship to Freebuff

- Freebuff is built on Codebuff; Codebuff provides orchestration, tools, and the SDK.
- The skills/knowledge context model is shared between the two products.
- Freebuff adds a curated free model catalog and the `.agents/mcp.json` Freebuff loader
  behavior; Codebuff is the framework underneath.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| CLI fails to start | Missing Node/npm | Install Node (includes npm) |
| Stale or corrupt binary | Cached download | Delete `~/.config/manicode/codebuff`; restart |
| `/init` did not create context | Ran outside a project dir | Re-run from the repo root |
| Custom agent work not starting | Skipped `/init` | Run `/init`, then author the agent |

## Sources

- https://www.codebuff.com/docs - quick start, `/init`, binary cache path, troubleshooting
- https://www.codebuff.com/docs/tips/knowledge-files - knowledge.md, subdirectory files, home precedence
- https://www.codebuff.com/docs/tips/skills - skill layout, frontmatter, name rules, discovery order
- https://github.com/CodebuffAI/freebuff - "Built on Codebuff", `@codebuff/sdk`, monorepo (Bun)
