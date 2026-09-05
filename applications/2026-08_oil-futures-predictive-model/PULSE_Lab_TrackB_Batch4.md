# Pulse record — Lab Track B invent→test batch 4 (docs only)

**Date:** 2026-09-05  
**Application:** `2026-08_oil-futures-predictive-model`  
**Object:** Track B (EIA spot 21-day vs continuation) — **not** R-F-SKILL / F-CC futures  
**Protocol:** `Lock_Hunt_Spot_Trend`  
**Series:** FRED EIA spot WTI `DCOILWTICO` / Brent `DCOILBRENTEU`  
**Discovery:** n=500, dates **≤2023-08-21**, vs continuation  
**Continuation:** WTI **0.5080** / Brent **0.5060**  
**Confirm:** windows **250 / 500 / 750**, **survivors only**  
**Gatekeeper (new skill horses):** **REJECT / burn** SHRINK / VOLTGT / QUANT on both boards. Confirm survivors among new skill horses: **NONE**.  
**Gatekeeper (scoped survivor ROBUST):** Brent **H-SPOT-MOY-CONT** remains **scoped confirm** on record — mark **FRAGILE**. **Not** skill-met. **Not** a null burn. **Not** an elevation. Scripts **not** on master.

---

## 0. Plain-language framing

**What this is:** The locked cite pack for Lab invent→test batch 4. Three new skill horses were scored. **None** survived. The batch-3 scoped confirm survivor (Brent month-continuation) was then stress-tested for year-stability. It **stays on the card** as a scoped confirm pass, now marked **FRAGILE**.

**What this settles:** SHRINK / VOLTGT / QUANT — **burned** (both boards). Confirm survivors among new skill horses: **NONE**. Brent **H-SPOT-MOY-CONT** is still a scoped confirm pass — **not** a null, **not** skill-met, **not** C-SPOT-SEAS established, **not** WTI-met, **not** elevated. Year-stability Amb is constrained **toward fragile**, not toward clearance. Burned-class invent queue is **empty**. Live scoped horse stays on record, now **FRAGILE**. Spot-trend skill is still **not established**. Amb ≠ clearance. Not a trade.

**What this is not:** Not an R-F-SKILL pulse. Not a futures horse. Not Track B skill-met. Not an elevation of Brent MOY-CONT. Not a reason to treat Brent MOY-CONT as burned. Not a reason to revive FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, DXY, SHORT, VOTE, RATES, SPREAD, VIX, THRESH, SKEW, SHRINK, VOLTGT, or QUANT. VOLTGT ABS05 is **vol-target**, not the already-burned direction-THRESH ABS05.

---

## 1. Locked cite — new skill-horse burns

| Class | Horse | WTI | Brent |
|-------|-------|-----|-------|
| **C-SPOT-SHRINK** | SHRINK25 | RMSE vs 0-forecast **worsens**; no confirm | RMSE vs 0-forecast **worsens**; no confirm |
| **C-SPOT-SHRINK** | SHRINK50 | RMSE vs 0-forecast **worsens**; no confirm | RMSE vs 0-forecast **worsens**; no confirm |
| **C-SPOT-VOLTGT** | MAG | loses to always-predict-1; no confirm | loses to always-predict-1; no confirm |
| **C-SPOT-VOLTGT** | ABS05 | loses to always-predict-1; no confirm (**vol-target** ≠ burned direction-THRESH ABS05) | loses to always-predict-1; no confirm (**vol-target** ≠ burned direction-THRESH ABS05) |
| **C-SPOT-QUANT** | QUANT | definitional collapse: hr ≡ continuation; `noncont_calls=0` | definitional collapse: hr ≡ continuation; `noncont_calls=0` |

**Confirm survivors among new skill horses:** **NONE**. Nothing admitted from this invent set.

**Still burned (prior Track B):** FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, DXY, SHORT, VOTE, RATES, SPREAD, VIX, THRESH, SKEW. C-SPOT-SEAS MOY-DIR both boards and WTI MOY-CONT remain burned. Brent MOY-CONT is **not** in that burn set.

---

## 2. Locked cite — scoped confirm survivor now FRAGILE (not skill-met / not elevate / not a null)

Brent **H-SPOT-MOY-CONT** remains the **scoped confirm pass** recorded in batch 3 (last_500 **0.5440 > 0.5100**; last_250 **0.5600 > 0.5200**; last_750 **0.5253 > 0.5147**). ROBUST stress does **not** retract that scoped confirm. It marks the horse **FRAGILE**.

| Check | Result | Read |
|-------|--------|------|
| **(a)** Discovery cutoff **2018-08-21**, last-500 | Brent still beats continuation | Stability under earlier cutoff — **not** clearance |
| **(b)** Leave-one-year-out **post-2023-08-21** | **2023 FAIL** **0.374 vs 0.582** (n=91); **2024 / 2025 / 2026 beat** | Year-stability **fails 2023**; later years do not erase that fail |

**FRAGILE ≠ elevated.** Do **not** promote to skill-met. Do **not** claim C-SPOT-SEAS established. Do **not** claim WTI-met. Do **not** treat as a null burn to keep the invent queue “empty.” Year-stability Amb is constrained **toward fragile**, not toward clearance.

**Do record:** scoped confirm remains on record; mark **FRAGILE**; Amb ≠ clearance; not a trade.

---

## 3. Notes

- Discovery n=500 ≤2023-08-21; cont WTI=0.5080 Brent=0.5060; confirm 250/500/750 survivors only.
- SHRINK is RMSE vs **0-forecast**. Shrunk momentum **worsens** RMSE on both boards (SHRINK25 / SHRINK50). No confirm window.
- VOLTGT accuracy is vs **always-predict-1**. MAG and ABS05 lose both boards. VOLTGT ABS05 is **vol-target**, not the burned direction-THRESH ABS05.
- QUANT is a **dead definition**, not a near-miss: hit-rate ≡ continuation and `noncont_calls=0`. Burn. Do not keep as a horse.
- Brent MOY-CONT year-stability: 2023 leave-one-year-out **FAIL** (0.374 vs 0.582, n=91). 2024/25/26 beat does **not** clear year-stability. FRAGILE, not elevate, not burn-as-null.
- C-SPOT-SEAS is still **not** class-met. WTI-met ≠ Brent-met. Scoped confirm ≠ slogan clearance. FRAGILE scoped confirm ≠ skill-met.
- Burned-class invent queue is **empty**. Live scoped horse: Brent **H-SPOT-MOY-CONT** (**FRAGILE**).
- Scripts / hunt code **not** merged.
- **P3=B** (Founder/user 2026-09-05, after this fold): all-day directional invent **parked**. Do **not** mint new beat-continuation / direction horse classes. Residual left open is **vehicle + cutoff fragility** on Brent MOY-CONT (scoped confirm + FRAGILE). Must **not** revive the burned set (now including SHRINK / VOLTGT / QUANT). Must **not** treat Brent MOY-CONT as a null. Must **not** promote it to skill-met.

---

*Docs only. Track B ≠ F-SKILL. Scoped confirm ≠ skill-met. FRAGILE ≠ elevated. Dead definition ≠ near-miss. Discovery beat ≠ confirm. No least-bad. Not trading advice.*
