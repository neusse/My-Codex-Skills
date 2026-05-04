---
name: python-roadmap-planner
description: Convert architecture into a Functional Module Roadmap (FMR) for Python delivery. Use when Codex needs a milestone-based execution plan with dependency ordering, task granularity, and verification gates.
---

# Python Roadmap Planner

## Workflow

1. List modules from architecture and classify by criticality and user/business value.
2. Build dependency graph and identify critical path.
3. Split work into milestones and deliverable increments.
4. Define task-level deliverables for each module.
5. Attach test/verification gates to each milestone.
6. Define rollback or fallback strategy for risky milestones.
7. Preserve traceability to high-priority requirements/FSD capabilities per milestone.

## Output Template

- Delivery Strategy
- Module Inventory
- Dependency Graph (text list)
- Milestones
- Per-Milestone Tasks
- Verification Gates
- Critical Path
- Requirement/FSD Traceability by Milestone
- Risks and Mitigations

## Quality Bar

- Each task should fit in a short implementation cycle.
- Dependencies must be explicit, no hidden prerequisites.
- Every milestone must produce demonstrable working behavior.
- Milestones should cite source FR/NFR identifiers when available.
