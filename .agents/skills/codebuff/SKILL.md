---
name: codebuff
description: The Codebuff framework and CLI that Freebuff is built on - install and run steps, /init project setup, knowledge.md and AGENTS.md/CLAUDE.md context, the skills spec, custom agents, the SDK, config paths, and troubleshooting. Use when working with the Codebuff CLI, scaffolding project context, or building custom agents.
license: MIT
metadata:
  category: tooling
  platform: codebuff
---

# Codebuff (framework and CLI)

Use this skill when the task is about the **Codebuff framework or CLI**: installing and
running it, scaffolding a project with `/init`, how it loads context, or building custom
agents. Codebuff is the open multi-agent framework that **Freebuff is built on**.

- Hosting inside VS Code and IDE-side configuration: use the **vscode** skill.
- Freebuff product behavior and `.agents/mcp.json`: use the **freebuff** skill.

## 1. Install and run

```bash
npm install -g codebuff
cd /path/to/repo
codebuff
```

Node (which includes npm) is required. Modes include Free, Max, and Plan.

## 2. `/init` and project setup

Run `/init` inside Codebuff to scaffold project files. Useful for:

- **New projects** that lack an `AGENTS.md` or `CLAUDE.md` (Codebuff reads both).
- **Building custom agents** - `/init` is the documented first step.

`/init` creates `.agents/` and a `knowledge.md` describing build commands, structure, and
conventions.

## 3. Context files

- **`knowledge.md`** at the repo root captures facts not obvious from code: project goals,
  technical decisions, coding standards, pitfalls, build/deploy requirements, and
  verification commands to run after edits. "A few hundred lines is fine."
- Optional `knowledge.md` files in subdirectories keep context next to the code it
  describes (`backend/knowledge.md`, `frontend/knowledge.md`).
- Home-directory files, first match wins (case-insensitive): `~/.knowledge.md` >
  `~/.AGENTS.md` > `~/.CLAUDE.md`.
- Project knowledge files add to, and can override, home preferences.
- `AGENTS.md` and `CLAUDE.md` at the project root are read as context.

## 4. Skills

Codebuff loads on-demand skills from `.agents/skills/` (project) and `~/.agents/skills/`
(global), plus the `.claude/` equivalents. Each skill becomes a `/skill:<name>` command and
can be auto-loaded via the `skill` tool when its description matches.

Full discovery order and frontmatter rules are shared across the family - see the
**freebuff** skill and this skill's `reference.md`.

## 5. Custom agents and SDK

- `/init` is the starting point for authoring custom agents.
- To embed Codebuff agents in another application, use `@codebuff/sdk` (see the Codebuff
  documentation).
- Freebuff is a TypeScript monorepo built with Bun; it composes Codebuff agents, tools, and
  the SDK.

## 6. Troubleshooting

- Ensure Node and npm are installed.
- If the CLI misbehaves, delete the downloaded binary at `~/.config/manicode/codebuff`
  (Windows: `%USERPROFILE%\.config\manicode\codebuff`) and restart Codebuff.
- For the Freebuff client the equivalent binary is
  `~/.config/manicode/freebuff.exe`.

## 7. Sources

- Codebuff quick start / docs: https://www.codebuff.com/docs
- Knowledge files: https://www.codebuff.com/docs/tips/knowledge-files
- Skills: https://www.codebuff.com/docs/tips/skills
- Freebuff (built on Codebuff, SDK pointer): https://github.com/CodebuffAI/freebuff
