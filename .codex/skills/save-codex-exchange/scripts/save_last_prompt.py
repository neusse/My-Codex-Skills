
"""
save_last_prompt.py

Write the previous Codex prompt/result pair to Markdown or Discord-friendly text.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


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


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    if "|" not in stripped:
        return False
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_ascii_table(rows: list[list[str]]) -> list[str]:
    if not rows:
        return []

    column_count = max(len(row) for row in rows)
    normalized = [row + [""] * (column_count - len(row)) for row in rows]
    widths = [max(len(row[index]) for row in normalized) for index in range(column_count)]
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    rendered = [border]
    for row_index, row in enumerate(normalized):
        rendered.append(
            "| "
            + " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row))
            + " |"
        )
        if row_index == 0:
            rendered.append(border)
    rendered.append(border)
    return rendered


def convert_markdown_tables_to_text(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    index = 0
    in_code_block = False

    while index < len(lines):
        line = lines[index]
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            output.append(line)
            index += 1
            continue

        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        if not in_code_block and "|" in line and is_table_separator(next_line):
            table_rows = [split_table_row(line)]
            index += 2
            while index < len(lines) and "|" in lines[index].strip():
                table_rows.append(split_table_row(lines[index]))
                index += 1
            output.extend(render_ascii_table(table_rows))
            continue

        output.append(line)
        index += 1

    return "\n".join(output)


def simplify_markdown_for_text(text: str) -> str:
    text = convert_markdown_tables_to_text(text)
    lines = []
    in_code_block = False

    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            lines.append(line)
            continue
        if in_code_block:
            lines.append(line)
            continue

        line = re.sub(r"^\s{0,3}#{1,6}\s+", "", line)
        line = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", line)
        line = re.sub(r"(\*\*|__)(.*?)\1", r"\2", line)
        line = re.sub(r"(\*|_)(.*?)\1", r"\2", line)
        line = line.replace("`", "")
        lines.append(line)

    return "\n".join(lines).strip()


def build_discord_text(filename: Path, prompt: str, result: str, notes: str | None = None) -> str:
    saved_at = datetime.now(timezone.utc).isoformat()
    parts = [
        "Saved Codex Exchange",
        "=" * 20,
        "",
        f"Saved: {saved_at}",
        "Source: Codex conversation",
        f"Filename: {filename}",
        "",
        "Prompt",
        "------",
        "",
        simplify_markdown_for_text(prompt) or "No previous prompt content was available.",
        "",
        "Response",
        "--------",
        "",
        simplify_markdown_for_text(result) or "No previous result content was available.",
    ]

    if notes:
        parts.extend(["", "Notes", "-----", "", simplify_markdown_for_text(notes)])

    parts.append("")
    return "\n".join(parts)


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
        help="Output format. markdown preserves the archive format; discord-text creates a text preview with ASCII tables.",
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
    if args.format == "discord-text":
        content = build_discord_text(output_path, prompt, result, args.notes)
    else:
        content = build_markdown(output_path, prompt, result, args.notes)

    output_path.write_text(content, encoding="utf-8")

    print(f"Saved previous Codex exchange to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
