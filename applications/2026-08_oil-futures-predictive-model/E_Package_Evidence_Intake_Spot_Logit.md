# Package-Satisfying Evidence Intake — EIA spot expanding-window logistic pulse

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 (F-SKILL parked) + L-HUNT-SPOT-TREND + L-HUNT-SPOT-LOGIT + L-SPOT-QUEUE**  
**Target dependent(s):** **R-SPOT-TREND** (same 21-day object). Not F-CC.  
**Named-class pulse?** **Yes** (operator **B**: C-SPOT-LOGIT)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | Pick-one on discovery hit-rate last 500 of prefix ≤ 2023-08-21 only if **strictly** beats continuation; confirm never trains; expanding past-only logistic; do not unburn; do not change 21 |
| Named source class | **L-HUNT-SPOT-LOGIT** two horses on existing EIA spot tapes (`Lock_Hunt_Spot_Logit.md`) |
| Named enough? | **Yes** (features, train clock, min-train, two-horse cap written before confirm) |
| Non-circular? | Yes — past-only fit is not the Rank 4 CL RMSE brochure and not a 21 retune |
| Schema match | **Partial** — FRED reprints; last-750 overlaps discovery prefix by inherited rule |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** |

Do **not** retune after confirm losses. Do **not** unburn.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | Same 21-day spot sign | Inherited spots |
| Train | Expanding past-only; outcome_date < t | Yes |
| Metric | Hit-rate vs continuation | Discovery beat; confirm lose both boards |
| Protocol | Discovery/confirm; three arms | Confirm ran; losses |
| Burned rows | Stay burned | Prior horses not scored |

**Schema match?** **Partial.**

---

## 2. Artifact summary

**Source / citation:** `PULSE_Hunt_Spot_Logit.md` · `data/spot_logit_hunt_scores.json`.

**What it reports:** WTI discovery FULL/SIGN 0.532 vs 0.508; Brent 0.550 vs 0.506; survivor FULL both. Confirm WTI 0.430/0.476/0.463 vs cont 0.552/0.572/0.557. Confirm Brent 0.442/0.496/0.465 vs cont 0.522/0.524/0.525. All confirm **lose**.

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — FRED EIA reprints, not a live desk
  - [x] Other: stand-in badge required

**If conflicted:** Labeled stand-in numbers only. Must **not** solely affirm P-NonNegligible skill.

### Quantitative bar?
Yes. Rubric: `E_Quantitative_Evidence_Rubric_Spot_Logit.md`. Result: **not establish**.

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** L-HUNT-SPOT-LOGIT as protocol; L-PULSE-SPOT-LOGIT-1 as evaluation  
- [ ] Aim **ADMIT** spot-trend skill or F-SKILL established — **rejected**  
- [x] Aim **REJECT** confirm-as-train, unburning, changing 21, or discovery-alone clearance  

---

## 4. Scoped-result honesty

Discovery survivors that lose confirm are **not** skill-met. Queue empty ≠ clearance. Do not retune.

---

*Standing rule: Package-Satisfying Evidence Intake.*
