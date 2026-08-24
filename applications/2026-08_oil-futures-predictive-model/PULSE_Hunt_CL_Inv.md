# Pulse result — EIA weekly inventory overlay on Yahoo CL

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-CL-INV-1**  
**Locks:** `Lock_Hunt_CL_Inv.md` · `Lock_Screen_Yahoo_Promote.md`  
**Live vs stand-in:** Yahoo `CL=F` + EIA weekly crude ex-SPR. **Not** Bloomberg surprise. **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** You asked for the next different futures recipe on Yahoo. We took the public weekly U.S. crude stockpile report (naive surprise, and raw week-change) and asked whether either helped forecast the next whole CL session better than “assume no change.” Neither did on the older exam. Confirm was **not** run. Burned lag / sparse / gap / pretell / DJT / COT recipes were **not** retuned.

**What this settles:** Numeric discovery F-CC for this two-horse drawer. Hunt **failed at discovery**. Not a trade.

---

## 1. Vehicle (not a fail)

Inventory reports in discovery session span: well above 30. Yahoo stand-in OK.

---

## 2. Discovery (locked before last-500 confirm)

Cutoff: CL sessions **≤ 2023-08-21**. Scoreboard: last **500** F-CC RMSE vs 0.

| Horse | RMSE horse | RMSE 0 | Beats 0? |
|-------|------------|--------|----------|
| **H-CL-INV-SURP** | 0.026836 | 0.026705 | **no** |
| **H-CL-INV-WOW** | 0.026803 | 0.026705 | **no** (closest miss) |

**Survivor:** **none.** Do **not** pick least-bad.

---

## 3. Confirm

**Skipped.** Promote **does not fire**.

---

## 4. Establishment-stop drill

**Would honest `04` declare F-SKILL established?** **No.**

**Would honest `04` declare F-SKILL refuted?** **No.** A finite drawer miss is not “inventories never matter.”

---

## 5. Scripts / artifacts

- `scripts/cl_inv_hunt.py`  
- `data/cl_inv_hunt_scores.json`  
- Reproduce: `python3 scripts/cl_inv_hunt.py --phase discovery`

---

*Not trading advice. Naive surprise ≠ Bloomberg. No survivor ≠ least-bad. Confirm is not a training arm.*
