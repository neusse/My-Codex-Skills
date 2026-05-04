# Trading Window And Calendar

Use this file to determine anchor session and timing language for US markets.

## Default Time Zone

Use America/New_York and exact dates.

## Session Handling

### After regular close and before next regular open

This is the preferred window.

- use latest completed regular session as anchor day
- add overnight company/macro updates
- write intended buy window for next regular session explicitly

### During live regular session

State clearly that framework is optimized for post-close to pre-open and intraday conclusions are provisional.

During live hours:

- do not treat current session as final
- separate completed-session facts from live observations
- avoid overconfident exact levels while tape is evolving

### Weekend or market holiday

Use most recent completed trading session as anchor and state this explicitly.

When next session date is uncertain:

- avoid relative phrasing only
- use wording like `next regular trading session open`

## Exact-Date Rule

Whenever relative dates may confuse, include exact dates for:

- anchor session date
- catalyst dates
- intended buy window
- review or sell window

## Timing Language

Use horizon-appropriate phrasing:

- short term: `next open 09:35-10:30 ET`, `on breakout confirmation`
- medium term: `staged entry over next 1-5 sessions`
- long term: `staged accumulation over next 5-20 sessions`

Do not mix long-term thesis language with tight intraday execution language unless explicitly explaining horizon shift.
