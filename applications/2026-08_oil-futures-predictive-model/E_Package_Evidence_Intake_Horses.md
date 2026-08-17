# Package-Satisfying Evidence Intake — named horses pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + L-STANDIN-Y-CHAIN + H-LAG-WF + H-KS-FTS**  
**Target dependent(s):** F-SKILL / F-ON / F-DAY / F-CC  
**Named-class pulse?** **Yes** (operator `ok proceed` to name and score both horses)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | F-CC = Rank 4 F-SKILL; F-ON / F-DAY per L-SESS; walk-forward RMSE vs no-change |
| Named source class | **H-LAG-WF** on Yahoo `CL=F`; **H-KS-FTS** on Yahoo month-chain CL1–CL18 (attempted) |
| Named enough? | **Yes** (recipes written before OOS look) |
| Non-circular? | Yes — lagged OLS / FTS are not the Rank 4 brochure |
| Schema match | **Partial** — H-LAG-WF scored on stand-in; H-KS-FTS tape **fail**; stamps not official CME |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** |

Do **not** collapse F-CC to the overnight tiny dip. Do **not** relabel leftover far months as CL1.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | NYMEX CL front-month next-session log-return | H-LAG on Yahoo `CL=F` stand-in; KS needs CL1–CL18 **absent** |
| Horizon | F-ON / F-DAY / F-CC | H-LAG scored; KS not run |
| Metric | RMSE vs 0 | H-LAG computed; F-CC horse **worse** than 0 |
| Protocol | Expanding walk-forward; last-500 OOS | Yes for H-LAG |
| Baseline | No-change | Same window as L-PULSE-STANDIN-1 |

**Schema match?** **Partial.**

---

## 2. Artifact summary

**Source / citation:** `PULSE_Horses_Standin.md` · `data/horse_scores.json` · operator `ok proceed` 2026-08-17.

**What it reports:** H-LAG last-500: F-ON 0.01283 vs 0 0.01291 (tiny beat); F-DAY 0.02670 vs 0.02663 (loss); F-CC 0.02888 vs 0.02869 (loss). H-KS-FTS not run (54 true-front dates vs 750 needed).

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — vendor generic (Yahoo), not exchange official
  - [x] Other: stand-in badge required

**If conflicted:** Labeled stand-in numbers only. Must **not** solely affirm P-NonNegligible skill as if live CME.

### Quantitative bar?
Yes. Rubric: `E_Quantitative_Evidence_Rubric_Horses.md`. Result: **not establish**.

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** H-LAG-WF / H-KS-FTS as named horses; L-PULSE-HORSES-1 as evaluation  
- [ ] Aim **ADMIT** F-SKILL established — **rejected**  
- [x] Aim **REJECT** reading the overnight dip as F-SKILL-met; reject leftover far months as CL1  

---

## 4. Scoped-result honesty

Stand-in ≠ live. F-DAY-met ≠ F-CC-met. Tiny F-ON RMSE dip ≠ F-ON-met. Missing curve ≠ FTS refute.

---

*Standing rule: Package-Satisfying Evidence Intake.*
