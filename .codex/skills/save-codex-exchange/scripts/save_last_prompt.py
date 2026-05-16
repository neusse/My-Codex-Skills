"""
save_last_prompt.py

Write the previous Codex prompt/result pair to Markdown or Discord-friendly text.
"""

from __future__ import annotations

import argparse
import re
import textwrap
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_WIDTH = 78
DISCORD_TEXT_EXTENSIONS = {".log", ".txt"}


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    return path.read_text(encoding="utf-8").strip()


def ensure_output_filename(filename: str, output_format: str) -> Path:
    path = Path(filename).expanduser()
    if output_format == "markdown" and path.suffix.lower() != ".md":
        return path.with_suffix(path.suffix + ".md") if path.suffix else path.with_suffix(".md")
    if output_format == "discord-text" and path.suffix.lower() not in DISCORD_TEXT_EXTENSIONS:
        return path.with_suffix(path.suffix + ".txt") if path.suffix else path.with_suffix(".txt")
    return path


def build_markdown(filename: Path, prompt: str, result: str, notes: str | None = None) -> str:
    saved_at = datetime.now(timezone.utc).isoformat()

    parts = [
        "# Saved Codex Exchange",
        "",
        f"- Saved: {saved_at}",
        "- Source: Codex conversation",
        f"- Filename: `{filename}`",
        "",
        "## Prompt:",
        "",
        prompt or "_No previous prompt content was available._",
        "",
        "## Response:",
        "",
        result or "_No previous result content was available._",
    ]

    if notes:
        parts.extend(["", "## Notes", "", notes.strip()])

    parts.append("")
    return "\n".join(parts)


def strip_inline_markdown(text: str) -> str:
    """Convert common inline Markdown into readable plain text."""

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"[Image: \1]", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)

    text = re.sub(r"\*\*\*([^*]+)\*\*\*", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)

    text = re.sub(r"___([^_]+)___", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)

    text = re.sub(r"~~([^~]+)~~", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)

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
    stripped = line.strip()
    return bool(re.fullmatch(r"(-\s*){3,}|(\*\s*){3,}|(_\s*){3,}", stripped))


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    if "|" not in stripped:
        return False

    stripped = stripped.strip("|").strip()
    cells = [cell.strip() for cell in stripped.split("|")]
    if not cells:
        return False

    return all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [strip_inline_markdown(cell.strip()) for cell in stripped.split("|")]


def looks_like_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    return "|" in lines[index] and is_table_separator(lines[index + 1])


