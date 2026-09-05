# Greer-style sync-pulse TDOA — reading guide

**Application ID:** `2026-09_greer-sync-pulse-tdoa`  
**Opened:** 2026-09-05  

**JOINT1 Soften** on the record (Kill **not** triggered; Aim A **partial**). **GEOM0 HARDEN**, **MULTIPATH1 Soften**, and prior **SYNC1 Soften** (Chan-alone) still stand. First-pulse fog peek **ADMITTED** (C1/C2/C3 SUCCEED). Founder **CLAIM LOCK** recorded. Provisional **sim X = 0.50 m** remains, scoped to **`σ_sync ≲ 3 ns` under JOINT1 + mild NLOS** (**median**-not-p90; 1 ns p90 ≈ **1.16 m**). **Not** multipath-robust. **Not** drift-robust. **PARK** hardware **X**. Next (**not this fold**): **DRIFT1**.

**NEW Amb:** Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA. Owner-requested **collaboration framing** with [US10135667B1](https://patents.google.com/patent/US10135667B1/en) (bibliographic; custom-beacon substrate, **not** a carrier-mast Amb). **No claim-language copy.**

This is **not** a locator. This is **not** a trained map. Training is **not** established. This is **not** RF fingerprinting. This is **not** fingerprint rescue. This is **not** GPS / DGPS as the mobile fix. This is **not** skill-met. This is **not** rithm. This is **not** a product claim copied from the named patent. Soften / HARDEN is **not** claim clearance and is **not** a multipath-robust or drift-robust 0.50 m. Hardware **X** is **not** locked. **X** is **not** a p90 bar. Do **not** invent fingerprint / ML / RF to rescue loose sync or drift.

The cell-tower Amb (`2026-09_cell-tower-geometry`) is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED**. This app does **not** reopen either.

## Claim (Founder lock — replace any prior draft wording)

On a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) can recover mobile position with median error ≤ **X** on a held-out path inside a GPS-denied box — **without RF fingerprint training**.

**X:** provisional **sim X = 0.50 m** remains (**median** @ 1 ns RX noise). Honest only under **mild NLOS + `σ_sync ≲ 3 ns` under JOINT1** (path-shared / fixed_trial). **X is median-not-p90** (1 ns p90 ≈ **1.16 m**). **Hardware X PARKED**. **Not** drift-robust.

## Intent / reverse framing

Not opportunistic cellular fingerprinting. Not GPS-crowdsourced mast maps. Not using GPS/DGPS as the phone / mobile fix. This Amb asks whether dedicated synchronized reference nodes plus mobile TDOA can place a receiver inside a GPS-denied box on a laptop-feasible sim/prototype path.

**Collaboration framing (owner-requested; bibliographic only):** US10135667B1, Kerry L. Greer, *System and method for increased indoor position tracking accuracy* (2018). Named as a custom-beacon substrate for collaboration, **not** a carrier-mast Amb. **Do not** copy patent claims. **Do not** paste claim language into this folder.

## Honest fog (named; C1–C3 gated)

1. **Spectrum / hardware vs sim-only.** **C1 SUCCEED** — sim-only path poseable. **#0** locked **sim X = 0.50 m**. Hardware **X PARKED**.
2. **Clock / sync.** **C2 SUCCEED** (story named). **#0 and MULTIPATH1 assumed** ideal sync. **SYNC1 Soften** — Chan-alone bar survives only at `σ_sync ≲ 0.3 ns` (median **0.382 m**); 1 ns scrapes **0.513 m**. **JOINT1 Soften** — path-shared joint clocks restore X under fixed_trial `σ_sync ≲ 3 ns` (**0.231 m** @ 1 ns; **0.439 m** @ 3 ns). 10 ns fails (**1.816 m**). Drift 3 ns/path still fails (JOINT1 **0.919 m**).
3. **Multipath.** **C3 SUCCEED** — scoring poseable. **MULTIPATH1 Soften** — poseable under LOS + mild / intermittent NLOS; **not** poseable under strong persistent multipath with frozen Chan alone. Do **not** claim a multipath-robust 0.50 m. **No** fingerprint rescue.

