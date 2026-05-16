---
name: save-codex-exchange
description: Save the immediately previous user prompt and Codex result to a Markdown file. Trigger when the user says save_codex_exchange, save_last_prompt, save the last prompt, or save the previous prompt/result.
---

# Save Codex Exchange

## Purpose

Save the immediately previous user prompt and the immediately previous Codex result as Markdown or Discord-friendly text.

This skill takes one required user-supplied argument:

- `filename`: the output file path to write.

If the user asks for Discord upload readability, use `--format discord-text`. Otherwise use the default Markdown archive format.

## Important behavior

When invoked, identify the exchange immediately before the invocation message:

1. The previous user prompt.
2. The previous Codex response/result for that prompt.

Do not save the invocation message itself.

If the previous exchange included code blocks, command output, plans, or explanations, preserve them as Markdown as accurately as possible.

If the previous exchange is unavailable, incomplete, or ambiguous, write the best available reconstruction and include a short note under `## Notes`.

## Markdown output format

Write the file using this structure:

```markdown
# Saved Codex Exchange

- Saved: <ISO-8601 timestamp>
- Source: Codex conversation
- Filename: <filename>

## Prompt:

<previous user prompt>

## Response:

<previous Codex result>

## Notes

<only include if needed>
```

## Discord text output

Use Discord text output when the saved exchange will be uploaded to Discord as a file and needs to preview readably.

This mode:
- Writes `.txt` by default.
- Builds the normal Markdown document first, then renders that Markdown into fixed-width text.
- Wraps headings, paragraphs, lists, blockquotes, links, and tables for plain-text readability.
- Converts Markdown tables into fixed-width text tables.
- Preserves fenced code blocks as labeled code sections.
- Avoids relying on Discord to render Markdown tables.

## Script usage on Windows

Use PowerShell temp files from the skill folder:

```powershell
$PromptFile = Join-Path $env:TEMP "save_last_prompt_prompt.md"
$ResultFile = Join-Path $env:TEMP "save_last_prompt_result.md"

@'
<previous user prompt>
'@ | Set-Content -Path $PromptFile -Encoding UTF8

@'
<previous Codex result>
'@ | Set-Content -Path $ResultFile -Encoding UTF8

py .\scripts\save_last_prompt.py `
  --filename "handoff\last_exchange.md" `
  --prompt-file $PromptFile `
  --result-file $ResultFile
```

For a Discord-friendly upload file:

```powershell
py .\scripts\save_last_prompt.py `
  --filename "handoff\last_exchange.txt" `
  --format discord-text `
  --width 78 `
  --prompt-file $PromptFile `
  --result-file $ResultFile
```

## Safety

- Do not save secrets unless they were already present in the previous exchange and the user explicitly wants that exchange saved.
- Prefer repo-relative output paths when working inside a project.
- Create parent directories automatically through the helper script.
