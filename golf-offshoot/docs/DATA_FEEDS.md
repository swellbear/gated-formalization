# Data feeds

## Contract

Every `DataFeed.fetch` returns `(payload, DataQuality)`.

`DataQuality` includes: score, role (primary / fallback / mock / manual), **source_kind**, source name, as-of time, n observations, lag hours, missing flag, notes.

`source_kind` is one of:

| Label | Meaning |
|-------|---------|
| `real_live` | Current public feed (this week’s scoreboard, forecast, live odds) |
| `real_historical` | Archived real observations (completed ESPN leaderboards, Open-Meteo archive) |
| `derived_from_real` | Transform of real observations (finish-percentile talent, form residual, wind fit) |
| `unavailable` | No source; field is missing — **not** filled with a fake number |
| `mock` | Unit tests and the labeled `python -m golf_offshoot demo` path only |

## Hard rule

Mocks are **banned** from rankings, probabilities, edges, calibration, strategy advice, and pressure tests. If a real source is missing, the operating path marks the field `unavailable`, documents the gap, and lowers reliability. It does not silently substitute zeros or demo names.

`FieldSnapshot.operating=True` makes the pipeline raise `MockOnOperatingPathError` if any mock-labeled quality appears.

## Primary vs fallback

`FallbackChain` still exists. Operating ingest uses explicit primary/fallback **without** mock feeds in the chain:

| Need | Primary | Fallback | If both fail |
|------|---------|----------|----------------|
| Field list / IDs | ESPN leaderboard (`site.web.api`) | Pinned-book Winner names (Bovada or Polymarket, not mixed) joined to ESPN history ids by name | **Unavailable** — `n=0`; no invented athlete ids |
| Talent / form / course history | Derived from ESPN completed leaderboards (events that **started before** this tee time) | — | wide prior, unconstrained form |
| Season driving / putts/GIR | ESPN athlete overview rankings | — | those factors unconstrained |
| Strokes gained long-term | PGA Tour GraphQL `THROUGH_EVENT` of the last completed pill dated **before** this tee time | Season StatDetails, then prior-season table | **Unavailable** for unmatched names |
| Recent SG windows | Data Golf last-8 fields if a key exists **and** the payload contains a true recent window; otherwise PGA Tour GraphQL `EVENT_ONLY` mean of the last **16** completed pills before tee time (weeks the player actually appears; misses skipped, not zero-filled) | — | **Unavailable** — season tables are **not** used as last-N |
| Odds | The Odds API if `THE_ODDS_API_KEY` is set **and** a golf outright exists | Bovada public golf coupon (`Winner` / `Winner Live` / Finishes when listed) | **Unavailable** — no invented prices |
| Odds (Hard Rock Bet) | The Odds API with `bookmakers=hardrockbet` (and FL/AZ/OH skins, not averaged) when `--book hardrockbet` or `GOLF_ODDS_BOOK=hardrockbet` | — (Bovada is **not** a substitute) | **Unavailable** — Hard Rock has no Bovada-style public CLI coupon |
| Odds (Polymarket) | Polymarket **US** golf futures (`gateway.polymarket.us`, `--book polymarket`) | — (Gamma international and Bovada are **not** substitutes) | **Unavailable** — unmatched names stay unmatched; no CLOB orders |
| OWGR | ESPN rankings core endpoint | — | **Unavailable** (endpoint empty) |
| Weather now | ESPN course AccuWeather blob | Open-Meteo forecast | weather unconstrained |
| Weather history | Open-Meteo archive | — | weather-fit unconstrained |
| Health | ESPN `STATUS_WITHDRAW` | — | injury wire **Unavailable** |
| Course agronomy (stimp, rough, firmness) | — | — | **Unavailable**; yards/par/name are real |

HTTP GET/POST responses are snapshotted under `data/cache/` (sha256 of URL, plus canonical POST body) so a run can be reproduced.

Odds TTL / cache policy:

| Mode | TTL | If the fetch fails |
|------|-----|--------------------|
| Pre-tournament | 600s (10 min) | Disk snapshot may be used if younger than 15 min, labeled `STALE_FALLBACK`, quality cut |
| Live | 45s | Same fallback; if the snapshot is **older than 15 min**, quotes are **not** used for edges (`EDGES_SUPPRESSED_STALE`) |

`--refresh` bypasses TTL and always tries the network. Live passes do **not** reload ESPN history just to refresh odds. PGA SG tables use a 6-hour TTL.

ESPN `STATUS_FINISH` means the player has holed out the **current round**. Hole count uses `period` (round number) + `thru`, not 72, so a finished Round 1 is 18 holes remaining 54.

## Odds de-juice

Bovada (and Odds API / Hard Rock Bet via Odds API) decimals are stored with `as_of` and `book`. Overround removal is **proportional**:

```
implied_raw_i = 1 / decimal_i
implied_fair_i = implied_raw_i / Σ_j implied_raw_j
```

Displayed Win edge is `model_p − implied_fair`. That is a probability-scale comparison, not a ticket. Live winner coupons can carry a large overround; longshot fair probs shrink a lot. The decision/strategy layer therefore also requires **beating the posted number**: Winner uses `model_p − 1/decimal ≥ MIN_EDGE_TO_CONSIDER` (3pp). End-of-round leader still has to beat the Yes ask, but the consider bar scales with posted Yes (floored, capped at Winner 3pp). Players with no matched outcome are `unavailable` — no invented price.

