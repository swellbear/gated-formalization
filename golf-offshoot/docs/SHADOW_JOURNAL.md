# Shadow journal

Paper-observation log of strategy advises. **Never auto-bet.** This is not a ticket writer and not a bankroll.

## What is logged

When the strategy layer emits `new_bet`, `add`, `reduce`, `exit`, or `reallocate` on the **operating** path (`FieldSnapshot.operating=True` and `persist=True`):

| Field | Meaning |
|-------|---------|
| timestamp | Recommendation `as_of` |
| tournament / tournament_id | Event |
| player / player_id | ESPN-matched name |
| market | `win` / `top_10` / `top_5` / `make_cut` / `top_20` |
| posted_decimal | Book decimal at ingest, if a real coupon existed |
| model_probability + range | Central / low / high for that horizon |
| suggested_stake | Advisory stake delta (not placed) |
| mode | `stay_selective` / `press_edges` / `protect_profits` |
| run_mode | `pre_tournament` / `live` |
| reason | Strategy explanation |
| odds_as_of | Coupon `as_of` timestamp |
| never_auto_bet | Always true |
| settle_status | Optional join: `paper_win` / `paper_lose` / `never_settled`. Absent = SETTLE_PENDING |
| settled_at | Optional. Present only when a real paper/ledger settle timestamp exists |
| settle_source | Optional. Where the join came from (`paper_ledger_ticket`, `espn_official_final`, `paper_book_official_winner`, or a loud `never_settled` reason) |

`hold` and `no_action` are not logged. New advises are written **without** invented settles.

## Storage

JSONL at `golf-offshoot/data/shadow/advises.jsonl` (gitignored). Each line is one advise.

Demo / mock runs do **not** write here.

## Review later

```bash
python -m golf_offshoot shadow
```

Opening quotes (`line_role=opening`) are never used as the posted price for a logged advise. The journal still records `top_5` / `top_10` / `top_20` / `make_cut` when those real coupons exist. If the book has not listed those markets, they stay unavailable and are not synthesized from winner odds.

## Settle join (honesty / operator shell)

The Phase 1 honesty adapter **joins** existing journals (including an external artifact root with `shadow/advises.jsonl`) onto real operating evidence. It does not invent win/lose and does not rewrite history on read.

**Join rule** for one advise `(tournament_id, player_id, market)` that does not already have a valid `settle_status`:

1. Lived paper ledger ticket on that event (`paper/ledger.json`) matching player + market → `paper_win` / `paper_lose`, source `paper_ledger_ticket`.
2. Official ESPN-shaped inspect (`completed` and exactly one official winner): same `ticket_hit` rule as `paper-settle`. Round-leader markets and unknown finishes → `never_settled`. Unofficial / playoff / inspect failure → leave unset (`SETTLE_PENDING`). Source `espn_official_final`. Cached inspects may live at `{artifact_root}/settlements/{event_id}.json`.
3. Settled lived paper book (`settled_at` set + `settlement_winner`) for `market=win` only → `paper_win` / `paper_lose` by exact winner name, source `paper_book_official_winner`. Place markets are not guessed from a winner name.

Kalshi demo fills and MOCK/DEMO blobs are not sources.

`SETTLE_PENDING` on the operator surface **clears only when every relevant advise** (`win` / `top_5` / `top_10` / `top_20` / `make_cut`) is `paper_win` or `paper_lose`. `never_settled` and missing `settle_status` keep the weekly operating claim blocked.

Backfill (`python -m golf_offshoot shadow --backfill-settles`) writes `paper_win` / `paper_lose` only when that join already knows a real settle. It does not write invented outcomes or Kalshi/demo fills. `--join-settles` adds live official ESPN inspect for events still unset.
