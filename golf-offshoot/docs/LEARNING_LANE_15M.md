# Learning lane: 15-min Kalshi

Lane name: `learning_lane_15m`

Primary series: `KXBTC15M`

Why: continuous 15-min windows + public CF Benchmarks settle → fast feedback for the shared ops loop

Explicit: independent of PGA calendar; not a golf stress sidecar; golf artifacts stay primary for golf Amb

---

This is a **general system learning lane**, not a golf-edge sidecar. The job is the shared operating loop with fast feedback:

**ingest → live → paper autobet → settle join → hub viz → dated weekly honesty**

Hub viz for this lane is not yet available (empty / observation-only). Do not invent charts. Do not carry golf WC1 / Ill into this lane.

## Locked posture

- Trading NOT ARMED. No Kalshi API keys. No cash scopes. No order placement.
- AI never deposit / withdraw / transfer. There is no 15-min cash UI.
- Paper money only. `PAPER OBSERVATION ONLY`.
- Do **not** retune golf θ from 15-min.
- Do **not** widen past `KXBTC15M` in this PR. The adapter has a series registry / config hook (`learning_lane_15m.series_registry`) so later 15-min series can plug in; they stay unshipped here.
- No geo. No LIVE cash. No invented edge / banked-edge claims.
- 15-min Kalshi is not live trading and not a golf WC1 edge.

## Paths (never mix with golf)

| Lane | Artifact root |
|------|----------------|
| golf | `golf-offshoot/data/` (`paper/`, `shadow/`, `exports/`) |
| `learning_lane_15m` | `/workspace/kalshi_15m_exports/` (repo-local fallback: `golf-offshoot/data/learning_lane_15m/`) |

Paper ledger, shadow advises, and settlements for this lane live under the 15m roots only.

## Public adapter

Read-only Kalshi elections API: `https://api.elections.kalshi.com/trade-api/v2/` (`events`, `markets`, `series/KXBTC15M?include_volume=true`). Bare series GET can return `volume_fp=null`.

Settlement source: CF Benchmarks, as documented on event `settlement_sources`. CF index id is pinned `BRTI` (from `rules_primary`).

## Settle / field locks (Kalshi Micro SETUP_MAP)

`/workspace/kalshi-micro/SETUP_MAP.md` + `research.md` were not visible on this box; the Founder locks below are folded in. Cite Digestor spine as the later SOURCE honesty owner.

- **Authoritative settle:** Kalshi market `result` is primary. Support with `settlement_value_dollars`, `settlement_ts`, `expiration_value`.
- **Display-only (not settle):** `yes_bid` / `yes_ask`, `last_price`, `volume`.
- **CF index:** `BRTI` (Bitcoin Real-Time Index). CRYPTO15M rule: 60 RTI prints in the last minute; official value is that average, rounded to 2 decimals.
- **`floor_strike`:** stamped Target / open-avg context once present. Missing → do not invent.
- **Status map:** `finalized` / `determined` + `result` → settle. `active` / `closed` without result → `SETTLE_PENDING`. `disputed` / `under-review` → `SETTLE_PENDING` banner. Hard NO invent.
- **Times:** API UTC `open_time` / `close_time` are the fields. ET labels are display-only. Honor `can_close_early` by waiting for the Kalshi result.
- **Paper marks:** public mid, else last. Record `fee_type=quadratic` × 1 and `tapered_deci_cent` in metadata. Paper money only.
- **CFB websocket / DIY 60s average:** observe/debug only. Hard NO as official settle without match-to-Kalshi result.
- Export root: `/workspace/kalshi_15m_exports/`

# Digestor owns SOURCE honesty digest later. Do not invent Digestor docs.
# Read-only reference boards (do not rewrite):
# `/workspace/kalshi_15m_lab/SPINE_STAMP.md`
# `/workspace/kalshi_15m_lab/SOURCE_INDEX.md`
# `/workspace/kalshi_15m_lab/LIVING_SPINE_INDEX.md`
# `/workspace/kalshi_15m_lab/SOURCE/` PDFs

Hard NOs for settle join:

- DIY CFB average as official settle without match-to-Kalshi result
- Demo fills as settles
- Invent win/lose
- Golf artifact mix
- Trading ARMED

If Kalshi `result` is not yet available, settle join leaves `SETTLE_PENDING` / `never_settled`.

Desktop finish notify reuses golf `publish_ntfy` / `notify_run_complete` (same `.env` `NTFY_TOPIC`). Operator-triggered ingest/live/loop from the Phase 1 Desktop hub (`Open-Phase1-Hub.bat` → `python -m golf_offshoot shell`) pings once on run finish for `lane=learning_lane_15m` too. Live and loop still run paper autobet + settle join. 15m watch state stays under the 15m paper root. Not a new trading UI.

## Ticker / window parse

- Event ticker: `KXBTC15M-YYMONDDHHMM` (example `KXBTC15M-26SEP071400`).
- Market ticker may append a minute suffix: `KXBTC15M-26SEP071415-15`. Trailing `-15` is **not** a series id.
- Do **not** substring-match `BTC`. Do **not** use threshold series `KXBTC`.
- No multi-series. No Pyth metals.
- Window bounds are market `open_time` / `close_time` (UTC journal). EDT titles are display-only.
- `can_close_early=true` is observed. If `close_time` moves, the window re-keys. Stay `SETTLE_PENDING` until Kalshi `result`.
- CF index id is pinned `BRTI`. Any CFB websocket average is observe-only.

## Shareable observability

Hub UI SoT is PR #151: `docs/observability-hub/data/manifest.json` + [SCHEMA.md](https://github.com/swellbear/gated-formalization/blob/master/docs/observability-hub/data/SCHEMA.md). Local paper autobet / settle stay on the operator shell. See [SHAREABLE_OBSERVABILITY_EXPORT.md](SHAREABLE_OBSERVABILITY_EXPORT.md).

## Hub

Operator surface owns a single selector field: `lane=golf|learning_lane_15m` (exact). No short `15m` alias. Default is `golf`. Unknown → golf. Switching reloads that lane’s artifacts only.

## Week-1 leftovers (PROPOSED — not Softened)

1. Digestor SOURCE honesty digest (hook only in this PR).
2. 15-min hub viz wall (currently `not yet available`).
3. Dated weekly honesty rollup for this lane.
4. Expansion past `KXBTC15M`.
5. CFB websocket observe/debug feed (never official settle).

## Expansion shortlist (PROPOSED — not Softened; do not implement here)

- Other CRYPTO15M cadences / tickers (e.g. ETH 15-min) after the KXBTC15M loop is honest.
- Fee-accurate paper vs mid (quadratic × 1 is recorded, not claimed as a live ticket).
- Shared weekly honesty page that still keeps golf and 15m journals separate.
- Pyth metals and any series other than `KXBTC15M`.

This PR implements **`KXBTC15M` only**. Researcher hire is deferred — no researcher docs.

## Commands

```bash
python -m golf_offshoot hub                              # default Golf Phase 1
python -m golf_offshoot hub --lane learning_lane_15m
python -m golf_offshoot lane-15m                         # ingest → live → paper autobet → settle join
python -m golf_offshoot observability-export             # read-only shareable snapshot
```
