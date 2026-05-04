# Output Template

Use this file when writing final stock recommendations.

## Required Shape

If user explicitly asks for one horizon, output only that horizon.

Otherwise provide three sections:

1. Short-term picks
2. Medium-term picks
3. Long-term picks

If capital or holdings context exists, add a short `Capital and Position Context` block before the first section.

Each section must start with this exact column order:

`Symbol | Previous Open | Previous Close | Setup Type | Key Support | Key Resistance | Core Thesis | Entry Timing | Trigger Price | Stop Price | Target 1 | Target 2 | Risk/Reward | Exit Plan | Hold Window | Skip Condition`

Use this Markdown table skeleton:

```markdown
| Symbol | Previous Open | Previous Close | Setup Type | Key Support | Key Resistance | Core Thesis | Entry Timing | Trigger Price | Stop Price | Target 1 | Target 2 | Risk/Reward | Exit Plan | Hold Window | Skip Condition |
|---|---:|---:|---|---:|---:|---|---|---:|---:|---:|---:|---|---|---|---|
| AAPL | 211.10 | 213.45 | Breakout | 209.80 | 214.20 | Earnings momentum + strong tape | 2026-04-14 09:35-10:30 ET | 213.60 | 209.70 | 217.00 | 220.50 | 1:2.1 | Scale out at T1, reassess at T2 | 1-5 days | Skip if open gaps >2% above trigger then loses volume |
```

## Column Guidance

- `Symbol`: ticker plus company/ETF name
- `Previous Open`: verified open of latest complete session
- `Previous Close`: verified close of latest complete session
- `Setup Type`: one of `Breakout` `Pullback` `Trend` `Range Reclaim`
- `Key Support`: structure-derived support
- `Key Resistance`: nearest meaningful resistance
- `Core Thesis`: one short sentence
- `Entry Timing`: concrete execution window in ET
- `Trigger Price`: exact trigger or conditional trigger zone
- `Stop Price`: invalidation level
- `Target 1`: realistic first target
- `Target 2`: stretch target
- `Risk/Reward`: compact summary such as `1:2.1`
- `Exit Plan`: condition-based reduction/review
- `Hold Window`: expected duration
- `Skip Condition`: one sentence when not to enter

## Evidence Notes

After each table, add short notes for each symbol:

- catalyst/disclosure evidence
- price/history evidence
- why it beat nearby alternatives
- suggested share count or max capital usage when capital is known

## Writing Rules

- use exact dates for anchor session and intended entry windows
- keep tables compact
- keep notes short but concrete
- do not pad weak names to fill slots
