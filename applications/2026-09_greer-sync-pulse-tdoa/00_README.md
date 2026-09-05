# Greer-style sync-pulse TDOA — reading guide

**Application ID:** `2026-09_greer-sync-pulse-tdoa`  
**Opened:** 2026-09-05  

**REOPEN** (solve framing — **not** park forever). **Solve-target:** sync fragility. **(A)** named Soften beyond 0.3 ns / drift without fingerprint / ML **or (B)** detect from measurements alone and Soften / widen **X** / refuse a point fix. Baseline standing **preserved:** **GEOM0 HARDEN**; **MULTIPATH1 Soften** (mild-NLOS); **SYNC1 Soften** (`σ_sync ≲ 0.3 ns`). First-pulse fog peek **ADMITTED** (C1/C2/C3 SUCCEED). Founder **CLAIM LOCK** recorded. Provisional **sim X = 0.50 m** remains, scoped to **near-ideal sync + NLOS** (**median**-not-p90; 1 ns p90 ≈ **1.16 m**). **PARK** hardware **X**. Lab **HOLD lifted for the invent board only.** Multipath wave-2 after the sync string. **Not** a remake of commercial RTLS.

**NEW Amb:** Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA. **Collaboration-with-owner:** Greer (patent owner, [US10135667B1](https://patents.google.com/patent/US10135667B1/en)) **requested** they solve his problem. Deliverable is **for him by request**, **not** an unsolicited write-up. **Do not** invent product claim-language copy. Founder **may re-aim** when Greer’s success criteria arrive.

This is **not** a locator. This is **not** a trained map. Training is **not** established. This is **not** RF fingerprinting. This is **not** fingerprint rescue. This is **not** GPS / DGPS as the mobile fix. This is **not** skill-met. This is **not** rithm. This is **not** a product claim copied from the named patent. This is **not** invented product claim-language. This is **not** an unsolicited write-up. This is **not** a remake of commercial RTLS. Soften / HARDEN / REOPEN is **not** claim clearance and is **not** a multipath-robust 0.50 m. Hardware **X** is **not** locked. **X** is **not** a p90 bar. Lab HOLD is lifted **only** for the (A)/(B) invent board. Do **not** invent fingerprint / ML / RF to rescue loose sync. Do **not** start multipath wave-2 until the sync string clears or parks. Sync-fragility solve-target is **kept** until Founder re-aims.

The cell-tower Amb (`2026-09_cell-tower-geometry`) is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED**. This app does **not** reopen either.

## Claim (Founder lock — replace any prior draft wording)

On a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) can recover mobile position with median error ≤ **X** on a held-out path inside a GPS-denied box — **without RF fingerprint training**.

**X:** provisional **sim X = 0.50 m** remains (**median** @ 1 ns RX noise). Honest only under **mild NLOS + near-ideal inter-ref sync** (`σ_sync ≲ 0.3 ns`). **X is median-not-p90** (1 ns p90 ≈ **1.16 m**). **Hardware X PARKED**.

## Intent / reverse framing

Not opportunistic cellular fingerprinting. Not GPS-crowdsourced mast maps. Not using GPS/DGPS as the phone / mobile fix. This Amb asks whether dedicated synchronized reference nodes plus mobile TDOA can place a receiver inside a GPS-denied box on a laptop-feasible sim/prototype path.

**Collaboration-with-owner (bibliographic + request):** US10135667B1, Kerry L. Greer, *System and method for increased indoor position tracking accuracy* (2018). Greer **requested** they solve his problem. The later deliverable is **for him by request**, **not** an unsolicited write-up. **Custom-beacon substrate, not a carrier-mast Amb.** **Do not** copy patent claims. **Do not** invent product claim-language copy. **Do not** paste claim language into this folder. Founder **may re-aim** when Greer’s success criteria arrive.

## Honest fog (named; C1–C3 gated)

1. **Spectrum / hardware vs sim-only.** **C1 SUCCEED** — sim-only path poseable. **#0** locked **sim X = 0.50 m**. Hardware **X PARKED**.
2. **Clock / sync.** **C2 SUCCEED** (story named). **#0 and MULTIPATH1 assumed** ideal sync. **SYNC1 Soften** — bar survives only at `σ_sync ≲ 0.3 ns` (median **0.382 m**). 1 ns scrapes **0.513 m**. `≥ 3 ns` / path drift fails X.
3. **Multipath.** **C3 SUCCEED** — scoring poseable. **MULTIPATH1 Soften** — poseable under LOS + mild / intermittent NLOS; **not** poseable under strong persistent multipath with frozen Chan alone. Do **not** claim a multipath-robust 0.50 m. **No** fingerprint rescue.

Remaining live fog = **sync fidelity + multipath** (not hyperbolic geometry).

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

## SYNC1 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered. Frozen Chan 1994; `σ_t` = 1 ns; same refs / L-path. `σ_sync ≲ 0.3 ns` → median **0.382 m** ≤ X. `σ_sync` = 1 ns scrapes **0.513 m**. `≥ 3 ns` / 3 ns path drift **fails X**. Combined **X** scope = near-ideal sync + prior MULTIPATH1 NLOS scope. See [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md).

## Next (REOPEN — invent board authorized, not run)

Founder / Operator **REOPEN**. Lab invents **2–3 cheap-check options** for **(A) / (B)**; Founder ranks. **Not this fold.** Still **no RF / ML**. Multipath wave-2 after the sync string. Fog peek + later gates: [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md). REOPEN digestion: [`DIGESTION_REOPEN_SYNC.md`](DIGESTION_REOPEN_SYNC.md).

## Reading order

1. [`STATUS.md`](STATUS.md) — where we are
2. [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) — the open / parked / hardened / Soften / REOPEN lines
3. [`DIGESTION_REOPEN_SYNC.md`](DIGESTION_REOPEN_SYNC.md) — REOPEN framing (DIGEST baseline preserved)
4. [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md) — SYNC1 gated metrics
5. [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md) — what SYNC1 taught (Founder DIGEST baseline)
6. [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md) — MULTIPATH1 gated metrics (prior Soften)
7. [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md) — what MULTIPATH1 taught
8. [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md) — #0 gated metrics
9. [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md) — what #0 taught
10. [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md) — Lab fog peek + later gates
11. [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md) — what the peek taught
12. [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md) — what the last string taught
13. [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) — decision log
14. [`notes.md`](notes.md) — one-line pointer
