---
name: python-project-template-scaffolder
description: Scaffold a full Python project starter directory with execution-ready templates for workflow documents. Use when Codex needs to create a new project folder containing root artifacts, src/tests layout, and a Documents directory prefilled for fsd-writer plus python-requirements-author, python-architecture-designer, python-roadmap-planner, python-module-implementer, python-integration-finisher, python-test-strategy, python-quality-gates, and python-release-ops.
---

# Python Project Template Scaffolder

## Workflow

1. Capture required inputs:
- `project_name` (human readable)
- `package_name` (Python import-safe; default derived from project name)
- `destination_root` (where new folder should be created)

2. Run:
- `python scripts/scaffold_python_project.py --project-name "<project_name>" --destination-root "<destination_root>" --package-name "<package_name>"`
- If `--package-name` is omitted, script derives one.

3. Verify output includes:
- Root templates (`README.md`, `pyproject.toml`, `.gitignore`, `.env.example`)
- Code layout (`src/<package_name>/`, `tests/`)
- Skills handoff docs in `Documents/`

4. If destination already exists and overwrite is not explicitly requested, stop and ask.

## Generated Documents Mapping

`Documents/01-fsd-template.md` -> `fsd-writer` input/output handoff

`Documents/02-requirements.md` -> `python-requirements-author`

`Documents/03-architecture.md` -> `python-architecture-designer`

`Documents/04-roadmap.md` -> `python-roadmap-planner`

`Documents/05-module-implementation-log.md` -> `python-module-implementer`

`Documents/06-integration-checklist.md` -> `python-integration-finisher`

`Documents/07-test-strategy.md` -> `python-test-strategy`

`Documents/08-quality-gates.md` -> `python-quality-gates`

`Documents/09-release-ops.md` -> `python-release-ops`

`Documents/10-traceability-matrix.md` -> cross-phase traceability

## Notes

- Prefer this skill at project kickoff before module implementation.
- Preferred sequence is FSD -> requirements -> architecture; requirements-first is acceptable if `fsd-writer` is used in evolve mode after requirements.
- Keep template placeholders until project decisions are finalized.
