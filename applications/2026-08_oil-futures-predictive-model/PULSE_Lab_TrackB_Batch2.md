# Pulse record — Lab Track B invent→test batch 2 (docs only)

**Date:** 2026-09-05  
**Application:** `2026-08_oil-futures-predictive-model`  
**Object:** Track B (EIA spot 21-day vs continuation) — **not** R-F-SKILL / F-CC futures  
**Protocol:** `Lock_Hunt_Spot_Trend`  
**Series:** FRED EIA spot WTI `DCOILWTICO` / Brent `DCOILBRENTEU`  
**Discovery:** n=500, dates **≤2023-08-21**, vs continuation  
**Continuation:** WTI **0.5080** / Brent **0.5060**  
**Confirm:** windows **250 / 500 / 750**, **survivors only**  
**Rates vehicle:** FRED **DGS10** (not DXY)  
**Spread vehicle:** Brent−WTI z expanding, past-only (not CROSS)  
**Gatekeeper:** **REJECT / burn** all Lab batch-2 classes and horses on both boards. Confirm survivors: **NONE**. Scripts **not** on master.

---

## 0. Plain-language framing

**What this is:** The locked cite pack for Lab invent→test batch 2. Four new spot classes were scored against continuation. Some horses survived discovery, including a **strong** DGS10-ALIGN hit (~0.61–0.62). **None** survived confirm.

**What this settles:** SHORT / VOTE / RATES / SPREAD — **all horses, both boards — burned**. Named Track B queue remains **empty**. Spot-trend skill is still **not established**. Discovery beat ≠ confirm. Last-750 near-miss ≠ least-bad. Not a trade.

**What this is not:** Not an R-F-SKILL pulse. Not a futures horse. Not a reason to revive FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, DXY, SHORT, VOTE, RATES, or SPREAD.

---

## 1. Locked cite (all burned)

| Class | Horse | WTI | Brent |
|-------|-------|-----|-------|
| **C-SPOT-SHORT** | SIGN5 | disc survivor → confirm kill | disc survivor → confirm kill |
| **C-SPOT-SHORT** | SIGN10 | disc survivor → confirm kill | disc survivor → confirm kill |
| **C-SPOT-VOTE** | VOTE3 | disc survivor → confirm kill | disc survivor → confirm kill |
| **C-SPOT-VOTE** | VOTE-STRICT | killed disc (tautology: 0 noncont / always continuation) | killed disc (tautology: 0 noncont / always continuation) |
| **C-SPOT-RATES** | DGS10-INV | killed disc | killed disc |
| **C-SPOT-RATES** | DGS10-ALIGN | disc strong (~0.61–0.62) → confirm kill (**last-500 tie**) | disc strong (~0.61–0.62) → confirm kill |
| **C-SPOT-SPREAD** | SPREAD-FADE | disc survivor → confirm kill | killed disc (opposite horse) |
| **C-SPOT-SPREAD** | SPREAD-CATCH | killed disc (opposite horse) | disc survivor → confirm kill (**500/250 yes, 750 no**) |

**Confirm survivors:** **NONE**. Nothing admitted.

**Still burned (prior Track B):** FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, DXY.

---

## 2. Notes

- Discovery n=500 ≤2023-08-21; cont WTI=0.5080 Brent=0.5060; confirm 500/250/750 survivors only.
- Rates vehicle is **DGS10**, not DXY. Spread is Brent−WTI z expanding past-only — **not** CROSS.
- Strong disc (DGS10-ALIGN ~0.61–0.62) ≠ confirm. WTI last-500 **tie** ≠ pick.
- Brent SPREAD-CATCH nearest miss (500/250 yes, **750 no**) ≠ least-bad.
- VOTE-STRICT tautology (0 noncont / always continuation) is a disc kill, not a horse.
- Scripts / hunt code **not** merged.
- Lab may invent **new** classes after this fold. Must **not** revive the burned set.

---

*Docs only. Track B ≠ F-SKILL. Discovery beat ≠ confirm. No least-bad. Not trading advice.*
