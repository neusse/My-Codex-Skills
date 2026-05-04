---
name: fsd-writer
description: >
  Generate or update a Functional Specification Document (FSD) in Markdown,
  especially for ESP32 and embedded projects. Turns rough project descriptions
  into structured FSDs with requirements, phases, interfaces, tests, and a
  mandatory traceability matrix. Use for "FSD", "functional spec",
  "specification document", "write FSD", "create FSD", "generate FSD",
  "update FSD", or "evolve FSD" requests.
---

# FSD Writer

Generate a new Functional Specification Document (FSD) from a rough description,
or update an existing FSD while preserving stable numbering and unaffected
content.

This skill is intended for Codex. Do not refer to non-Codex tools, slash
commands, or internal tool names in normal use.

## Quick Start

Use this skill when the user wants any of the following:

- A new FSD from an idea, sketch, codebase, or project brief
- An existing FSD updated with new requirements, constraints, or features
- A requirements-first spec with phases, interfaces, verification, and
  traceability

Default behavior:

1. Determine whether this is initial generation or evolve mode.
2. Gather only the minimum project context needed from the repo.
3. Resolve requirements intake from a project idea document if available.
4. Ask concise in-chat questions only when missing information would materially
   change the architecture or requirement set.
5. Write or update the Markdown file.

## Requirements Intake

Before drafting or editing an FSD, use a requirements-intake input.

Preferred input order:

1. User-provided requirements document path
2. `Documents/project-idea-description.md`
3. `docs/project-idea-description.md`
4. `project-idea-description.md`

If no intake document exists, create:

`Documents/project-idea-description.md`

from:

`references/project-idea-description-template.md`

Then ask the user to fill only missing architecture-critical fields. Do not
block on optional details.

Treat the intake document as the source of truth for:

- goals and scope
- users and workflows
- interfaces and integrations
- constraints and quality attributes
- explicit out-of-scope items

## Operating Modes

### Initial Generation

Use when no FSD exists yet or the user asks to create one from scratch.

Default output path if the user does not specify one:

`Documents/<project-name-kebab-case>-fsd.md`

Create `Documents/` if needed.

### Evolve Existing FSD

Use when the user provides an existing FSD path or asks to update one.

If no path is given, search in this order:

1. `Documents/*-fsd.md`
2. `Documents/*-FSD.md`
3. `docs/*-fsd.md`
4. project root `*-fsd.md`

When updating:

- Preserve unaffected sections verbatim where practical.
- Regenerate only the sections impacted by the delta.
- Keep requirement IDs stable unless the user explicitly asks to renumber.
- Always update tests and the traceability matrix when requirements change.

## Codex Workflow

### Repo Discovery

Before drafting the FSD, inspect the codebase when it exists.

Preferred commands:

- `rg --files` for structure discovery
- `rg -n "BLE|WiFi|MQTT|HTTP|REST|WebSocket|LoRa|OCPP|Modbus|OTA|NVS"` for
  protocols and integrations
- `Get-Content` or `sed -n` to read targeted config and source files

Look for:

- firmware and app entry points
- build config such as `platformio.ini`, `sdkconfig.defaults`,
  `CMakeLists.txt`, `package.json`, `Cargo.toml`, `docker-compose.yml`
- hardware targets, transport protocols, cloud dependencies, and storage
  mechanisms

Use these findings to reduce clarifying questions and pre-fill architecture,
interfaces, constraints, and operational procedures.

### Clarifying Questions

Ask questions only when the missing detail is architecture-critical. Ask in
plain chat, 1-3 concise questions at a time.

If a requirements-intake document exists, ask only questions not already
answered in that document.

Ask when the missing detail affects:

- platform or hardware choice
- protocol selection
- external integrations
- interface shape or command format
- safety, reliability, or regulatory constraints
- deployment and update strategy
- system decomposition into phases or subsystems

Do not ask when the cost of inference is low. Infer reasonable defaults and mark
them as `(assumed)` in the FSD.

Safe default inferences:

- "web API" -> HTTP + JSON
- "logs" -> structured logs to serial, console, or file as appropriate
- "dashboard" -> generic dashboard system without naming a product
- unspecified embedded persistence -> NVS or local flash `(assumed)`
- unspecified relational backend -> PostgreSQL `(assumed)`

### Editing Rules

When creating files, use `apply_patch` to add the new Markdown file.

When updating an FSD:

- prefer surgical edits with `apply_patch`
- do not rewrite the entire file unless the existing structure is unsalvageable
- remove contradictions rather than leaving stale content in place
- keep section structure intact unless the user asks for a reorganization

## Complexity Scaling

Infer complexity from:

- number of distinct components
- number of protocols and integrations
- presence of OTA, mobile apps, cloud services, or dashboards
- real-time, safety, or regulatory constraints
- number of users, operators, or deployment environments

Use these tiers:

| Tier | Characteristics | Target Length | Phases |
|------|-----------------|---------------|--------|
| Low | Single MCU or service, simple flows, 1-2 interfaces | 3-5 pages | 1-2 |
| Medium | MCU + app/service, OTA, 2-4 protocols | 6-12 pages | 2-3 |
| High | Distributed, multi-protocol, real-time or regulated | 15-25+ pages | 3-5 |

Scale the document accordingly:

