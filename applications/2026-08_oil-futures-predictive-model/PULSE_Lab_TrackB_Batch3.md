# Pulse record — Lab Track B invent→test batch 3 (docs only)

**Date:** 2026-09-05  
**Application:** `2026-08_oil-futures-predictive-model`  
**Object:** Track B (EIA spot 21-day vs continuation) — **not** R-F-SKILL / F-CC futures  
**Protocol:** `Lock_Hunt_Spot_Trend`  
**Series:** FRED EIA spot WTI `DCOILWTICO` / Brent `DCOILBRENTEU`  
**Discovery:** n=500, dates **≤2023-08-21**, vs continuation  
**Continuation:** WTI **0.5080** / Brent **0.5060**  
**Confirm:** windows **250 / 500 / 750**, **survivors only**  
**VIX vehicle:** FRED **VIXCLS**  
**Gatekeeper:** **REJECT / burn** VIX / THRESH / SKEW and C-SPOT-SEAS MOY-DIR (both boards) plus WTI MOY-CONT (killed disc). **Scoped confirm survivor:** Brent **H-SPOT-MOY-CONT** — **not** skill-met, **not** C-SPOT-SEAS established, **not** WTI-met. Scripts **not** on master.

---

## 0. Plain-language framing

**What this is:** The locked cite pack for Lab invent→test batch 3. Four new spot classes were scored against continuation. VIX-ALIGN repeated the DGS10-ALIGN pattern (strong discovery, then confirm kill). One horse — Brent month-continuation (**H-SPOT-MOY-CONT**) — **survived confirm** under the protocol. That is a **scoped confirm pass**, not a parent-claim clearance.

**What this settles:** VIX / THRESH / SKEW — **burned** (SKEW UPFRAC ≡ UPFRAC-GATE; one family). C-SPOT-SEAS is **not** established (MOY-DIR confirm-killed both boards; WTI MOY-CONT killed at discovery). Brent MOY-CONT is **not** a null — record it as a scoped confirm pass. Burned-class invent queue is **empty**. Live scoped horse: **Brent H-SPOT-MOY-CONT**. Spot-trend skill is still **not established**. WTI-met ≠ Brent-met. Amb ≠ clearance. Not a trade.

**What this is not:** Not an R-F-SKILL pulse. Not a futures horse. Not Track B skill-met. Not C-SPOT-SEAS class-met. Not WTI-met. Not a reason to revive FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, DXY, SHORT, VOTE, RATES, SPREAD, VIX, THRESH, or SKEW. Not a reason to treat Brent MOY-CONT as burned.

---

## 1. Locked cite — burns

| Class | Horse | WTI | Brent |
|-------|-------|-----|-------|
| **C-SPOT-VIX** | VIX-INV | burned both boards | burned both boards |
| **C-SPOT-VIX** | VIX-ALIGN | disc strong → confirm kill (same pattern as DGS10-ALIGN) | disc strong → confirm kill (same pattern as DGS10-ALIGN) |
| **C-SPOT-THRESH** | ABS05 | disc survivor → confirm kill | killed disc |
| **C-SPOT-THRESH** | ABS10 | burned | killed disc |
| **C-SPOT-SKEW** | UPFRAC | burned (definitionally ≡ UPFRAC-GATE; one family) | burned (definitionally ≡ UPFRAC-GATE; one family) |
| **C-SPOT-SKEW** | UPFRAC-GATE | burned (≡ UPFRAC; one family) | burned (≡ UPFRAC; one family) |
| **C-SPOT-SEAS** | MOY-DIR | confirm kill | confirm kill |
| **C-SPOT-SEAS** | MOY-CONT | killed disc | — see scoped survivor below — |

**Still burned (prior Track B):** FLIP/REV, INV, CROSS, LOGIT, MAG, PERSIST, BREAK, DXY, SHORT, VOTE, RATES, SPREAD.

---

## 2. Locked cite — scoped confirm survivor (not skill-met)

| Horse | Board | last_500 | last_250 | last_750 | Gatekeeper |
|-------|-------|----------|----------|----------|------------|
| **H-SPOT-MOY-CONT** | **Brent only** | **0.5440 > 0.5100** | **0.5600 > 0.5200** | **0.5253 > 0.5147** (small margin; still strict beat) | **scoped confirm pass** |

**Do not claim:** Track B spot-trend skill established. C-SPOT-SEAS established. WTI-met. Parent slogan cleared.

**Do not burn:** Brent MOY-CONT as a null.

**Do record:** scoped confirm pass under `Lock_Hunt_Spot_Trend`. Amb ≠ clearance. Not a trade.

---

## 3. Notes

- Discovery n=500 ≤2023-08-21; cont WTI=0.5080 Brent=0.5060; confirm 250/500/750 survivors only.
- VIX vehicle is **VIXCLS**. VIX-ALIGN disc-strong-then-confirm-kill = same pressure point as DGS10-ALIGN.
- UPFRAC and UPFRAC-GATE are definitionally equivalent — burned as one family.
- C-SPOT-SEAS is **not** class-met: MOY-DIR failed confirm both boards; WTI MOY-CONT failed discovery.
- WTI-met ≠ Brent-met. First scoped confirm ≠ slogan clearance.
- Burned-class invent queue is **empty**. Live scoped horse: Brent **H-SPOT-MOY-CONT**.
- Scripts / hunt code **not** merged.
- Lab may invent **new** classes after this fold. Must **not** revive the burned set. Must **not** treat Brent MOY-CONT as a null.

---

*Docs only. Track B ≠ F-SKILL. Scoped confirm ≠ skill-met. Discovery beat ≠ confirm. No least-bad. Not trading advice.*
