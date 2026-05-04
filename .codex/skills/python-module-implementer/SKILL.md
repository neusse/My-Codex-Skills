---
name: python-module-implementer
description: Implement a single Python module from roadmap/design specs. Use when Codex needs to build production code with tests for one module while preserving interface contracts and coding standards.
---

# Python Module Implementer

## Workflow

1. Read module spec, interfaces, acceptance criteria, and linked requirements/FSD traceability.
2. Implement minimal vertical slice first.
3. Add unit tests and error-path tests.
4. Add input validation, typed interfaces, and logging hooks.
5. Document module entry points and assumptions.
6. Validate declared execution entrypoint(s) from a user perspective (for example `python -m package.main` and, if claimed, `python src/package/main.py`).
7. Run local quality checks and report outcomes.

## Implementation Rules

- Preserve declared interfaces unless explicitly approved.
- Keep module cohesive; avoid cross-module leakage.
- Add tests for edge cases and failure paths.
- Prefer simple, explicit logic over clever abstractions.
- Do not claim a run mode in README/docs unless you executed that exact command successfully.

## Output Template

- Input Artifacts Used
- Implemented Files
- Behavior Implemented
- Tests Added
- Validation Commands Run
- Known Gaps
