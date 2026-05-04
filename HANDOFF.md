# HANDOFF

## Project
- Name: My-Codex-Skills
- Path: C:\Users\georg\Codex_Projects\My-Codex-Skills
- Last Updated (Local): 2026-05-04 America/Los_Angeles
- Last Updated (UTC): 2026-05-04 UTC

## Current State
- Initialized as a dedicated repository for personal Codex skills.
- Starter structure created for local development and deployment.
- Deployment script added to sync skills to `%USERPROFILE%\\.codex\\skills`.
- First starter skill added: `news-scout`.

## Files Created
- README.md
- templates/skill-template/SKILL.md
- scripts/deploy-skills.ps1
- .codex/skills/news-scout/SKILL.md

## Startup Questions (to refine this repo)
1. Which first production news skills should be built next (e.g., market-open brief, earnings tracker, SEC filing alerts, macro digest)?
2. Should deployment overwrite existing installed skills by default, or add `-NoClobber` safety mode?
3. Do you want automated validation (lint/check) before deployment?

## Resume Commands
- Show tree:
  - `Get-ChildItem -Recurse`
- Deploy all skills:
  - `pwsh -ExecutionPolicy Bypass -File .\\scripts\\deploy-skills.ps1 -All`
- Deploy one skill:
  - `pwsh -ExecutionPolicy Bypass -File .\\scripts\\deploy-skills.ps1 -Skills news-scout`

## Next Steps
1. Define 2-3 concrete news-skill specs with triggers and output contracts.
2. Implement each under `.codex/skills/<name>/SKILL.md`.
3. Deploy locally and run smoke tests in Codex.
4. Add a changelog and versioning convention.