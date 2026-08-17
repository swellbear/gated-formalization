# Lock Record — stipulated stand-in (Yahoo CL=F)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** `Ok do what needs to be done then` after the recommended stipulation line  
**App-local lock ID:** **L-STANDIN-Y-CLF**  
**Status:** **IN FORCE as the stipulated skill tape.** Pulse ran. Bars **not established**. Does **not** replace **F-SRC-CME-TAPE** as the live class.

---

## 0. Plain-language framing

**What was decided:**  
Until official CME stamps are in hand, night / day / whole-trip RMSE may be scored on **Yahoo `CL=F` daily Open and Close**, labeled **stand-in**. Close stands in for official settlement. Open stands in for official printed open.

**What this settles:**  
The live-vs-stand-in fork. Yahoo is no longer an unstipulated silent proxy.

**What this does *not* settle:**  
That skill is shown. That Yahoo is CME settlement. That anyone should trade.

---

## Named stand-in (quote this)

**Yahoo Finance `CL=F` (NYMEX Light Sweet Crude continuous generic) daily Open and Close.**  
**Badge:** **stand-in** — not official CME open/settlement.  
**Roll note:** `CL=F` is already a vendor-spliced continuous series. `front_id` is constant `CL=F`, so roll rule **R1 never drops rows**. Yahoo splice ≠ CME R1. Do **not** treat Panama/Yahoo price levels as official settlement.

**Formulas (Close as settle):**

```
r_ON,t  = ln(Open_t / Close_{t-1})
r_DAY,t = ln(Close_t / Open_t)
r_CC,t  = ln(Close_t / Close_{t-1})
```

---

## Locked content

**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF**.

| ID | Rule |
|----|------|
| **Live vs stand-in** | **Stand-in stipulated** as above. Live remains official CME DataMine EOD. |
| **F-COMBO** | Still **parked**. |
| **Kearney–Shang FTS** | Still **not run** (no CL1–CL18 on this generic). |

---

## What this does *not* do

- Does **not** establish F-CC, F-ON, F-DAY, F-COMBO, or V-VALUE.  
- Does **not** license trading.  
- Does **not** convert a stand-in pass into live clearance.  
- Does **not** enter Phase 2.  
- Does **not** start an oil offshoot.

**Lock-time Amb warning:** Closing the tape fork drops leftover-ambiguity. **Amb drop ≠ clearance.**

---

## Reopen

`live CME only` — replace this tape with official open/settle and re-run the same formulas. Honest **established** still **stops**.
