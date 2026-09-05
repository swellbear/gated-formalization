# Named-gap ledger — human BIA → weight

Habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). One line per open gap. This is a problem-solving scoreboard, **not** a commercial weighing claim, **not** livestock transfer, and **not** rithm.

**Opened:** 2026-09-05 — Founder opens the **human BIA → weight** step-1 data hunt as **method practice** after poultry #47, cattle #49, sheep #51 **DATA-BLOCKED** and companion #53 **Soften** (tiny n) + training-scale **DATA-BLOCKED**. Lab invents ranked hunt probes. Operator gates.

**Last check:** 2026-09-05 — Operator **ADMIT Ship-A (S1-B)** method-practice predict package under [`ship/`](ship/) after S1 HARDEN (#56). Dry-run example → **75.2460** kg (synthetic). S2 Soften/park (MISS). S3 HOLD/park (not run). Score: [`SCORE_S1_PROPOSED.md`](SCORE_S1_PROPOSED.md). Digestion: [`DIGESTION_S1_HOLDOUT.md`](DIGESTION_S1_HOLDOUT.md).

**What this is not:** This is **not** rithm. Livestock transfer is **not** claimed. Farm livestock continuous-weighing is a **separate** Amb. Farm / commercial weighing is **not** solved. Residual ~11 kg RMSE is **not** a product win. **Not clinical.** Step-1 SUCCEED is **not** a trained commercial map. S1 HARDEN / Ship-A is **method-practice only**. DUA: statistical analysis / **no re-id**. Example is synthetic. Do **not** invent rows. Do **not** write skill-met / elevated language for farm weighing.

**Process:** Lab invented hunt probes, then a cheap sklearn holdout. Operator admits, rejects, or parks. Lab does **not** self-admit. After this fold Lab is **HOLD** on this bite unless a Founder opens a new named gap.

**Poultry BIA→weight** step-1 remains **parked** (#47 DATA-BLOCKED). This app does **not** reopen it.  
**Cattle BIA→weight** step-1 remains **parked** (#49 DATA-BLOCKED). This app does **not** reopen it.  
**Sheep BIA→weight** step-1 remains **parked** (#51 DATA-BLOCKED). This app does **not** reopen it.  
**Companion BIA→weight** remains **parked** (#53 Soften n=13 + training-scale DATA-BLOCKED). This app does **not** reopen it.  
**Farm livestock continuous-weighing** remains a **separate** Amb. This app does **not** open or clear it.  
**Collatz playground** is **done** (#45). Lab HOLD there (unchanged).  
**Track B invent** remains **paused** (unchanged).  
**llm-gwt R-REPL** remains **parked** (unchanged).

## Lines

`public row-level human BIA + weight under reusable public terms` → kill vs succeed: citable URL/DOI + schema + license + usable n → **SUCCEED** (NHANES 1999–2004 BIX↔BMX; SEQN; BIXS\*/BIXC\* + BMXWT; proven BIX_C∩BMX_C n=4278; stacked ~13221; NCHS DUA — statistical analysis only; no re-identification; **not CC-BY**; Operator: no explicit ML train/eval ban → Succeed, not Soften) → last check: 2026-09-05 Operator + Founder **ADMIT SUCCEED** (#55); Soften secondaries logged, not substitutes ([`PROPOSED_HUNT.md`](PROPOSED_HUNT.md)) → status: **killed** / **SUCCEED**

`cheap sklearn holdout of human BIA→weight vs mean and height-only / anthro baselines on NHANES Cycle C (DUA / statistical-analysis framing)` → kill vs harden: holdout fails baselines vs Ridge R50+Xc50+height+sex+age beats height+sex+age alone under the 0.90 ratio bar → last check: 2026-09-05 Cycle C n eligible **4276** (train 3420 / test 856; SEQN 80/20; `random_state=0`); test RMSE kg B0 21.997 / B1 15.683 / B1+ 14.655 / S1-A 14.057 / S1-B 11.271; S1-B/B1+ = **0.769** ≤ 0.90; S1-A < B0 → status: **hardened** (method-practice Amb bite; BIA beyond anthro on this holdout; residual ~11 kg RMSE leftover honesty — **not** commercial weighing)

`method-practice S1-B predict package (Ship-A)` → kill vs land: dry-run example prints **75.2460** kg from the admitted S1-B pipeline vs a broken or over-claimed ship → last check: 2026-09-05 Operator **ADMIT Ship-A** under [`ship/`](ship/) (`StandardScaler`+`RidgeCV`; n_train 3420 / n_test 856; alpha 3.1622776601683795; holdout RMSE 11.271495752140735 / MAE 8.783979696023593 / R² 0.7363714213498394; fit_note train-split only matching HARDEN; example synthetic) → status: **hardened** / **ADMITTED** (method-practice ship only; ~11 kg RMSE ≠ commercial; not clinical; no livestock transfer; DUA statistical / no re-id)

`S2 multi-freq 5/50/100 required for this Amb on Cycle C` → kill vs harden: a cheap multi-freq lift that would clear the provisional bar vs only a thin miss → last check: S2-B RMSE 10.963 vs S1-B 11.271 (ratio **0.973**); MAE drop **0.23 kg < 0.5** — provisional tag **MISS** → status: **paused** (Soften / park; multi-freq not required for this Amb on C)

`S3 further holdout invent on Cycle C` → kill vs harden: a needed extra check vs ceremony after S1 already clear → last check: **not run** — Operator **HOLD/park**; not needed given S1 clear → status: **paused**
