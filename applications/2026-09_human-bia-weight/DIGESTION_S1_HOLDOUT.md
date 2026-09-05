# Digestion — human BIA→weight S1 holdout (2026-09-05)

A short plain note after the method-practice holdout. Habit: [`docs/DIGESTION_HABIT.md`](../../docs/DIGESTION_HABIT.md). Incoming Step-1 lesson stays on [`DIGESTION_FROM_COMPANION.md`](DIGESTION_FROM_COMPANION.md). This does **not** score a commercial weighing product. It does **not** reopen the animal parks.

**This string:** cheap sklearn holdout on NHANES Cycle C after Step-1 SUCCEED (#55). Score: [`SCORE_S1_PROPOSED.md`](SCORE_S1_PROPOSED.md). Lab scratch was **not** on this VM; metrics copied from the Operator gate.

---

## What this string tried

See whether, on a cheap Cycle C holdout framed as statistical analysis under the NCHS DUA, BIA features add weight signal beyond a mean baseline and beyond anthro (height / height+sex+age).

Lab invented S1 (50 kHz Ridge), S2 (multi-freq 5/50/100), and held S3. Operator gated. Lab does **not** self-admit.

It was **not** trying to solve commercial continuous weighing, transfer to livestock, or clear a rithm / farm-weighing skill.

---

## What fog moved

On Cycle C (n eligible **4276**; train **3420** / test **856**; SEQN 80/20; `random_state=0`):

| Model | Test RMSE (kg) | Gate role |
|-------|----------------|-----------|
| **B0** | 21.997 | mean baseline |
| **B1** | 15.683 | height-only |
| **B1+** | 14.655 | height+sex+age |
| **S1-A** | 14.057 | S1-A < B0 |
| **S1-B** | 11.271 | Ridge R50+Xc50 + height+sex+age |

**S1-B / B1+ = 0.769 ≤ 0.90.** Operator **ADMIT S1 HARDEN**.

Admitted claim (this holdout only): Ridge on R50+Xc50 + height+sex+age beats height+sex+age alone — **BIA features add weight signal beyond anthro**.

That is a method-practice **Amb bite**. It is **not** commercial weighing solved.

---

## What did not move / what we park

- **S2 multi-freq MISS.** S2-B RMSE **10.963** vs S1-B **11.271** (ratio **0.973**). MAE drop **0.23 kg < 0.5**. Provisional tag **MISS**. Multi-freq is **not** required for this Amb on C. **Soften / park.**
- **S3 not run.** **HOLD / park.** Not needed given S1 clear.
- **Residual ~11 kg RMSE.** S1-B test RMSE **11.271 kg** is leftover honesty. It is **not** a continuous-weighing product. It is **not** farm weighing solved.
- **n:** hunt proven join was **4278**; S1 eligible is **4276**. Do not collapse those two counts.

---

## What we refuse

- Commercial continuous weighing is **not** solved.
- Livestock transfer is **not** claimed. Poultry #47, cattle #49, sheep #51, companion #53 stay **parked**.
- Farm livestock continuous-weighing stays a **separate** Amb.
- This is **not** skill-met for farm weighing. This is **not** rithm.
- DUA: **statistical analysis only**. **No re-identification.** **Not CC-BY.**
- Do **not** invent rows. Do **not** write skill-met / elevated language.

---

## Where invent sits now

**S1 HARDEN is on the record. S2 / S3 parked. Lab HOLD on this bite** unless a Founder opens a new named gap.

Do **not** treat residual ~11 kg RMSE as a green light for a product invent. Do **not** reopen animal parks. Do **not** run S3 for ceremony.

---

## Pointers

| Record | What it is |
|--------|------------|
| [`SCORE_S1_PROPOSED.md`](SCORE_S1_PROPOSED.md) | S1 HARDEN + S2 MISS + S3 HOLD; full RMSE table |
| [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) | Scoreboard lines |
| [`DIGESTION_FROM_COMPANION.md`](DIGESTION_FROM_COMPANION.md) | Incoming animal-park + Step-1 SUCCEED lesson |
| [`PROPOSED_HUNT.md`](PROPOSED_HUNT.md) | Step-1 SUCCEED hunt (#55) |

---

*Docs only. S1 HARDEN ≠ commercial weighing. Residual ~11 kg RMSE is leftover honesty. No livestock transfer. DUA / no re-id. Not rithm. Lab does not self-admit.*
