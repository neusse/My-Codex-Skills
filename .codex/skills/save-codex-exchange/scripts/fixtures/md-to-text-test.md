# Markdown To Text Converter Test

This fixture is intentionally broad. It gives `md-to-text.py` a stable input file for checking heading rendering, paragraph wrapping, spacing, inline cleanup, tables, and code blocks before the converter is wired into the `save-codex-exchange` skill.

## Paragraph Wrapping

This paragraph should wrap cleanly when the converter is run at a narrow width. It includes enough words to force multiple output lines while preserving readable spacing for small displays and fixed-font screens.

This paragraph includes `inline code`, **bold text**, *italic text*, ***bold italic text***, __alternate bold text__, _alternate italic text_, and ~~struck text~~ so the inline cleanup can be inspected in one place.

## Bullet Lists

- First bullet item with a short value.
- Second bullet item with a longer sentence that should wrap under the bullet marker instead of starting at the far left edge of the output.
  - Nested-ish bullet item that uses indentation and should keep a visible nested shape.
    - Deeper nested-ish bullet item that should be capped to a practical indentation width.

## Numbered Lists

1. First numbered item.
2. Second numbered item with enough detail to wrap and preserve the numbered list alignment.
   1. Nested numbered item using indentation.
   2. Another nested numbered item.

## Blockquotes

> This blockquote should render with a simple quote marker and wrap cleanly at the selected output width.
> This second quoted line includes a [basic link](https://example.com/docs) and **bold text**.

## Horizontal Rule

The line below should become a full-width rule.

---

## Markdown Table

| Feature | Expected Text Output |
| --- | --- |
| Headings | Uppercase level one and level two headings with simple underline rules. |
| Tables | Fixed-width ASCII-style table with wrapped cells. |
| Links | Link text followed by the URL in parentheses. |
| Code | Fenced blocks get a language label and preserved content. |

## Fenced Code Block

```powershell
$Path = ".\example.md"
python .\md-to-text.py $Path ".\example.txt" --width 78
```

## Fenced Code Block Without Language

```
plain fenced text should receive the default code label
and preserve spacing as much as possible.
```

## Basic Link Rendering

Read the [project README](../../../../README.md) before changing the converter behavior.

## Final Spacing Check

There should be readable blank-line separation around sections without creating huge vertical gaps in the text output.
