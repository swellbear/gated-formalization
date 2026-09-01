# Pulse result — annual season overlay on Yahoo CL

**Date:** 2026-09-01  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-CL-SEAS-1**  
**Locks:** `Lock_Hunt_CL_Seas.md` · `Lock_Screen_Yahoo_Promote.md` · `QUEUE_CL_Yahoo_Exploration.md`  
**Live vs stand-in:** Yahoo `CL=F`. **Not** H-SPARSE-CAL event-day sparse. **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** The operator asked to decide the next unused futures recipes and chip them without a further prompt. First on the frozen list: calendar **season** of the session date (smooth annual cycle, and calendar-month dummies) as extra numbers in a next-session CL forecast versus “assume no change.” Neither helped on the older exam. Confirm was **not** run. Burned lag / sparse / gap / pretell / DJT / COT / INV recipes were **not** retuned. Spot 21-day stayed parked.

**What this settles:** Numeric discovery F-CC for this two-horse drawer. Hunt **failed at discovery**. Not a trade. Frozen next class remains **C-CL-DOW**.

---

## 1. Vehicle (not a fail)

Yahoo stand-in discovery sessions: **5769** (2000-08-24 … 2023-08-21). Last-500 F-CC pool OK.

---

## 2. Discovery (locked before last-500 confirm)

Cutoff: CL sessions **≤ 2023-08-21**. Scoreboard: last **500** F-CC RMSE vs 0.

| Horse | RMSE horse | RMSE 0 | Beats 0? |
|-------|------------|--------|----------|
| **H-CL-SEAS-ANN** | 0.026799 | 0.026705 | **no** (closest miss) |
| **H-CL-SEAS-MON** | 0.026816 | 0.026705 | **no** |

**Survivor:** **none.** Do **not** pick least-bad.

---

## 3. Confirm

**Skipped.** Promote **does not fire**.

---

## 4. Establishment-stop drill

**Would honest `04` declare F-SKILL established?** **No.**

**Would honest `04` declare F-SKILL refuted?** **No.** A finite drawer miss is not “oil has no season.”

---

## 5. Scripts / artifacts

- `scripts/cl_seas_hunt.py`  
- `data/cl_seas_hunt_scores.json`  
- Reproduce: `python3 scripts/cl_seas_hunt.py --phase discovery`

---

*Not trading advice. Annual season ≠ event-day sparse. No survivor ≠ least-bad. Confirm is not a training arm.*
