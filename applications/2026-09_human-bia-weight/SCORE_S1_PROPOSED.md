# S1 / S2 / S3 score — cheap sklearn holdout on NHANES Cycle C (PROPOSED; Operator-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_human-bia-weight`  
**String:** method-practice sklearn holdout — BIA→weight vs mean / height / anthro baselines  
**Check:** **S1** (50 kHz Ridge) · **S2** (multi-freq 5/50/100) · **S3** (not run) on **NHANES Cycle C (2003–2004)**  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master.

**What this is not:** Commercial continuous weighing is **not** solved. This is **not** livestock transfer. This is **not** skill-met for farm weighing. This is **not** rithm. Residual ~11 kg RMSE is **not** a product claim. DUA use is **statistical analysis only**; **no re-identification**.

---

## 0. Plain-language framing

**What this is:** After Step-1 SUCCEED (#55), Lab ran a cheap sklearn holdout on NHANES Cycle C. Operator gated **S1 HARDEN**, **S2 Soften/park**, and **S3 HOLD/park**.

**What this settles:** On this Cycle C holdout, Ridge on **R50 + Xc50 + height + sex + age** beats **height + sex + age** alone. BIA features add weight signal beyond anthro. That is an **Amb HARDEN** of the method-practice bite. It is **not** commercial weighing solved.

**What this is not:** Not a trained product map. Not farm / livestock transfer. Not rithm. Not skill-met for farm weighing. Multi-freq (**S2**) is **not** required for this Amb on C. **S3** was **not** needed. Animal parks stay.

---

## 1. Board (Cycle C)

| Field | Gated record |
|-------|----------------|
| Corpus | NHANES Cycle **C** (2003–2004) BIX↔BMX |
| Split | SEQN **80/20**; `random_state=0` |
| n eligible | **4276** (train **3420** / test **856**) |
| vs Step-1 proven join | Hunt recorded `BIX_C ∩ BMX_C` n=**4278** (BIXS050K+BIXC050K+BMXWT). S1 eligible **4276** — two-row drop vs that join (extra eligibility, e.g. height/sex/age). Do **not** collapse the two n’s. |
| Framing | Statistical analysis under the [NCHS DUA](https://www.cdc.gov/nchs/policy/data-user-agreement.html). **No re-identification.** **Not CC-BY.** |

This fold does **not** re-download, re-join, or re-fit. Numbers are the gated Lab summary.

---

## 2. Lab score — S1 (50 kHz)

**S1-B** = Ridge on **R50 + Xc50 + height + sex + age**  
**B1+** = height + sex + age alone  
**S1-A** = the S1 BIA-side check gated as **S1-A < B0**  
**B0** / **B1** = mean and height-only baselines from the #55 invent board

| Model | Test RMSE (kg) |
|-------|----------------|
| **B0** | 21.997 |
| **B1** | 15.683 |
| **B1+** | 14.655 |
| **S1-A** | 14.057 |
| **S1-B** | 11.271 |

**Ratio** S1-B / B1+ = **0.769** ≤ provisional **0.90** bar.  
**S1-A < B0** (14.057 < 21.997).

Admitted claim (scoped to this holdout): Ridge on R50+Xc50 + height+sex+age beats height+sex+age alone — **BIA features add weight signal beyond anthro**.

**Ship-A (S1-B) ADMITTED** under method-practice: local predict package at [`ship/`](ship/README.md) (`s1b_pipeline.joblib` + `predict.py`). Dry-run example → **75.2460** kg (synthetic). Machine record: [`ship/meta.json`](ship/meta.json). String **CLOSE**: the product-accuracy claim is **KILL** (~11 kg / ~25 lb RMSE) — [`DIGESTION_STRING_CLOSE.md`](DIGESTION_STRING_CLOSE.md).

---

## 3. Lab score — S2 (multi-freq 5 / 50 / 100)

| Check | Test RMSE (kg) |
|-------|----------------|
| **S1-B** (50 kHz + anthro) | 11.271 |
| **S2-B** (5/50/100 + anthro) | 10.963 |

**Ratio** S2-B / S1-B = **0.973**.  
**MAE drop** 0.23 kg **< 0.5** kg.  
Provisional tag: **MISS**.

Multi-freq is **not** required for this Amb on Cycle C.

---

## 4. S3

**HOLD / park.** Not run. Not needed given **S1** clear.

---

## 5. Operator gate (authoritative)

**S1 — ADMIT HARDEN.**

On this Cycle C holdout, S1-B / B1+ = 0.769 ≤ 0.90 and S1-A < B0. Claim admitted: Ridge on R50+Xc50 + height+sex+age beats height+sex+age alone — BIA features add weight signal beyond anthro.

**S2 — Soften / park.**

S2-B 10.963 vs S1-B 11.271 (ratio 0.973); MAE drop 0.23 kg < 0.5 — provisional tag **MISS**. Multi-freq **not** required for this Amb on C.

**S3 — HOLD / park.**

Not run. Not needed given S1 clear.

Honesty, required on the record:

- **Method-practice holdout only.**
- Residual **~11 kg RMSE ≠ commercial continuous weighing solved**.
- **No livestock transfer.** Animal parks stay (#47 / #49 / #51 / #53).
- **DUA:** statistical analysis / **no re-identification**.
- **Not** skill-met for farm weighing / rithm product.

---

## 6. Amb remainder (named)

| Piece | Status | Remainder |
|-------|--------|-----------|
| S1 — BIA beyond anthro on Cycle C holdout | **hardened** | Scoped: this SEQN 80/20, `random_state=0`, Cycle C. Residual test RMSE **11.271 kg**. Does **not** clear commercial continuous weighing. Does **not** transfer to livestock. |
| S2 — multi-freq 5/50/100 required? | **paused** (MISS / Soften) | Ratio 0.973; MAE drop 0.23 kg < 0.5. Not required for this Amb on C. |
| S3 | **paused** (HOLD; not run) | Not needed given S1 clear. |
| Commercial / farm continuous weighing | **not this bite** | ~11 kg residual RMSE is honesty, not a product win. |
| Livestock BIA→weight | **parked** (other apps) | No transfer. |

---

## 7. Unchanged strings

- Poultry BIA→weight step-1 remains **parked** (#47 DATA-BLOCKED).
- Cattle BIA→weight step-1 remains **parked** (#49 DATA-BLOCKED).
- Sheep BIA→weight step-1 remains **parked** (#51 DATA-BLOCKED).
- Companion BIA→weight remains **parked** (#53 Soften n=13 + training-scale DATA-BLOCKED).
- Farm livestock continuous-weighing remains a **separate** Amb.
- Collatz playground remains **done** (#45). Lab HOLD there.
- Track B invent remains **paused**.
- llm-gwt R-REPL remains **parked**.

---

*Docs only. S1 HARDEN ≠ commercial weighing. S2 MISS ≠ multi-freq required. S3 not run. Residual ~11 kg RMSE is leftover honesty. No livestock transfer. DUA / no re-id. Not rithm. Lab does not self-admit.*