Remaining live leftover includes **drift** (shared-τ vs ramp) + **multipath** (not hyperbolic geometry).

## Eval rules (locked at peek)

- GPS / DGPS, if used at all, **place and time the reference nodes only**. They are **never** the mobile fix.
- Estimator class for the live path is ≥3-reference **simultaneous-sync TDOA** on a **sim-only** path (frozen Chan 1994; JOINT1 adds path-shared shared-τ). **No** RF fingerprint training. **No** fingerprint rescue.
- Path must stay **laptop-feasible** sim. Hardware **X** is **PARKED**.
- Metric: **median** error on a held-out path inside a GPS-denied box. Provisional **sim X = 0.50 m** (**JOINT1-sync + NLOS-scoped**; **median-not-p90**; p90 ≈ 1.16 m @ 1 ns LOS is honesty, not the bar). Hardware **X** stays parked.
- This is **not** a fingerprinting claim and **not** a patent-product claim.

## #0 (gated)

Operator **ADMIT HARDEN**. Frozen Chan (1994) 2D WLS; numpy; 5 refs; L-path 101 samples; 40 MC; seed 20260905. `σ_t` = 1 ns → median **0.361 m** (`σ_d` ≈ 0.300 m); **p90 ≈ 1.16 m**. `σ_t` = 3 ns → median **1.081 m**. Zero-noise ~1e-14 m. 0 failures. Geometry is **not** the bottleneck under ideal sync + Gaussian Δt. **X is median-not-p90.** See [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md).

## MULTIPATH1 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered. Frozen Chan 1994; `σ_t` = 1 ns; positive range-bias; same refs / L-path as #0. Baseline **0.364 m**. `random_k=1` `b=0.5` → **0.476 m**. `epoch_f=0.25` `b=1` → **0.452 m**. Strong persistent `b≥1–2 m` → **0.73–4.7+ m** (not poseable with Chan alone). p90 ≈ **1.16 m** @ 1 ns LOS. **X = 0.50 m** remains **LOCKED**, NLOS-scoped. See [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md).

## SYNC1 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered. Frozen Chan 1994; `σ_t` = 1 ns; same refs / L-path. `σ_sync ≲ 0.3 ns` → median **0.382 m** ≤ X. `σ_sync` = 1 ns scrapes **0.513 m**. `≥ 3 ns` / 3 ns path drift **fails X**. Chan-alone window stays near-ideal. See [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md).

## JOINT1 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered. Aim A **partial**. Path-shared joint clocks (shared-τ) under **fixed_trial** `σ_sync`. **0.231 m** @ 1 ns; **0.439 m** @ 3 ns ≤ X. Chan scrape at 1 ns **restored**. `σ_sync` = 10 ns fails (**1.816 m**). Drift 3 ns/path still breaks X (JOINT1 **0.919 m** — shared-τ misspecified vs ramp). Named sync Soften budget **widens** to **`σ_sync ≲ 3 ns` under JOINT1** + prior mild-NLOS. **Not** multipath-robust. **Not** drift-robust. See [`SCORE_JOINT1.md`](SCORE_JOINT1.md).

## Next (DRIFT1 — not this fold)

**DRIFT1** pulse is **named**, not run here. Still **no RF / ML**. Fog peek + later gates: [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md).

## Reading order

1. [`STATUS.md`](STATUS.md) — where we are
2. [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) — the open / parked / hardened / Soften lines
3. [`SCORE_JOINT1.md`](SCORE_JOINT1.md) — JOINT1 gated metrics
4. [`DIGESTION_JOINT1.md`](DIGESTION_JOINT1.md) — what JOINT1 taught
5. [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md) — SYNC1 gated metrics (prior Soften)
6. [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md) — what SYNC1 taught
7. [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md) — MULTIPATH1 gated metrics (prior Soften)
8. [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md) — what MULTIPATH1 taught
9. [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md) — #0 gated metrics
10. [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md) — what #0 taught
11. [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md) — Lab fog peek + later gates
12. [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md) — what the peek taught
13. [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md) — what the last string taught
14. [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) — decision log
15. [`notes.md`](notes.md) — one-line pointer
