---
name: wiki-update
description: Revise existing wiki pages when knowledge changes, new information updates or contradicts existing content, a lint report recommends changes, or the user wants to edit wiki content with LLM assistance.
---

# Wiki Update

Revise existing wiki pages. Always show diffs before writing. Always log. Always cite the source of new information.

## Pre-condition

Find `SCHEMA.md` by searching from the current directory upward. If not found, also check `%USERPROFILE%\wikis` for likely wiki roots. If no schema is found, tell the user to run `wiki-init` first.

Read `SCHEMA.md` to get the wiki root path and conventions.

## Process

### 1. Identify What to Update

The user may provide:

- Specific page names: update those pages.
- New information: read `wiki\index.md` to find affected pages, then read those pages.
- A lint report: work through its recommendations item by item.

### 2. For Each Page to Update

Read the current content in full. Propose the change:

```markdown
**Current:** `<quote the existing text>`
**Proposed:** `<replacement text>`
**Reason:** `<why this change is warranted>`
**Source:** `<URL, file path, or description of where this information comes from>`
```

Always include `Source`. An edit without a source citation creates untraceability.

Ask for confirmation before writing each page. Do not batch-apply changes without per-page confirmation.

### 3. Check for Downstream Effects

After identifying primary pages to update, search for `[[slug]]` references to those pages across all of `wiki\pages\`.

For each page that links to an updated page:

- Decide whether the update changes anything that page asserts.
- If yes, flag it explicitly: "`[[other-page]]` may also need updating based on this change."
- Offer to update it with the same confirm-before-write flow.

### 4. Contradiction Sweep

If the new information contradicts something in the wiki, search all pages for the contradicted claim before updating. It may appear in more than one place. Update all occurrences, not just the most obvious one.

### 5. Update `wiki\index.md`

If the one-line summary for any updated page changed, update it in `index.md`. Update the `updated` date in each changed page's frontmatter.

### 6. Update `wiki\overview.md`

Re-read `overview.md`. If the updates shift the overall synthesis, resolve an open question, or change a key claim, propose edits to `overview.md` using the same confirm-before-write flow.

### 7. Append to `wiki\log.md`

Always append without asking permission. If `log.md` does not exist, create it.

```markdown
## [<today>] update | <list of updated page slugs>
Reason: <brief description of what changed and why>
Source: <URL or description>
```

## Common Mistakes

- Updating without citing the source. Always include where the new information came from.
- Skipping the downstream check. Related pages may become inconsistent.
- Skipping the log. Every change must be logged.
- Batch-writing without confirmation. Show each diff individually.
