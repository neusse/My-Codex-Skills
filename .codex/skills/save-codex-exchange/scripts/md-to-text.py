#!/usr/bin/env python3
"""
md-to-text.py - Render Markdown as plain fixed-width text.

Handles:
    - Headings
    - Paragraph wrapping
    - Bullet and numbered lists
    - Nested-ish lists
    - Blockquotes
    - Fenced code blocks
    - Inline code
    - Bold/italic cleanup
    - Horizontal rules
    - Markdown tables
    - Basic link rendering
    - Extra spacing for small displays and fixed-font screens

Usage:
    python md-to-text.py input.md
    python md-to-text.py input.md output.txt
    python md-to-text.py input.md output.txt --width 78
    python md-to-text.py input.md output.txt --compact
"""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path
from typing import List, Optional


DEFAULT_WIDTH = 78


def strip_inline_markdown(text: str) -> str:
    """
    Convert common inline Markdown into readable plain text.
    This is intentionally conservative.
    """

    # Images: ![alt](url) -> [Image: alt]
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"[Image: \1]", text)

    # Links: [text](url) -> text (url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)

    # Inline code: `code` -> code
    text = re.sub(r"`([^`]+)`", r"\1", text)

    # Bold/italic markers
    text = re.sub(r"\*\*\*([^*]+)\*\*\*", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)

    text = re.sub(r"___([^_]+)___", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)

    # Strikethrough
    text = re.sub(r"~~([^~]+)~~", r"\1", text)

    # HTML tags, simple removal
    text = re.sub(r"<[^>]+>", "", text)

    # Decode a few common HTML entities
    text = (
        text.replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )

    return text.strip()


def is_horizontal_rule(line: str) -> bool:
    s = line.strip()
    return bool(re.fullmatch(r"(-\s*){3,}|(\*\s*){3,}|(_\s*){3,}", s))


def is_table_separator(line: str) -> bool:
    """
    Detect Markdown table separator line:
        | --- | :---: | ---: |
    """
    s = line.strip()
    if "|" not in s:
        return False

    s = s.strip("|").strip()
    cells = [c.strip() for c in s.split("|")]

    if not cells:
        return False

    return all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells)


def split_table_row(line: str) -> List[str]:
    s = line.strip().strip("|")
    return [strip_inline_markdown(cell.strip()) for cell in s.split("|")]


