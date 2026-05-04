---
name: wiki-query
description: Answer questions against a personal wiki created with wiki-init and populated with wiki-ingest. Use when the user asks about wiki contents, asks what the wiki knows, or wants a wiki-grounded synthesis. Always read the wiki pages first.
---

# Wiki Query

Ask a question, read the wiki, synthesize with citations, and offer to file the answer back into the wiki.

## Pre-condition

Find `SCHEMA.md` by searching from the current directory upward. If not found, also check `%USERPROFILE%\wikis` for likely wiki roots. If no schema is found, tell the user to run `wiki-init` first.

Read `SCHEMA.md` to get the wiki root path and cross-reference convention.

## Process

### 1. Read `wiki\index.md` First

Scan the full index to identify likely relevant pages. Do not answer from general knowledge. The wiki is the source of truth for this task, even when it contradicts general knowledge.

### 2. Read Relevant Pages

Read the identified pages in full. Follow one level of `[[slug]]` links when the linked pages seem relevant to the question.

### 3. Synthesize the Answer

Write a response that:

- Is grounded in the wiki pages read.
- Cites inline using `[[slug]]` for every claim sourced from a specific page.
- Notes agreements and disagreements between pages.
- Flags gaps, such as "The wiki has no page on X" or "`[[page]]` does not cover Y yet."
- Suggests follow-up sources to ingest or questions to investigate.

Format by question type:

- Factual: prose with citations.
- Comparison: table.
- How-it-works: numbered steps.
- What-do-we-know-about-X: structured summary with open questions.

### 4. Always Offer to Save

After answering, ask:

> Worth saving as `wiki\pages\<suggested-slug>.md`?

If yes:

- Write the page with frontmatter: `tags: [query, analysis]`, `sources: [all cited slugs]`.
- Add an entry to `wiki\index.md` under the correct category, usually `Analyses`.
- Append to `wiki\log.md`:

```markdown
## [<today>] query | <question summary>
Filed as: [[<slug>]]
```

If no:

- Append to `wiki\log.md`:

```markdown
## [<today>] query | <question summary>
Not filed.
```

## Common Mistakes

- Answering from memory. Always read the wiki pages first.
- Skipping the save offer. Good query answers compound the wiki's value.
- Omitting citations. Every factual claim should trace back to a `[[slug]]`.