def render_table(table_lines: list[str], width: int) -> list[str]:
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

    column_count = max(len(row) for row in rows)
    for row in rows:
        while len(row) < column_count:
            row.append("")

    column_widths = []
    for column in range(column_count):
        max_length = max(len(row[column]) for row in rows)
        column_widths.append(max(max_length, 3))

    total_width = sum(column_widths) + (3 * (column_count - 1)) + 4
    if total_width > width:
        available = max(width - (3 * (column_count - 1)) - 4, column_count * 5)
        base = max(5, available // column_count)
        column_widths = [min(column_width, base) for column_width in column_widths]

    def wrap_cell(text: str, column_width: int) -> list[str]:
        if not text:
            return [""]
        return (
            textwrap.wrap(
                text,
                width=column_width,
                replace_whitespace=True,
                drop_whitespace=True,
            )
            or [""]
        )

    def render_row(row: list[str]) -> list[str]:
        wrapped_cells = [
            wrap_cell(row[index], column_widths[index]) for index in range(column_count)
        ]
        max_lines = max(len(cell) for cell in wrapped_cells)
        output = []

        for line_index in range(max_lines):
            parts = []
            for column in range(column_count):
                cell_lines = wrapped_cells[column]
                value = cell_lines[line_index] if line_index < len(cell_lines) else ""
                parts.append(value.ljust(column_widths[column]))
            output.append("| " + " | ".join(parts) + " |")

        return output

    separator = "+-" + "-+-".join("-" * column_width for column_width in column_widths) + "-+"

    output = [separator]
    output.extend(render_row(rows[0]))
    output.append(separator)

    for row in rows[1:]:
        output.extend(render_row(row))

    output.append(separator)
    return output


def render_heading(line: str, width: int) -> list[str]:
    match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
    if not match:
        return [line]

    level = len(match.group(1))
    title = strip_inline_markdown(match.group(2))
    if level <= 2:
        title = title.upper()

    if level == 1:
        border = "=" * min(width, max(len(title), 10))
        return ["", border, title, border, ""]

    if level == 2:
        border = "-" * min(width, max(len(title), 10))
        return ["", title, border, ""]

    prefix = "#" * level
    return ["", f"{prefix} {title}", ""]


def render_list_item(line: str, width: int) -> list[str] | None:
    bullet_match = re.match(r"^(\s*)([-*+])\s+(.*)$", line)
    numbered_match = re.match(r"^(\s*)(\d+)[.)]\s+(.*)$", line)

    if bullet_match:
        indent_raw, _bullet, text = bullet_match.groups()
        indent = " " * min(len(indent_raw), 8)
        marker = "- "
        content = strip_inline_markdown(text)
        return textwrap.wrap(
            content,
            width=max(20, width - len(indent) - len(marker)),
            initial_indent=indent + marker,
            subsequent_indent=indent + "  ",
        ) or [indent + marker]

    if numbered_match:
        indent_raw, number, text = numbered_match.groups()
        indent = " " * min(len(indent_raw), 8)
        marker = f"{number}. "
        content = strip_inline_markdown(text)
        return textwrap.wrap(
            content,
            width=max(20, width - len(indent) - len(marker)),
            initial_indent=indent + marker,
            subsequent_indent=indent + " " * len(marker),
        ) or [indent + marker]

    return None


def render_blockquote(line: str, width: int) -> list[str] | None:
    match = re.match(r"^\s*>\s?(.*)$", line)
    if not match:
        return None

    text = strip_inline_markdown(match.group(1))
    return textwrap.wrap(
        text,
        width=max(20, width - 4),
        initial_indent="| ",
        subsequent_indent="| ",
    ) or ["|"]


def flush_paragraph(
    paragraph: list[str], output: list[str], width: int, compact: bool
) -> None:
    if not paragraph:
        return

    text = " ".join(line.strip() for line in paragraph)
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


def render_markdown_to_text(
    markdown: str, width: int = DEFAULT_WIDTH, compact: bool = False
) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    paragraph: list[str] = []

    in_code_block = False
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        fence_match = re.match(r"^(```+|~~~+)\s*(\w+)?\s*$", stripped)
        if fence_match:
            flush_paragraph(paragraph, output, width, compact)

            if not in_code_block:
                in_code_block = True
                code_language = fence_match.group(2) or "code"
                output.append("")
                output.append(f"[ {code_language} ]")
                output.append("-" * min(width, 20))
            else:
                in_code_block = False
                output.append("-" * min(width, 20))
                if not compact:
                    output.append("")

            index += 1
            continue

        if in_code_block:
            if len(line) <= width:
                output.append(line)
            else:
                chunks = [line[start : start + width] for start in range(0, len(line), width)]
                output.extend(chunks)
            index += 1
            continue

        if stripped == "":
            flush_paragraph(paragraph, output, width, compact)
            if output and output[-1] != "":
                output.append("")
            index += 1
            continue

        if looks_like_table_start(lines, index):
            flush_paragraph(paragraph, output, width, compact)

            table_lines = [lines[index], lines[index + 1]]
            index += 2
            while index < len(lines) and "|" in lines[index].strip() and lines[index].strip():
                table_lines.append(lines[index])
                index += 1

            if output and output[-1] != "":
                output.append("")
            output.extend(render_table(table_lines, width))
            if not compact:
                output.append("")
            continue

        if re.match(r"^#{1,6}\s+", stripped):
            flush_paragraph(paragraph, output, width, compact)
            output.extend(render_heading(line, width))
            index += 1
            continue

        if is_horizontal_rule(line):
            flush_paragraph(paragraph, output, width, compact)
            output.append("-" * width)
            if not compact:
                output.append("")
            index += 1
            continue

        quote = render_blockquote(line, width)
        if quote is not None:
            flush_paragraph(paragraph, output, width, compact)
            output.extend(quote)
            if not compact:
                output.append("")
            index += 1
            continue

        list_item = render_list_item(line, width)
        if list_item is not None:
            flush_paragraph(paragraph, output, width, compact)
            output.extend(list_item)
            index += 1
            continue

        if stripped.startswith("<!--") and stripped.endswith("-->"):
            index += 1
            continue

        paragraph.append(line)
        index += 1

    flush_paragraph(paragraph, output, width, compact)

    cleaned: list[str] = []
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
        description="Save the previous Codex prompt and result."
    )
    parser.add_argument(
        "--filename",
        required=True,
        help="Output filename. Missing extensions default to .md or .txt based on --format.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "discord-text"),
        default="markdown",
        help="Output format. markdown preserves the archive format; discord-text renders that Markdown as fixed-width text.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help=f"Text output width for --format discord-text. Default: {DEFAULT_WIDTH}",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Reduce extra blank lines in --format discord-text output.",
    )
    parser.add_argument(
        "--prompt-file",
        required=True,
        help="File containing the previous user prompt.",
    )
    parser.add_argument(
        "--result-file",
        required=True,
        help="File containing the previous Codex result.",
    )
    parser.add_argument(
        "--notes",
        default=None,
        help="Optional note to include under ## Notes.",
    )

    args = parser.parse_args()

    output_path = ensure_output_filename(args.filename, args.format)
    prompt_path = Path(args.prompt_file)
    result_path = Path(args.result_file)

    prompt = read_text(prompt_path)
    result = read_text(result_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown = build_markdown(output_path, prompt, result, args.notes)
    if args.format == "discord-text":
        content = render_markdown_to_text(
            markdown,
            width=max(40, args.width),
            compact=args.compact,
        )
    else:
        content = markdown

    output_path.write_text(content, encoding="utf-8")

    print(f"Saved previous Codex exchange to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