def looks_like_table_start(lines: List[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False

    return "|" in lines[index] and is_table_separator(lines[index + 1])


def render_table(table_lines: List[str], width: int) -> List[str]:
    """
    Render a Markdown table into a fixed-width text table.

    Example:
        | Name | Age |
        | --- | --- |
        | Bob | 34 |
    """

    if len(table_lines) < 2:
        return table_lines

    header = split_table_row(table_lines[0])
    body_lines = table_lines[2:]

    rows = [header]
    for line in body_lines:
        if "|" in line.strip():
            rows.append(split_table_row(line))

    if not rows:
        return []

    col_count = max(len(row) for row in rows)

    # Normalize row lengths
    for row in rows:
        while len(row) < col_count:
            row.append("")

    # Compute column widths
    col_widths = []
    for col in range(col_count):
        max_len = max(len(row[col]) for row in rows)
        col_widths.append(max(max_len, 3))

    # If table is too wide, shrink columns evenly-ish
    total_width = sum(col_widths) + (3 * (col_count - 1)) + 4

    if total_width > width:
        available = max(width - (3 * (col_count - 1)) - 4, col_count * 5)
        base = max(5, available // col_count)
        col_widths = [min(w, base) for w in col_widths]

    def wrap_cell(text: str, col_width: int) -> List[str]:
        if not text:
            return [""]
        return textwrap.wrap(
            text,
            width=col_width,
            replace_whitespace=True,
            drop_whitespace=True,
        ) or [""]

    def render_row(row: List[str]) -> List[str]:
        wrapped_cells = [wrap_cell(row[i], col_widths[i]) for i in range(col_count)]
        max_lines = max(len(cell) for cell in wrapped_cells)

        output = []

        for line_index in range(max_lines):
            parts = []
            for col in range(col_count):
                cell_lines = wrapped_cells[col]
                value = cell_lines[line_index] if line_index < len(cell_lines) else ""
                parts.append(value.ljust(col_widths[col]))

            output.append("| " + " | ".join(parts) + " |")

        return output

    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"

    output = []
    output.append(separator)
    output.extend(render_row(rows[0]))
    output.append(separator)

    for row in rows[1:]:
        output.extend(render_row(row))

    output.append(separator)
    return output


def render_heading(line: str, width: int) -> List[str]:
    match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
    if not match:
        return [line]

    level = len(match.group(1))
    title = strip_inline_markdown(match.group(2)).upper() if level <= 2 else strip_inline_markdown(match.group(2))

    if level == 1:
        border = "=" * min(width, max(len(title), 10))
        return ["", border, title, border, ""]

    if level == 2:
        border = "-" * min(width, max(len(title), 10))
        return ["", title, border, ""]

    prefix = "#" * level
    return ["", f"{prefix} {title}", ""]


def render_list_item(line: str, width: int) -> Optional[List[str]]:
    """
    Render bullet or numbered list items.
    Supports rough indentation.
    """

    bullet_match = re.match(r"^(\s*)([-*+])\s+(.*)$", line)
    numbered_match = re.match(r"^(\s*)(\d+)[.)]\s+(.*)$", line)

    if bullet_match:
        indent_raw, bullet, text = bullet_match.groups()
        indent = " " * min(len(indent_raw), 8)
        marker = "- "
        content = strip_inline_markdown(text)

        wrapped = textwrap.wrap(
            content,
            width=max(20, width - len(indent) - len(marker)),
            initial_indent=indent + marker,
            subsequent_indent=indent + "  ",
        )
        return wrapped or [indent + marker]

    if numbered_match:
        indent_raw, number, text = numbered_match.groups()
        indent = " " * min(len(indent_raw), 8)
        marker = f"{number}. "
        content = strip_inline_markdown(text)

        wrapped = textwrap.wrap(
            content,
            width=max(20, width - len(indent) - len(marker)),
            initial_indent=indent + marker,
            subsequent_indent=indent + " " * len(marker),
        )
        return wrapped or [indent + marker]

    return None


def render_blockquote(line: str, width: int) -> Optional[List[str]]:
    match = re.match(r"^\s*>\s?(.*)$", line)
    if not match:
        return None

    text = strip_inline_markdown(match.group(1))

    wrapped = textwrap.wrap(
        text,
        width=max(20, width - 4),
        initial_indent="| ",
        subsequent_indent="| ",
    )

    return wrapped or ["|"]


def flush_paragraph(paragraph: List[str], output: List[str], width: int, compact: bool) -> None:
    if not paragraph:
        return

    text = " ".join(x.strip() for x in paragraph)
    text = strip_inline_markdown(text)

    if text:
        wrapped = textwrap.wrap(
            text,
            width=width,
            replace_whitespace=True,
            drop_whitespace=True,
        )
        output.extend(wrapped)

        if not compact:
            output.append("")

    paragraph.clear()


def render_markdown_to_text(markdown: str, width: int = DEFAULT_WIDTH, compact: bool = False) -> str:
    lines = markdown.splitlines()
    output: List[str] = []
    paragraph: List[str] = []

    in_code_block = False
    code_fence = ""
    code_language = ""

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Fenced code block start/end
        fence_match = re.match(r"^(```+|~~~+)\s*(\w+)?\s*$", stripped)

        if fence_match:
            flush_paragraph(paragraph, output, width, compact)

            fence = fence_match.group(1)

            if not in_code_block:
                in_code_block = True
                code_fence = fence
                code_language = fence_match.group(2) or "code"

                output.append("")
                output.append(f"[ {code_language} ]")
                output.append("-" * min(width, 20))
            else:
                in_code_block = False
                code_fence = ""
                code_language = ""
                output.append("-" * min(width, 20))
                if not compact:
                    output.append("")

            i += 1
            continue

        if in_code_block:
            # Preserve code exactly, but do not let very long lines explode too badly.
            if len(line) <= width:
                output.append(line)
            else:
                chunks = [line[x : x + width] for x in range(0, len(line), width)]
                output.extend(chunks)
            i += 1
            continue

        # Blank line
        if stripped == "":
            flush_paragraph(paragraph, output, width, compact)

            if output and output[-1] != "":
                output.append("")

            i += 1
            continue

        # Markdown table
        if looks_like_table_start(lines, i):
            flush_paragraph(paragraph, output, width, compact)

            table_lines = [lines[i], lines[i + 1]]
            i += 2

            while i < len(lines) and "|" in lines[i].strip() and lines[i].strip():
                table_lines.append(lines[i])
                i += 1

            if output and output[-1] != "":
                output.append("")

            output.extend(render_table(table_lines, width))

            if not compact:
                output.append("")

            continue

        # Heading
        if re.match(r"^#{1,6}\s+", stripped):
            flush_paragraph(paragraph, output, width, compact)
            output.extend(render_heading(line, width))
            i += 1
            continue

        # Horizontal rule
        if is_horizontal_rule(line):
            flush_paragraph(paragraph, output, width, compact)
            output.append("-" * width)
            if not compact:
                output.append("")
            i += 1
            continue

        # Blockquote
        quote = render_blockquote(line, width)
        if quote is not None:
            flush_paragraph(paragraph, output, width, compact)
            output.extend(quote)
            if not compact:
                output.append("")
            i += 1
            continue

        # List item
        list_item = render_list_item(line, width)
        if list_item is not None:
            flush_paragraph(paragraph, output, width, compact)
            output.extend(list_item)
            i += 1
            continue

        # Raw HTML comment skip
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            i += 1
            continue

        # Normal paragraph line
        paragraph.append(line)
        i += 1

    flush_paragraph(paragraph, output, width, compact)

    # Cleanup excessive blank lines
    cleaned: List[str] = []
    blank_count = 0

    for line in output:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 2:
                cleaned.append("")
        else:
            blank_count = 0
            cleaned.append(line.rstrip())

    return "\n".join(cleaned).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a Markdown document as a plain fixed-width text file."
    )

    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument(
        "output",
        nargs="?",
        help="Output text file. Defaults to input filename with .txt extension.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help=f"Output width. Default: {DEFAULT_WIDTH}",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Reduce extra blank lines.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return 1

    if not input_path.is_file():
        print(f"ERROR: Input path is not a file: {input_path}")
        return 1

    output_path = Path(args.output) if args.output else input_path.with_suffix(".txt")

    markdown = input_path.read_text(encoding="utf-8", errors="replace")

    rendered = render_markdown_to_text(
        markdown,
        width=max(40, args.width),
        compact=args.compact,
    )

    output_path.write_text(rendered, encoding="utf-8")

    print(f"Rendered: {input_path} -> {output_path}")
    print(f"Width:    {max(40, args.width)} columns")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
