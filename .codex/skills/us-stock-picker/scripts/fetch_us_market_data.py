#!/usr/bin/env python3
"""Fetch and normalize US market data with Schwab primary and Alpaca fallback."""

from __future__ import annotations

import argparse
import json
import sys

from us_market_data import FetchError, fetch_normalized_us_data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbol", default="BAC", help="US symbol, example: AAPL or BRK.B")
    parser.add_argument("--days", type=int, default=120, help="History rows to keep in output")
    parser.add_argument(
        "--include-intraday",
        action="store_true",
        help="Fetch and summarize minute-level data when providers support it",
    )
    parser.add_argument(
        "--skip-yfinance",
        action="store_true",
        help="Skip yfinance cross-check",
    )
    parser.add_argument(
        "--skip-alpaca",
        action="store_true",
        help="Skip Alpaca cross-check and fallback",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    payload = fetch_normalized_us_data(
        args.symbol,
        days=args.days,
        include_intraday=args.include_intraday,
        skip_yfinance=args.skip_yfinance,
        skip_alpaca=args.skip_alpaca,
    )

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FetchError as exc:
        print(f"Fetch error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(f"Unexpected error: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
