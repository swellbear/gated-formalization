# Data feeds

## Contract

Every `DataFeed.fetch` returns `(payload, DataQuality)`.

`DataQuality` includes: score, role (primary / fallback / mock / manual), source name, as-of time, n observations, lag hours, missing flag, notes.

## Rules

| Situation | Behavior |
|-----------|----------|
| Primary throws / times out | `FallbackChain` tries the next feed |
| Primary quality < 0.35 | Skip to fallback; keep primary only if nothing else lands |
| Lag > 36 hours | Quality capped (stale) |
| Missing | `missing=True`, score 0 — **not** treated as evidence of 0 skill |

## Implemented now

Mocks: talent, SG, weather, odds, injury, field. `UnreachablePrimary` exists to test fallback.

To connect a live vendor, implement `DataFeed` and put it first in the chain. Do not teach the engine about HTTP.

## Health / setup

Injury notes are expected to be **low quality**. The engine already moves them less than SG.
