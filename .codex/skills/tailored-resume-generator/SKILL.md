---
name: tailored-resume-generator
description: Tailor a resume to a target job description by mapping real candidate experience to requirements, improving ATS keyword alignment, and preserving truthful claims.
---

# Tailored Resume Generator

Use this skill when a user asks to tailor, rewrite, target, optimize, or adapt a resume for a specific job, recruiter, or application.

## Workflow

1. Gather the target job description and the candidate's current resume or background.
2. Extract must-have requirements, preferred qualifications, keywords, tools, domain terms, and role seniority signals.
3. Map each requirement to real candidate evidence. Mark gaps instead of fabricating experience.
4. Rewrite the summary, skills, and experience bullets to emphasize the strongest matches.
5. Use standard ATS-friendly section headings and readable Markdown or plain text unless the user requests another format.
6. Provide a short gap/strategy note after the resume, including interview or cover-letter points when useful.

## Resume Rules

- Never invent employers, titles, dates, degrees, certifications, clearances, metrics, tools, or responsibilities.
- Quantify impact only when the user supplied enough evidence or clearly authorizes a reasonable estimate.
- Keep claims defensible and interview-ready.
- Preserve important user constraints such as page count, format, location, work authorization, salary range, and remote/on-site preferences.
- If a master resume exists in the active workspace, prefer it over asking the user to paste everything again.

## Output

Default structure:

1. Target-role fit summary.
2. Tailored resume.
3. Gap notes and optional cover-letter/interview hooks.
4. Any assumptions that need user confirmation.
