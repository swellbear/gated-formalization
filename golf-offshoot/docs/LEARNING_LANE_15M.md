# Learning lane: 15-min Kalshi

Resume / leave-off SoT: [docs/AGENT_LEAVE_OFF.md](../../docs/AGENT_LEAVE_OFF.md)

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
- Do **not** widen past `KXBTC15M` in this PR (the adapter is shaped to expand later).
- No geo. No LIVE cash. No invented edge / banked-edge claims.
- 15-min Kalshi is not live trading and not a golf WC1 edge.

## Paths (never mix with golf)

| Lane | Artifact root |
|------|----------------|
| golf | `golf-offshoot/data/` (`paper/`, `shadow/`, `exports/`) |
| `learning_lane_15m` | `/workspace/kalshi_15m_exports/` (repo-local fallback: `golf-offshoot/data/learning_lane_15m/`) |

Paper ledger, shadow advises, and settlements for this lane live under the 15m roots only.

## Public adapter

Read-only Kalshi elections API: `https://api.elections.kalshi.com/trade-api/v2/` (`events`, `markets`, `series/KXBTC15M`). Markets and events fetch `status=open` first, then merge `settled` / `closed` so settle-join still sees official results. Series GET uses `include_volume=true`. `initialized` rows with null marks are not paper-autobet candidates. `latest/journal.json` windows come from paper books and settlement joins, not only the live snapshot.

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

# Digestor owns the SOURCE honesty digest. It exists now — do not invent a second one:
# `golf-offshoot/docs/LEARNING_LANE_15M_SOURCE_DIGEST.md`
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

Desktop finish notify reuses golf `publish_ntfy` / `notify_run_complete` (same `.env` `NTFY_TOPIC`). Operator-triggered ingest/live/loop from the Phase 1 Desktop hub (`Open-Phase1-Hub.bat` → `python -m golf_offshoot shell`) and `lane-15m` ping once on run finish for `lane=learning_lane_15m` too. Live and loop still run paper autobet + settle join. 15m watch state stays under the 15m paper root. Not a new trading UI.

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

Operator surface owns a single selector field: `lane=golf|learning_lane_15m` (canonical Hub UI SoT). No bare `15m` alias. Default is `golf`. Unknown → golf. Journal display label `15m` and CLI command `lane-15m` are not selector values. Switching reloads that lane’s artifacts only.

## Learning wake

PaperWatch repeats researcher + export on its own. That is not learning: nothing wakes the crew when a window settles. The wake closes that half.

Every PaperWatch cycle (and every `learn-15m`) scans `settlements/*.json`, `paper/*.json` + `paper/ledger.json`, `latest/journal.json` and the published `manifest.json`, compares that fingerprint to `latest/learning_wake.json` (gitignored), and records:

| Event | Raised when |
|-------|-------------|
| `new_settle` | a window gained an official Kalshi `result` |
| `new_fill` | a new paper book appeared on this tree |
| `pending_cleared` | a window left the pending list |

Each event carries `roles_owed` in Protocol order — `digest-figures` → `operator` → `systems` → `validator`. Human `digestor` is not named on a routine settle; it is keyed on the standing caveats file. `lab` is added only when the CoS honesty checklist is stamped all-PASS **and** an Operator residual is passed in explicitly; a scan alone never owes Lab. Nothing new on a cycle records a heartbeat instead (`no new settle; watch still running`).

**`roles_owed` is a request, never a completion.** The wake writes no desk thread line, Softens nothing, ADMITs nothing, and invents no win, lose or pnl. An owed role keeps its `owed_since`, so a wake nobody answered ages in plain sight. A role leaves the list only when an agent that really ran calls it:

```bash
python -c "from golf_offshoot.learning_lane_15m.learn import mark_roles_served; mark_roles_served(['digest-figures'], by='digest-figures', note='posted generated figures')"
```

A window can carry an official Kalshi result while its paper book is not on this tree. The scan reports that as a **missing paper join** with no paper pnl — never as a pending window, and never as a paper win or loss.

`observability-export` reads the published `manifest.json` back in as its starting point, so a hand edit to the published wording is overwritten on the next cycle. The export writer therefore restates it from the wake scan on every run (`_apply_wake_wording` in `operator_surface/observability.py`): a residual, headline, note or field that calls a missing-join window pending is re-worded onto the digest §4a sentence, the window drops out of the pending count without ever gaining a pnl, and a window Kalshi genuinely has not spoken on stays `SETTLE_PENDING`. Published lineage-B figures ride through untouched; `paper_ledger` names the lineage its rows describe and `learning_status` names lineage A, so the two books are never reconciled against each other. `settle.counts` prefixes its published rows `Lineage B ·` so the settle-file count beside them cannot read as a denominator.

**Pending is decided at export time, not by the wake file.** The wake is written on the ~90s watch cycle while the export runs on its own clock, so a window that gains its official Kalshi result in between is still cached as pending. `_reconcile_pending` re-reads `settlements/*.json` at export time and publishes one pending list that feeds the count, the headline ticker and `learning_status.pending_windows` alike — a live `settled` status vetoes a cached wake entry, never the other way round, and a window gains no pnl by leaving the list. `_assert_pending_is_not_settled` then refuses the export outright if any window is both pending and settled in the same manifest, or if the pending count disagrees with the pending list.

## Week-1 leftovers (PROPOSED — not Softened)

1. ~~Digestor SOURCE honesty digest (hook only in this PR).~~ **Landed 2026-09-07 18:03 EDT:** [`LEARNING_LANE_15M_SOURCE_DIGEST.md`](LEARNING_LANE_15M_SOURCE_DIGEST.md) — living spine, every claim cited to a file. Conflict flag stays at [`LEARNING_LANE_15M_SOURCE_CONFLICT.md`](LEARNING_LANE_15M_SOURCE_CONFLICT.md).
2. 15-min hub viz wall (currently `not yet available`).
3. Dated weekly honesty rollup for this lane.
4. Expansion past `KXBTC15M`. **Founder HOLD 2026-09-07: not until this loop is honest.**
5. CFB websocket observe/debug feed (never official settle).

## Expansion shortlist (PROPOSED — not Softened; do not implement here)

- Other CRYPTO15M cadences / tickers (e.g. ETH 15-min) after the KXBTC15M loop is honest.
- Fee-accurate paper vs mid (quadratic × 1 is recorded, not claimed as a live ticket).
- Shared weekly honesty page that still keeps golf and 15m journals separate.
- Pyth metals and any series other than `KXBTC15M`.

This PR implements **`KXBTC15M` only**.

## Commands

```bash
python -m golf_offshoot hub                              # default Golf Phase 1
python -m golf_offshoot hub --lane learning_lane_15m
python -m golf_offshoot lane-15m                         # ingest → live → paper autobet → settle join
python -m golf_offshoot lane-15m --watch                 # keep the paper loop repeating; prints the wake each cycle
python -m golf_offshoot learn-15m                        # the learning tick: new events, roles owed, pending, heartbeat
python -m golf_offshoot learn-15m --json                 # same tick as JSON
python -m golf_offshoot observability-export             # read-only shareable snapshot
```
