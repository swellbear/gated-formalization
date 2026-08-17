# Package-Satisfying Evidence Intake — pretell hunt pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 + L-SESS + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-PRETELL + L-STANDIN-Y-TELLS**  
**Target dependent(s):** F-SKILL / F-ON / F-DAY / F-CC  
**Named-class pulse?** **Yes** (operator **C** `proceed with C` — named finite discovery/confirm hunt)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | F-CC = Rank 4 F-SKILL; pick-one on discovery F-CC last 500 of prefix ≤ 2023-08-21 only if strictly beats 0; confirm one survivor (or none); promote = F-CC beat on 500 and not-lose on 250/750 |
| Named source class | **L-HUNT-PRETELL** eight horses on Yahoo `CL=F` + **L-STANDIN-Y-TELLS** (`Lock_Hunt_Pretell.md`) |
| Named enough? | **Yes** (drawer, lag, cutoff, pick-one written before last-500 confirm) |
| Non-circular? | Yes — lagged other-series OLS is not the Rank 4 brochure |
| Schema match | **Partial** — scored on stand-in; stamps not official CME |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** |

Do **not** collapse F-CC to a discovery F-DAY dip. Do **not** send a discovery loser to confirm. Do **not** expand the drawer after scores.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | NYMEX CL front-month next-session log-return | Yahoo `CL=F` stand-in + six Yahoo tells |
| Horizon | F-ON / F-DAY / F-CC | All eight scored on discovery; selection = F-CC only |
| Metric | RMSE vs 0 | Discovery F-CC: **all eight lose** |
| Protocol | Discovery/confirm; expanding walk-forward | Yes; confirm **skipped** |
| Baseline | No-change | Discovery last 500 of prefix |
| Promote | F-CC < 0 on 500 and ≤ 0 on 250 and 750 | **Does not fire** (no survivor) |

**Schema match?** **Partial.**

---

## 2. Artifact summary

**Source / citation:** `PULSE_Hunt_Pretell.md` · `data/pretell_hunt_scores.json` · operator **C** 2026-08-17.

**What it reports:** None of eight horses beat 0 on discovery F-CC (0 = 0.026705; closest loss H-TELL-SPX 0.026765). Survivor **none**. Confirm **null**. Promote `fires` false.

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — vendor generics (Yahoo), not exchange official
  - [x] Other: stand-in badge required

**If conflicted:** Labeled stand-in numbers only. Must **not** solely affirm P-NonNegligible skill as if live CME.

### Quantitative bar?
Yes. Rubric: `E_Quantitative_Evidence_Rubric_Pretell.md`. Result: **not establish**.

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** L-HUNT-PRETELL / L-STANDIN-Y-TELLS as protocol + named drawer; L-PULSE-PRETELL-1 as evaluation  
- [ ] Aim **ADMIT** F-SKILL established — **rejected**  
- [x] Aim **REJECT** picking a discovery F-CC loser, or treating a tiny F-DAY dip as a survivor  

---

## 4. Scoped-result honesty

Stand-in ≠ live. No survivor ≠ least-bad. F-DAY-met ≠ F-CC-met. Eight rows ≠ an unbounded kitchen sink. Do not re-hunt confirm.

---

*Standing rule: Package-Satisfying Evidence Intake.*
