# Universe And Risk Filters

Use this file before scoring candidates.

## Default Universe

By default, include only:

- US-listed common equities
- US-listed ETFs

Exclude unless user explicitly asks:

- options
- futures
- mutual funds
- crypto products
- OTC/pink sheet symbols

## Hard Exclusions

Normally exclude from final picks:

- halted symbols
- symbols with unresolved delisting/compliance alerts
- symbols with unresolved accounting/fraud/governance alarms
- symbols with insufficient price history for target horizon

## Listing-History Rules

Minimum structure rules:

- short term: at least 20 complete daily rows preferred
- medium term: at least 60 complete daily rows preferred
- long term: at least 120 complete daily rows preferred and ideally one full year

If history is too short, state that explicitly instead of pretending structure is reliable.

## Liquidity And Execution Rules

Downgrade exact-price plans when:

- average volume is too low for believable fills
- slippage risk is unusually high
- open behavior is highly erratic relative to planned trigger

## Concentration Rules

Avoid over-concentration in:

- one macro theme
- one narrow sector
- one correlated risk cluster

If multiple symbols are similar, keep the strongest expression and remove weaker copies.

## Disclosure Rules

Before finalizing a pick, check for:

- upcoming earnings date
- major insider/sponsor selling activity
- regulatory or legal developments
- material balance-sheet stress

If negative disclosures materially weaken thesis, remove symbol even if price action looks strong.
