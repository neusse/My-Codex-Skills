# US Environment Contract

This skill loads credentials from `.env` and process environment variables. If both are set, process environment values are used.

## Required Variables

### Schwab

- `SCHWAB_API_KEY`
- `SCHWAB_APP_SECRET`
- `SCHWAB_CALLBACK_URL`
- `SCHWAB_TOKEN_PATH` (absolute path to Schwab token JSON file)

### Alpaca

- `ALPACA_PAPER_API_KEY`
- `ALPACA_PAPER_SECRET`

## Optional Variables

- `ALPACA_PAPER_ENDPOINT` (use only for custom Alpaca endpoint routing)

## Example `.env`

```dotenv
SCHWAB_APP_KEY=your_app_key
SCHWAB_APP_SECRET=your_app_secret
SCHWAB_REDIRECT_URI=https://127.0.0.1
SCHWAB_TOKEN_JSON=C:/secure/schwab/token.json
APCA_API_KEY_ID=your_alpaca_key
APCA_API_SECRET_KEY=your_alpaca_secret
APCA_API_BASE_URL=https://data.alpaca.markets
```

## Failure Modes

- Missing Schwab variables: fetch fails with explicit missing-key error.
- Missing Alpaca variables: cross-check/fallback unavailable; auto source fails if Schwab also unavailable.
- Invalid `SCHWAB_TOKEN_JSON` path: Schwab provider returns token-file-not-found error.

## Troubleshooting

1. Confirm env variables are visible to the current shell process.
2. Confirm `SCHWAB_TOKEN_JSON` points to an existing, readable file.
3. Run deterministic smoke test first: `python scripts/smoke_test.py`.
4. Run live fetch only after env setup: `python scripts/fetch_us_market_data.py AAPL --pretty`.
