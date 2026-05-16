---
name: invoice-organizer
description: Organize invoices, receipts, and statements by extracting document details, proposing safe filenames/folders, and creating reviewable tax or bookkeeping summaries.
---

# Invoice Organizer

Use this skill when a user asks to sort, rename, summarize, or prepare invoice and receipt files for bookkeeping, taxes, reimbursement, or archive cleanup.

## Workflow

1. Inventory candidate files before changing anything. Include counts, formats, and current folder shape.
2. Extract available details from each file: date, vendor, invoice/receipt number, amount, description, and likely category.
3. Flag low-confidence extraction instead of guessing. Use file metadata only as a fallback and label it as such.
4. Propose a folder and filename plan before moving or copying files.
5. Preserve originals by default. Copy into the organized structure unless the user explicitly requests moves.
6. Create a CSV or spreadsheet summary when useful for accounting review.
7. Report processed files, skipped files, low-confidence items, duplicates, and output locations.

## Default Filename

Use this pattern unless the user specifies another:

```
YYYY-MM-DD Vendor - DocumentType - ShortDescription.ext
```

Example:

```
2026-04-15 Adobe - Invoice - Creative Cloud.pdf
```

## Default Folder Structure

```
Organized-Invoices/
  YYYY/
    Category/
      Vendor/
```

Adjust the folder structure when the user already has an accountant-preferred layout.

## Safety Rules

- Do not silently invent vendors, dates, amounts, or tax categories.
- Do not delete originals.
- Do not classify legal tax treatment as certain. Use "candidate category" or "needs review" when unsure.
- Keep secrets and account numbers out of generated summaries unless the user explicitly requests them.
