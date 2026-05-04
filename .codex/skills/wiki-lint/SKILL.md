---
name: wiki-lint
description: Audit an LLM-maintained wiki for health issues, including contradictions, orphan pages, broken cross-references, stale claims, missing frontmatter, missing pages, and coverage gaps. Use after several ingests or when the user asks to check wiki health.
---

# Wiki Lint

Audit the wiki, produce a categorized report, offer concrete fixes, and log the operation.

## Pre-condition

Find `SCHEMA.md` by searching from the current directory upward. If not found, also check `%USERPROFILE%\wikis` for likely wiki roots. If no schema is found, tell the user to run `wiki-init` first.

Read `SCHEMA.md` to get the wiki root path and conventions.

## Process

### 1. Build the Page Inventory

Read `wiki\index.md`, `wiki\overview.md`, and all files in `wiki\pages\`. Build a map of:

- All existing slugs, using filenames without `.md`.
- All `[[slug]]` references found in any page.
- All `sources` listed in frontmatter.

### 2. Run All Checks

Errors:

- Broken links: `[[slug]]` references where no corresponding `wiki\pages\<slug>.md` exists.
- Missing frontmatter: pages without required `title`, `tags`, `sources`, or `updated` fields.

Warnings:

- Orphan pages: pages with zero inbound `[[slug]]` links from any other page, excluding `index.md` and `overview.md`.
- Contradictions: claims in one page that directly conflict with claims in another, such as dates, counts, names, or relationships.
- Stale claims: pages not updated within 90 days that contain words like "current", "latest", "recent", "state-of-the-art", or year literals two or more years old.

Info:

- Missing concept pages: `[[slug]]` references that appear three or more times across the wiki but have no dedicated page.
- Coverage gaps: open questions in `overview.md` that could be answered by a web search or new ingest.
- Missing cross-references: two pages discuss the same entity but do not link to each other.

### 3. Write the Lint Report

Write `wiki\pages\lint-<today>.md` without asking permission:

```markdown
---
title: Lint Report <today>
tags: [lint, maintenance]
sources: []
updated: <today>
---

# Lint Report - <today>

## Summary
- Errors: N
- Warnings: N
- Info: N

## Errors - Broken Links
- [[source-page]] references [[missing-slug]] - does not exist
  Fix: create the page or remove the reference

## Errors - Missing Frontmatter
- [[page]] is missing: title, updated

## Warnings - Orphan Pages
- [[slug]] - no inbound links
  Fix: add link from [[related-page]], or delete if no longer relevant

## Warnings - Contradictions
- [[page-a]] says: "<claim>"
- [[page-b]] says: "<conflicting claim>"
  Recommendation: <which to trust, or "investigate further">

## Warnings - Stale Claims
- [[page]] last updated <date>, contains "latest" - may be outdated
  Fix: re-verify claims or add an "as of <date>" qualifier

## Info - Missing Concept Pages
- [[slug]] referenced N times but no page exists
  Fix: run wiki-ingest or create a stub

## Info - Coverage Gaps
- Open question from overview.md: "<question>"
  Suggestion: search for <X> or ingest <source type>

## Info - Missing Cross-References
- [[page-a]] and [[page-b]] both discuss <entity> but do not link to each other
```

Add the lint report to `wiki\index.md` under a `Maintenance` category. Create that category if it does not exist.

### 4. Offer Concrete Fixes

For each fixable category, offer:

- Broken links: remove broken `[[slug]]` references after showing each change.
- Missing cross-references: add missing links between page pairs.
- Orphan page tags: add `status: orphan` to frontmatter of orphan pages.
- Missing frontmatter: add missing fields with placeholder values.

Show the exact diff for each change before writing. Apply only after confirmation.

### 5. Append to `wiki\log.md`

Always append without asking permission:

```markdown
## [<today>] lint | <N errors> errors, <N warnings> warnings, <N info> info
Report: [[lint-<today>]]
Fixed: <list what was fixed, or "none">
```
