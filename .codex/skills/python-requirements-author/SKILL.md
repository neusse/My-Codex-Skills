---
name: python-requirements-author
description: Convert rough ideas into implementation-ready Python product requirements. Use when Codex needs to define scope, users, outcomes, constraints, acceptance criteria, and non-goals before design or coding.
---

# Python Requirements Author

## Workflow

1. Capture source inputs: rough idea, target user, and desired business/user outcome.
2. If an FSD exists (prefer `Documents/*-fsd.md` from `fsd-writer`), use it as the primary source and normalize it into explicit, testable requirements.
3. Define scope boundaries: in-scope, out-of-scope, assumptions, constraints.
4. Produce functional requirements as numbered statements.
5. Produce non-functional requirements (performance, security, reliability, compliance, cost).
6. Define acceptance criteria per major feature using testable statements.
7. Identify risks and unresolved decisions.
8. Output a build-ready requirements document with traceability to source input/FSD sections.

## Output Template

Use this exact section order:
- Source Inputs
- Problem Statement
- Users and Use Cases
- Goals and Non-Goals
- Functional Requirements
- Non-Functional Requirements
- Constraints and Assumptions
- Acceptance Criteria
- Risks and Open Questions
- Traceability Notes
- Definition of Done

## Quality Bar

- Every requirement must be testable.
- Avoid vague verbs like "support" without measurable behavior.
- Distinguish must-have vs nice-to-have.
- Call out unknowns explicitly; do not hide ambiguity.
- Preserve FR/NFR intent and numbering references from the FSD where practical.
