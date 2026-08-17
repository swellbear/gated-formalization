# Package-Satisfying Evidence Intake — gap horses pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 + L-SESS + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-GAP**  
**Target dependent(s):** F-DAY (selection); F-ON / F-CC locked to 0; F-SKILL parent remains F-CC  
**Named-class pulse?** **Yes** (operator `ok proceed with your suggested route` — **H-GAP-FADE + H-GAP-CONT**)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | F-DAY gap horses; pick-one on discovery F-DAY last 500 of prefix ≤ 2023-08-21 only if strictly beats 0; F-ON/F-CC = 0; promote = F-CC not F-DAY |
| Named source class | **H-GAP-FADE** / **H-GAP-CONT** on Yahoo `CL=F` (`Lock_Horses_Gap.md`) |
| Named enough? | **Yes** (trigger, scale, emit, cutoff written before last-500 confirm) |
| Non-circular? | Yes — overnight-gap fade/continuation is not the Rank 4 brochure and not L-HUNT-PRETELL |
| Schema match | **Partial** — F-DAY scored on stand-in; parent F-SKILL is F-CC (locked to 0 here) |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No** (not F-SKILL/F-CC; not F-DAY P-NonNegligible) |

Do **not** collapse F-CC to a small F-DAY dip. Do **not** promote on F-DAY. Do **not** send CONT to confirm after FADE was picked.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | NYMEX CL front-month log-return | Yahoo `CL=F` stand-in |
| Horizon | F-DAY (this pulse); F-ON/F-CC reported as 0 | Yes |
| Metric | RMSE vs 0 | Discovery FADE tiny beat; CONT loss; confirm FADE small F-DAY beats |
| Protocol | Discovery/confirm; expanding walk-forward | Yes |
| Baseline | No-change | Discovery last 500 of prefix; confirm last 250/500/750 |
| Promote | F-CC < 0 on 500 and ≤ 0 on 250 and 750 | **Does not fire** (F-CC tied with 0) |

**Schema match?** **Partial.**

---

## 2. Artifact summary

**Source / citation:** `PULSE_Horses_Gap.md` · `data/gap_horse_scores.json` · operator 2026-08-17.

**What it reports:** Survivor **H-GAP-FADE**. Discovery F-DAY 0.02584386 vs 0 0.02584659. Confirm last-500 F-DAY 0.026584 vs 0 0.026634. F-CC equals 0. Promote `fires` false.

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — vendor generic (Yahoo), not exchange official
  - [x] Other: stand-in badge required

**If conflicted:** Labeled stand-in numbers only. Must **not** solely affirm P-NonNegligible skill as if live CME.

### Quantitative bar?
Yes. Rubric: `E_Quantitative_Evidence_Rubric_Gap.md`. Result: **not establish**.

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** H-GAP-FADE / H-GAP-CONT as named horses; L-HUNT-GAP / L-PULSE-GAP-1 as evaluation  
- [ ] Aim **ADMIT** F-SKILL / F-DAY / F-CC established — **rejected**  
- [x] Aim **REJECT** reading a small F-DAY dip as F-SKILL-met or as a promote  

---

## 4. Scoped-result honesty

Stand-in ≠ live. Tiny ≠ met. F-DAY-met ≠ F-CC-met. Day win ≠ promote. Two rows ≠ a zoo. Combo still unnamed.

---

*Standing rule: Package-Satisfying Evidence Intake.*
