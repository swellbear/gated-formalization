# Pulse record — Lab Track B Deep1 P1/P2 (Amb constraints only; not skill)

**Date:** 2026-09-05  
**Application:** `2026-08_oil-futures-predictive-model`  
**Object:** Track B (EIA spot 21-day vs continuation) — **not** R-F-SKILL / F-CC futures  
**Protocol:** `Lock_Hunt_Spot_Trend`  
**Horse:** Brent **H-SPOT-MOY-CONT** (scoped confirm + **FRAGILE**; **not** skill-met)  
**Gatekeeper:** **ADMIT as Amb constraint only** — **P1** C-SPOT-CUTOFF-SWEEP and **P2** C-SPOT-VEHICLE. **Not** skill-met. **Not** an elevation. **Not** a null burn. Scripts **not** on master.

---

## 0. Plain-language framing

**What this is:** Deeper-solve probes on the already-scoped Brent month-continuation horse. P1 asks whether the FRED confirm is a single-cutoff artifact. P2 asks whether the FRED packaging is the vehicle. Both are **Amb constraints**, not a skill pass.

**What this settles:** Among {2018, 2020, 2023} the FRED Brent MOY-CONT confirm is **not** a single-cutoff artifact; 2015 fails discovery. The 2023 leave-one-year-out fail is **not** FRED-only packaging. FRED-scoped confirm does **not** fully replicate on EIA (last-750 flips) — vehicle-sensitive at last-750. Multi-cutoff confirm is partly redundant (FULL-file last-N windows overlap). Batch-4 LOY fragility is **untouched** by the cutoff sweep alone. Still **not** skill-met. Does **not** elevate. Does **not** null-burn. P3=B held (no new all-day beat-continuation invent — park fold is #32). Open residual remains fragility/vehicle Amb of Brent MOY-CONT (scoped+FRAGILE).

**What this is not:** Not an R-F-SKILL pulse. Not Track B skill-met. Not an elevation of Brent MOY-CONT. Not a reason to treat Brent MOY-CONT as burned. Not a new direction class. Not a reason to revive burned horses.

---

## 1. P1 C-SPOT-CUTOFF-SWEEP — ADMIT as Amb constraint only

**Pre-registered cutoffs:** {2015-08-21, 2018-08-21, 2020-08-21, 2023-08-21}  
**Horse:** H-SPOT-MOY-CONT  
**Primary:** FRED Brent  
**WTI:** info-only

| Cutoff | Discovery | Confirm (FULL last-500 / 250 / 750) |
|--------|-----------|-------------------------------------|
| 2015-08-21 | **KILL** (0.494≤0.540) | — |
| 2018-08-21 | survive | **SURVIVE** |
| 2020-08-21 | survive | **SURVIVE** |
| 2023-08-21 | survive | **SURVIVE** |

- Brent confirm-survive: **3/4**.
- WTI info-only confirm-survive: **0/4**.
- Honesty: confirm windows are FULL-file last-N and **overlap across cutoffs** ⇒ multi-cutoff confirm is **partly redundant**, not independent eras.
- LOY fragility from batch 4 is **untouched** by this sweep alone.

**Amb tightened:** among {2018, 2020, 2023} the FRED Brent MOY-CONT confirm is **not** a single-cutoff artifact; 2015 fails discovery.

**Still NOT skill-met. Does NOT elevate. Does NOT null-burn.**

---

## 2. P2 C-SPOT-VEHICLE — ADMIT as Amb constraint only

- EIA v2 `petroleum/pri/spt` DEMO_KEY OK (legacy 404).
- EIA Brent MOY-CONT confirm: last-500 **Y**, last-250 **Y**, last-750 **N** (0.514667 vs cont 0.517333) ⇒ **all-windows FAIL**.
- EIA LOY after 2023-08-21: **2023 FAIL** 0.352 vs 0.582; 2024–26 beat. Replicates batch-4 FRED 2023 LOY fail.

**Amb tightened:** 2023 LOY fail is **NOT** FRED-only packaging. But FRED-scoped confirm does **NOT** fully replicate on EIA (last-750 flips) ⇒ **vehicle-sensitive at last-750**.

**Still NOT skill-met. Does NOT elevate. Does NOT null-burn.**

---

## 3. Disposition

- **P3=B held** (Founder/user; park fold is #32): no new all-day beat-continuation invent.
- Open residual: fragility/vehicle Amb of Brent MOY-CONT (scoped+FRAGILE).
- P1 and P2 probes **completed** (Amb constraints recorded).
- Lab held from new direction classes unless Founder locks a new named missing constraint.

---

## 4. Notes

- FRED Brent remains primary. WTI is info-only on the cutoff sweep (0/4 confirm-survive).
- Confirm-window overlap across cutoffs is an honesty constraint, not a second independent-era test.
- EIA last-750 flip does **not** retract the FRED scoped confirm; it marks vehicle-sensitivity.
- EIA 2023 LOY fail (0.352 vs 0.582) does **not** retract the FRED scoped confirm; it tightens the “not FRED-only” Amb on the already-recorded 2023 fail.
- Scripts / hunt code **not** merged.
- Do **not** revive burned direction classes. Do **not** promote Brent MOY-CONT. Do **not** treat it as a null.

---

*Docs only. Track B ≠ F-SKILL. Amb constraint ≠ skill-met. FRAGILE ≠ elevated. Not a null burn. Not trading advice.*
