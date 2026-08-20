# Package-Satisfying Evidence Intake — EIA spot 21-day trend hunt pulse

**Date:** 2026-08-20  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 (F-SKILL parked this pulse) + L-HUNT-SPOT-TREND + L-STANDIN-EIA-SPOT + L-SPOT-ARMS + L-SPOT-QUEUE**  
**Target dependent(s):** **R-SPOT-TREND** (spot 21-day sign vs continuation). Not F-CC.  
**Named-class pulse?** **Yes** (operator: build Track B)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | Pick-one on discovery hit-rate last 500 of prefix ≤ 2023-08-21 only if **strictly** beats continuation; confirm one survivor per scoreboard (or none); confirm never trains; WTI-met ≠ Brent-met |
| Named source class | **L-HUNT-SPOT-TREND** two horses on EIA Cushing WTI + Europe Brent spots (`Lock_Hunt_Spot_Trend.md`); vehicle **L-STANDIN-EIA-SPOT** (FRED EIA reprint this pulse) |
| Named enough? | **Yes** (object, 21-day label, flip, baseline, two-horse cap, three arms, queue written before last-500 confirm) |
| Non-circular? | Yes — cash 21-day sign is not the Rank 4 next-session CL RMSE brochure |
| Schema match | **Partial** — FRED reprint of EIA daily spots, not EIA Open Data v2; not futures |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** |

Do **not** send a discovery loser to confirm. Do **not** change 21 after scores. Do **not** use confirm as train.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | EIA spot WTI + Brent; two scoreboards | FRED DCOILWTICO / DCOILBRENTEU |
| Horizon | Next 21 price-day sign | Yes |
| Metric | Hit-rate vs continuation | Discovery: **both horses lose** on both boards |
| Protocol | Discovery/confirm; three arms | Confirm **skipped**; train N/A |
| Baseline | Continuation (not a horse) | WTI 0.508 / Brent 0.506 on discovery 500 |
| F-SKILL promote | Does not apply | **Does not fire** |

**Schema match?** **Partial.**

---

## 2. Artifact summary

**Source / citation:** `PULSE_Hunt_Spot_Trend.md` · `data/spot_trend_hunt_scores.json` · FRED EIA reprints 2026-08-20.

**What it reports:** Vehicle OK. WTI discovery: continuation 0.508; FLIP-HOLD 0.494; REV 0.492. Brent: continuation 0.506; FLIP-HOLD 0.496; REV 0.494. Survivor **none** both boards. Confirm **null**.

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — third-party FRED reprint of EIA daily spots, not a live cash desk
  - [x] Other: stand-in badge required

**If conflicted:** Labeled stand-in numbers only. Must **not** solely affirm P-NonNegligible skill as if a live trading tape.

### Quantitative bar?
Yes. Rubric: `E_Quantitative_Evidence_Rubric_Spot_Trend.md`. Result: **not establish**.

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** L-HUNT-SPOT-TREND / L-STANDIN-EIA-SPOT / L-SPOT-ARMS / L-SPOT-QUEUE as protocol; L-PULSE-SPOT-1 as evaluation  
- [ ] Aim **ADMIT** spot-trend skill or F-SKILL established — **rejected**  
- [x] Aim **REJECT** picking a discovery loser, changing 21 after scores, or using confirm as train  

---

## 4. Scoped-result honesty

Spot ≠ futures. No survivor ≠ least-bad. Two rows ≠ an unbounded trend kitchen sink. Do not re-hunt confirm. Do not claim this shows oil “has no trend.” Descriptive Up as of 2026-08-18 is not a pass.

---

*Standing rule: Package-Satisfying Evidence Intake.*
