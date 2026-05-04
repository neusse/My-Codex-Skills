---
name: python-architecture-designer
description: Transform approved Python requirements into technical architecture and module design. Use when Codex needs to define module boundaries, interfaces, data flow, storage, API contracts, and key engineering decisions before implementation.
---

# Python Architecture Designer

## Workflow

1. Read requirements and any upstream FSD (prefer `Documents/*-fsd.md`) and restate architectural drivers.
2. Choose system style (monolith, modular monolith, services) with rationale.
3. Define module boundaries and responsibilities.
4. Specify API contracts and inter-module interfaces.
5. Define data model and persistence strategy.
6. Record architecture decisions and tradeoffs (ADRs).
7. Map requirements/FSD capabilities to modules to ensure full coverage.

## Output Template

- Architecture Drivers
- Context Diagram (text form)
- Module Breakdown
- Interface Contracts
- Data Model
- Cross-Cutting Concerns (auth, logging, errors, config)
- ADR List
- Requirement-to-Module Traceability
- FSD-to-Architecture Traceability (if FSD exists)

## Quality Bar

- No module should have ambiguous ownership.
- Explicitly describe failure modes and error propagation.
- Keep interfaces stable and implementation details hidden.
- Flag technical risk hotspots early.
- Keep cross-references to upstream FR/NFR IDs where available.
