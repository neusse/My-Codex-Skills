---
name: save-codex-exchange
description: Save the immediately previous user prompt and Codex result to a Markdown file. Trigger when the user says save_codex_exchange, save_last_prompt, save the last prompt, or save the previous prompt/result.
---

# Save Codex Exchange

## Purpose

Save the immediately previous user prompt and the immediately previous Codex result as Markdown or Discord-compatible text.

This skill takes one required user-supplied argument:

- `filename`: the output file path to write.

If the requested filename contains underscores, the helper changes them to hyphens in the output filename and reports that change.

If the user asks for a Discord-compatible text file, request a `.txt` filename or use `--format discord-text`. The helper always writes a Markdown intermediate first, converts that Markdown with `md-to-text.py`, writes the final `.txt` file, and removes the intermediate Markdown file.

If the user asks for Markdown, the helper writes the Markdown file and does not use the converter.

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

For a Discord-compatible upload file:

```powershell
py .\scripts\save_last_prompt.py `
  --filename "handoff\last_exchange.txt" `
  --prompt-file $PromptFile `
  --result-file $ResultFile
```

The helper will save the final file as `last-exchange.txt`, because underscores in the filename are normalized to hyphens.

## Required user report

After running the helper, tell the user:

- Whether underscores were changed to hyphens in the output filename.
- Whether the final output was Markdown or Discord-compatible text.
- For Discord text, that Markdown was written as an intermediate, converted, and removed.
- The final output path.

## Safety

- Do not save secrets unless they were already present in the previous exchange and the user explicitly wants that exchange saved.
- Prefer repo-relative output paths when working inside a project.
- Create parent directories automatically through the helper script.
