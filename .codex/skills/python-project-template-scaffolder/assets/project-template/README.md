# {{PROJECT_NAME}}

Created on {{DATE}} using `python-project-template-scaffolder`.

## Purpose

Describe the product goal, target users, and success metrics.

## Project Layout

- `src/{{PACKAGE_NAME}}/`: application package code
- `tests/`: automated tests
- `Documents/`: planning and execution artifacts for workflow skills

## Quick Start

1. Create environment:
   `python -m venv .venv`
2. Activate and install:
   `pip install -e .[dev]`
3. Run tests:
   `pytest`
4. Verify app entrypoint command(s):
   `python -m {{PACKAGE_NAME}}.main --help`

If you document direct script execution, verify it exactly as documented (example):
`python src/{{PACKAGE_NAME}}/main.py --help`

## Recommended Skill Flow

Choose one of these two tracks:

1. Spec-first (recommended for this skill pack contract):
   `00-project-brief` -> `fsd-writer` -> `python-requirements-author` -> `python-architecture-designer` -> `python-roadmap-planner` -> implementation/integration/testing/gates/release docs.
2. Requirements-first (valid alternative):
   `00-project-brief` -> `python-requirements-author` -> `fsd-writer` (evolve FSD from requirements) -> `python-architecture-designer` -> remaining phases.

Use spec-first when possible because `python-requirements-author` is designed to normalize an existing FSD into implementation-ready requirements.

## Definition of Ready

- Problem statement and users are defined.
- Scope constraints are documented.
- Initial risks are logged in `Documents/10-traceability-matrix.md`.
