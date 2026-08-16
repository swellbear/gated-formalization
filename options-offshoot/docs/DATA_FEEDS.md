# Data feeds

## Contract

Operating path needs a **real bid and ask**, or the row is `n/a`.

| Need | v1 | If missing |
|------|----|------------|
| Options chain + bid/ask/OI/volume | Polygon snapshot (`admitted_quotes`) | `unavailable` — not a fake mid |
| Spot | Polygon underlying price on the snapshot | `unavailable` |
| Realized vol | Polygon daily aggregates (predeclared price history) | A may use schema default σ; honest path leaves unconstrained |
| Earnings calendar | Polygon if the key’s plan includes it | Frozen `data/fields/earnings_us_week.txt` only as a closed fallback list |
| S&P-style universe | Frozen `data/fields/spx_this_friday.txt` | Empty field |

Key: `POLYGON_API_KEY` in `options-offshoot/.env`. Never commit `.env`.

**Refuse on operating path:** Yahoo, HTML scrape, open web, “whatever chain we found.”

**Later, not v1:** Interactive Brokers venue ask.

Mocks are banned when `operating=True`. Demo is labeled `OFFLINE DEMO — MOCK DATA`.

HTTP responses cache under `data/cache/` (gitignored).
