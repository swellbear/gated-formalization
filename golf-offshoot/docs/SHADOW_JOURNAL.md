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

`hold` and `no_action` are not logged.

## Storage

JSONL at `golf-offshoot/data/shadow/advises.jsonl` (gitignored). Each line is one advise.

Demo / mock runs do **not** write here.

## Review later

```bash
python -m golf_offshoot shadow
```

Opening quotes (`line_role=opening`) are never used as the posted price for a logged advise. The journal still records `top_5` / `top_10` / `top_20` / `make_cut` when those real coupons exist. If the book has not listed those markets, they stay unavailable and are not synthesized from winner odds.
