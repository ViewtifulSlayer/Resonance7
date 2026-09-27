---
name: skill-authoring
description: How to write and review agent skills - SKILL.md structure, YAML frontmatter, naming rules, writing a good description, companion reference.md and resource files, and cross-agent portability. Use when creating a new skill, editing an existing one, or reviewing skill quality.
license: MIT
metadata:
  category: documentation
  topic: skills
---

# Skill authoring

Use this skill when **creating, editing, or reviewing a skill** (a `.agents/skills/<name>/`
package). A skill is a folder of instructions the agent loads on demand; the entry point is
always `SKILL.md`.

Plain (non-skill) documentation belongs in `library/docs/` or a README, not in a skill.

## 1. Anatomy

```
.agents/skills/my-skill/
  SKILL.md        # required; frontmatter + instructions
  reference.md    # optional; deep detail loaded only when referenced
  *.py, *.json    # optional; scripts, templates, examples
```

Keep `SKILL.md` focused and skimmable. Move long tables, background, and edge cases into
`reference.md` (or another resource file) and link to it.

## 2. Frontmatter

```markdown
---
name: my-skill
description: What the skill does and exactly when to load it. Name the tasks and triggers.
license: MIT
metadata:
  category: tooling
---
```

| Field | Required | Rule |
|-------|----------|------|
| `name` | Yes | Lowercase letters, digits, hyphens; max 64; must equal the directory name; no leading/trailing/consecutive hyphens |
| `description` | Yes | 1-1024 chars; drives auto-load matching |
| `license` | No | e.g. `MIT` |
| `metadata` | No | key/value tags for organization |

Do not add namespace prefixes (`myorg/skill` or `myorg:skill`) to `name` - they cause the
skill to silently fail to load.

## 3. Write the description for discovery

The description is the only text the agent sees before deciding to load the skill. Make it
specific:

- Good: "How to write and review agent skills - SKILL.md structure, frontmatter, naming, and companion files."
- Bad: "Skill stuff."

Name the capability and the trigger contexts, then stop.

## 4. Body structure

Recommended sections, in this order:

1. One line on what the skill is and when to use it.
2. **What to use instead** when the task is out of scope (route to sibling skills).
3. The procedure or knowledge, as numbered steps or short tables.
4. A checklist for verification.
5. Sources (URLs) for any external facts.

Write instructions, not prose. Prefer tables and explicit commands.

## 5. Companion files

Reference resource files from `SKILL.md` with relative Markdown links or `#file:./name`
notation, for example `[spec tables](./reference.md)`. Agents load a resource only when the
instructions reference it, so unreferenced files are ignored.

## 6. Conventions in this repo

- ASCII punctuation only (see the **markdown-punctuation** skill): hyphens, not en/em dashes;
  `- [x]` markers, not emoji.
- Cite sources for platform facts; do not hardcode volatile values (model names, limits).
- Keep `AGENTS.md` thin; put durable protocol in `library/agent_foundation.json` and detail
  in skills.

## 7. Checklist

- [ ] Directory name equals the frontmatter `name`, and the name is valid.
- [ ] `description` names both the capability and when to invoke it.
- [ ] `SKILL.md` is focused; long detail is in a referenced companion file.
- [ ] Any companion file is referenced from `SKILL.md`.
- [ ] ASCII-only punctuation; sources included.
- [ ] Verified the skill loads (slash command or `skill` tool) after a restart.

## 8. Sources

- Codebuff skills: https://www.codebuff.com/docs/tips/skills
- VS Code Agent Skills: https://code.visualstudio.com/docs/agent-customization/agent-skills
- Full spec tables: `reference.md`
