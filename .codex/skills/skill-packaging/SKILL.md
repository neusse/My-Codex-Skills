---
name: skill-packaging
description: Use when creating, reviewing, or migrating Codex skills in a repository. Package each skill under .codex/skills/<skill-name>/SKILL.md, keep frontmatter trigger-focused, avoid prompt-conflict language, and move bulky examples or reference material out of the main skill file.
---

# Skill Packaging

Package skills so Codex can actually discover and use them well.

## Required Layout

Each project skill should live at:

`.codex/skills/<skill-name>/SKILL.md`

Use one folder per skill and the exact filename `SKILL.md`.

## Frontmatter Rules

- Include `name`
- Include `description`
- Make the description do real trigger work:
  - what the skill does
  - when to use it
  - useful boundaries when relevant

## Body Rules

- Keep the body operational and concise.
- Prefer procedure over theory.
- Make the skill standalone when possible.
- Do not claim the skill can override higher-priority instructions.
- Avoid references to non-existent helper skills.

## Good Packaging Hygiene

- Use lowercase hyphenated skill names.
- Avoid duplicate skill names across project and user scope unless intentional.
- Move long examples, templates, or reference material into `references/`.
- Add scripts or assets only when they meaningfully reduce repeated work.

## Review Checklist

- Canonical path and filename
- Valid frontmatter
- Trigger description is narrow enough
- No dead-end references
- No prompt-conflict language
- No unnecessary bulk in `SKILL.md`
