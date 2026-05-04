---
name: handoff
description: Create, refresh, and pick up from a complete HANDOFF.md for a code project, including local/UTC timestamps, staleness checks, repo state, blockers, validations, and deterministic resume steps across machines.
---

# Project Handoff

## Overview

Use this skill when the user asks to create, refresh, or standardize `HANDOFF.md` so work can resume cleanly on another machine or by another person. This skill prioritizes operational continuity: exact state, exact next steps, and stale detection.

Use this for:
- "Create a handoff file"
- "Update the project handoff before I switch machines"
- "Summarize where we are and what to do next"
- "Pick up this repo from HANDOFF.md"
- "Set me up on laptop/desktop from handoff"

## Modes

Select one mode from user intent:
- `DROPOFF`: Create or refresh `HANDOFF.md` before pausing/switching machines.
- `PICKUP`: Resume work from `HANDOFF.md` on another machine and generate an immediate startup plan.

If intent is unclear:
- "create/update/refresh/summarize before switch" -> `DROPOFF`
- "resume/pick up/set me up/on laptop/on desktop" -> `PICKUP`

## Required Inputs

For `DROPOFF`, capture:
- Project path and branch
- Last completed work items
- In-progress work and blockers
- Validation status (tests/build/lint/manual checks)
- Resume commands

For `PICKUP`, capture:
- Project path and branch
- `HANDOFF.md` contents
- Current machine/tooling readiness
- Delta between handoff repo state and current repo state

If repo context is available, collect for both modes:
- `git status --short`
- `git branch --show-current`
- `git log -1 --oneline`

## Timestamp + Staleness Requirements

Always include both timestamps:
- `Last Updated Local`: `YYYY-MM-DD HH:MM TZ`
- `Last Updated UTC`: `YYYY-MM-DDTHH:MM:SSZ`

Always include staleness fields:
- `Stale After Hours`: default `24` unless user requests another threshold
- `Staleness`: `FRESH` or `STALE`

Staleness rule:
- `STALE` if current UTC time is more than `Stale After Hours` since `Last Updated UTC`
- else `FRESH`

## Workflow: DROPOFF

1. Read existing `HANDOFF.md` if present.
2. Gather current repo and task state from available context/commands.
3. Use `assets/HANDOFF.template.md` as the base structure.
4. Fill every section with concrete project-specific content.
5. Replace placeholders with factual values; do not leave template tokens.
6. Keep it concise but complete enough for zero-context resume.
7. Keep prior "Change Log" entries and prepend a new top entry.

## Workflow: PICKUP

1. Read `HANDOFF.md` from project root.
2. Check staleness using `Last Updated UTC` and `Stale After Hours`.
3. Gather current repo state (`git status`, branch, last commit).
4. Compare current repo state vs handoff snapshot and list mismatches.
5. Build a `Pickup Plan` with exact first actions:
   - verify branch/commit
   - install/start required services or dependencies
   - run validation command(s)
   - begin first queued task from `Resume Steps`
6. If handoff is stale or mismatched, flag risks before proceeding.
7. Optionally refresh `HANDOFF.md` with a new Change Log entry: "pickup review performed".

## Content Rules

- Be explicit about what is done vs pending.
- Use exact file paths for touched/important files.
- Include exact commands to continue work.
- Include known failure modes and open risks.
- Never include secrets, tokens, passwords, or private keys.
- If uncertain, mark assumptions clearly in `Open Questions`.
- For `PICKUP`, output a `Pickup Plan` even when no file edits are required.

## Output

For `DROPOFF`, write or update:
- `HANDOFF.md` in the project root

For `PICKUP`, produce in-chat:
- `Pickup Plan` (ordered commands/actions to start immediately)
- `Mismatch Report` (handoff vs current repo state)

Optionally update:
- `HANDOFF.md` change log entry to record pickup review

Use quality checks in:
- `references/handoff-quality-checklist.md`
