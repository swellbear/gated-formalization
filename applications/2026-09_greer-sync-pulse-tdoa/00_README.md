# Greer-style sync-pulse TDOA — reading guide

**Application ID:** `2026-09_greer-sync-pulse-tdoa`  
**Opened:** 2026-09-05  

**#0 geometry HARDEN** on the record. First-pulse fog peek **ADMITTED** (C1/C2/C3 SUCCEED). Founder **CLAIM LOCK** recorded. Provisional **sim X = 0.50 m**. **PARK** hardware **X**. Lab **HOLD**.

**NEW Amb:** Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA (contrast prior art [US10135667B1](https://patents.google.com/patent/US10135667B1/en) — method practice / explore the idea; **not** copy claims for product).

This is **not** a locator. This is **not** a trained map. Training is **not** established. This is **not** RF fingerprinting. This is **not** GPS / DGPS as the mobile fix. This is **not** skill-met. This is **not** rithm. This is **not** a product claim copied from the named patent. Peek succeed / #0 HARDEN is **not** claim clearance. Hardware **X** is **not** locked. Lab **HOLD** until Founder / Operator opens a sync-imperfection or multipath-bias pulse (still no RF / ML).

The cell-tower Amb (`2026-09_cell-tower-geometry`) is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED**. This app does **not** reopen either.

## Claim (Founder lock — replace any prior draft wording)

On a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) can recover mobile position with median error ≤ **X** on a held-out path inside a GPS-denied box — **without RF fingerprint training**.

**X:** provisional **sim X = 0.50 m** (Operator #0; 1 ns median + margin). **Hardware X PARKED** until a sync / multipath gate.

## Intent / reverse framing

Not opportunistic cellular fingerprinting. Not GPS-crowdsourced mast maps. Not using GPS/DGPS as the phone / mobile fix. This Amb asks whether dedicated synchronized reference nodes plus mobile TDOA can place a receiver inside a GPS-denied box on a laptop-feasible sim/prototype path.

**Prior-art contrast (bibliographic only):** US10135667B1, Kerry L. Greer, *System and method for increased indoor position tracking accuracy* (2018). Named so the idea can be practiced / explored under this method. **Do not** copy patent claims for a product. **Do not** paste claim language into this folder.

## Honest fog (named; C1–C3 gated)

1. **Spectrum / hardware vs sim-only.** **C1 SUCCEED** — sim-only path poseable. **#0** locked **sim X = 0.50 m**. Hardware **X PARKED**.
2. **Clock resolution.** **C2 SUCCEED** — provisional ideal simultaneous TX + Δt → Δd = c·Δt (~0.3 m/ns). **#0 assumed** that idealization. Sync-imperfection is **not** opened.
3. **Multipath.** **C3 SUCCEED** — scoring poseable with GPS refs-only. **#0 did not inject** multipath. Multipath **stays on fog**.

## Eval rules (locked at peek)

- GPS / DGPS, if used at all, **place and time the reference nodes only**. They are **never** the mobile fix.
- Estimator class for the live path is ≥3-reference **simultaneous-sync TDOA** on a **sim-only** path. **No** RF fingerprint training.
- Path must stay **laptop-feasible** sim. Hardware **X** is **PARKED**.
- Metric: median error on a held-out path inside a GPS-denied box. Provisional **sim X = 0.50 m**. Hardware **X** stays parked.
- This is **not** a fingerprinting claim and **not** a patent-product claim.

## #0 (gated)

Operator **ADMIT HARDEN**. Frozen Chan (1994) 2D WLS; numpy; 5 refs; L-path 101 samples; 40 MC; seed 20260905. `σ_t` = 1 ns → median **0.361 m** (`σ_d` ≈ 0.300 m). `σ_t` = 3 ns → median **1.081 m**. Zero-noise ~1e-14 m. 0 failures. Geometry is **not** the bottleneck under ideal sync + Gaussian Δt. See [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md).

## Next pulse (HOLD)

Lab **HOLD**. Do **not** invent until Founder / Operator opens **sync-imperfection** or **multipath-bias**. Still **no RF / ML**. Fog peek record: [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md).

## Reading order

1. [`STATUS.md`](STATUS.md) — where we are
2. [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) — the open / parked / hardened lines
3. [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md) — #0 gated metrics
4. [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md) — what #0 taught
5. [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md) — Lab fog peek + Operator gate
6. [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md) — what the peek taught
7. [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md) — what the last string taught
8. [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) — decision log
9. [`notes.md`](notes.md) — one-line pointer
