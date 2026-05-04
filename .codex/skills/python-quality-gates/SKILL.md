---
name: python-quality-gates
description: Define enforceable Python quality gates for local and CI workflows. Use when Codex needs to configure linting, typing, tests, formatting, and merge-blocking policies.
---

# Python Quality Gates

## Workflow

1. Define minimum merge gates (lint, type-check, tests).
2. Configure toolchain: ruff, mypy, pytest, pre-commit.
3. Set pass/fail thresholds and exception policy.
4. Define fast local checks vs full CI checks.
5. Document gate ownership and remediation expectations.

## Baseline Gates

- `ruff check .`
- `mypy .`
- `pytest -q`
- `python -m <package>.main --help` (or documented equivalent entrypoint smoke test)

For projects that document direct script execution, also gate:

- `python src/<package>/main.py --help`

## Output Template

- Gate Matrix
- Tool Config Decisions
- Local Developer Workflow
- CI Workflow
- Exception/Override Policy

## Quality Bar

- Gate failures must block merge by default.
- Exceptions require explicit reason and follow-up owner.
- Keep local feedback fast to encourage compliance.
