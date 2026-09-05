# Greer-style sync-pulse TDOA — reading guide

**Application ID:** `2026-09_greer-sync-pulse-tdoa`  
**Opened:** 2026-09-05  

**First-pulse fog peek ADMITTED.** Founder **CLAIM LOCK** recorded. **C1 SUCCEED.** **C2 SUCCEED.** **C3 SUCCEED.** **LOCK:** sim-only path; provisional **X = sim-geometry first**. **PARK** hardware **X**.

**NEW Amb:** Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA (contrast prior art [US10135667B1](https://patents.google.com/patent/US10135667B1/en) — method practice / explore the idea; **not** copy claims for product).

This is **not** a locator. This is **not** a trained map. Training is **not** established. This is **not** RF fingerprinting. This is **not** GPS / DGPS as the mobile fix. This is **not** skill-met. This is **not** rithm. This is **not** a product claim copied from the named patent. Peek succeed is **not** claim clearance. Numeric sim **X** is **not** frozen. Next pulse (**#0 geometry-bottleneck sim**) is **admitted** and is **not** this fold. Lab **HOLD** on running #0 here.

The cell-tower Amb (`2026-09_cell-tower-geometry`) is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED**. This app does **not** reopen either.

## Claim (Founder lock — replace any prior draft wording)

On a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) can recover mobile position with median error ≤ **X** on a held-out path inside a GPS-denied box — **without RF fingerprint training**.

**X:** sim-geometry first (provisional class lock). Numeric sim **X** frozen only after scored pulse **#0**. Hardware **X PARKED**.

## Intent / reverse framing

Not opportunistic cellular fingerprinting. Not GPS-crowdsourced mast maps. Not using GPS/DGPS as the phone / mobile fix. This Amb asks whether dedicated synchronized reference nodes plus mobile TDOA can place a receiver inside a GPS-denied box on a laptop-feasible sim/prototype path.

**Prior-art contrast (bibliographic only):** US10135667B1, Kerry L. Greer, *System and method for increased indoor position tracking accuracy* (2018). Named so the idea can be practiced / explored under this method. **Do not** copy patent claims for a product. **Do not** paste claim language into this folder.

## Honest fog (named; C1–C3 gated)

1. **Spectrum / hardware vs sim-only.** **C1 SUCCEED** — sim-only path poseable; hardware not required to name a sim **X**. Hardware **X PARKED**.
2. **Clock resolution.** **C2 SUCCEED** — provisional ideal simultaneous TX + Δt → Δd = c·Δt (~0.3 m/ns). Still not a locator.
3. **Multipath.** **C3 SUCCEED** — scoring poseable with GPS refs-only. Multipath **stays on fog**. A GPS-denied box is a hard radio environment.

## Eval rules (locked at peek)

- GPS / DGPS, if used at all, **place and time the reference nodes only**. They are **never** the mobile fix.
- Estimator class for the live path is ≥3-reference **simultaneous-sync TDOA** on a **sim-only** path. **No** RF fingerprint training.
- Path must stay **laptop-feasible** sim. Hardware **X** is **PARKED**.
- Metric: median error on a held-out path inside a GPS-denied box. **X** class = sim-geometry first. Numeric sim **X** stays unset until after scored pulse **#0**.
- This is **not** a fingerprinting claim and **not** a patent-product claim.

## Next pulse (admitted; not this fold)

**#0 geometry-bottleneck sim** — laptop; no RF; frozen textbook multilateration only; no trained estimator invent; no fingerprint; GPS/DGPS refs only, never the mobile fix. Numeric sim **X** frozen only after that scored pulse. See [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md). **No #0 run on the peek fold.**

## Reading order

1. [`STATUS.md`](STATUS.md) — where we are
2. [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) — the open / parked / hardened lines
3. [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md) — Lab peek + Operator gate
4. [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md) — what the peek taught
5. [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md) — what the last string taught
6. [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) — decision log
7. [`notes.md`](notes.md) — one-line pointer
