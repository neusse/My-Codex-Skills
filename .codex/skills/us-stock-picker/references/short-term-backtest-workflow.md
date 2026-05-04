# Short-Term Backtest Workflow

Use this file to validate the short-term breakout rule with historical US data.

## Goal

Check whether the short-term breakout logic behaves reasonably on recent US symbol history.

## Local Script

Run:

```powershell
.venv\Scripts\python.exe scripts\backtest_short_term_rule_us.py AAPL --start-date 20250101 --end-date 20260410 --source auto --pretty
```

The script uses:

- Schwab history when available
- Alpaca fallback in `auto` mode when Schwab fails
- yfinance when explicitly selected as source
- `backtrader` for order simulation

## Rule Being Tested

Minimal short-term breakout confirmation rule:

- breakout above prior 5-day high
- same-day volume above recent 5-day average by multiplier
- close in upper part of day range
- bullish body confirmation
- stop anchored to recent 3-day support low
- first target from 2.0 risk/reward multiple
- forced time exit after 3 bars if neither stop nor target is hit

## How To Use Result

Use result as confidence check, not proof. Focus on:

- total closed trades
- win rate
- total return
- max drawdown
- trade log tail

If sample size is tiny or drawdown is weak, reduce confidence in short-term narrative.

## Important Limits

- minimal validation harness, not institutional research stack
- daily bars approximate intraday fill quality
- tests one rule family, not full discretionary process
- outcomes vary materially by symbol and window
