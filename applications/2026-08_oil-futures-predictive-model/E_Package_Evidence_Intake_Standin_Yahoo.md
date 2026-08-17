# Package-Satisfying Evidence Intake — Yahoo CL=F stand-in pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF**  
**Target dependent(s):** F-SKILL / F-ON / F-DAY / F-CC; live vs stand-in  
**Named-class pulse?** **Yes** (stipulated stand-in)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | F-CC = Rank 4 F-SKILL; F-ON / F-DAY per L-SESS; RMSE vs no-change; walk-forward / pre-declared holdout |
| Named source class | **Stand-in:** Yahoo `CL=F` daily Open/Close; Close as settlement; R1 does not fire |
| Named enough? | **Yes** (operator stipulated this series) |
| Non-circular? | Yes — vendor generic is not the Rank 4 brochure; no-change is the baseline |
| Schema match | **Partial** — object/horizon/metric computed; stamps are **not** official CME; roll R1 **not** applied |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** |

Do **not** collapse the bar to “we have some RMSE.” Do **not** treat Kearney–Shang MAE as this pulse.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | NYMEX CL front-month official open/settle | **Stand-in** Yahoo `CL=F` Open/Close |
| Horizon | F-ON / F-DAY / F-CC | Computed |
| Metric | RMSE vs 0 | Computed on last 500 (+ 250/750) |
| Protocol | Pre-declared holdout | Last 500 sessions (2024-08-20 … 2026-08-14) |
| Baseline | No-change | Scored; no horse vs baseline |
| Roll R1 | Drop ON/CC on front change | **Not applied** (constant `front_id`) |
| Optional FTS | Kearney–Shang on same tape | **Not run** |

**Schema match?** **Partial.** Numeric baseline **yes**. Official stamps / R1 **no**.

---

## 2. Artifact summary

**Source / citation:** Yahoo Finance chart API for `CL=F`; operator stipulation 2026-08-17; `PULSE_Standin_Yahoo_CLF_RMSE.md`.

**What it reports:** Stand-in last-500 RMSE: F-ON 0.01291; F-DAY 0.02663; F-CC 0.02869 (n=500). Skill bars **not established**.

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — vendor generic (Yahoo), not exchange official
  - [x] Other: commercial vendor continuous future; **stand-in badge required**

**If conflicted:** May support **scenario / kinship / labeled stand-in numbers only**. Must **not** be the sole basis for affirming P-NonNegligible skill as if live CME.

### Quantitative bar?
Yes. Rubric: `E_Quantitative_Evidence_Rubric_Standin_Yahoo.md`. Result: **not establish**.

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** L-STANDIN-Y-CLF (stipulation) + L-PULSE-STANDIN-1 (baseline RMSE, stand-in)  
- [ ] Aim **ADMIT** F-SKILL established — **rejected**  
- [x] Aim **REJECT** reading these numbers as live CME or as a model beating no-change  

---

## 4. Scoped-result honesty

Hold **under:** Rank 4 + L-SESS + stipulated Yahoo stand-in.  
**Must not be promoted to:** F-SKILL-met; live CME; “daytime is easier”; a trade; oil-offshoot clearance.

---

## 5. Next

Record not-established. Combo still parked. No Phase 2. Reopen live tape with `live CME only`.

---

*Standing rule: Package-satisfying evidence intake. Print-match ≠ clearance.*
