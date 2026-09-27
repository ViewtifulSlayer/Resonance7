# Skill authoring reference

Companion detail for the **skill-authoring** skill. The Agent Skills folder format is a
cross-agent standard; the discovery locations differ by host.

## Discovery order (highest overrides lower, per host)

Codebuff / Freebuff:

1. `~/.claude/skills/`
2. `~/.agents/skills/`
3. `.claude/skills/`
4. `.agents/skills/` (project, highest)

VS Code (Copilot):

- Project: `.github/skills/`, `.claude/skills/`, `.agents/skills/`
- Personal: `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/`

`.agents/skills/` is the shared, host-neutral location used by this repo.

## Frontmatter fields

Core (Codebuff/Freebuff and the shared spec):

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | 1-64 chars; lowercase letters/digits/hyphens; equals the directory; no leading/trailing/consecutive hyphens |
| `description` | Yes | 1-1024 chars |
| `license` | No | e.g. `MIT` |
| `metadata` | No | free-form key/value pairs |

VS Code (Copilot) adds:

| Field | Required | Notes |
|-------|----------|-------|
| `argument-hint` | No | hint shown for the slash command |
| `user-invocable` | No | default true; false hides it from the `/` menu |
| `disable-model-invocation` | No | default false; true makes it on-demand only |
| `context` | No | experimental; `fork` runs the skill in a subagent context |

## Name validation examples

Valid: `git-release`, `api-design`, `review2`, `deploy-prod`.
Invalid: `Git-Release`, `my--skill`, `-skill`, `skill-`, `myorg/skill`, `myorg:skill`.

## Progressive loading

1. **Discovery**: only `name` and `description` are read.
2. **Instructions**: the `SKILL.md` body loads on a relevance match or manual invocation.
3. **Resources**: files referenced by the instructions load only as needed.

This is why descriptions matter more than the body for triggering, and why large detail
belongs in companion files.

## Minimal templates

SKILL.md:

```markdown
---
name: my-skill
description: What it does and when to invoke it.
---

# My Skill

Use this when ...

## Steps
1. ...
```

reference.md: plain Markdown, no frontmatter required. Link it from `SKILL.md`.

## Review checklist (deeper)

- Name matches directory and passes validation; no namespace prefixes.
- Description is specific and includes trigger contexts.
- Scope is a single capability; sibling skills cover adjacent tasks.
- Body has steps/tables, not prose; verification checklist present.
- Companion files are referenced; relative links use `/` separators.
- External facts cite a source URL; volatile values are avoided.
- Skill loads after restart (or confirm the loader picked it up).

## Common failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Not listed | Wrong folder depth, name mismatch, invalid characters | Fix path/name; restart host |
| Never auto-loads | Vague description | Rewrite description with triggers |
| Loads but ignores resources | Companion file not referenced | Link it from `SKILL.md` |
| Silently absent | Namespace prefix in `name` | Remove prefix |

## Sources

- https://www.codebuff.com/docs/tips/skills - Codebuff skill layout, frontmatter, name rules, discovery
- https://code.visualstudio.com/docs/agent-customization/agent-skills - VS Code locations, frontmatter, loading
