---
name: python-test-strategy
description: Build a Python test strategy aligned to architecture and risk. Use when Codex needs a practical test plan covering unit, integration, end-to-end, fixtures, data setup, and CI sequencing.
---

# Python Test Strategy

## Workflow

1. Identify risk areas and critical business flows.
2. Partition tests: unit, integration, end-to-end, contract, regression.
3. Define fixture/data strategy and environment setup.
4. Set coverage goals by module criticality.
5. Define CI execution order and failure policy.
6. Specify flakiness controls and test maintenance rules.

## Output Template

- Test Objectives
- Test Pyramid Allocation
- High-Risk Flows and Coverage
- Fixture/Data Strategy
- CI Test Stages
- Coverage Targets
- Flakiness Controls

## Quality Bar

- Focus on behavior, not implementation trivia.
- Keep tests deterministic and isolated.
- Include negative/error-path assertions.
