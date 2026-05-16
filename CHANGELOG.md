# Changelog

All notable skill-repository changes are documented in this file.

## 2026-05-16 - Render Discord text from Markdown

### Changed
- `save-codex-exchange`: Replaced the initial direct Discord text converter with a fixed-width Markdown renderer that handles headings, paragraphs, lists, blockquotes, fenced code, links, and wrapped tables before writing Discord-friendly text output (`.codex/skills/save-codex-exchange/scripts/save_last_prompt.py`).
- `save-codex-exchange`: Documented that Discord text output is rendered from the Markdown archive and added the `--width` option to the usage example (`.codex/skills/save-codex-exchange/SKILL.md`).

## 2026-05-16 - Add Discord text output for saved exchanges

### Added
- `save-codex-exchange`: Added `--format discord-text` output for Discord-readable text files with ASCII table conversion and preserved fenced code blocks (`.codex/skills/save-codex-exchange/scripts/save_last_prompt.py`).

### Changed
- `save-codex-exchange`: Updated skill instructions with Discord upload guidance and the new text output example (`.codex/skills/save-codex-exchange/SKILL.md`).

## 2026-05-16 - Refine save-codex-exchange output headings

### Changed
- `save-codex-exchange`: Changed saved Markdown section headings to `Prompt:` and `Response:` and aligned the skill instructions with the helper output (`.codex/skills/save-codex-exchange/scripts/save_last_prompt.py`, `.codex/skills/save-codex-exchange/SKILL.md`).

## 2026-05-16 - Add and validate utility skills

### Added
- `image-enhancer`: Added concise Codex skill for image and screenshot enhancement workflows (`.codex/skills/image-enhancer/SKILL.md`).
- `invoice-organizer`: Added concise Codex skill for invoice and receipt organization workflows (`.codex/skills/invoice-organizer/SKILL.md`).
- `save-codex-exchange`: Added Codex skill and helper script for saving the previous prompt/result exchange to Markdown (`.codex/skills/save-codex-exchange/SKILL.md`, `.codex/skills/save-codex-exchange/scripts/save_last_prompt.py`).
- `tailored-resume-generator`: Added concise Codex skill for truthful job-targeted resume tailoring (`.codex/skills/tailored-resume-generator/SKILL.md`).

### Changed
- Approved skills table: Added the four validated utility skills (`README.md`).
- Inventory table: Added the four validated utility skills and refreshed the generated date (`SKILLS_INVENTORY.md`).
- Project handoff: Refreshed repo state, validation status, approved skill list, and resume commands (`HANDOFF.md`).

## 2026-05-12 - Add requirements-clarity skill

### Added
- `requirements-clarity`: Added Codex-compatible clarification workflow skill (`.codex/skills/requirements-clarity/SKILL.md`).
- `requirements-clarity` PRD template: Added reference template for durable requirements output (`.codex/skills/requirements-clarity/references/prd-template.md`).

### Changed
- Approved skills table: Added `requirements-clarity` row with one-line description (`README.md`).
- Inventory table: Added `requirements-clarity` row with matching description (`SKILLS_INVENTORY.md`).

## 2026-05-04 - Add news-scout skill

### Added
- `news-scout`: Added new skill for recent news scouting and high-signal summarization (`.codex/skills/news-scout/SKILL.md`).

### Changed
- Approved skills table: Added `news-scout` row with one-line description (`README.md`).
- Inventory table: Added `news-scout` row with matching description (`SKILLS_INVENTORY.md`).

## 2026-05-04 - Initialize changelog automation policy

### Added
- Repository policy: Added `AGENTS.md` with required changelog-update behavior for all skill lifecycle changes (`AGENTS.md`).
- Changelog baseline: Added this changelog file and entry template workflow (`CHANGELOG.md`).
