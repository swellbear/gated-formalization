# Compare method (A vs B)

Parallel paper machines. **Never auto-trades. Never real money.** $20,000 **per field per path**. Do not write one shared ledger across fields.

Hashed constitution: `method_law_v1` in `options_offshoot.compare.law`. Printed on every pack.

| Path | Estimate | Ticket bar |
|------|----------|------------|
| lived | current pipeline | mid **and** ask |
| A-replay | current (schema default σ if realized vol missing) | mid only |
| B-guts | honest (missing vol stays missing) | mid only |
| B-nerves | current | ask |
| B-full | honest | ask |

`--compare-method` does **not** `--lock-paper` lived and does **not** write the lived ledger. Independent A/B books only.

Honest: no earnings narrative, no IV from blogs, no missing greeks as 0, no invented bid from last, no default σ. B-guts is GPF-*like*, not GPF.

Settle at expiry. Marks during the week are not the result. Scores: `posted_ask_pnl`, `expiry_settle_pnl`.

The **fights** page is who each path holds and why they disagree (honest vs current, mid vs **venue** ask).

The **fields** index is a map from last snapshots: field id, n, n_ask, n_clear. Sorted by field id, never by n_clear. **No** “allocate 20k here.”

```bash
python -m options_offshoot live --field spx_this_friday --compare-method
python -m options_offshoot fields
```

Batch pack `00_full_readout.pdf`: trigger, how-to-read, fights, table, why-bets, leftover, books, bankroll, law hash. Open in Edge/Chrome/Adobe.

Leftover callout is required on ingest/live. No hunter.
