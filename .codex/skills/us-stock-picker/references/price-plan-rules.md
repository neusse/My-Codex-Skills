# Price Plan Rules

Use this file when exact buy, stop, target, or timing levels are requested.

## Core Principle

Derive all price levels from verified session data and recent structure. Do not infer exact levels from one session alone.

Minimum inputs before exact levels:

- latest complete-session open/high/low/close
- previous complete-session open/high/low/close
- recent structure window by horizon
- intraday path summary when short-term execution quality matters

If data is stale or inconsistent, downgrade to conditional trigger language.

## Fixed Calculation Sequence

Always follow this order:

1. determine horizon
2. pull required window
3. classify setup type
4. mark support/resistance from structure
5. anchor with latest complete session
6. derive trigger, stop, targets, and risk/reward
7. reject setup if structure quality is weak

## Structure Checklist

Before setting levels, identify:

- latest complete-session close
- latest complete-session high and low
- previous-session close
- recent 5-day high and low
- recent 20-day high and low for medium term
- recent 60-day or 6-12 month structure for long term
- close location in session range
- whether volume was expanding, stable, or fading

## Short-Term Rules

Use for next session to roughly 5 sessions.

Preferred setup types:

1. breakout continuation
2. controlled pullback after strong close
3. reclaim of key level after intraday washout

Short-term stop should anchor to nearest invalidation (latest low or recent support pocket).

Short-term targets:

- `Target 1`: nearest realistic resistance
- `Target 2`: next structural resistance

## Medium-Term Rules

Use for roughly 2 to 12 weeks.

- prefer entry zone near latest close and 20-60 day structure
- place stop below base support or recent swing low
- use staged targets at structural resistance zones

## Long-Term Rules

Use for roughly 6 to 24 months.

- use staged entry zones instead of single-tick entries
- stop is wider thesis-break line or major support break
- targets map to re-rating/earnings trajectory scenarios

## When To Downgrade

Do not output exact levels when:

- source data cannot be verified
- source mismatch is material and unresolved
- tradability is unclear
- structure is too chaotic for a clean invalidation line

Switch to conditional trigger ranges and explicit invalidation criteria.

## Output Style

When exact levels are used:

- tie numbers to exact anchor-session date
- state setup type clearly
- include key support and resistance
- compute risk/reward from trigger, stop, and first target
