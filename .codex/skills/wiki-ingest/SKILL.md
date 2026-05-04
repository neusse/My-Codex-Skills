---
name: wiki-ingest
description: Add a new source to an LLM-maintained wiki, such as a paper, article, URL, file, transcript, code document, or pasted text. Use when the user wants to ingest source material into a wiki created with wiki-init.
---

# Wiki Ingest

Add a source to the wiki. Read it, discuss it with the user, write a summary page, update entity or concept pages, and maintain the index, overview, and log.

## Pre-condition

Find `SCHEMA.md` by searching from the current directory upward. If not found, also check `%USERPROFILE%\wikis` for likely wiki roots. If no schema is found, tell the user to run `wiki-init` first.

Read `SCHEMA.md` to learn the wiki root path, page frontmatter format, cross-reference convention, log entry format, and index category taxonomy.

## Process

### 1. Accept the Source

The source can be:

- File path: read it directly; copy it to `raw\<filename>` if it is not already there.
- URL: use available web browsing to fetch it; save a source copy or citation record under `raw\<slug>.<ext>` when practical.
- Pasted text: use the provided content and save it under `raw\<slug>.md` if it should be preserved.

### 2. Read the Source in Full

Read all content. For long sources, read in sections. Do not skip sections.

### 3. Surface Takeaways Without Blocking Writes

Tell the user:

- 3-5 key takeaways.
- Which entities or concepts this introduces or updates.
- Whether it appears to contradict existing wiki content, after reading `wiki\index.md` and relevant pages.

Do not pause the ingest flow for confirmation at this stage. If the user has not provided emphasis guidance, continue with default neutral synthesis and finish all required wiki writes.

If you ask: "Anything specific you want me to emphasize or de-emphasize?", explicitly state that ingest will continue and that any emphasis changes will be applied in a follow-up update after pages are written.

### 4. Generate the Slug

Use lowercase words, hyphens, and no special characters.

Example: `Attention Is All You Need` becomes `attention-is-all-you-need`.

### 5. Write the Source Summary Page

Write `wiki\pages\<slug>.md`:

```markdown
---
title: <source title>
tags: [<relevant tags>]
sources: [<slug>]
updated: <today>
---

# <Source Title>

**Source:** <original URL or file path>
**Date ingested:** <today>
**Type:** <paper | article | transcript | code | other>

## Summary

<2-3 paragraph synthesis in your own words>

## Key Takeaways

- <bullet>

## Entities & Concepts

<list of entities/concepts as [[slug]] links>

## Relation to Other Wiki Pages

<how this connects to or updates existing knowledge>
```

### 6. Update Entity and Concept Pages

For each entity or concept touched by this source:

- Page exists: read it, add or update the relevant section, add this source to the frontmatter `sources` list, and update the `updated` date.
- Page does not exist: create it with this shape:

```markdown
---
title: <Entity or Concept Name>
tags: [entity | concept]
sources: [<this-source-slug>]
updated: <today>
---

# <Name>

## Description

<synthesis across all sources that discuss this>

## Appearances in Sources

- [[source-slug]] - <one-line note>

## Related Concepts

- [[related-slug]] - <relationship>
```

### 7. Backlink Audit

Scan all existing pages in `wiki\pages\` for mentions of this source's entities and concepts that do not yet link to the new or updated page. Add `[[slug]]` references where appropriate.

This step is required. A compounding wiki depends on bidirectional links.

### 8. Update `wiki\index.md`

Add an entry under the correct category:

```markdown
- [[<slug>]] - <one-line summary> _(ingested <date>)_
```

For any new entity or concept pages created, add index entries for those pages too.

### 9. Update `wiki\overview.md`

Re-read the current overview. If this source introduces a significant concept, shifts the overall understanding, or raises a new question, update the appropriate overview section.

Update the frontmatter `updated` date.

### 10. Append to `wiki\log.md`

```markdown
## [<today>] ingest | <source title>
Pages written: <slug>
Pages updated: <comma-separated list>
```

### 11. Report to the User

Report:

- Summary page path.
- Entity or concept pages created or updated.
- Pages that received backlinks.
- Whether the index and overview were updated.

Only after reporting completed writes may you ask if the user wants emphasis or tone adjustments. Treat those as a follow-up edit pass, not a gate for initial page creation.
