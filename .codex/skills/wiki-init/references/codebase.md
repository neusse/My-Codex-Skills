# Codebase Wiki Guide

Use this when `wiki-init` is configured for a codebase domain. It covers structure, ingestion order, exploration strategy, and decision capture.

## Recommended Categories

```text
Modules | APIs | Decisions | Flows
```

- Modules: major packages, services, or libraries, with one page per unit of deployment or ownership.
- APIs: public interfaces, REST endpoints, RPC contracts, and SDK surfaces.
- Decisions: architectural and technical decisions, both documented and reconstructed.
- Flows: end-to-end paths through the system, such as request lifecycle, data pipeline, or auth flow.

## What to Ingest First

Order matters because later pages can cross-reference earlier ones:

1. Top-level `README.md` and any `docs\` directory.
2. Existing ADRs or decision docs, such as `docs\adr\` or `DECISIONS.md`.
3. CI/CD config, such as `Makefile`, `Justfile`, or `.github\workflows\`, because it reveals the build model and deployment topology.
4. Dependency manifests, such as `package.json`, `pyproject.toml`, or `go.mod`, because they reveal external surface area and key choices.
5. Entry point files, such as `main.py`, `cmd\server\main.go`, or `src\index.ts`, because they reveal system shape.

If formal documentation is sparse or missing, skip to exploration and treat the codebase itself as the source.

## Exploration Strategy

Work outward from the edges of the system:

1. Entry points: where execution starts and what the top-level handlers are.
2. Module boundaries: coarse-grained units and ownership boundaries.
3. API surface: what the system exposes and consumes.
4. Key flows: trace two or three representative user journeys end to end.
5. Decision log: capture every non-obvious choice encountered while exploring.

Resist documenting everything at once. Five deep pages are better than fifty shallow ones.

## Capturing Decisions

`Decisions` pages are especially valuable when formal documentation is sparse.

Two types:

- Sourced: a formal ADR or decision doc exists. Ingest it as a source; the wiki page synthesizes and cross-references affected modules and flows.
- Reconstructed: no formal doc exists. The decision is inferred from code structure, git history, dependency choices, or naming conventions. The wiki page becomes the first written record.

Watch for undocumented decisions while exploring:

- Why is this library used instead of a more common alternative?
- Why is this boundary drawn here?
- Why does this flow bypass the usual path?
- Why is this module structured differently from its neighbors?

When you notice one, create a `Decisions` page immediately instead of saving it for later.

## Slug Conventions

`wiki\pages\` is flat. Use prefixes to group related pages:

| Prefix | Example | Use for |
|---|---|---|
| `mod-` | `mod-auth-service` | Module or service pages |
| `api-` | `api-user-endpoints` | API surface pages |
| `dec-` | `dec-postgres-over-mysql` | Decisions, sourced or reconstructed |
| `flow-` | `flow-checkout-request` | End-to-end flows |

## Handling Drift

Codebases change. Keep the wiki current by:

- Running `wiki-lint` after significant refactors to find stale claims.
- Using `wiki-update` when a module is renamed, split, or deleted.
- Noting the approximate date or git ref a claim was verified, for example `> Verified 2026-04`.
- Flagging pages with `stale: true` in frontmatter when they need revisiting.

## README vs. Wiki

Maintain this distinction on every ingest and update.

README answers: what is this, how do I run it, how do I contribute?

Wiki answers: why is it this way, how does it fit together, what tradeoffs were accepted?

| Belongs in README | Belongs in wiki |
|---|---|
| Setup and installation | Architectural rationale |
| How to run tests | Module relationships and boundaries |
| Contributing guidelines | Decision history, sourced and reconstructed |
| Environment variables | End-to-end flows |
| Quick-start examples | Cross-cutting concerns |

The test: if a PR reviewer would ask whether the README reflects the change, it belongs in the README. If explaining it requires cross-referencing multiple parts of the system, it belongs in the wiki.

When ingesting a README:

1. Extract for the wiki: structural signals, modules, system shape, and design intent. Do not reproduce operational content. Link to the README instead, for example: `See the project README for setup instructions.`
2. Evaluate the README itself: flag missing sections, outdated content, content that belongs in the wiki, and suggested edits.

Subdirectory READMEs, such as `src\auth\README.md`, follow the same pattern.

## Cross-Referencing Code

Anchor claims to specific locations using inline code paths:

```markdown
The request router is defined in `src/server/router.ts` and delegates to handlers in `src/handlers/`.
```

Do not embed full code snippets in wiki pages. The wiki describes what and why; the codebase is the source of truth for how.
