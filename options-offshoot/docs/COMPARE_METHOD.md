# Compare method (A vs B)

Parallel paper machines. **Never auto-trades. Never real money.** $20,000 **per field per path**. Do not write one shared ledger across fields.

Hashed constitution: `method_law_v1` in `options_offshoot.compare.law`.

| Path | Estimate | Ticket bar |
|------|----------|------------|
| lived | current pipeline | mid **and** ask |
| A-replay | current (schema default σ if realized vol missing) | mid only |
| B-guts | honest (missing vol stays missing) | mid only |
| B-nerves | current | ask |
| B-full | honest | ask |

Honest: no earnings narrative, no IV from blogs, no missing greeks as 0, no invented bid from last. B-guts is GPF-*like*, not GPF.

Settle at expiry. Marks during the week are not the result.

The **fights** page is who each path holds and why they disagree (honest vs current, mid vs ask).

The **fields** index is a map: field id, n contracts, n with a real ask, n that clear the bar. **No** “allocate 20k here.”

```bash
python -m options_offshoot live --field spx_this_friday --compare-method
python -m options_offshoot fields
```

Leftover callout is required on ingest/live. No hunter in v1.
