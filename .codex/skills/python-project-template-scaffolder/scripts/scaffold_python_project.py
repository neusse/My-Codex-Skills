#!/usr/bin/env python3
"""Scaffold a Python project from bundled templates."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
from pathlib import Path


TOKEN_PATTERN = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def slugify_package_name(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    normalized = normalized.strip("_")
    if not normalized:
        return "my_project"
    if normalized[0].isdigit():
        normalized = f"project_{normalized}"
    return normalized


def render_tokenized(text: str, replacements: dict[str, str]) -> str:
    def _replace(match: re.Match[str]) -> str:
        key = match.group(1)
        return replacements.get(key, match.group(0))

    return TOKEN_PATTERN.sub(_replace, text)


def scaffold(
    project_name: str,
    package_name: str,
    destination_root: Path,
    force: bool,
) -> Path:
    skill_dir = Path(__file__).resolve().parents[1]
    template_root = skill_dir / "assets" / "project-template"
    if not template_root.exists():
        raise FileNotFoundError(f"Template root not found: {template_root}")

    project_slug = re.sub(r"[^a-zA-Z0-9]+", "-", project_name.strip().lower()).strip("-")
    if not project_slug:
        project_slug = "new-python-project"

    destination_dir = destination_root / project_slug
    if destination_dir.exists():
        if force:
            shutil.rmtree(destination_dir)
        else:
            raise FileExistsError(
                f"Destination already exists: {destination_dir}. "
                "Pass --force to overwrite."
            )

    replacements = {
        "PROJECT_NAME": project_name.strip(),
        "PROJECT_SLUG": project_slug,
        "PACKAGE_NAME": package_name,
        "DATE": dt.date.today().isoformat(),
    }

    for src in template_root.rglob("*"):
        relative = src.relative_to(template_root)
        rendered_relative = Path(
            *[render_tokenized(part, replacements) for part in relative.parts]
        )
        dest = destination_dir / rendered_relative

        if src.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        content = src.read_text(encoding="utf-8")
        dest.write_text(render_tokenized(content, replacements), encoding="utf-8")

    return destination_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a Python project with workflow document templates."
    )
    parser.add_argument("--project-name", required=True, help="Human-readable project name")
    parser.add_argument(
        "--package-name",
        help="Python package name (default: derived from --project-name)",
    )
    parser.add_argument(
        "--destination-root",
        required=True,
        type=Path,
        help="Directory where the project folder will be created",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite destination if it already exists",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    package_name = args.package_name or slugify_package_name(args.project_name)
    destination_root = args.destination_root.resolve()
    destination_root.mkdir(parents=True, exist_ok=True)

    output_dir = scaffold(
        project_name=args.project_name,
        package_name=package_name,
        destination_root=destination_root,
        force=args.force,
    )
    print(f"Scaffold created: {output_dir}")
    print(f"Package name: {package_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
