# Human BIA → weight — reading guide

**Application ID:** `2026-09_human-bia-weight`  
**Opened:** 2026-09-05  

**Ship-A ADMITTED** (method-practice S1-B predict package) after **S1 HARDEN** (#56) and Step-1 **SUCCEED** (#55). Named data gap: public row-level human BIA + weight under reusable public terms — NHANES 1999–2004 **BIX↔BMX** (NCHS DUA; **not CC-BY**). Holdout: NHANES Cycle C; n eligible **4276** (3420/856); S1-B RMSE **11.271** kg vs B1+ **14.655** (ratio **0.769**). Dry-run: `python ship/predict.py ship/example_input.csv` → **75.2460** (synthetic).

This is **not** commercial continuous weighing solved (residual ~11 kg RMSE). This is **not** clinical. This is **not** livestock transfer. This is **not** skill-met for farm weighing. This is **not** rithm. DUA: statistical analysis / **no re-id**. Do **not** invent rows. Poultry #47, cattle #49, sheep #51, and companion #53 stay **parked**. S2 multi-freq **MISS** / park. S3 **HOLD** / park.

## Reading order

1. [`STATUS.md`](STATUS.md) — where we are
2. [`ship/README.md`](ship/README.md) — ADMITTED S1-B predict package (Ship-A)
3. [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) — SUCCEED + S1 HARDEN + Ship-A ADMIT + S2/S3 park
4. [`SCORE_S1_PROPOSED.md`](SCORE_S1_PROPOSED.md) — Lab metrics + Operator gate
5. [`DIGESTION_S1_HOLDOUT.md`](DIGESTION_S1_HOLDOUT.md) — what this holdout taught
6. [`PROPOSED_HUNT.md`](PROPOSED_HUNT.md) — Step-1 SUCCEED hunt
7. [`DIGESTION_FROM_COMPANION.md`](DIGESTION_FROM_COMPANION.md) — incoming animal-park lesson
8. [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) — decision log
9. [`notes.md`](notes.md) — one-line pointer
