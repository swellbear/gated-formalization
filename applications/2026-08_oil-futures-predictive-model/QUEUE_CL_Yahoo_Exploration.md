# Exploration queue — Yahoo CL F-CC (R-F-SKILL leftover)

**Date:** 2026-09-01  
**Lock this pulse:** `Lock_Hunt_CL_Seas.md`  
**Machine register:** `data/cl_yahoo_queue.json`  
**Operator:** delegated — decide the unused classes and chip them without a further prompt.

---

## 0. Plain-language framing

**What we’re doing:** Keep a written list of *kinds* of next-session CL recipe still unused on Yahoo, and a list of recipes that already failed. One kind at a time. The recent exam is never where we invent a new rule.

**What this does *not* mean:** Auto-naming after scores. Unburning burned CL horses. A new cash 21-day spot class (Track B already lost confirm; continuation won that object). Curve/FTS on the Yahoo month chain (that file is not historical CL1–CL18). Days-to-expiry from `front_id` (stand-in `front_id` is always `CL=F`).

---

## Rules (frozen)

1. **One class, two horses max** per pulse.  
2. Freeze the rule **before** discovery. Discovery **before** confirm.  
3. Pick one only if it **strictly beats** no-change on discovery F-CC. Else **no survivor**. Do not pick least-bad.  
4. **Burned** rows are not remixed after RMSE.  
5. Confirm last 500 / 250 / 750 **never** trains.  
6. The loop **only reads `next`**. It does not append a class after seeing hit-rate.  
7. Stop when `next` is empty, a horse **promotes**, or park-90d.  
8. Wrong object (spot 21-day, live CME, DataMine) stays **out** of this queue.

---

## Frozen `next` (named before any SEAS scores)

| Queue ID | Class | Why it is a different class |
|----------|-------|------------------------------|
| **C-CL-SEAS** (this pulse) | Annual calendar harmonics / month overlay | Every-session season, not EIA/FOMC **event-day** sparse (`H-SPARSE-CAL`) |
| **C-CL-DOW** | Weekday overlay | Weekly cycle, not annual season and not event-day sparse |

**Not queued (refused):** new Track B spot class; Yahoo month-chain curve; `front_id` roll clock; retune INV/COT/DJT/gap/pretell/lag/sparse; pick least-bad discovery loser.

---

## This pulse — **C-CL-SEAS** / **L-HUNT-CL-SEAS**

| ID | Role |
|----|------|
| **H-CL-SEAS-ANN** | Expanding OLS: CL lags + annual sin/cos of day-of-year |
| **H-CL-SEAS-MON** | Expanding OLS: CL lags + calendar-month dummies (Jan baseline) |
| No-change **0** | **Baseline, not a horse** |

**Burned (do not retune / do not unburn):** H-LAG-WF, H-SPARSE-CAL, H-SPARSE-VOL, H-GAP-FADE, H-GAP-CONT, L-HUNT-PRETELL, L-HUNT-DJT, L-HUNT-COT, H-CL-INV-SURP, H-CL-INV-WOW.

---

*Failed discovery is an allowed useful negative. The project learns. The horse does not peek.*
