#!/usr/bin/env python3
"""Run deterministic smoke tests for the US market skill helpers."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from us_market_data import choose_authoritative_source, compare_latest_rows, normalize_us_symbol, ProviderResult


ROOT = Path(__file__).resolve().parent
FETCH = ROOT / "fetch_us_market_data.py"
BACKTEST = ROOT / "backtest_short_term_rule_us.py"
PORTFOLIO = ROOT / "portfolio_state_us.py"
PYTHON = sys.executable
LIVE_SAMPLES = ["AAPL", "SPY"]


def run_checked(command: list[str]) -> str:
    proc = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed ({proc.returncode}): {' '.join(command)}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )
    return proc.stdout


def run_deterministic_checks() -> dict[str, object]:
    symbol = normalize_us_symbol("brk-b")
    assert symbol.canonical == "BRK.B"
    assert symbol.yfinance == "BRK-B"

    schwab = ProviderResult(
        provider="schwab",
        requested_symbol="AAPL",
        provider_symbol="AAPL",
        available=True,
        history_rows=[{"date": "20260410", "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1}],
    )
    alpaca = ProviderResult(
        provider="alpaca",
        requested_symbol="AAPL",
        provider_symbol="AAPL",
        available=True,
        history_rows=[{"date": "20260410", "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1}],
    )
    source, downgraded, reason = choose_authoritative_source({"schwab": schwab, "alpaca": alpaca})
    assert source == "schwab"
    assert downgraded is False
    assert reason is None

    mismatch = compare_latest_rows(
        {"date": "20260410", "open": 100.0, "high": 102.0, "low": 99.0, "close": 101.0, "volume": 1_000_000},
        {"date": "20260410", "open": 100.01, "high": 102.0, "low": 99.02, "close": 101.0, "volume": 1_010_000},
    )

    state_file = Path.cwd() / "_smoke_state_portfolio_us.json"
    if state_file.exists():
        state_file.unlink()
    try:
        run_checked(
            [
                PYTHON,
                str(PORTFOLIO),
                "--state-file",
                str(state_file),
                "init",
                "--cash",
                "10000",
                "--as-of-date",
                "20260410",
                "--overwrite",
            ]
        )

        run_checked(
            [
                PYTHON,
                str(PORTFOLIO),
                "--state-file",
                str(state_file),
                "buy",
                "AAPL",
                "--price",
                "200",
                "--budget",
                "1000",
                "--date",
                "20260410",
                "--name",
                "Apple Inc",
                "--estimated",
            ]
        )

        portfolio_payload = json.loads(
            run_checked(
                [
                    PYTHON,
                    str(PORTFOLIO),
                    "--state-file",
                    str(state_file),
                    "show",
                ]
            )
        )
    finally:
        if state_file.exists():
            state_file.unlink()

    return {
        "symbol_normalization": {
            "canonical": symbol.canonical,
            "yfinance": symbol.yfinance,
        },
        "source_selection": {
            "authoritative": source,
            "source_downgrade": downgraded,
        },
        "mismatch_check": mismatch,
        "portfolio_sample": {
            "cash_available": portfolio_payload["cash_available"],
            "position_count": len(portfolio_payload["positions"]),
            "first_symbol": portfolio_payload["positions"][0]["symbol"],
            "first_shares": portfolio_payload["positions"][0]["shares"],
        },
    }


def run_live_checks() -> list[dict[str, object]]:
    outputs: list[dict[str, object]] = []
    for symbol in LIVE_SAMPLES:
        payload = json.loads(
            run_checked([PYTHON, str(FETCH), symbol, "--days", "60", "--include-intraday"])
        )
        outputs.append(
            {
                "symbol": payload["symbol"],
                "authoritative": payload["source_selection"]["authoritative"],
                "source_downgrade": payload["source_selection"]["source_downgrade"],
                "anchor_session_date": payload["latest_complete_session"]["date"],
            }
        )

    backtest_payload = json.loads(
        run_checked(
            [
                PYTHON,
                str(BACKTEST),
                "AAPL",
                "--source",
                "auto",
                "--start-date",
                "20250101",
                "--end-date",
                "20260410",
            ]
        )
    )
    outputs.append(
        {
            "backtest": {
                "symbol": backtest_payload["symbol"],
                "data_source": backtest_payload["data_source"],
                "closed_trades": backtest_payload["trades"]["closed"],
            }
        }
    )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="Also run networked checks against configured data providers",
    )
    args = parser.parse_args()

    deterministic = run_deterministic_checks()
    payload: dict[str, object] = {
        "ok": True,
        "mode": "deterministic" if not args.live else "deterministic+live",
        "deterministic": deterministic,
    }

    if args.live:
        payload["live"] = run_live_checks()

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
