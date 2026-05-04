# Capital And Position Management

Use this file whenever the user mentions cash, holdings, position size, add-position, reduce-position, or asks whether a trade is executable.

## Persistent State

Default state path:

- `stock_logs/portfolio_state_us.json`

Default helper:

```powershell
.venv\Scripts\python.exe scripts\portfolio_state_us.py show
```

Use the helper to:

- initialize starting cash
- record estimated or exact buys
- record estimated or exact sells
- show current available cash and market value

## Known Vs Estimated

If exact fill data is missing:

- estimate share count conservatively
- label the transaction as estimated
- state the assumption in the answer and the log

Do not present estimated cash or cost as confirmed facts.

## Small-Account Rules

### Under 5,000 USD

- default to at most 1 active short-term position
- do not recommend a symbol if one share does not fit deployable cash
- if user already has a position above roughly 70% of total equity, new ideas should default to watchlist-only unless existing position is being reduced

### 5,000 to 20,000 USD

- default to at most 2 active short-term positions
- single-idea size usually 25% to 50% depending on conviction and correlation

### Above 20,000 USD

- still avoid concentrated same-theme duplication unless explicitly requested

## Executability Check

Before saying a symbol is executable:

1. compute one-share cost at planned trigger price
2. compare to deployable cash
3. check for correlation with existing positions

If trade is not executable:

- mark it watchlist-only
- do not present a fake exact entry plan

## Allocation Guidance In Answers

When capital is known, every executable short-term idea should include:

- suggested share count or max affordable shares
- rough cash usage
- whether idea is first-priority, backup, or watchlist-only

## Logging Rules

When the user asks to write the stock log, or clearly states a new trade:

- update `stock_logs/portfolio_state_us.json`
- write or append a dated Markdown log under `stock_logs/`
- mention whether state change was exact or estimated

## Post-Trade Management

When the user already holds a symbol and asks for tomorrow's plan:

- manage existing position first
- discuss new buys only after checking whether current position is likely to be reduced
- if not reducing, new names should usually be observation candidates only
