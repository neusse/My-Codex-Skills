# US Validation Matrix

Use this matrix to validate US-skill behavior before release.

## Deterministic Tests

| Scenario | Command | Expected Result |
|---|---|---|
| Symbol normalization | `python scripts/smoke_test.py` | `BRK-B` normalizes to canonical `BRK.B` and yfinance symbol `BRK-B` |
| Source precedence | `python scripts/smoke_test.py` | Schwab selected when both Schwab and Alpaca are available |
| Portfolio buy with budget | `python scripts/smoke_test.py` | `AAPL` buy at 200 with budget 1000 creates 5 shares and cash 9000 |

## Integration Scenarios

| Scenario | Command | Expected Result |
|---|---|---|
| Fetch normalized data | `python scripts/fetch_us_market_data.py AAPL --days 120 --pretty` | Includes `latest_complete_session`, `previous_session`, `windows`, `source_diagnostics`, `mismatch_diagnostics` |
| Fallback behavior | Disable Schwab access and run fetch | `source_selection.source_downgrade=true` and authoritative provider `alpaca` |
| Intraday summary | `python scripts/fetch_us_market_data.py SPY --include-intraday --pretty` | `intraday.available` reflects provider minute-data availability |

## Backtest Scenarios

| Scenario | Command | Expected Result |
|---|---|---|
| Auto source backtest | `python scripts/backtest_short_term_rule_us.py AAPL --source auto --start-date 20250101 --end-date 20260410 --pretty` | Reports source, closed trades, return, max drawdown |
| Explicit yfinance backtest | `python scripts/backtest_short_term_rule_us.py SPY --source yfinance --start-date 20250101 --end-date 20260410 --pretty` | Completes with `data_source=yfinance` |

## CI Gate

The following must pass on each PR:

1. `python -m compileall scripts`
2. deterministic validation block in `.github/workflows/ci.yml`
3. `python scripts/smoke_test.py`
