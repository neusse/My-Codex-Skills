# Handoff Quality Checklist

Use this checklist before finalizing `HANDOFF.md`.

- Metadata has both local and UTC timestamps.
- Staleness field is present and matches the timestamp rule.
- Objective and status are specific and current.
- Done/in-progress/blocker sections are all filled.
- Validation section reflects what was actually run.
- Resume Steps are executable in order.
- Important files use absolute paths.
- No secrets or credentials are present.
- Open questions/assumptions are explicit.
- Change Log has a new top entry for this update.

## Pickup Quality Checklist

Use this checklist when resuming from `HANDOFF.md`.

- `HANDOFF.md` exists and was read.
- Staleness was evaluated from `Last Updated UTC` and threshold.
- Current branch/commit/status were captured.
- Mismatches from handoff snapshot were identified.
- Immediate `Pickup Plan` was produced with executable first steps.
- Risks from stale data or repo drift were called out.
