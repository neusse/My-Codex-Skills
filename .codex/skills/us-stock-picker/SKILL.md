---
name: us-stock-picker
description: Capital-aware US equities and ETF recommendation, position management, and pre-open planning for the window between the previous regular session close and the next regular session open. Use when Codex needs short-term, medium-term, or long-term US ideas, executable sizing checks, holdings-aware guidance, or portfolio-state updates in stock_logs.
---

# US Stock Picker

## Overview

Recommend US stocks and ETFs across three horizons in one pass:

- 3 short-term picks
- 3 medium-term picks
- 3 long-term picks

This skill is US-only and uses:

- Schwab data as the authoritative source
- yfinance cross-checks
- Alpaca cross-checks and fallback when Schwab is unavailable

It also tracks approximate portfolio state under `stock_logs/portfolio_state_us.json`.

## Operating Window

This skill is optimized for:

- after regular US market close (4:00 PM ET)
- overnight catalyst review
- before the next regular market open (9:30 AM ET)

Use exact dates and America/New_York timing in all plans.

## Local Helper Scripts

Use local scripts first when available:

- `scripts/fetch_us_market_data.py`
- `scripts/backtest_short_term_rule_us.py`
- `scripts/portfolio_state_us.py`
- `scripts/smoke_test.py`

Preferred usage:

```powershell
.venv\Scripts\python.exe scripts\fetch_us_market_data.py AAPL --days 120 --include-intraday --pretty
```

Fetch script output includes:

- latest complete session OHLCV
- previous session OHLCV
- 5/10/20/60/120-session windows
- intraday summary when available
- source diagnostics and mismatch diagnostics
- source downgrade reason when Schwab fails and Alpaca is used

## Environment Contract

Load credentials from `.env` and system environment variables (system env wins).

Required keys:

- `SCHWAB_APP_KEY`
- `SCHWAB_APP_SECRET`
- `SCHWAB_REDIRECT_URI`
- `SCHWAB_TOKEN_JSON`
- `APCA_API_KEY_ID`
- `APCA_API_SECRET_KEY`

Optional:

- `APCA_API_BASE_URL`

If required keys are missing, scripts must fail with explicit errors.

## Capital State And Logging

Default state path:

- `stock_logs/portfolio_state_us.json`

When the user mentions cash, holdings, buy/sell actions, or sizing:

1. load state with `scripts/portfolio_state_us.py show`
2. reconcile with latest user statement
3. update state if a new transaction is clearly implied
4. check executable share count before recommending exact entries

Rules:

- minimum buy size is 1 share
- reject exact executable plans when available cash cannot afford 1 share
- distinguish estimated vs exact transactions when fill details are unknown

## Workflow

### 0. Load capital context first

If the user mentions cash or holdings:

1. read current state
2. calculate deployable cash
3. prioritize existing-position management before new entries

### 1. Confirm output scope

Default output: 3 short-term + 3 medium-term + 3 long-term names.

If user asks for one horizon only, output only that horizon.

### 2. Pull data proactively

Preferred source order:

1. local fetch script output
2. Schwab authoritative session/history data
3. yfinance cross-check
4. Alpaca cross-check and fallback
5. official filings and reputable US market news

Never use user-supplied prices as source of truth.

### 3. Apply hard filters

Reject or downgrade at minimum:

- halted or clearly untradable symbols
- stale or inconsistent data
- symbols with insufficient history for horizon
- names that are non-executable vs user cash when executable picks were requested

### 4. Build evidence pack

Each final pick must include:

1. one price/structure reason
2. one catalyst reason
3. one fundamental/disclosure reason

### 5. Score by horizon

Use horizon framework in `references/horizon-selection-framework.md`.

When exact levels are requested, apply `references/price-plan-rules.md`.

## Output Standard

When capital context exists, start with a compact `Capital and Position Context` block containing:

- total equity estimate
- deployable cash estimate
- current open positions
- whether list is executable or watchlist-only
- assumptions marked as estimates where needed

Section order:

1. Short-term picks
2. Medium-term picks
3. Long-term picks

Each section starts with this table:

`Symbol | Previous Open | Previous Close | Setup Type | Key Support | Key Resistance | Core Thesis | Entry Timing | Trigger Price | Stop Price | Target 1 | Target 2 | Risk/Reward | Exit Plan | Hold Window | Skip Condition`

```markdown
| Symbol | Previous Open | Previous Close | Setup Type | Key Support | Key Resistance | Core Thesis | Entry Timing | Trigger Price | Stop Price | Target 1 | Target 2 | Risk/Reward | Exit Plan | Hold Window | Skip Condition |
|---|---:|---:|---|---:|---:|---|---|---:|---:|---:|---:|---|---|---|---|
| AAPL | 211.10 | 213.45 | Breakout | 209.80 | 214.20 | Earnings momentum + strong tape | 2026-04-14 09:35-10:30 ET | 213.60 | 209.70 | 217.00 | 220.50 | 1:2.1 | Scale at T1, review at T2 | 1-5 days | Skip if opens >2% above trigger and fades volume |
```

After each table, add short notes for each symbol:

- why selected
- key catalyst/disclosure
- why it beat alternatives
- suggested share size or max capital usage when capital is known

## References

Load as needed:

- `references/capital-and-position-management.md`
- `references/data-sources-and-window.md`
- `references/horizon-selection-framework.md`
- `references/price-plan-rules.md`
- `references/output-template.md`
- `references/universe-and-risk-filters.md`
- `references/trading-window-and-calendar.md`
- `references/short-term-backtest-workflow.md`
- `references/us-env-contract.md`
- `references/us-validation-matrix.md`
