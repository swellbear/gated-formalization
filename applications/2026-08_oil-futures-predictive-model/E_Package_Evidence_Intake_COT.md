# Package-Satisfying Evidence Intake — CFTC positioning hunt pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 + L-SESS + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-COT + L-STANDIN-CFTC-COT**  
**Target dependent(s):** F-SKILL / F-ON / F-DAY / F-CC  
**Named-class pulse?** **Yes** (operator: implement named CFTC positioning hunt)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | F-CC = Rank 4 F-SKILL; pick-one on discovery F-CC last 500 of prefix ≤ 2023-08-21 only if **strictly** beats 0; confirm one survivor (or none); promote = F-CC beat on 500 and not-lose on 250/750 |
| Named source class | **L-HUNT-COT** two horses on Yahoo `CL=F` + **L-STANDIN-CFTC-COT** (CFTC disagg futures-only 067651; `Lock_Hunt_COT.md`) |
| Named enough? | **Yes** (archive, two features, scale, clock, two-horse cap written before last-500 confirm) |
| Non-circular? | Yes — lagged weekly positioning is not the Rank 4 brochure |
| Schema match | **Partial** — scored on stand-in; stamps not official CME; Friday-of-week release proxy |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** |

Do **not** send a discovery loser to confirm. Do **not** add percent-of-OI or other trader groups after scores.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | NYMEX CL front-month next-session log-return | Yahoo `CL=F` stand-in + CFTC MM net |
| Horizon | F-ON / F-DAY / F-CC | Both horses scored on discovery; selection = F-CC only |
| Metric | RMSE vs 0 | Discovery F-CC: **both lose** (0 = 0.026705) |
| Protocol | Discovery/confirm; expanding walk-forward | Yes; confirm **skipped** |
| Baseline | No-change | Discovery last 500 of prefix |
| Promote | F-CC < 0 on 500 and ≤ 0 on 250 and 750 | **Does not fire** (no survivor) |

**Schema match?** **Partial.**

---

## 2. Artifact summary

**Source / citation:** `PULSE_Hunt_COT.md` · `data/cot_hunt_scores.json` · CFTC disagg futures-only 2026-08-17.

**What it reports:** 711 reports in discovery span (vehicle OK). Both horses lose discovery F-CC (closest H-COT-NET 0.026796 vs 0 0.026705). Survivor **none**. Confirm **null**. Promote `fires` false.

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — vendor generic (Yahoo) + public regulator file (CFTC), not exchange official settlement
  - [x] Other: stand-in badge required

**If conflicted:** Labeled stand-in numbers only. Must **not** solely affirm P-NonNegligible skill as if live CME.

### Quantitative bar?
Yes. Rubric: `E_Quantitative_Evidence_Rubric_COT.md`. Result: **not establish**.

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** L-HUNT-COT / L-STANDIN-CFTC-COT as protocol + named drawer; L-PULSE-COT-1 as evaluation  
- [ ] Aim **ADMIT** F-SKILL established — **rejected**  
- [x] Aim **REJECT** picking a discovery F-CC loser, or adding percent-of-OI / other trader groups after scores  

---

## 4. Scoped-result honesty

Stand-in ≠ live. No survivor ≠ least-bad. Two rows ≠ an unbounded positioning kitchen sink. Do not re-hunt confirm. Do not claim this shows specs do or do not “drive” crude.

---

*Standing rule: Package-Satisfying Evidence Intake.*
