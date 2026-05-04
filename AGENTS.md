# AGENTS.md instructions for My-Codex-Skills

## Scope

These instructions apply to the entire repository.

## Primary Goal

Maintain this repo as the source of truth for personal Codex skills under `.codex/skills`, with a reliable, always-updated `CHANGELOG.md`.

## Required Behavior For Any Skill Change

When a skill is added, modified, renamed, moved, or deleted, the agent must update `CHANGELOG.md` in the same task before finishing.

Applies to:
- `.codex/skills/**`
- `templates/skill-template/**`
- scripts that affect skill creation/deployment/inventory
- inventory updates in `SKILLS_INVENTORY.md`

## Changelog Rules

1. Keep changelog file at repo root: `CHANGELOG.md`.
2. Use reverse chronological order (newest entries first).
3. Add one entry per user-request batch of related changes.
4. Entry must include:
   - Date (local): `YYYY-MM-DD`
   - Summary line
   - `Added`, `Changed`, `Removed` sections (include only sections used)
   - Explicit skill names and touched file paths
5. Never delete historical entries.
6. If no skill-related files changed, changelog update is not required.

## Entry Template

Use this structure for each entry:

```md
## YYYY-MM-DD - <short summary>

### Added
- <skill or file>: <what was added> (`<path>`)

### Changed
- <skill or file>: <what changed and why> (`<path>`)

### Removed
- <skill or file>: <what was removed> (`<path>`)
```

## Operational Notes

- Keep `README.md` and `SKILLS_INVENTORY.md` aligned with approved skills.
- Prefer deterministic file names for new assets and skills.
- Do not edit shipped/core Codex skills outside this repository.
