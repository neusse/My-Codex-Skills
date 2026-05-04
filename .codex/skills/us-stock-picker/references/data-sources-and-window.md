# Data Sources And Window

Use this file when collecting price anchors, history, and timing context for the US stock picker.

## Default Window

This skill is built for:

- previous regular US trading session close
- overnight company, macro, and policy news
- up to next regular US session open

Treat the latest completed regular session as the primary anchor.

## Preferred Local Entry Point

If helper script exists locally, use it first:

```powershell
.venv\Scripts\python.exe scripts\fetch_us_market_data.py AAPL --days 120 --include-intraday --pretty
```

Use the script to fetch:

- latest complete-session open, high, low, close, volume
- previous-session open and close
- recent 5/10/20/60/120-session structure
- minute-path summary when available
- yfinance cross-check row
- Alpaca cross-check row
- source fallback reason when Schwab is unavailable

## Source Priority

Collect data in this order:

1. local helper script output
2. Schwab API (authoritative)
3. yfinance (cross-check)
4. Alpaca (cross-check and fallback)
5. official SEC filings and company disclosures
6. official releases and reputable market media

## Required Data Pull

For every final candidate, retrieve:

- previous-session open
- previous-session close
- latest complete-session open
- latest complete-session close
- relevant historical window, not just anchor day
- recent highs and lows
- volume context
- one catalyst from earnings/news/policy/company events
- one disclosure or fundamental check

Minimum history windows:

- short term: at least 5 sessions, preferably 10
- medium term: at least 20 sessions, preferably 60
- long term: at least 6 months, preferably 12 months

Do not use user-supplied prices as source of truth.

## Freshness Rules

- short-term exact prices must anchor to latest completed regular session
- medium-term exact prices must anchor to latest completed session plus recent 20-60 session structure
- long-term entry zones must anchor to recent 6-12 month context
- if Schwab and secondary sources disagree, keep Schwab as authoritative and note mismatch
- if Schwab is unavailable and Alpaca is used, explicitly mark source downgrade
- if latest verified price is stale/inconsistent, switch to conditional language instead of fake precision
