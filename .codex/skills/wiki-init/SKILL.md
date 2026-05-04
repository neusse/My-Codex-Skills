---
name: wiki-init
description: Bootstrap a new LLM-maintained personal wiki for a knowledge domain, including research, codebase documentation, reading notes, competitive analysis, or long-term knowledge accumulation. Use when the user wants to create, initialize, or start a new wiki.
---

# Wiki Init

Bootstrap a new LLM-maintained wiki at a user-specified path.

## Pre-flight

Check whether a `SCHEMA.md` already exists in the current directory or any parent directory. If yes, ask the user whether to reinitialize or continue with the existing wiki.

## Process

### 1. Gather Configuration

Ask one question at a time:

1. Where should the wiki live? Use an absolute path, for example `C:\Users\georg\wikis\ml-research`.
2. What is the domain or purpose? Ask for one sentence.
3. What types of sources will be added? Examples: papers, URLs, code files, transcripts.
4. What categories should `index.md` use?

Default categories:

- Research: `Sources | Entities | Concepts | Analyses`
- Codebase: `Modules | APIs | Decisions | Flows`
- Custom: use the user's specified categories

For codebase wikis, read `references/codebase.md` from this skill directory and apply its guidance.

### 2. Create Directory Structure

Create:

```text
<wiki-root>\
  SCHEMA.md
  raw\
  wiki\
    index.md
    log.md
    overview.md
    pages\
  assets\
```

`wiki\pages\` is flat. All pages live there as `<slug>.md`. Do not create page subdirectories. Slugs are lowercase and hyphen-separated.

### 3. Write `SCHEMA.md`

```markdown
# Wiki Schema

## Identity
- **Path:** <absolute path to wiki-root>
- **Domain:** <user's domain description>
- **Source types:** <list>
- **Created:** <YYYY-MM-DD>

## Page Frontmatter
Every wiki page must start with:
---
title: <page title>
tags: [tag1, tag2]
sources: [source-slug1]
updated: YYYY-MM-DD
---

## Cross-References
Use `[[slug]]` where slug = filename without `.md`.
Example: `[[transformer-architecture]]` resolves to `wiki/pages/transformer-architecture.md`.

## Log Entry Format
## [YYYY-MM-DD] <operation> | <title>
Operations: init, ingest, query, update, lint

## Index Categories
<one per line, matching the user's chosen taxonomy>

## Conventions
- `raw/` is immutable. Skills never modify it after a source is stored there.
- `log.md` is append-only. Never rewrite it; only append.
- `index.md` is updated on every operation that adds or changes pages.
- All pages live flat in `wiki/pages/`. Do not create page subdirectories.
- `overview.md` reflects the current synthesis across all sources.
```

For a codebase domain, also add:

```markdown
- README boundary: wiki pages must not duplicate README content. Extract structural signals; link to the README for operational content such as setup, contributing, and running. When ingesting any README, also evaluate it for gaps and suggest edits.
```

### 4. Write `wiki/index.md`

```markdown
# Wiki Index - <domain>

### <Category Name>
<!-- entries added by wiki-ingest -->
```

Create one category section for each chosen category.

### 5. Write `wiki/log.md`

```markdown
# Wiki Log

Append-only. Format: `## [YYYY-MM-DD] <operation> | <title>`
Recent entries on Windows PowerShell:
`Select-String -Path .\wiki\log.md -Pattern '^## \[' | Select-Object -Last 10`

---

## [<today>] init | <domain>
```

### 6. Write `wiki/overview.md`

```markdown
---
title: Overview
tags: [overview, synthesis]
sources: []
updated: <today>
---

# <Domain> - Overview

> Evolving synthesis of everything in the wiki. Updated by wiki-ingest when sources shift the understanding.

## Current Understanding

*No sources ingested yet.*

## Open Questions

*Add questions here as they arise.*

## Key Entities / Concepts

*Populated as pages are created.*
```

### 7. Confirm

Tell the user:

- Wiki initialized at `<path>`.
- Add sources to `raw\` manually, or run `wiki-ingest` with a URL, file path, or pasted text.
- Run `wiki-lint` periodically to keep the wiki healthy.
- `SCHEMA.md` is how the other wiki skills locate the wiki. Do not move or delete it.
