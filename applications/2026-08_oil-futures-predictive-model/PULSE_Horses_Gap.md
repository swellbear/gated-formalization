# Pulse result — overnight-gap day horses (Yahoo stand-in)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-GAP-1**  
**Locks:** `Lock_Horses_Gap.md` · `Lock_Screen_Yahoo_Promote.md` · `Lock_Standin_Yahoo_CLF.md`  
**Live vs stand-in:** **Stand-in.** **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** Two recipes that usually predict “no change” for the **day**, and only speak after a **large overnight gap**. One fades; one continues. Fade **barely** beat no-change on the older day exam, so it was the only one sent to the recent day exam. It still beat there, by a **small** amount. The **whole trip** was left as no-change, so this does **not** buy official CME. Not a trade. Flattening before the close is **still not named**.

**What this settles:** Numeric RMSE for **H-GAP-FADE** / **H-GAP-CONT**. Fade is the discovery survivor. Promote does **not** fire. F-DAY is **not** treated as F-SKILL-met. Tiny ≠ met.

---

## 1. Discovery (locked before last-500 confirm)

Prefix: CL sessions **≤ 2023-08-21** (n = **5769**). Scoreboard: last **500** of that prefix (**2021-08-25 … 2023-08-21**). Triggered **98 / 500** F-DAY sessions. F-ON / F-CC forecasts locked to **0**.

Discovery F-DAY RMSE of 0: **0.025847**.

| Horse | F-DAY RMSE | vs 0 | Beats 0? |
|-------|------------|------|----------|
| **H-GAP-FADE** | **0.025844** | 0.025847 | tiny yes |
| **H-GAP-CONT** | 0.025855 | 0.025847 | **no** |

Exact FADE: **0.02584386** vs 0 **0.02584659**. Difference ≈ **0.000003**.

**Survivor:** **H-GAP-FADE**. CONT is **not** sent to confirm.

---

## 2. Confirm (H-GAP-FADE only)

F-DAY vs 0:

| Window | RMSE horse | RMSE 0 | n triggered | Beats 0? |
|--------|------------|--------|-------------|----------|
| last 250 | 0.03089 | 0.03093 | 91 / 250 | yes (small) |
| last 500 | **0.02658** | **0.02663** | 135 / 500 | yes (small) |
| last 750 | 0.02392 | 0.02396 | 169 / 750 | yes (small) |

Last-500 F-DAY exact: horse **0.026584** vs 0 **0.026634**. Difference ≈ **0.000050**.

F-ON and F-CC: horse RMSE **equals** 0 on 250 / 500 / 750 (forecast locked to 0). F-CC last 500: **0.02869 = 0.02869**.

**L-SCREEN-Y-PROMOTE:** **does not fire** (F-CC does not **strictly** beat 0). A day win **does not promote**.

---

## 3. Establishment-stop drill

**Would honest `04` declare F-SKILL / F-CC established?** **No.**

**Would honest `04` declare F-DAY established (P-NonNegligible)?** **No.**

Stand-in Yahoo; point RMSE only; discovery edge **0.000003**; confirm last-500 edge **0.000050**. Tiny ≠ met. F-DAY-met ≠ F-CC-met. Combo / flatten-before-close still unnamed. Cap remains these two rows.

**Would honest `04` declare those bars refuted?** **No.** A small day-session fade on Yahoo does not refute every day recipe, and does not refute F-CC.

---

## 4. Scripts / artifacts

- `scripts/cl_gap_horses.py` · `data/gap_horse_scores.json`  
- Reproduce: `python3 scripts/cl_gap_horses.py` from this application folder.

---

*Not trading advice. Stand-in ≠ live. Tiny F-DAY dip ≠ skill-met. Day win ≠ promote. Do not remix this pair. Combo still unnamed.*
