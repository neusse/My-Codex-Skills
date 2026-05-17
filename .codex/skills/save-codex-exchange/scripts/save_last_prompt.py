
"""
save_last_prompt.py

Write the previous Codex prompt/result pair to Markdown, with optional text conversion.
"""

from __future__ import annotations

import argparse
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

DISCORD_TEXT_EXTENSIONS = {".log", ".txt"}


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    return path.read_text(encoding="utf-8-sig").strip()


def normalize_underscores(path: Path) -> tuple[Path, bool]:
    normalized_name = path.name.replace("_", "-")
    if normalized_name == path.name:
        return path, False
    return path.with_name(normalized_name), True


def resolve_output_format(filename: str, requested_format: str) -> str:
    if requested_format != "auto":
        return requested_format

    suffix = Path(filename).expanduser().suffix.lower()
    if suffix in DISCORD_TEXT_EXTENSIONS:
        return "discord-text"
    return "markdown"


def ensure_output_path(filename: str, output_format: str) -> tuple[Path, bool]:
    path = Path(filename).expanduser()
    path, renamed = normalize_underscores(path)

    if output_format == "discord-text":
        if path.suffix.lower() not in DISCORD_TEXT_EXTENSIONS:
            path = path.with_suffix(".txt")
        elif path.suffix.lower() == ".log":
            path = path.with_suffix(".txt")
        return path, renamed

    if path.suffix.lower() != ".md":
        path = path.with_suffix(path.suffix + ".md") if path.suffix else path.with_suffix(".md")
    return path, renamed


def load_md_to_text_renderer():
    converter_path = Path(__file__).with_name("md-to-text.py")
    spec = importlib.util.spec_from_file_location("md_to_text_converter", converter_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load Markdown converter: {converter_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.render_markdown_to_text


def intermediate_markdown_path(output_path: Path) -> Path:
    return output_path.with_suffix(".md")


def remove_intermediate(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def write_output(
    output_path: Path,
    markdown: str,
    output_format: str,
    width: int,
    compact: bool,
) -> tuple[Path, Path | None]:
    if output_format == "markdown":
        output_path.write_text(markdown, encoding="utf-8")
        return output_path, None

    markdown_path = intermediate_markdown_path(output_path)
    markdown_path.write_text(markdown, encoding="utf-8")

    render_markdown_to_text = load_md_to_text_renderer()
    text = render_markdown_to_text(markdown, width=max(40, width), compact=compact)
    output_path.write_text(text, encoding="utf-8")
    remove_intermediate(markdown_path)
    return output_path, markdown_path


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
        description="Save the previous Codex prompt and result."
    )
    parser.add_argument(
        "--filename",
        required=True,
        help="Output filename. .txt/.log requests produce Discord text; other names produce Markdown.",
    )
    parser.add_argument(
        "--format",
        choices=("auto", "markdown", "discord-text"),
        default="auto",
        help="Output format. auto uses discord-text for .txt/.log filenames and markdown otherwise.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=78,
        help="Text output width for Discord text. Default: 78",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Reduce extra blank lines in Discord text output.",
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

    output_format = resolve_output_format(args.filename, args.format)
    output_path, renamed = ensure_output_path(args.filename, output_format)
    prompt_path = Path(args.prompt_file)
    result_path = Path(args.result_file)

    prompt = read_text(prompt_path)
    result = read_text(result_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown = build_markdown(output_path, prompt, result, args.notes)
    final_path, intermediate_path = write_output(
        output_path,
        markdown,
        output_format,
        args.width,
        args.compact,
    )

    if renamed:
        print("Renamed underscores to hyphens in the output filename.")

    if output_format == "discord-text":
        print(f"Created Markdown intermediate: {intermediate_path}")
        print("Converted Markdown intermediate to Discord text.")
        print("Removed Markdown intermediate.")
        print(f"Saved Discord text exchange to: {final_path}")
    else:
        print("Saved Markdown exchange; converter was not used.")
        print(f"Saved Markdown exchange to: {final_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
