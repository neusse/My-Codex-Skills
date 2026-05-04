#!/usr/bin/env python3
"""US market data providers and normalization utilities."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from statistics import mean
from typing import Any
from zoneinfo import ZoneInfo

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency at runtime
    load_dotenv = None


ET_ZONE = ZoneInfo("America/New_York")
DEFAULT_PRICE_TOLERANCE = 0.01
DEFAULT_VOLUME_TOLERANCE_PCT = 2.0


class FetchError(RuntimeError):
    """Raised when no usable market data can be produced."""


@dataclass(frozen=True)
class NormalizedSymbol:
    canonical: str
    schwab: str
    alpaca: str
    yfinance: str


@dataclass
class ProviderResult:
    provider: str
    requested_symbol: str
    provider_symbol: str
    available: bool
    history_rows: list[dict[str, Any]]
    latest_quote: dict[str, Any] | None = None
    intraday_summary: dict[str, Any] | None = None
    error: str | None = None


def _compact_exception(exc: Exception) -> str:
    return f"{type(exc).__name__}: {exc}"


def load_env() -> None:
    """Load .env without overriding process-level environment variables."""
    if load_dotenv is not None:
        load_dotenv(override=False)


def normalize_us_symbol(raw: str) -> NormalizedSymbol:
    if not raw or not raw.strip():
        raise FetchError("symbol is required")

    symbol = raw.strip().upper().replace(" ", "")
    symbol = symbol.replace("/", ".")
    if "-" in symbol and "." not in symbol and symbol.count("-") == 1:
        left, right = symbol.split("-", 1)
        if len(right) == 1:
            symbol = f"{left}.{right}"

    if not re.fullmatch(r"[A-Z][A-Z0-9.\-]{0,14}", symbol):
        raise FetchError(f"unsupported US symbol format: {raw!r}")

    return NormalizedSymbol(
        canonical=symbol,
        schwab=symbol,
        alpaca=symbol,
        yfinance=symbol.replace(".", "-"),
    )


def _require_env(keys: list[str], *, provider: str) -> dict[str, str]:
    missing = [key for key in keys if not os.getenv(key)]
    if missing:
        joined = ", ".join(missing)
        raise FetchError(
            f"{provider} requires environment variables: {joined}. "
            f"Add them to system environment or .env before running."
        )
    return {key: str(os.getenv(key)) for key in keys}


def _to_yyyymmdd(timestamp_like: Any) -> str:
    if timestamp_like is None:
        raise FetchError("cannot format missing timestamp")
    if isinstance(timestamp_like, datetime):
        dt = timestamp_like
    else:
        if isinstance(timestamp_like, (int, float)):
            dt = datetime.fromtimestamp(float(timestamp_like), tz=UTC)
        else:
            text = str(timestamp_like)
            if text.endswith("Z"):
                text = text[:-1] + "+00:00"
            dt = datetime.fromisoformat(text)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(ET_ZONE).strftime("%Y%m%d")


def _safe_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _safe_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(float(value))


def summarize_window(rows: list[dict[str, Any]], size: int) -> dict[str, Any] | None:
    if len(rows) < size:
        return None
    window = rows[-size:]
    amounts = [float(row["amount_estimate"]) for row in window if row.get("amount_estimate") is not None]
    closes = [float(row["close"]) for row in window]
    return {
        "sessions": size,
        "high": max(float(row["high"]) for row in window),
        "low": min(float(row["low"]) for row in window),
        "avg_volume": round(mean(float(row["volume"]) for row in window if row.get("volume") is not None), 2),
        "avg_amount_estimate": round(mean(amounts), 2) if amounts else None,
        "change_pct": round(((closes[-1] / closes[0]) - 1.0) * 100.0, 2),
    }


def build_windows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        key: summarize_window(rows, size)
        for key, size in (
            ("5d", 5),
            ("10d", 10),
            ("20d", 20),
            ("60d", 60),
            ("120d", 120),
        )
    }


def summarize_intraday(points: list[dict[str, Any]]) -> dict[str, Any]:
    if not points:
        return {"available": False}

    prices = [float(p["price"]) for p in points]
    high_price = max(prices)
    low_price = min(prices)
    close_price = prices[-1]
    close_location = None
    if high_price != low_price:
        close_location = round((close_price - low_price) / (high_price - low_price), 4)

    return {
        "available": True,
        "points": len(points),
        "open_price": prices[0],
        "close_price": close_price,
        "high_price": high_price,
        "low_price": low_price,
        "high_time": next(p["time"] for p in points if float(p["price"]) == high_price),
        "low_time": next(p["time"] for p in points if float(p["price"]) == low_price),
        "close_location_in_day_range": close_location,
    }


def compare_latest_rows(
    authoritative_row: dict[str, Any] | None,
    secondary_row: dict[str, Any] | None,
    *,
    price_tolerance: float = DEFAULT_PRICE_TOLERANCE,
    volume_tolerance_pct: float = DEFAULT_VOLUME_TOLERANCE_PCT,
) -> dict[str, Any] | None:
    if not authoritative_row or not secondary_row:
        return None

    out: dict[str, Any] = {
        "date_match": authoritative_row.get("date") == secondary_row.get("date"),
        "price_tolerance": price_tolerance,
        "volume_tolerance_pct": volume_tolerance_pct,
    }

    core_match = out["date_match"]
    for field in ("open", "high", "low", "close"):
        left = _safe_float(authoritative_row.get(field))
        right = _safe_float(secondary_row.get(field))
        diff = None if left is None or right is None else round(abs(left - right), 6)
        match = left is not None and right is not None and diff <= price_tolerance
        core_match = core_match and match
        out[field] = {
            "authoritative": left,
            "secondary": right,
            "abs_diff": diff,
            "match": match,
        }

    left_volume = _safe_float(authoritative_row.get("volume"))
    right_volume = _safe_float(secondary_row.get("volume"))
    volume_diff_pct = None
    volume_match = False
    if left_volume and right_volume:
        volume_diff_pct = abs(left_volume - right_volume) / left_volume * 100.0
        volume_match = volume_diff_pct <= volume_tolerance_pct
    out["volume"] = {
        "authoritative": _safe_int(left_volume),
        "secondary": _safe_int(right_volume),
        "diff_pct": round(volume_diff_pct, 6) if volume_diff_pct is not None else None,
        "match": volume_match,
    }
    out["all_core_fields_match"] = bool(core_match)
    return out


def determine_market_phase(now_et: datetime | None = None) -> dict[str, Any]:
    now_et = now_et or datetime.now(ET_ZONE)
    weekday = now_et.weekday()
    time_hhmm = now_et.strftime("%H:%M")

    if weekday >= 5:
        phase = "weekend_closed"
    else:
        minute_of_day = now_et.hour * 60 + now_et.minute
        if minute_of_day < 4 * 60:
            phase = "overnight"
        elif minute_of_day < 9 * 60 + 30:
            phase = "premarket"
        elif minute_of_day < 16 * 60:
            phase = "regular"
        elif minute_of_day < 20 * 60:
            phase = "after_hours"
        else:
            phase = "overnight"

    return {
        "timezone": "America/New_York",
        "generated_at_et": now_et.isoformat(timespec="seconds"),
        "weekday": weekday,
        "time_et": time_hhmm,
        "market_phase": phase,
    }


def _normalize_daily_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        if any(row.get(field) is None for field in ("date", "open", "high", "low", "close")):
            continue
        close = float(row["close"])
        volume = _safe_float(row.get("volume"))
        out.append(
            {
                "date": str(row["date"]),
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": close,
                "volume": _safe_int(volume),
                "amount_estimate": round(close * volume, 2) if volume is not None else None,
            }
        )

    out.sort(key=lambda item: item["date"])
    dedup: dict[str, dict[str, Any]] = {row["date"]: row for row in out}
    return [dedup[key] for key in sorted(dedup)]


def _result_unavailable(provider: str, requested_symbol: str, provider_symbol: str, exc: Exception) -> ProviderResult:
    return ProviderResult(
        provider=provider,
        requested_symbol=requested_symbol,
        provider_symbol=provider_symbol,
        available=False,
        history_rows=[],
        error=_compact_exception(exc),
    )


def fetch_from_schwab(symbols: NormalizedSymbol, *, days: int, include_intraday: bool) -> ProviderResult:
    try:
        load_env()
        env = _require_env(
            ["SCHWAB_API_KEY", "SCHWAB_APP_SECRET", "SCHWAB_CALLBACK_URL", "SCHWAB_TOKEN_PATH"],
            provider="Schwab",
        )

        token_path = env["SCHWAB_TOKEN_PATH"]
        if not os.path.exists(token_path):
            raise FetchError(f"Schwab token file does not exist: {token_path}")

        from schwab.auth import easy_client

        client = easy_client(
            api_key=env["SCHWAB_API_KEY"],
            app_secret=env["SCHWAB_APP_SECRET"],
            callback_url=env["SCHWAB_CALLBACK_URL"],
            token_path=token_path,
        )

        hist_response = client.get_price_history_every_day(symbols.schwab)
        if getattr(hist_response, "status_code", 500) >= 400:
            raise FetchError(
                f"Schwab history request failed ({hist_response.status_code}): {getattr(hist_response, 'text', '')}"
            )
        hist_payload = hist_response.json()
        raw_rows = []
        for candle in hist_payload.get("candles", []):
            raw_rows.append(
                {
                    "date": _to_yyyymmdd(candle.get("datetime")),
                    "open": _safe_float(candle.get("open")),
                    "high": _safe_float(candle.get("high")),
                    "low": _safe_float(candle.get("low")),
                    "close": _safe_float(candle.get("close")),
                    "volume": _safe_int(candle.get("volume")),
                }
            )

        rows = _normalize_daily_rows(raw_rows)
        rows = rows[-max(days, 2) :]

        latest_quote = None
        try:
            quote_response = client.get_quote(symbols.schwab)
            if getattr(quote_response, "status_code", 500) < 400:
                quote_payload = quote_response.json()
                if isinstance(quote_payload, dict):
                    latest_quote = quote_payload.get(symbols.schwab, quote_payload)
        except Exception:
            latest_quote = None

        intraday_summary = None
        if include_intraday:
            try:
                minute_response = client.get_price_history_every_minute(symbols.schwab)
                if getattr(minute_response, "status_code", 500) < 400:
                    minute_payload = minute_response.json()
                    points: list[dict[str, Any]] = []
                    for candle in minute_payload.get("candles", [])[-390:]:
                        dt = datetime.fromtimestamp(float(candle.get("datetime", 0)) / 1000.0, tz=UTC).astimezone(ET_ZONE)
                        points.append(
                            {
                                "time": dt.strftime("%H:%M"),
                                "price": _safe_float(candle.get("close")),
                            }
                        )
                    points = [p for p in points if p.get("price") is not None]
                    intraday_summary = summarize_intraday(points)
            except Exception:
                intraday_summary = {"available": False}

        return ProviderResult(
            provider="schwab",
            requested_symbol=symbols.canonical,
            provider_symbol=symbols.schwab,
            available=bool(rows),
            history_rows=rows,
            latest_quote=latest_quote,
            intraday_summary=intraday_summary,
            error=None if rows else "Schwab returned no daily rows",
        )
    except Exception as exc:
        return _result_unavailable("schwab", symbols.canonical, symbols.schwab, exc)


def _extract_alpaca_bars(raw: Any, symbol: str) -> list[Any]:
    if hasattr(raw, "data") and isinstance(raw.data, dict):
        bars = raw.data.get(symbol)
        if bars is not None:
            return list(bars)

    if isinstance(raw, dict):
        if symbol in raw and isinstance(raw[symbol], list):
            return raw[symbol]
        bars_obj = raw.get("bars") if isinstance(raw.get("bars"), dict) else None
        if bars_obj and symbol in bars_obj:
            return list(bars_obj[symbol])
    return []


def _alpaca_bar_to_row(bar: Any) -> dict[str, Any] | None:
    if isinstance(bar, dict):
        timestamp = bar.get("timestamp") or bar.get("t")
        open_ = bar.get("open") if "open" in bar else bar.get("o")
        high = bar.get("high") if "high" in bar else bar.get("h")
        low = bar.get("low") if "low" in bar else bar.get("l")
        close = bar.get("close") if "close" in bar else bar.get("c")
        volume = bar.get("volume") if "volume" in bar else bar.get("v")
    else:
        timestamp = getattr(bar, "timestamp", None) or getattr(bar, "t", None)
        open_ = getattr(bar, "open", None) if hasattr(bar, "open") else getattr(bar, "o", None)
        high = getattr(bar, "high", None) if hasattr(bar, "high") else getattr(bar, "h", None)
        low = getattr(bar, "low", None) if hasattr(bar, "low") else getattr(bar, "l", None)
        close = getattr(bar, "close", None) if hasattr(bar, "close") else getattr(bar, "c", None)
        volume = getattr(bar, "volume", None) if hasattr(bar, "volume") else getattr(bar, "v", None)

    if timestamp is None:
        return None

    return {
        "date": _to_yyyymmdd(timestamp),
        "open": _safe_float(open_),
        "high": _safe_float(high),
        "low": _safe_float(low),
        "close": _safe_float(close),
        "volume": _safe_int(volume),
    }


def fetch_from_alpaca(symbols: NormalizedSymbol, *, days: int, include_intraday: bool) -> ProviderResult:
    try:
        load_env()
        env = _require_env(["ALPACA_PAPER_API_KEY", "ALPACA_PAPER_SECRET"], provider="Alpaca")

        from alpaca.data.historical import StockHistoricalDataClient
        from alpaca.data.requests import StockBarsRequest
        from alpaca.data.timeframe import TimeFrame

        client = StockHistoricalDataClient(
            api_key=env["ALPACA_PAPER_API_KEY"],
            secret_key=env["ALPACA_PAPER_SECRET"],
            url_override=os.getenv("ALPACA_PAPER_ENDPOINT"),
        )

        start = datetime.now(UTC) - timedelta(days=max(days * 3, 365))
        end = datetime.now(UTC)

        daily_request = StockBarsRequest(
            symbol_or_symbols=[symbols.alpaca],
            timeframe=TimeFrame.Day,
            start=start,
            end=end,
        )
        daily_raw = client.get_stock_bars(daily_request)
        rows = [_alpaca_bar_to_row(bar) for bar in _extract_alpaca_bars(daily_raw, symbols.alpaca)]
        rows = [row for row in rows if row is not None]
        daily_rows = _normalize_daily_rows(rows)[-max(days, 2) :]

        intraday_summary = None
        if include_intraday:
            minute_request = StockBarsRequest(
                symbol_or_symbols=[symbols.alpaca],
                timeframe=TimeFrame.Minute,
                start=datetime.now(UTC) - timedelta(days=2),
                end=end,
            )
            minute_raw = client.get_stock_bars(minute_request)
            minute_points: list[dict[str, Any]] = []
            for bar in _extract_alpaca_bars(minute_raw, symbols.alpaca)[-390:]:
                row = _alpaca_bar_to_row(bar)
                if not row:
                    continue
                timestamp = getattr(bar, "timestamp", None) if not isinstance(bar, dict) else bar.get("timestamp") or bar.get("t")
                if timestamp is None:
                    continue
                dt = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00")).astimezone(ET_ZONE)
                minute_points.append({"time": dt.strftime("%H:%M"), "price": row["close"]})
            intraday_summary = summarize_intraday(minute_points)

        return ProviderResult(
            provider="alpaca",
            requested_symbol=symbols.canonical,
            provider_symbol=symbols.alpaca,
            available=bool(daily_rows),
            history_rows=daily_rows,
            intraday_summary=intraday_summary,
            error=None if daily_rows else "Alpaca returned no daily rows",
        )
    except Exception as exc:
        return _result_unavailable("alpaca", symbols.canonical, symbols.alpaca, exc)


def fetch_from_yfinance(symbols: NormalizedSymbol, *, days: int, include_intraday: bool) -> ProviderResult:
    try:
        import yfinance as yf

        ticker = yf.Ticker(symbols.yfinance)
        history = ticker.history(
            period=f"{max(days * 2, 365)}d",
            interval="1d",
            auto_adjust=False,
            actions=False,
        )
        if history.empty:
            raise FetchError(f"yfinance returned no rows for {symbols.yfinance}")

        rows: list[dict[str, Any]] = []
        for idx, row in history.iterrows():
            rows.append(
                {
                    "date": idx.tz_localize(ET_ZONE).strftime("%Y%m%d") if idx.tzinfo is None else idx.tz_convert(ET_ZONE).strftime("%Y%m%d"),
                    "open": _safe_float(row.get("Open")),
                    "high": _safe_float(row.get("High")),
                    "low": _safe_float(row.get("Low")),
                    "close": _safe_float(row.get("Close")),
                    "volume": _safe_int(row.get("Volume")),
                }
            )

        daily_rows = _normalize_daily_rows(rows)[-max(days, 2) :]

        intraday_summary = None
        if include_intraday:
            intraday = ticker.history(period="1d", interval="1m", auto_adjust=False, prepost=True)
            if not intraday.empty:
                points: list[dict[str, Any]] = []
                for idx, row in intraday.tail(390).iterrows():
                    dt = idx.tz_localize(ET_ZONE) if idx.tzinfo is None else idx.tz_convert(ET_ZONE)
                    points.append({"time": dt.strftime("%H:%M"), "price": _safe_float(row.get("Close"))})
                points = [point for point in points if point["price"] is not None]
                intraday_summary = summarize_intraday(points)

        return ProviderResult(
            provider="yfinance",
            requested_symbol=symbols.canonical,
            provider_symbol=symbols.yfinance,
            available=bool(daily_rows),
            history_rows=daily_rows,
            intraday_summary=intraday_summary,
            error=None if daily_rows else "yfinance returned no normalized rows",
        )
    except Exception as exc:
        return _result_unavailable("yfinance", symbols.canonical, symbols.yfinance, exc)


def choose_authoritative_source(results: dict[str, ProviderResult]) -> tuple[str, bool, str | None]:
    schwab = results.get("schwab")
    alpaca = results.get("alpaca")

    if schwab and schwab.available and schwab.history_rows:
        return "schwab", False, None

    if alpaca and alpaca.available and alpaca.history_rows:
        reason = "Schwab unavailable; switched authoritative source to Alpaca"
        return "alpaca", True, reason

    raise FetchError(
        "No authoritative source available. "
        f"Schwab error: {schwab.error if schwab else 'not requested'}; "
        f"Alpaca error: {alpaca.error if alpaca else 'not requested'}"
    )


def fetch_normalized_us_data(
    symbol: str,
    *,
    days: int = 120,
    include_intraday: bool = False,
    skip_yfinance: bool = False,
    skip_alpaca: bool = False,
) -> dict[str, Any]:
    symbols = normalize_us_symbol(symbol)

    results: dict[str, ProviderResult] = {}
    results["schwab"] = fetch_from_schwab(symbols, days=days, include_intraday=include_intraday)

    if not skip_alpaca:
        results["alpaca"] = fetch_from_alpaca(symbols, days=days, include_intraday=include_intraday)
    else:
        results["alpaca"] = ProviderResult(
            provider="alpaca",
            requested_symbol=symbols.canonical,
            provider_symbol=symbols.alpaca,
            available=False,
            history_rows=[],
            error="skipped_by_flag",
        )

    if not skip_yfinance:
        results["yfinance"] = fetch_from_yfinance(symbols, days=days, include_intraday=include_intraday)
    else:
        results["yfinance"] = ProviderResult(
            provider="yfinance",
            requested_symbol=symbols.canonical,
            provider_symbol=symbols.yfinance,
            available=False,
            history_rows=[],
            error="skipped_by_flag",
        )

    authoritative_provider, source_downgrade, fallback_reason = choose_authoritative_source(results)
    authoritative_rows = results[authoritative_provider].history_rows[-max(days, 2) :]
    if len(authoritative_rows) < 2:
        raise FetchError(
            f"Authoritative provider {authoritative_provider} returned fewer than 2 sessions"
        )

    latest_complete = authoritative_rows[-1]
    previous_session = authoritative_rows[-2]

    mismatches = {
        provider_name: {
            "available": result.available,
            "error": result.error,
            "comparison": compare_latest_rows(latest_complete, result.history_rows[-1] if result.history_rows else None),
        }
        for provider_name, result in results.items()
        if provider_name != authoritative_provider
    }

    output = {
        "symbol": symbols.canonical,
        "provider_symbols": {
            "schwab": symbols.schwab,
            "alpaca": symbols.alpaca,
            "yfinance": symbols.yfinance,
        },
        "source_selection": {
            "authoritative": authoritative_provider,
            "source_downgrade": source_downgrade,
            "fallback_provider": "alpaca" if source_downgrade else None,
            "fallback_reason": fallback_reason,
        },
        "latest_complete_session": latest_complete,
        "previous_session": previous_session,
        "history_rows": authoritative_rows,
        "windows": build_windows(authoritative_rows),
        "intraday": results[authoritative_provider].intraday_summary or {"available": False},
        "source_diagnostics": {
            name: {
                "available": result.available,
                "error": result.error,
                "history_rows": len(result.history_rows),
                "provider_symbol": result.provider_symbol,
            }
            for name, result in results.items()
        },
        "mismatch_diagnostics": mismatches,
        "anchor_context": {
            **determine_market_phase(),
            "anchor_session_date": latest_complete["date"],
            "previous_session_date": previous_session["date"],
        },
    }

    return output


def get_history_for_source(
    symbol: str,
    *,
    source: str,
    days: int,
    include_intraday: bool = False,
) -> tuple[list[dict[str, Any]], str, str | None]:
    symbols = normalize_us_symbol(symbol)
    provider = source.lower()

    if provider == "schwab":
        result = fetch_from_schwab(symbols, days=days, include_intraday=include_intraday)
        if not result.available:
            raise FetchError(result.error or "Schwab unavailable")
        return result.history_rows, "schwab", None

    if provider == "alpaca":
        result = fetch_from_alpaca(symbols, days=days, include_intraday=include_intraday)
        if not result.available:
            raise FetchError(result.error or "Alpaca unavailable")
        return result.history_rows, "alpaca", None

    if provider == "yfinance":
        result = fetch_from_yfinance(symbols, days=days, include_intraday=include_intraday)
        if not result.available:
            raise FetchError(result.error or "yfinance unavailable")
        return result.history_rows, "yfinance", None

    normalized = fetch_normalized_us_data(
        symbol,
        days=days,
        include_intraday=include_intraday,
        skip_yfinance=False,
        skip_alpaca=False,
    )
    return (
        normalized["history_rows"],
        normalized["source_selection"]["authoritative"],
        normalized["source_selection"].get("fallback_reason"),
    )


def get_latest_price(symbol: str) -> float:
    normalized = fetch_normalized_us_data(
        symbol,
        days=5,
        include_intraday=False,
        skip_yfinance=True,
        skip_alpaca=False,
    )
    return float(normalized["latest_complete_session"]["close"])