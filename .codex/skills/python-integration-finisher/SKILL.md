---
name: python-integration-finisher
description: Integrate completed Python modules into a functional application. Use when Codex needs to wire modules together, finalize configuration, align data flow, and verify end-to-end behavior.
---

# Python Integration Finisher

## Workflow

1. Collect integration inputs: architecture contracts, roadmap milestones, and implemented module outputs.
2. Identify integration points across modules.
3. Wire dependencies and configuration boundaries.
4. Implement glue code and adapters where needed.
5. Add integration tests for critical user flows.
6. Validate startup, shutdown, and failure handling.
7. Validate at least one real user invocation command from project docs.
8. Produce a final integration report and remaining risks.

## Output Template

- Integration Scope
- Input Artifacts Used
- Wiring Changes
- Config and Environment Changes
- Integration Tests
- End-to-End Validation Result
- Remaining Risks

## Quality Bar

- No hidden coupling across modules.
- Clear config ownership and defaults.
- Integration tests cover at least one happy path and one failure path.
- Project docs must include at least one verified run command that works as written.
