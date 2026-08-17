# Package-Satisfying Evidence Intake — sparse horses pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 + L-SESS + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + H-SPARSE-CAL + H-SPARSE-VOL**  
**Target dependent(s):** F-SKILL / F-ON / F-DAY / F-CC  
**Named-class pulse?** **Yes** (operator **B** `name horse H-SPARSE-CAL + H-SPARSE-VOL`)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | F-CC = Rank 4 F-SKILL; F-ON / F-DAY per L-SESS; walk-forward RMSE vs no-change; promote = F-CC beat on 500 and not-lose on 250/750 |
| Named source class | **H-SPARSE-CAL** and **H-SPARSE-VOL** on Yahoo `CL=F` (`Lock_Horses_Sparse.md`) |
| Named enough? | **Yes** (recipes and calendar written before OOS look) |
| Non-circular? | Yes — gated OLS is not the Rank 4 brochure |
| Schema match | **Partial** — scored on stand-in; stamps not official CME |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** |

Do **not** collapse F-CC to the 0.000004 last-500 dip. Do **not** treat a failed 750 as a promote.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | NYMEX CL front-month next-session log-return | Yahoo `CL=F` stand-in |
| Horizon | F-ON / F-DAY / F-CC | Both horses scored |
| Metric | RMSE vs 0 | Computed; CAL tiny 500 beat; VOL F-CC **loss** |
| Protocol | Expanding walk-forward; last-500 OOS | Yes |
| Baseline | No-change | Same window as L-PULSE-STANDIN-1 |
| Promote | F-CC < 0 on 500 and ≤ 0 on 250 and 750 | **Neither fires** (CAL fails 750; VOL fails all three) |

**Schema match?** **Partial.**

---

## 2. Artifact summary

**Source / citation:** `PULSE_Horses_Sparse.md` · `data/horse_scores.json` · operator **B** 2026-08-17.

**What it reports:** CAL last-500 F-CC 0.02868990 vs 0 0.02869369 (tiny beat; **fails** last 750). VOL last-500 F-CC 0.02885 vs 0.02869 (**loss**). Cap = two rows.

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — vendor generic (Yahoo), not exchange official
  - [x] Other: stand-in badge required

**If conflicted:** Labeled stand-in numbers only. Must **not** solely affirm P-NonNegligible skill as if live CME.

### Quantitative bar?
Yes. Rubric: `E_Quantitative_Evidence_Rubric_Sparse.md`. Result: **not establish**.

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** H-SPARSE-CAL / H-SPARSE-VOL as named horses; L-PULSE-SPARSE-1 as evaluation  
- [ ] Aim **ADMIT** F-SKILL established — **rejected**  
- [x] Aim **REJECT** reading the tiny F-CC 500 dip as F-SKILL-met or as a promote  

---

## 4. Scoped-result honesty

Stand-in ≠ live. Tiny ≠ met. Failed 750 ≠ promote. Two rows ≠ a zoo. F-DAY-met ≠ F-CC-met.

---

*Standing rule: Package-Satisfying Evidence Intake.*
