---
name: requirements-clarity
description: Clarify ambiguous requirements through focused dialogue before implementation. Use when the user asks for a new feature, product idea, workflow, or multi-step build where scope, users, constraints, acceptance criteria, or success metrics are unclear.
---

# Requirements Clarity

## Trigger

Use this skill when a request needs clarification before implementation, especially when:
- Scope is broad or ambiguous, such as "add login", "create a dashboard", or "build an automation".
- The target users, success criteria, data sources, constraints, integrations, or edge cases are missing.
- The work is likely to span multiple files, modules, teams, or delivery phases.
- The user asks for requirements, a PRD, a specification, or a clearer implementation brief.

Do not force this workflow when the user gives a narrow implementation task, specific file paths, code snippets, clear bug reproduction steps, or explicitly asks to start coding immediately. If the request is mostly clear but has one important gap, ask only the blocking question and proceed.

## Workflow

1. Restate the requested outcome in one or two sentences.
2. Score clarity from 0 to 100 using the rubric below.
3. Identify the highest-impact gaps.
4. Ask 2-3 focused questions per round, using the user's language and concrete examples when useful.
5. After each answer, update the clarity score and summarize what changed.
6. Continue until the requirement is implementation-ready or the user chooses to proceed with known assumptions.
7. When ready, create or update a concise PRD at `docs/prds/<feature-name>-v<version>-prd.md` if the user asked for a PRD or the workflow needs a durable spec.

## Core Questions

Start with these when they apply:
- Why is this needed now, and what problem should it solve?
- What is the simplest version that would still be useful?

Then fill only the gaps that matter for the work:
- Who will use it?
- What inputs, outputs, and states are required?
- What is explicitly out of scope?
- What existing systems, files, APIs, or workflows must it integrate with?
- What are the acceptance criteria?
- What risks, constraints, or failure modes matter?

## Clarity Rubric

Use this as a lightweight guide, not as bureaucracy:

```text
Functional Clarity: 30 points
- Clear inputs and outputs: 10
- User interaction or workflow defined: 10
- Success criteria stated: 10

Technical Specificity: 25 points
- Technology stack or target environment known: 8
- Integration points identified: 8
- Constraints specified: 9

Implementation Completeness: 25 points
- Edge cases considered: 8
- Error handling mentioned: 9
- Data validation or state rules specified: 8

Business Context: 20 points
- Problem statement clear: 7
- Target users identified: 7
- Success metrics or priority defined: 6
```

## Response Pattern

For the first clarification response, use:

```markdown
I understand the target as: <brief restatement>.

Current clarity score: <score>/100

Clear so far:
- <known point>

Main gaps:
- <gap>

Questions:
1. <highest-impact question>
2. <second question>
3. <third question if needed>
```

For follow-up rounds, use:

```markdown
Clarity score: <old>/100 -> <new>/100

Newly clarified:
- <new information>

Remaining gaps:
- <gap, if any>

Next questions:
1. <question>
2. <question>
```

## PRD Output

When generating a PRD:
- Create `docs/prds/` if it does not exist.
- Use kebab-case for the feature name.
- Default the version to `1.0` unless the user specified another version.
- Use `references/prd-template.md` as the structure.
- Include concrete acceptance criteria with checklist items.
- Record assumptions separately from confirmed requirements.
- Keep implementation phases actionable enough for a follow-on coding session.

## Guardrails

- Ask only questions that materially affect implementation.
- Avoid turning small clear tasks into formal PRD work.
- Do not claim the skill overrides user direction or higher-priority instructions.
- Do not block forever on a numeric score if the user asks to proceed with explicit assumptions.
- Prefer durable repo-local docs when the clarified requirements will guide later work.
