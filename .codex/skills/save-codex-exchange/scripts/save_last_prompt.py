
"""
save_last_prompt.py

Write the previous Codex prompt/result pair to a Markdown file.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    return path.read_text(encoding="utf-8").strip()


def ensure_markdown_filename(filename: str) -> Path:
    path = Path(filename).expanduser()
    if path.suffix.lower() != ".md":
        path = path.with_suffix(path.suffix + ".md") if path.suffix else path.with_suffix(".md")
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Save the previous Codex prompt and result as Markdown."
    )
    parser.add_argument(
        "--filename",
        required=True,
        help="Output Markdown filename. If .md is missing, it will be appended.",
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

    output_path = ensure_markdown_filename(args.filename)
    prompt_path = Path(args.prompt_file)
    result_path = Path(args.result_file)

    prompt = read_text(prompt_path)
    result = read_text(result_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown = build_markdown(output_path, prompt, result, args.notes)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"Saved previous Codex exchange to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
