# Pulse result — CFTC managed-money WTI positioning hunt (Yahoo stand-in)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-COT-1**  
**Locks:** `Lock_Hunt_COT.md` · `Lock_Screen_Yahoo_Promote.md` · `Lock_Standin_Yahoo_CLF.md`  
**Live vs stand-in:** **Stand-in.** **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** You asked the computer to take the public weekly count of how many crude-oil futures “managed money” traders are long minus short, use either that level or the change from the week before, and pick at most one of those two — only if it already beat “assume no change” on **older** whole trips. Percent-of-open-interest and other trader groups were **not** in this test. Neither number beat no-change on that older exam. So **no winner was sent** to the recent exam. We did **not** switch to percent-of-OI after seeing that.

**What this settles:** Numeric discovery RMSE for the locked two-horse drawer. Hunt **failed at discovery**. Promote does **not** fire. Skill is still **not shown**. Not a trade.

---

## 1. Vehicle (not a fail)

CFTC Disaggregated Futures-Only zips + current-week file. Contract **067651** (Crude Oil, Light Sweet – NYMEX). **867** weekly reports, report dates **2010-01-05 … 2026-08-11** (release Fridays **2010-01-08 … 2026-08-14**). 2006–2009 annual zips were not obtained; 2010-on is enough for the discovery span.

| Count | Value |
|-------|-------|
| Reports (whole dump) | **867** |
| Reports with release in discovery session span | **711** (threshold 30 — **not** vehicle-fail) |
| Discovery sessions with nonzero carried net | **3423** / 5769 |
| Discovery sessions with nonzero week change | **3418** / 5769 |

Carry-forward is in force (unlike DJT silent-day = 0). Scale = net / **1e5**. Do **not** retune. Do **not** add percent-of-OI.

---

## 2. Discovery (locked before last-500 confirm)

Prefix: CL sessions **≤ 2023-08-21** (n = **5769** return sessions). Scoreboard: last **500** of that prefix (**2021-08-25 … 2023-08-21**). Walk-forward OLS, min train 250. COT lag: F-ON/F-CC use t−2; F-DAY uses t−1.

Discovery F-CC RMSE of 0: **0.026705**.

| Horse | F-CC RMSE | vs 0 | Beats 0? |
|-------|-----------|------|----------|
| **H-COT-NET** | 0.026796 | 0.026705 | **no** (closest loss) |
| **H-COT-CHG** | 0.026804 | 0.026705 | **no** |

Exact F-CC: NET **0.02679628** vs 0 **0.02670534**; CHG **0.02680389**. F-ON and F-DAY also **lose** for both horses.

**Survivor:** **none.** Reason: no horse **strictly** beat 0 on discovery F-CC. Do **not** pick the least-bad.

---

## 3. Confirm

**Skipped.** No discovery survivor. Last 250 / 500 / 750 were **not** used to pick a horse. Do **not** re-hunt this confirm window. Do **not** add percent-of-OI or other trader groups after scores.

**L-SCREEN-Y-PROMOTE:** **does not fire** (no named confirm horse).

---

## 4. Establishment-stop drill

**Would honest `04` declare F-SKILL / F-CC / F-ON / F-DAY established?** **No.**

Two named weekly positioning features that **both lose** F-CC on the discovery 500 are not P-NonNegligible skill. Failed discovery ≠ a promote. Cap remains these two rows.

**Would honest `04` declare those bars refuted?** **No.** A finite drawer miss does not refute every recipe. It also does **not** say specs “don’t move oil” in some other book or clock.

---

## 5. Scripts / artifacts

- `scripts/fetch_cftc_cot.py` · `scripts/cl_cot_hunt.py`  
- `data/cftc_cl_mm_net.csv` · `data/cftc_cot_fetch.json` · `data/cot_hunt_scores.json`  
- Reproduce: `python3 scripts/fetch_cftc_cot.py` then `python3 scripts/cl_cot_hunt.py` from this application folder.

---

*Not trading advice. Stand-in ≠ live. No survivor ≠ pick the least-bad. Do not re-hunt confirm. Cap remains these two rows.*
