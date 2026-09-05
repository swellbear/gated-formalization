# Pulse record — Lab Track B invent→test batch 1 (docs only)

**Date:** 2026-09-05  
**Application:** `2026-08_oil-futures-predictive-model`  
**Object:** Track B (EIA spot 21-day vs continuation) — **not** R-F-SKILL / F-CC futures  
**Protocol:** `Lock_Hunt_Spot_Trend`  
**Series:** FRED EIA spot WTI `DCOILWTICO` / Brent `DCOILBRENTEU`  
**Discovery:** n=500, dates **≤2023-08-21**, vs continuation  
**Continuation:** WTI **0.5080** / Brent **0.5060**  
**Confirm:** windows **250 / 500 / 750**, **survivors only**  
**DXY vehicle:** FRED **DTWEXBGS**  
**Gatekeeper:** **REJECT / burn** all Lab batch-1 classes and horses on both boards. Confirm survivors: **NONE**. Scripts **not** on master.

---

## 0. Plain-language framing

**What this is:** The locked cite pack for Lab invent→test batch 1. Four spot classes were scored against continuation. Some horses survived discovery. **None** survived confirm.

**What this settles:** MAG / PERSIST / BREAK / DXY — **all variants, both boards — burned**. Named Track B queue remains **empty**. Spot-trend skill is still **not established**. Discovery beat ≠ confirm. Do not pick least-bad. Not a trade.

**What this is not:** Not an R-F-SKILL pulse. Not a futures horse. Not a reason to revive FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, or DXY.

---

## 1. Locked cite (all burned)

| Class | Horse | WTI | Brent |
|-------|-------|-----|-------|
| **C-SPOT-MAG** | MAG-STRONG | killed disc | killed disc |
| **C-SPOT-MAG** | MAG-WEAK | killed disc | disc survivor → confirm fail (**250 no**) |
| **C-SPOT-PERSIST** | PERSIST | killed disc | killed disc |
| **C-SPOT-PERSIST** | FRESH | disc survivor → confirm fail (**500/250 no**) | disc survivor → confirm fail (**250 no**) |
| **C-SPOT-BREAK** | BREAK63 | disc tie → killed | disc tie → killed |
| **C-SPOT-BREAK** | BREAK42 | disc tie → killed | disc tie → killed |
| **C-SPOT-DXY** | DXY-INV | disc survivor → confirm fail | disc survivor → confirm fail |
| **C-SPOT-DXY** | DXY-ALIGN | killed disc | killed disc |

**Confirm survivors:** **NONE**. Nothing admitted.

**Still burned (prior Track B):** FLIP/REV, INV, CROSS, LOGIT.

---

## 2. Notes

- Discovery n=500 ≤2023-08-21; cont WTI=0.5080 Brent=0.5060; DXY=DTWEXBGS.
- Disc tie ≠ pick (BREAK63/42 both boards).
- Scripts / hunt code **not** merged.
- Lab may invent **new** classes after this fold. Must **not** revive the burned set.

---

*Docs only. Track B ≠ F-SKILL. Discovery beat ≠ confirm. No least-bad. Not trading advice.*
