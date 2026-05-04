---
name: readme-hero-forge
description: Creates a slick README hero banner section for the current project when missing, with consistent visual and content standards.
---

# Trigger
Use this skill when the user asks to add or generate a README hero banner for the current project, especially when the README lacks a strong top section.

# Workflow
1. Inspect the current project README and confirm whether a hero banner section already exists.
2. If missing, create a repo-local SVG hero banner under `docs/assets/` with a polished, modern style.
3. Update `README.md` top section with:
   - centered banner image
   - centered project title
   - one-line strong value proposition
   - centered badge row
4. Keep the rest of README structure intact unless the user asks for a full rewrite.
5. Verify paths render correctly in GitHub markdown.

# Requirements
- Banner asset must be created locally in-project (no remote hosted dependency).
- README hero must be visually consistent with the standard used in this repository:
  - centered image block
  - centered H1
  - centered short tagline
  - centered badge strip
- Use concise, high-impact language aimed at making the project look download-ready.
- Do not remove project-specific technical setup details unless explicitly requested.

# Guardrails
- Do not overwrite an existing hero banner unless the user asks to replace it.
- Do not use placeholders like "lorem ipsum" or generic AI filler copy.
- Keep file names deterministic and project-appropriate (for example `<project>-banner.svg`).
