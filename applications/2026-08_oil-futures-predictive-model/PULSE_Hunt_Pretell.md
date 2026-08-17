# Pulse result — pretell discovery/confirm hunt (Yahoo stand-in)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-PRETELL-1**  
**Locks:** `Lock_Hunt_Pretell.md` · `Lock_Screen_Yahoo_Promote.md` · `Lock_Standin_Yahoo_CLF.md`  
**Live vs stand-in:** **Stand-in.** **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** You asked the computer to hunt among eight named “other series then oil” recipes, choosing only on older sessions. None of those eight beat “assume no change” on the whole trip in that older window. So **no winner was sent** to the recent exam. We did **not** take the least-bad and hope.

**What this settles:** Numeric discovery RMSE for the locked drawer. Hunt **failed at discovery**. Promote does **not** fire. Skill is still **not shown**. Not a trade.

---

## 1. Discovery (locked before last-500 confirm)

Prefix: CL sessions **≤ 2023-08-21** (n = **5769** return sessions). Scoreboard: last **500** of that prefix (**2021-08-25 … 2023-08-21**). Walk-forward OLS, min train 250. F-CC vs 0. Tell lag: F-ON/F-CC use t−2; F-DAY uses t−1.

Discovery F-CC RMSE of 0: **0.026705**.

| Horse | F-CC RMSE | vs 0 | Beats 0? |
|-------|-----------|------|----------|
| H-TELL-DXY | 0.026791 | 0.026705 | **no** |
| H-TELL-RBOB | 0.026822 | 0.026705 | **no** |
| H-TELL-HO | 0.026806 | 0.026705 | **no** |
| H-TELL-SPX | 0.026765 | 0.026705 | **no** (closest loss) |
| H-TELL-HG | 0.026791 | 0.026705 | **no** |
| H-TELL-TNX | 0.026824 | 0.026705 | **no** |
| H-TELL-AND-DXY-RBOB | 0.026788 | 0.026705 | **no** (triggered 229/500) |
| H-TELL-AND-RBOB-HO | 0.026795 | 0.026705 | **no** (triggered 371/500) |

**Survivor:** **none.** Reason: no horse strictly beat 0 on discovery F-CC.

Not selection (F-DAY-met ≠ F-CC-met): H-TELL-TNX F-DAY 0.025817 vs 0 0.025847 (tiny yes); H-TELL-AND-RBOB-HO F-DAY 0.025844 vs 0 0.025847 (tiny yes). Those **do not** create a survivor.

---

## 2. Confirm

**Skipped.** No discovery survivor. Last 250 / 500 / 750 were **not** used to pick a horse. Do **not** re-hunt this confirm window.

**L-SCREEN-Y-PROMOTE:** **does not fire** (no named confirm horse).

---

## 3. Establishment-stop drill

**Would honest `04` declare F-SKILL / F-CC / F-ON / F-DAY established?** **No.**

Eight named stand-in tells that **all lose** F-CC on the discovery 500 are not P-NonNegligible skill. A tiny discovery F-DAY dip is not F-CC. Failed discovery ≠ a promote. Cap remains these eight rows.

**Would honest `04` declare those bars refuted?** **No.** A finite drawer miss does not refute every recipe.

---

## 4. Scripts / artifacts

- `scripts/fetch_yahoo_tells.py` · `scripts/cl_pretell_hunt.py`  
- `data/tell_*.csv` · `data/tell_yahoo_fetch.json` · `data/pretell_hunt_scores.json`  
- Reproduce: `python3 scripts/fetch_yahoo_tells.py` then `python3 scripts/cl_pretell_hunt.py` from this application folder.

---

*Not trading advice. Stand-in ≠ live. No survivor ≠ pick the least-bad. Do not re-hunt confirm. Cap remains these eight rows.*