| Section | Low | Medium | High |
|---------|-----|--------|------|
| Overview | Brief | Full | Full with stakeholders |
| Architecture | Compact | Full logical/platform/software | Detailed end-to-end |
| Requirements | 5-15 FR, 3-5 NFR | 15-30 FR, 5-10 NFR | 30+ FR, 10+ NFR |
| Risks | Bullet list | Table with mitigations | Risk register |
| Interfaces | Inline/table mix | Tables by protocol | Detailed schemas and flows |
| Verification | Checklist + matrix | Test tables + matrix | Full acceptance coverage |
| Troubleshooting | Optional | Include | Include fully |

## Required FSD Structure

All generated or updated FSDs must follow this structure unless a section is not
applicable:

```markdown
# <Project Name> - Functional Specification Document (FSD)

## 1. System Overview

## 2. System Architecture
### 2.1 Logical Architecture
### 2.2 Hardware / Platform Architecture
### 2.3 Software Architecture

## 3. Implementation Phases
### 3.1 Phase 1 - Infrastructure Foundation
### 3.2 Phase 2 - Core Functionality
### 3.3 Phase 3+ - Extensions / Enhancements

## 4. Functional Requirements
### 4.1 Functional Requirements (FR)
### 4.2 Non-Functional Requirements (NFR)
### 4.3 Constraints

## 5. Risks, Assumptions & Dependencies

## 6. Interface Specifications
### 6.1 External Interfaces
### 6.2 Internal Interfaces
### 6.3 Data Models / Schemas
### 6.4 Commands / Opcodes

## 7. Operational Procedures

## 8. Verification & Validation
### 8.1 Phase 1 Verification
### 8.2 Phase 2 Verification
### 8.3 Acceptance Tests
### 8.4 Traceability Matrix

## 9. Troubleshooting Guide

## 10. Appendix
```

Rules:

- Always include Sections 1, 2, 3, 4, 5, 7, and 8.
- Include Section 6.4 only when commands or custom protocols exist.
- Include Section 9 for medium and high complexity unless clearly not useful.
- Omit empty sections instead of writing `N/A`.
- If a section is omitted, keep the numbering coherent.

## Requirement Rules

### Functional Requirements

Convert behaviors into `FR-x.y` items:

- group by domain such as communication, safety, update, or user interaction
- assign `Must`, `Should`, or `May`
- use "shall" phrasing

Example:

- `FR-1.1 [Must]: The device shall publish periodic sensor measurements at a configurable interval (default: 60 s).`

### Non-Functional Requirements

Capture or infer:

- latency and throughput
- uptime and reliability
- power usage
- security and privacy
- accuracy and precision
- maintainability and update behavior

Use `NFR-x.y` numbering and the same priority scheme.

### Constraints

List technical, environmental, regulatory, voltage, power, memory, certification,
or deployment constraints separately from requirements.

## Phases

At minimum define:

- Phase 1: infrastructure and foundations
- Phase 2: core functional behavior
- Phase 3+: optimization, operations, analytics, UX, or optional extensions

Each phase must include:

- scope
- deliverables
- exit criteria
- dependencies

## Verification Rules

Every FSD must include:

- phase-based verification tables
- acceptance tests
- a mandatory traceability matrix

Traceability rules:

- every `Must` and `Should` FR/NFR must map to at least one test
- uncovered requirements must be marked `GAP`
- every test should clearly reference the requirement set it validates
- on evolve mode, regenerate the matrix whenever requirements or tests change

Recommended table shape:

| Requirement | Priority | Test Case(s) | Status |
|------------|----------|-------------|--------|
| FR-1.1 | Must | TC-1.1 | Covered |
| NFR-2.1 | Should | TC-5.1 | Covered |
| FR-3.4 | Must | --- | GAP |

## Formatting Rules

- Output pure Markdown.
- Use concise engineering language.
- Avoid marketing language and filler.
- Use bullet lists for requirements.
- Use tables for tests, interfaces, and troubleshooting when they add clarity.
- Mark inferred details with `(assumed)`.
- Keep numbering stable in evolve mode.

## Reference Files

This skill includes reusable reference specs under `references/`.

Load only the files relevant to the project:

- `references/ble-test-spec.md`
- `references/wifi-test-spec.md`
- `references/logging-test-spec.md`
- `references/watchdog-test-spec.md`
- `references/mqtt-test-spec.md`
- `references/usb-hid-test-spec.md`
- `references/captive-portal-test-spec.md`
- `references/ota-test-spec.md`
- `references/nvs-test-spec.md`
- `references/project-idea-description-template.md`

Use them selectively to:

- enrich requirement wording
- copy or adapt realistic verification cases
- improve edge-case coverage

Do not dump entire reference files into the FSD. Pull only what is relevant.

## Default Execution Pattern

When the user asks for an FSD:

1. Determine create vs update mode.
2. Resolve requirements intake from a project idea document.
3. Search the repo for relevant implementation and config files.
4. Ask concise questions only if architecture-critical information is missing.
5. Infer complexity tier.
6. Draft or update the FSD in Markdown.
7. Ensure FR/NFR numbering, phase structure, and traceability are coherent.
8. Write the file and report the path.

## Quality Bar

The final FSD should be:

- concrete enough for implementation planning
- explicit about assumptions and dependencies
- traceable from requirements to tests
- readable by engineers without extra explanation
- faithful to the existing codebase when one exists
