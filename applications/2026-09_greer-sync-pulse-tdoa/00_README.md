# Greer-style sync-pulse TDOA — reading guide

**Application ID:** `2026-09_greer-sync-pulse-tdoa`  
**Opened:** 2026-09-05  

**MULTIPATH1 Soften** on the record (Kill not triggered). **#0 geometry HARDEN** on the record. First-pulse fog peek **ADMITTED** (C1/C2/C3 SUCCEED). Founder **CLAIM LOCK** recorded. Provisional **sim X = 0.50 m** stays **LOCKED** with **NLOS scope annotation** (**median**-not-p90; 1 ns p90 ≈ **1.16 m**). **PARK** hardware **X**. Next pulse (**not this fold**): **sync-imperfection**.

**NEW Amb:** Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA (contrast prior art [US10135667B1](https://patents.google.com/patent/US10135667B1/en) — method practice / explore the idea; **not** copy claims for product).

This is **not** a locator. This is **not** a trained map. Training is **not** established. This is **not** RF fingerprinting. This is **not** fingerprint rescue. This is **not** GPS / DGPS as the mobile fix. This is **not** skill-met. This is **not** rithm. This is **not** a product claim copied from the named patent. Peek succeed / #0 HARDEN / MULTIPATH1 Soften is **not** claim clearance and is **not** a multipath-robust 0.50 m. Hardware **X** is **not** locked. **X** is **not** a p90 bar. Sync-imperfection is **admitted** and is **not** this fold. Lab **HOLD** on running it here.

The cell-tower Amb (`2026-09_cell-tower-geometry`) is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED**. This app does **not** reopen either.

## Claim (Founder lock — replace any prior draft wording)

On a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) can recover mobile position with median error ≤ **X** on a held-out path inside a GPS-denied box — **without RF fingerprint training**.

**X:** provisional **sim X = 0.50 m** (Operator #0; MULTIPATH1 Soften keeps it **LOCKED** with **NLOS scope** — LOS + mild / intermittent NLOS only; **median-not-p90**). **Hardware X PARKED**.

## Intent / reverse framing

Not opportunistic cellular fingerprinting. Not GPS-crowdsourced mast maps. Not using GPS/DGPS as the phone / mobile fix. This Amb asks whether dedicated synchronized reference nodes plus mobile TDOA can place a receiver inside a GPS-denied box on a laptop-feasible sim/prototype path.

**Prior-art contrast (bibliographic only):** US10135667B1, Kerry L. Greer, *System and method for increased indoor position tracking accuracy* (2018). Named so the idea can be practiced / explored under this method. **Do not** copy patent claims for a product. **Do not** paste claim language into this folder.

## Honest fog (named; C1–C3 gated)

1. **Spectrum / hardware vs sim-only.** **C1 SUCCEED** — sim-only path poseable. **#0** locked **sim X = 0.50 m**. Hardware **X PARKED**.
2. **Clock resolution.** **C2 SUCCEED** — provisional ideal simultaneous TX + Δt → Δd = c·Δt (~0.3 m/ns). **#0 and MULTIPATH1 assumed** that idealization. Leftover open until **sync-imperfection** (next pulse; not this fold).
3. **Multipath.** **C3 SUCCEED** — scoring poseable with GPS refs-only. **MULTIPATH1 Soften** — poseable under LOS + mild / intermittent NLOS; **not** poseable under strong persistent multipath with frozen Chan alone. Do **not** claim a multipath-robust 0.50 m. **No** fingerprint rescue.

## Eval rules (locked at peek)

- GPS / DGPS, if used at all, **place and time the reference nodes only**. They are **never** the mobile fix.
- Estimator class for the live path is ≥3-reference **simultaneous-sync TDOA** on a **sim-only** path (frozen Chan 1994). **No** RF fingerprint training. **No** fingerprint rescue.
- Path must stay **laptop-feasible** sim. Hardware **X** is **PARKED**.
- Metric: **median** error on a held-out path inside a GPS-denied box. Provisional **sim X = 0.50 m** (**NLOS-scoped**; **median-not-p90**; p90 ≈ 1.16 m @ 1 ns LOS is honesty, not the bar). Hardware **X** stays parked.
- This is **not** a fingerprinting claim and **not** a patent-product claim.

## #0 (gated)

Operator **ADMIT HARDEN**. Frozen Chan (1994) 2D WLS; numpy; 5 refs; L-path 101 samples; 40 MC; seed 20260905. `σ_t` = 1 ns → median **0.361 m** (`σ_d` ≈ 0.300 m); **p90 ≈ 1.16 m**. `σ_t` = 3 ns → median **1.081 m**. Zero-noise ~1e-14 m. 0 failures. Geometry is **not** the bottleneck under ideal sync + Gaussian Δt. **X is median-not-p90.** See [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md).

## MULTIPATH1 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered. Frozen Chan 1994; `σ_t` = 1 ns; positive range-bias; same refs / L-path as #0. Baseline **0.364 m**. `random_k=1` `b=0.5` → **0.476 m**. `epoch_f=0.25` `b=1` → **0.452 m**. Strong persistent `b≥1–2 m` → **0.73–4.7+ m** (not poseable with Chan alone). p90 ≈ **1.16 m** @ 1 ns LOS. **X = 0.50 m** remains **LOCKED**, NLOS-scoped. See [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md).

## Next pulse (admitted; not this fold)

**Sync-imperfection** — still no RF / ML; no fingerprint rescue; GPS/DGPS refs only, never the mobile fix. Fog peek + later gates: [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md). **No sync-imperfection run on this fold.**

## Reading order

1. [`STATUS.md`](STATUS.md) — where we are
2. [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) — the open / parked / hardened / Soften lines
3. [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md) — MULTIPATH1 gated metrics
4. [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md) — what MULTIPATH1 taught
5. [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md) — #0 gated metrics
6. [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md) — what #0 taught
7. [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md) — Lab fog peek + later gates
8. [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md) — what the peek taught
9. [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md) — what the last string taught
10. [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) — decision log
11. [`notes.md`](notes.md) — one-line pointer
