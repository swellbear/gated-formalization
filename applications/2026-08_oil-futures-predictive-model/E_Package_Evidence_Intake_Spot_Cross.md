# Package-Satisfying Evidence Intake — EIA spot WTI↔Brent cross-bench overlay pulse

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 (F-SKILL parked) + L-HUNT-SPOT-TREND + L-HUNT-SPOT-CROSS + L-SPOT-QUEUE**  
**Target dependent(s):** **R-SPOT-TREND** (same 21-day object). Not F-CC.  
**Named-class pulse?** **Yes** (operator **B**: C-SPOT-CROSS)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | Pick-one per board on discovery hit-rate last 500 of prefix ≤ 2023-08-21 only if **strictly** beats continuation; confirm never trains; tiny ≠ met; do not unburn FLIP-HOLD/REV/INV; do not change 21 |
| Named source class | **L-HUNT-SPOT-CROSS** two board-specific horses on existing EIA spot tapes (`Lock_Hunt_Spot_Cross.md`) |
| Named enough? | **Yes** (peer clock, board-specific cap, two-horse split written before confirm) |
| Non-circular? | Yes — the other oil’s 21-day sign is not the Rank 4 CL RMSE brochure and not a 21 retune |
| Schema match | **Partial** — FRED reprints; same-day peer print allowed; last-750 overlaps discovery prefix by inherited rule |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** |

Do **not** send the WTI discovery loser to confirm. Do **not** unburn. Do **not** add a dollar spread after scores.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | Same 21-day spot sign | Inherited spots; peer sign overlay |
| Overlay | Other oil’s 21-day sign as of date ≤ t | Yes |
| Metric | Hit-rate vs continuation | WTI lose; Brent discovery beat + confirm point-beats |
| Protocol | Discovery/confirm; three arms | WTI confirm skipped; Brent confirm ran |
| Burned rows | Stay burned | FLIP-HOLD/REV/INV not scored |

**Schema match?** **Partial.**

---

## 2. Artifact summary

**Source / citation:** `PULSE_Hunt_Spot_Cross.md` · `data/spot_cross_hunt_scores.json` · operator B.

**What it reports:** WTI: continuation 0.508; B2W 0.494; survivor **none**. Brent: continuation 0.506; W2B 0.528; survivor **H-SPOT-CROSS-W2B**. Confirm Brent last 500 0.544 vs 0.522; last 250 0.528 vs 0.524 (**+1**); last 750 0.545 vs 0.525.

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — FRED EIA reprints, not a live desk
  - [x] Other: stand-in badge required

**If conflicted:** Labeled stand-in numbers only. Must **not** solely affirm P-NonNegligible skill.

### Quantitative bar?
Yes. Rubric: `E_Quantitative_Evidence_Rubric_Spot_Cross.md`. Result: **not establish**.

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** L-HUNT-SPOT-CROSS as protocol; L-PULSE-SPOT-CROSS-1 as evaluation  
- [ ] Aim **ADMIT** spot-trend skill or F-SKILL established — **rejected**  
- [x] Aim **REJECT** picking the WTI loser, unburning, changing 21, using confirm as train, or treating tiny 250 as met  

---

## 4. Scoped-result honesty

Brent confirm point-beats ≠ unrestricted skill-met. Tiny 250 ≠ met. WTI-met ≠ Brent-met. Cross-bench ≠ dollar spread. Last-750 overlaps discovery prefix. Do not retune W2B after confirm.

---

*Standing rule: Package-Satisfying Evidence Intake.*
