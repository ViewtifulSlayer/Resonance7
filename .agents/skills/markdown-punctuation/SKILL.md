---
name: markdown-punctuation
description: Teaches agents to use ASCII-only punctuation in markdown for tooling compatibility and reliable search/replace. Use when editing or creating .md files, session logs, or documentation in the workspace.
---

# Markdown Punctuation (ASCII-Only)

When editing or creating markdown files (`.md`), use **ASCII punctuation only**. This keeps content searchable, diff-friendly, and compatible with search/replace and scripts.

## Why ASCII-Only

- **Curly/smart quotes** (`"` `"` `'`) are not recognized as string delimiters in code or by many tools; they break search/replace and can cause subtle bugs when text is pasted into code or configs.
- **En-dash** (`–` U+2013) and **em-dash** (`—` U+2014) are typographically correct in prose but often normalize to hyphen in tooling; using hyphen-minus everywhere avoids mismatches and failed replaces.
- Session logs and project docs are often edited by agents or scripts; ASCII ensures consistent behavior.

## Rules

| Use case | Use (ASCII) | Avoid (Unicode) |
|----------|-------------|-----------------|
| Double quotes | `"` (U+0022) | `"` `"` (U+201C, U+201D) |
| Single quote / apostrophe | `'` (U+0027) | `'` `'` (U+2018, U+2019) |
| Hyphen, minus, ranges | `-` (U+002D hyphen-minus) | `–` en-dash, `—` em-dash, `−` minus (U+2013, U+2014, U+2212) |
| Ellipsis | `...` (three periods) | `…` (U+2026) optional; ASCII preferred for consistency |
| Checkboxes / task lists | `- [ ]` / `- [x]` | `☐` `☑` `✓` `✅` `⬜` (or other emoji/symbol checkboxes) |
| Arrows | `->` | `→` (and other Unicode arrows) |

## In Practice

- **Quoted phrases**: Write `"forgot X ability"` and `'game's'` with straight `"` and `'`.
- **Ranges**: Write `$0224-$032E` and `2025-2027` with hyphen-minus, not en-dash.
- **Compound words and phrasal adjectives**: Use hyphen-minus (e.g. `cross-bank`, `one-off`).
- **Breaks in thought**: Use spaces and commas, or parentheses, instead of em-dash; or use ` - ` (space-hyphen-space) if a dash is needed.

## Check Before Saving

Before saving changes to a markdown file, scan for:

- Curly double quotes or apostrophes (they look slightly curved in some fonts).
- En-dash or em-dash in ranges or compound modifiers.
- Unicode checkbox symbols / emoji checkmarks.
- Unicode arrows.

If found, replace with the ASCII equivalent so future edits and tooling behave correctly.
