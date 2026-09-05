# Pulse record — Lab Track B P4 LOY2023 HARDEN (Amb constraint only; not skill)

**Date:** 2026-09-05  
**Application:** `2026-08_oil-futures-predictive-model`  
**Object:** Track B (EIA spot 21-day vs continuation) — **not** R-F-SKILL / F-CC futures  
**Protocol:** `Lock_Hunt_Spot_Trend`  
**Horse:** Brent **H-SPOT-MOY-CONT** (scoped confirm + **FRAGILE**; **not** skill-met)  
**Gatekeeper:** **ADMIT HARDEN as Amb constraint only** — **P4** C-SPOT-LOY2023-DECOMP. **Not** skill-met. **Not** an elevation. **Not** a null burn. **Not** RESTATE. Scripts **not** on master.

---

## 0. Plain-language framing

**What this is:** The one allowed year-fragility probe after P1/P2. Decompose the already-recorded 2023 leave-one-year-out fail (FRED Brent primary; EIA mirror). This is an **Amb HARDEN**, not a skill pass.

**What this settles:** On FRED Brent, eligible 2023-08-22..2023-12-31 (n=91), the 2023 fail is **not** thin-stub-only and **not** single-month-only: aggregate FAIL (0.374 vs 0.582); both halves FAIL; 3/4 months not-strict-beat. Honesty: Oct is the blow-up; Nov/Dec are ties (MOY-CONT ≡ continuation); Sep beats — still meets pre-reg HARDEN. Binomial cannot claim beat (p_gt≈1.0); horse below cont (p_lt≈4.8e-5). EIA shows the same HARDEN pattern. Still **not** skill-met. Does **not** elevate. Does **not** null-burn. P3=B held. Lab one-probe allotment **DONE**. Invent held unless Founder locks a new named missing constraint. **NOT RESTATE** (no pause-for-restate escalate from this gate alone). Open residual remains fragility/vehicle Amb of Brent MOY-CONT (scoped+FRAGILE), now with year-stability HARDENED toward “2023 really broke year-stability.”

**What this is not:** Not an R-F-SKILL pulse. Not Track B skill-met. Not an elevation of Brent MOY-CONT. Not a reason to treat Brent MOY-CONT as burned. Not a new direction class. Not a reason to revive burned horses. Not a restate escalate.

---

## 1. P4 C-SPOT-LOY2023-DECOMP — ADMIT HARDEN as Amb constraint only

**Window:** FRED Brent primary; eligible dates **2023-08-22..2023-12-31**; **n=91**. EIA mirror also run.

### FRED primary

| Slice | Horse vs cont | Read |
|-------|---------------|------|
| Aggregate (n=91) | **0.374 vs 0.582** | **FAIL** |
| Half A (n=45) | **0.222 vs 0.533** | **FAIL** |
| Half B (n=46) | **0.522 vs 0.630** | **FAIL** |

**Months:**
- Sep **BEATS** 0.333>0.143
- Oct **FAIL** 0.136 vs 0.864
- Nov **TIE** 0.955=0.955 (**FAIL** strict)
- Dec **TIE** 0.158=0.158 (**FAIL** strict)

→ **3/4 months not-strict-beat**

**Binomial:** p_gt≈1.0 (cannot claim beat); p_lt≈4.8e-5 (horse below cont)

### EIA mirror

Same HARDEN pattern: aggregate **0.352 vs 0.582**; both halves fail; 3/4 months.

**Amb tightened:** HARDEN toward “2023 really broke year-stability” (not thin-stub-only / not single-month-only). Honesty: Oct is the blow-up; Nov/Dec are ties (MOY-CONT ≡ continuation); Sep beats — still meets pre-reg HARDEN.

**Still NOT skill-met. Does NOT elevate. Does NOT null-burn.**

---

## 2. Disposition

- **P3=B held** (Founder/user; park fold is #32): no new all-day beat-continuation invent.
- P1 and P2 Amb constraints remain on record (cutoff/vehicle).
- Open residual: fragility/vehicle Amb of Brent MOY-CONT (scoped+FRAGILE), with year-stability **HARDENED** toward “2023 really broke year-stability.”
- Lab **one-probe allotment DONE**. Invent held unless Founder locks a new named missing constraint.
- **NOT RESTATE** — no pause-for-restate escalate from this gate alone.

---

## 3. Notes

- FRED Brent remains primary. EIA is the mirror (same HARDEN pattern).
- Batch-4 already recorded the 2023 LOY fail (0.374 vs 0.582, n=91). This probe **decomposes** that fail; it does **not** retract the scoped confirm and does **not** burn the horse as a null.
- Month-level Sep beat does **not** rescue year-stability. Oct blow-up plus late ties still meet pre-reg HARDEN.
- Nov/Dec ties mean MOY-CONT ≡ continuation on those months — **FAIL** under strict beat. Not a keep.
- Scripts / hunt code **not** merged.
- Do **not** revive burned direction classes. Do **not** promote Brent MOY-CONT. Do **not** treat it as a null.

---

*Docs only. Track B ≠ F-SKILL. Amb HARDEN ≠ skill-met. FRAGILE ≠ elevated. Not a null burn. Not RESTATE. Not trading advice.*
