# Pulse record — Lab Track B invent→test batch 1 (docs only)

**Date:** 2026-09-05  
**Application:** `2026-08_oil-futures-predictive-model`  
**Object:** Track B (EIA spot 21-day vs continuation) — **not** R-F-SKILL / F-CC futures  
**Protocol:** `Lock_Hunt_Spot_Trend`  
**Series:** FRED EIA spot WTI `DCOILWTICO` / Brent `DCOILBRENTEU`  
**Discovery:** cutoff **2023-08-21** last-500 vs continuation  
**Confirm:** windows **250 / 500 / 750**, **survivors only**  
**Gatekeeper:** **REJECT / burn** all Lab batch-1 classes and horses on both boards. Confirm survivors: **none**. Scripts **not** on master.

---

## 0. Plain-language framing

**What this is:** A short record of the Lab invent→test batch-1 boards. Four new spot classes were scored against continuation. Some horses beat discovery. **None** survived confirm.

**What this settles:** Those four classes and eight horses are **burned**. Named Track B queue remains **empty**. Spot-trend skill is still **not established**. Discovery beat ≠ confirm. Do not pick least-bad. Not a trade.

**What this is not:** Not an R-F-SKILL pulse. Not a futures horse. Not a reason to revive FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, or DXY.

---

## 1. Roster (all burned)

| Class | Horses |
|-------|--------|
| **C-SPOT-MAG** | MAG-STRONG / MAG-WEAK |
| **C-SPOT-PERSIST** | PERSIST / FRESH |
| **C-SPOT-BREAK** | BREAK63 / BREAK42 |
| **C-SPOT-DXY** | DXY-INV / DXY-ALIGN |

**Still burned (prior Track B):** FLIP/REV, INV, CROSS, LOGIT.

---

## 2. Discovery (last-500 vs continuation)

| Board | Continuation | Survivors (hit rate) | Killed |
|-------|--------------|----------------------|--------|
| **WTI** | 0.508 | FRESH **0.592**; DXY-INV **0.522** | MAG-STRONG / MAG-WEAK; PERSIST; BREAK63 / BREAK42 (tied continuation → killed); DXY-ALIGN |
| **Brent** | 0.506 | MAG-WEAK **0.526**; FRESH **0.628**; DXY-INV **0.524** | MAG-STRONG; PERSIST; BREAK63 / BREAK42; DXY-ALIGN |

BREAK made **0** non-continuation calls on discovery. Tie ≠ pick.

---

## 3. Confirm (survivors only; 250 / 500 / 750)

| Board | Survivor sent to confirm | Result |
|-------|--------------------------|--------|
| **WTI** | FRESH; DXY-INV | **killed** — no window set all strictly beat |
| **Brent** | MAG-WEAK; FRESH; DXY-INV | **killed** — each fails ≥1 window |

**Confirm survivors:** **none**. Nothing admitted.

---

## 4. Notes

- DXY vehicle: FRED **DTWEXBGS**.
- WTI skipped the **2020-04-20** nonpositive print.
- Scripts / hunt code **not** merged.
- Lab may invent **new** classes after this fold. Must **not** revive the burned set.

---

*Docs only. Track B ≠ F-SKILL. Discovery beat ≠ confirm. No least-bad. Not trading advice.*
