# Pulse result — weekday overlay on Yahoo CL

**Date:** 2026-09-01  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-CL-DOW-1**  
**Locks:** `Lock_Hunt_CL_Dow.md` · `Lock_Screen_Yahoo_Promote.md` · `QUEUE_CL_Yahoo_Exploration.md`  
**Live vs stand-in:** Yahoo `CL=F`. **Not** H-SPARSE-CAL. **Not** a retune of SEAS. **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** After annual season lost discovery, the frozen next class was weekday of the session date (Tue–Fri dummies, and Friday-only). Neither helped forecast the next whole CL session better than “assume no change” on the older exam. Confirm was **not** run. Frozen `next` is now **empty**. Stop.

**What this settles:** Numeric discovery F-CC for this two-horse drawer. Hunt **failed at discovery**. Not a trade.

---

## 1. Vehicle (not a fail)

Yahoo stand-in discovery sessions: **5769** (2000-08-24 … 2023-08-21). Last-500 F-CC pool OK.

---

## 2. Discovery (locked before last-500 confirm)

Cutoff: CL sessions **≤ 2023-08-21**. Scoreboard: last **500** F-CC RMSE vs 0.

| Horse | RMSE horse | RMSE 0 | Beats 0? |
|-------|------------|--------|----------|
| **H-CL-DOW-WD** | 0.026812 | 0.026705 | **no** |
| **H-CL-DOW-FRI** | 0.026775 | 0.026705 | **no** (closest miss) |

**Survivor:** **none.** Do **not** pick least-bad.

---

## 3. Confirm

**Skipped.** Promote **does not fire**.

---

## 4. Establishment-stop drill

**Would honest `04` declare F-SKILL established?** **No.**

**Would honest `04` declare F-SKILL refuted?** **No.** A finite drawer miss is not “oil has no weekday effect.”

---

## 5. Scripts / artifacts

- `scripts/cl_dow_hunt.py`  
- `data/cl_dow_hunt_scores.json`  
- Reproduce: `python3 scripts/cl_dow_hunt.py --phase discovery`

---

*Not trading advice. Weekday ≠ annual season ≠ event-day sparse. No survivor ≠ least-bad. Confirm is not a training arm. Frozen next empty → stop.*