Place / top-10 / top-5 / top-20 / make-cut / win-after-round-1/2/3 are ingested **only** if a matching coupon actually lists that market. Winner decimals are never converted into place or after-round prices. St. Jude Winner Live often has no Finishes card — those markets stay `unavailable`.

`--book hardrockbet` pins the operating path to Hard Rock Bet. Bovada prices are not used as a stand-in. That path needs `THE_ODDS_API_KEY` (shell env or `golf-offshoot/.env`; do not commit the file). Without it Hard Rock odds stay **unavailable**. Opening archives are stored per book family so a Bovada open is never relabeled as a Hard Rock open.

`--book polymarket` pins **Polymarket US** golf futures from `gateway.polymarket.us/v2/sports/golf/events?type=futures`. For this BMW week that is Winner plus End of Round 1/2/3 Leader (`pga-bmwcham-2026-08-20-w` / `…-r1l` / `r2l` / `r3l`). Top 5/10/20 on gamma-api.polymarket.com are international website cards and are not ingested. Classification uses the US question/title (`BMW Championship Winner`, `End of Round 1 Leader`). Posted Yes is `bestAskQuote.value` (decimal `1 / ask`). Typed fills mark with `bestBidQuote`. The CLI never places orders. Polymarket paper stays on path `polymarket`. Strategy uses Win or P(lead after round N) for those US cards only.

Bovada `Winner Live` during the round is an **in-play** outright (`book=bovada_live`), not a frozen opening line. A distinct prematch `Winner` coupon, when present on the same event, is stored as `line_role=opening`. The first observed prematch coupon is also archived under `data/openings/` and merged back after the market flips live. Current in-play prices are never relabeled as opens. If no distinct prematch coupon was captured, opening stays `unavailable`.

## Strokes gained

`pga_sg.py` POSTs the same public AppSync GraphQL operation `StatDetails` that pgatour.com/stats uses (`tourCode=R`), now with `eventQuery`.

- **Long-term:** `queryType=THROUGH_EVENT` for the last PGA tournament pill whose ESPN start is strictly before this event. Leakage rule: `THROUGH_EVENT(T)` includes T, so event T never uses its own pill.
- **Recent:** mean of up to 16 `queryType=EVENT_ONLY` tables for pills dated before this start. A player who skipped a week is absent from that table and is **not** zero-filled. Depth is measured events per player (p10/p50/p90), not the requested window length. If EVENT_ONLY fails or the window is empty, recent-SG is `unavailable`.
- Season-to-date (`eventQuery=null`) is a **fallback for long-term only**, never a fake last-8.

`asof_sg.py` binds pills to ESPN dates (token overlap ≥ 2, 1-to-1 across years). Undated pills are unused so a current-week pill cannot leak. StatDetails pills are loaded for the current year and the two prior seasons.

`datagolf.py` remains the preferred recent-window source when a key exists **and** the payload has last-8 fields. Without a key, PGA EVENT_ONLY last-16 is the real alternative.

The Bayesian board seeds `recent_form` from `PlayerInputs.recent_sg.total` when that profile is present. Per-player quality scales with measured EVENT_ONLY weeks. Finish residuals stay on `short_term_trend` and are **not** blended into recent-SG. Long-term THROUGH_EVENT still fills `sg_match` / `approach_sg` / ARG / putting.

## Connectors

| Module | Source |
|--------|--------|
| `data_feeds/espn.py` | ESPN site.web leaderboard, core season event lists, athlete overview |
| `data_feeds/openmeteo.py` | Geocoding + forecast + archive |
| `data_feeds/odds_api.py` | The Odds API outrights (key required; golf coverage is typically majors) |
| `data_feeds/bovada.py` | Public Bovada golf coupons — Winner / Winner Live / Finishes when listed; prematch + live URLs merged |
| `data_feeds/pga_sg.py` | PGA Tour GraphQL SG:OTT/APP/ARG/PUTT/Total — season, THROUGH_EVENT, EVENT_ONLY |
| `data_feeds/asof_sg.py` | Bind pills to ESPN dates; as-of long-term + last-16 EVENT_ONLY mean |
| `data_feeds/openings.py` | First-seen prematch coupon archive; never stores Winner Live |
| `data_feeds/datagolf.py` | Data Golf recent-SG windows when a key and true window fields exist |
| `audit/shadow.py` | Paper-observation JSONL of strategy advises (never a ticket) |
| `data_feeds/ingest.py` | `RealIngestor` — operating assembler |
| `data_feeds/history.py` | Pre-event feature index (no future leakage) |
| `data_feeds/names.py` | Accent/punctuation-insensitive player matching |
| `data_feeds/mocks.py` | Demo/tests only |

## CLI

```bash
python -m golf_offshoot ingest              # current PGA event, real data
python -m golf_offshoot ingest --event 401811963 --book bovada
python -m golf_offshoot live --event 401811963 --book bovada
python -m golf_offshoot shadow                 # review paper-observation advises
```
