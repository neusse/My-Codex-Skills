# US Migration Runbook

This runbook defines the ordered implementation and validation checklist for the US-only replacement.

## Task Sequence

1. Replace skill surface (`SKILL.md`, `agents/openai.yaml`) with US-only behavior.
2. Replace data stack with provider-based scripts (`fetch_us_market_data.py`, `us_market_data.py`).
3. Replace portfolio tracker with USD logic (`portfolio_state_us.py`).
4. Replace backtest harness with US providers (`backtest_short_term_rule_us.py`).
5. Replace deterministic smoke checks (`scripts/smoke_test.py`) and CI workflow.
6. Rewrite references and README to US-only docs.
7. Remove obsolete China-market scripts and references from command examples.

## Ownership Guide

- Data and provider code: maintain deterministic source precedence and explicit downgrade signals.
- Portfolio logic: keep cash/position math deterministic and schema-stable.
- Docs: ensure every command example maps to existing scripts.
- CI: enforce compile + deterministic checks without requiring live credentials.

## Acceptance Checks

- `python -m compileall scripts` succeeds.
- `python scripts/smoke_test.py` succeeds in deterministic mode.
- Portfolio init/buy/show workflow returns expected cash and share counts.
- `fetch_us_market_data.py` emits required schema keys.
- No docs mention Tonghuashun, AkShare, A-share, or board-lot rules.
