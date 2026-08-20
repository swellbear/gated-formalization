# Package-Satisfying Evidence Intake — EIA inventory-surprise overlay pulse

**Date:** 2026-08-20  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 (F-SKILL parked) + L-HUNT-SPOT-TREND + L-HUNT-SPOT-INV + L-STANDIN-EIA-INV + L-SPOT-QUEUE**  
**Target dependent(s):** **R-SPOT-TREND** (same 21-day object). Not F-CC.  
**Named-class pulse?** **Yes** (operator **B**: C-SPOT-INV)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | Pick-one on discovery hit-rate last 500 of prefix ≤ 2023-08-21 only if **strictly** beats continuation; confirm never trains; do not unburn FLIP-HOLD/REV; do not change 21 |
| Named source class | **L-HUNT-SPOT-INV** two horses on EIA **WCESTUS1** weekly crude ex-SPR + existing spot tapes (`Lock_Hunt_Spot_Inv.md`) |
| Named enough? | **Yes** (series, naive-surprise formula, clock, two-horse cap written before confirm) |
| Non-circular? | Yes — lagged weekly stocks overlay is not the Rank 4 CL RMSE brochure and not a 21 retune |
| Schema match | **Partial** — EIA HTML leaf, not Open Data v2; naive surprise ≠ Street poll |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** |

Do **not** send a discovery loser to confirm. Do **not** unburn. Do **not** add Cushing-only after scores.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | Same 21-day spot sign | Inherited spots + weekly WCESTUS1 |
| Overlay | Naive surprise (WoW − prior-4 mean) | Yes |
| Metric | Hit-rate vs continuation | Discovery: **both horses lose** both boards |
| Protocol | Discovery/confirm; three arms | Confirm **skipped** |
| Burned rows | Stay burned | FLIP-HOLD/REV not scored |

**Schema match?** **Partial.**

---

## 2. Artifact summary

**Source / citation:** `PULSE_Hunt_Spot_Inv.md` · `data/spot_inv_hunt_scores.json` · EIA leaf 2026-08-20.

**What it reports:** 2290 weeks (vehicle OK). WTI: continuation 0.508; CONT 0.506; FADE 0.494. Brent: continuation 0.506; CONT 0.502; FADE 0.498. Survivor **none**. Confirm **null**.

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — public EIA HTML scrape, not a live desk; naive residual not a survey
  - [x] Other: stand-in badge required

**If conflicted:** Labeled stand-in numbers only. Must **not** solely affirm P-NonNegligible skill.

### Quantitative bar?
Yes. Rubric: `E_Quantitative_Evidence_Rubric_Spot_Inv.md`. Result: **not establish**.

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** L-HUNT-SPOT-INV / L-STANDIN-EIA-INV as protocol; L-PULSE-SPOT-INV-1 as evaluation  
- [ ] Aim **ADMIT** spot-trend skill or F-SKILL established — **rejected**  
- [x] Aim **REJECT** picking a discovery loser, unburning FLIP-HOLD/REV, changing 21, or using confirm as train  

---

## 4. Scoped-result honesty

Naive surprise ≠ Bloomberg. No survivor ≠ least-bad. Closest CONT loss is **not** a pick. Do not re-hunt confirm.

---

*Standing rule: Package-Satisfying Evidence Intake.*
