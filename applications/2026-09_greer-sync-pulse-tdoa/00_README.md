# Greer-style sync-pulse TDOA — reading guide

**Application ID:** `2026-09_greer-sync-pulse-tdoa`  
**Opened:** 2026-09-05  

**Soften-admit send-candidate** on disk: [`GREER_WRITEUP_SEND.md`](GREER_WRITEUP_SEND.md) — **HOLD send** until user OK. Prior [`GREER_WRITEUP.md`](GREER_WRITEUP.md) remains **sync-fragility evidence only**. **Suite DIGEST Soften Amb ADMITTED** (not Harden; not wholesale Kill). After ingest + **A1→A4 Soften wrap**: A1 Soften · A2 Soften-conditional (JOINT1+~2.5 ns) · A3 Soften (mild/intermittent LE) · A4 Soften X/σ_t (jitter ≫1 ns; RF PARKED). Bars: patent-facing **≤1 m**; **X=0.50** perfect-ref only; **DGPS RN floor ~0.4–0.5 m** named. DIGEST: [`DIGESTION_A1A4_SUITE.md`](DIGESTION_A1A4_SUITE.md). Abstract ingest **ADMITTED** as Amb spine ([`SOURCE.md`](SOURCE.md)). Prior SYNC/JOINT/DRIFT/GATE = **sync-fragility evidence (partial)**. **GEOM0 HARDEN** stands. Link/map **PARKED**. First-pulse fog peek **ADMITTED** (C1/C2/C3 SUCCEED). Founder **CLAIM LOCK** recorded. Honesty: **path-shared batch**, **not** free per-epoch realtime. **Not** hardware. **PARK** hardware **X**. **PARK** RF bench. Lab audit: [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md). **Lab HOLD invent** (no named next pulse).

**NEW Amb (spine now the published abstract):** Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA. Owner-requested **collaboration framing** with [US10135667B1](https://patents.google.com/patent/US10135667B1/en) (published abstract ingested; custom-beacon substrate, **not** a carrier-mast Amb). **No claim-language copy.**

This is **not** a locator. This is **not** a trained map. Training is **not** established. This is **not** RF fingerprinting. This is **not** fingerprint rescue. This is **not** GPS / DGPS as the mobile fix. This is **not** skill-met. This is **not** rithm. This is **not** a product claim copied from the named patent. Soften / HARDEN / ingest is **not** claim clearance and is **not** an absolute, honest-phase-flip-1 ns, multipath-robust, or free per-epoch realtime 0.50 m. **0.50 m** is **not** the patent-facing bar and is **not** an absolute bar under the RN floor. Hardware **X** is **not** locked. RF bench is **not** unparked. **X** is **not** a p90 bar. Do **not** invent fingerprint / ML / RF to rescue detection jitter, the RN floor, loose sync, or free-epoch drift.

The cell-tower Amb (`2026-09_cell-tower-geometry`) is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED**. This app does **not** reopen either.

## Claim (Founder lock — replace any prior draft wording)

On a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) can recover mobile position with median error ≤ **X** on a held-out path inside a GPS-denied box — **without RF fingerprint training**.

**Bars (after abstract ingest + A1→A4 Soften):** patent-facing **≤1 m xy** **stands as object** (poseable under DGPS-class RN survey error + mild/intermittent LE; **fails** A4 J_stretch ~10 ns ~**3.8 m** and A3 persistent B_lb; **not** claim copy). **Sim X = 0.50 m** remains (**median** @ named 1 ns RX noise) only under **perfect-known refs + mild NLOS + `σ_sync ≲ 3 ns` under JOINT1 (fixed offsets) + named DRIFT1 batch α + GATE1 refuse-belt** — **Soften X/σ_t** as honest 50 kHz phase-flip; **not** a patent promise and **not** an absolute bar under the RN floor. **X is median-not-p90** (1 ns p90 ≈ **1.16 m**). **DGPS ~0.4–0.5 m** named absolute floor. **Hardware X PARKED**. **RF bench PARKED**. **Not** free per-epoch realtime.

## Intent / reverse framing

Not opportunistic cellular fingerprinting. Not GPS-crowdsourced mast maps. Not using GPS/DGPS as the phone / mobile fix. This Amb asks whether dedicated synchronized reference nodes plus mobile TDOA can place a receiver inside a GPS-denied box on a laptop-feasible sim/prototype path.

**Collaboration framing (owner-requested; abstract ingested as Amb spine):** US10135667B1, Kerry L. Greer, *System and method for increased indoor position tracking accuracy* (2018). Published abstract admitted: [`SOURCE.md`](SOURCE.md). Custom-beacon substrate, **not** a carrier-mast Amb. **Do not** copy patent claims. **Do not** paste claim language into this folder. Copy gate: [`COPY_GATE.md`](COPY_GATE.md).

## Honest fog (named; C1–C3 gated)

1. **Spectrum / hardware vs sim-only.** **C1 SUCCEED** — sim-only path poseable. **#0** locked **sim X = 0.50 m**. Hardware **X PARKED**.
2. **Clock / sync.** **C2 SUCCEED** (story named). **#0 and MULTIPATH1 assumed** ideal sync. **SYNC1 Soften** — Chan-alone bar survives only at `σ_sync ≲ 0.3 ns` (median **0.382 m**); 1 ns scrapes **0.513 m**. **JOINT1 Soften** — path-shared joint clocks restore X under fixed_trial `σ_sync ≲ 3 ns` (**0.231 m** @ 1 ns; **0.439 m** @ 3 ns). 10 ns fails (**1.816 m**). **DRIFT1 HARDEN** — batch path-shared τ + linear α restores SYNC1 drift breakers (drift=3 @ `σ=0` → **0.221 m**; drift=10 → **0.223 m**; **α̂ recovers**).
3. **Multipath.** **C3 SUCCEED** — scoring poseable. **MULTIPATH1 Soften** — poseable under LOS + mild / intermittent NLOS; **not** poseable under strong persistent multipath with frozen Chan alone. Do **not** claim a multipath-robust 0.50 m. **No** fingerprint rescue. **Later.**

Remaining live leftover is **send HOLD** (Founder rewrite on disk as Soften-admit send-candidate). Suite **A1→A4 Soften Amb DIGEST ADMITTED** ([`DIGESTION_A1A4_SUITE.md`](DIGESTION_A1A4_SUITE.md)). Link/map **PARKED**. RF bench **PARKED**. Our **MULTIPATH1** leftover stays **later** (not a substitute for A3). Prior GATE1 is scored as **partial** sync-fragility evidence.

## Eval rules (locked at peek)

- GPS / DGPS, if used at all, **place and time the reference nodes only**. They are **never** the mobile fix.
- Estimator class for the live path is ≥3-reference **simultaneous-sync TDOA** on a **sim-only** path (frozen Chan 1994; JOINT1 adds path-shared shared-τ; DRIFT1 adds batch linear α; GATE1 adds detect-only refuse). **No** RF fingerprint training. **No** fingerprint rescue.
- Path must stay **laptop-feasible** sim. Hardware **X** is **PARKED**.
- Metric: **median** error on a held-out path inside a GPS-denied box. Patent-facing **≤1 m xy** stands. Provisional **sim X = 0.50 m** is **perfect-ref scoped sim only** (**ideal refs + JOINT1 fixed-offset + named DRIFT1 batch α + GATE1 refuse-belt + NLOS-scoped**; **median-not-p90**; p90 ≈ 1.16 m @ 1 ns LOS is honesty, not the bar). **Not** an absolute bar under the RN floor. **DGPS ~0.4–0.5 m** absolute floor. Hardware **X** stays parked.
- This is **not** a fingerprinting claim and **not** a patent-product claim.

## #0 (gated)

Operator **ADMIT HARDEN**. Frozen Chan (1994) 2D WLS; numpy; 5 refs; L-path 101 samples; 40 MC; seed 20260905. `σ_t` = 1 ns → median **0.361 m** (`σ_d` ≈ 0.300 m); **p90 ≈ 1.16 m**. `σ_t` = 3 ns → median **1.081 m**. Zero-noise ~1e-14 m. 0 failures. Geometry is **not** the bottleneck under ideal sync + Gaussian Δt. **X is median-not-p90.** See [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md).

## MULTIPATH1 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered. Frozen Chan 1994; `σ_t` = 1 ns; positive range-bias; same refs / L-path as #0. Baseline **0.364 m**. `random_k=1` `b=0.5` → **0.476 m**. `epoch_f=0.25` `b=1` → **0.452 m**. Strong persistent `b≥1–2 m` → **0.73–4.7+ m** (not poseable with Chan alone). p90 ≈ **1.16 m** @ 1 ns LOS. **X = 0.50 m** remains **LOCKED**, NLOS-scoped. See [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md).

## SYNC1 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered. Frozen Chan 1994; `σ_t` = 1 ns; same refs / L-path. `σ_sync ≲ 0.3 ns` → median **0.382 m** ≤ X. `σ_sync` = 1 ns scrapes **0.513 m**. `≥ 3 ns` / 3 ns path drift **fails X**. Chan-alone window stays near-ideal. See [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md).

## JOINT1 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered. Aim A **partial**. Path-shared joint clocks (shared-τ) under **fixed_trial** `σ_sync`. **0.231 m** @ 1 ns; **0.439 m** @ 3 ns ≤ X. Chan scrape at 1 ns **restored**. `σ_sync` = 10 ns fails (**1.816 m**). Drift 3 ns/path still broke X on this pulse (JOINT1 **0.919 m** — shared-τ misspecified vs ramp; later **DRIFT1**). Named sync Soften budget **widens** to **`σ_sync ≲ 3 ns` under JOINT1** + prior mild-NLOS. **Not** multipath-robust. **Still stands** as the **fixed-offset** window. See [`SCORE_JOINT1.md`](SCORE_JOINT1.md).

## DRIFT1 (gated HARDEN)

Operator **ADMIT HARDEN** under the named DRIFT1 budget. Batch path-shared τ + linear α nuisance. SYNC1 drift breakers restore: drift=3 @ `σ=0` → **0.221 m**; drift=10 → **0.223 m**. **α̂ recovers.** Honesty: path-shared **batch** model, **not** free per-epoch realtime. **Not** multipath-robust. **Not** hardware. **JOINT1 Soften** still stands. See [`SCORE_DRIFT1.md`](SCORE_DRIFT1.md).

## GATE1 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered. Aim B **Succeed**. Detect-only refuse OR: G1a_DRIFT1 residual ∨ G1b raw LORO. FA `σ≤3` drift0 ≈ **0.100**; FA +matched drift3 ≈ **0.080**; TD σ=10 ≈ **0.828**; TD unmatched drift3 = **1.000**; TD per_epoch σ=3 = **1.000**. Residual-alone misses σ=10; raw LORO carries it. Injection-calibrated → Soften not Harden. Use: widen the error bar or refuse a point fix — **not** a magic accuracy repair. See [`SCORE_GATE1.md`](SCORE_GATE1.md).

## Abstract ingest (ADMITTED; Amb spine)

Operator **ADMIT ingest**. [`SOURCE.md`](SOURCE.md) · [`PROPOSED_ABSTRACT_INGEST.md`](PROPOSED_ABSTRACT_INGEST.md) · [`ABSTRACT_INGEST_SUMMARY.md`](ABSTRACT_INGEST_SUMMARY.md) · [`COPY_GATE.md`](COPY_GATE.md) · [`DIGESTION_ABSTRACT_INGEST.md`](DIGESTION_ABSTRACT_INGEST.md). Later the same day: **A1 Soften**.

## A1 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered. RN survey error on frozen Chan. Absolute ≤1 m poseable under DGPS-class RN survey error (Chan abs median **0.832 m** @ `σ_ref=0.5 m`, `σ_t=1 ns`). Absolute ≤0.50 m **not** under RN floor (**0.691 / 0.832** at 0.4 / 0.5). **X = 0.50 m** stays **perfect-ref scoped sim only**. JOINT1 scrape abs **0.449** @ `σ_ref=0.5` / `σ_sync=0` rides the floor — **do not Harden absolute X**. Silent GEOM0 absolute-≤0.50 **Softened**. Later the same day: **A2 Soften-conditional**, **A3 Soften**, **A4 Soften X/σ_t**. See [`SCORE_A1.md`](SCORE_A1.md).

## A2 (gated Soften-conditional)

Operator **ADMIT Soften-conditional**. JOINT1+~2.5 ns Soften; **Kill** bare Chan/commodity. Harden unsupported. Brutal lock: patent simultaneous-via-DGPS-1PPS ≠ commercial 1PPS. See [`SCORE_A2.md`](SCORE_A2.md) · [`DIGESTION_A2.md`](DIGESTION_A2.md). Suite wrap: [`DIGESTION_A1A4_SUITE.md`](DIGESTION_A1A4_SUITE.md).

## A3 (gated Soften)

Operator **ADMIT Soften**. Kill **not** triggered wholesale. Harden **unsupported**. Frozen Chan + RN `σ_ref=0.5` stack. Only mild/intermittent leading-edge residual (~**0.5–1 m** bias, or intermittent `f≈0.25`) survives patent **≤1 m**. Persistent `B_lb ≳ 2 m` and `B_dense` fail ≤1 m (`b=2` → abs **1.34 / 1.52**; `b=5` → ~**3.9**). 50 kHz `c/B` ~**6 km** = resolution caution only, **not** injected as fix error (distinct from A4 phase-flip detection jitter). See [`SCORE_A3.md`](SCORE_A3.md) · [`DIGESTION_A3.md`](DIGESTION_A3.md). Suite DIGEST: [`DIGESTION_A1A4_SUITE.md`](DIGESTION_A1A4_SUITE.md).

## A4 (gated Soften X/σ_t)

Operator **ADMIT Soften X/σ_t**. Kill **not** wholesale. Honest 50 kHz phase-flip detection jitter **≫ GEOM0 1 ns** (J_mid ~100–500 ns → tens of meters; J_stretch ~10 ns → ~3.8 m fails ≤1 m). JOINT1 does not cancel detection jitter. Harden unsupported. **RF bench PARKED.** See [`SCORE_A4.md`](SCORE_A4.md). Suite DIGEST: [`DIGESTION_A1A4_SUITE.md`](DIGESTION_A1A4_SUITE.md).

## Greer-facing write-up (Soften-admit send-candidate; HOLD send)

Founder-rewritten [`GREER_WRITEUP_SEND.md`](GREER_WRITEUP_SEND.md) is the **Soften-admit send-candidate**. **HOLD send** until user OK. Prior [`GREER_WRITEUP.md`](GREER_WRITEUP.md) remains **sync-fragility evidence only**. Lab audit: [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md). **Lab HOLD invent** (no named next pulse). Still **no RF / ML**. Fog peek + later gates: [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md).

## Reading order

1. [`STATUS.md`](STATUS.md) — where we are
2. [`DIGESTION_A1A4_SUITE.md`](DIGESTION_A1A4_SUITE.md) — A1→A4 suite DIGEST Soften Amb **ADMITTED**
3. [`SCORE_A4.md`](SCORE_A4.md) — A4 gated metrics (phase-flip jitter; Soften X/σ_t)
4. [`DIGESTION_A4.md`](DIGESTION_A4.md) — what A4 taught
5. [`SCORE_A1.md`](SCORE_A1.md) — A1 gated metrics (RN floor)
6. [`DIGESTION_A1.md`](DIGESTION_A1.md) — what A1 taught
6b. [`SCORE_A2.md`](SCORE_A2.md) — A2 gated metrics (JOINT1+~2.5 ns; Kill bare Chan/commodity)
6c. [`DIGESTION_A2.md`](DIGESTION_A2.md) — what A2 taught
6d. [`SCORE_A3.md`](SCORE_A3.md) — A3 gated metrics (mild LE residual)
6e. [`DIGESTION_A3.md`](DIGESTION_A3.md) — what A3 taught
7. [`ABSTRACT_INGEST_SUMMARY.md`](ABSTRACT_INGEST_SUMMARY.md) — gated ingest
8. [`SOURCE.md`](SOURCE.md) — published abstract (not claims)
9. [`DIGESTION_ABSTRACT_INGEST.md`](DIGESTION_ABSTRACT_INGEST.md) — what ingest taught
10. [`GREER_WRITEUP_SEND.md`](GREER_WRITEUP_SEND.md) — Founder-rewritten send-candidate (**Soften-admit**; **HOLD send** until user OK)
10b. [`GREER_WRITEUP.md`](GREER_WRITEUP.md) — prior write-up (**sync-fragility evidence only**)
11. [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md) — Lab audit draft
12. [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) — the open / parked / hardened / Soften lines
13. [`COPY_GATE.md`](COPY_GATE.md) — no claim-language product copy
14. [`PROPOSED_ABSTRACT_INGEST.md`](PROPOSED_ABSTRACT_INGEST.md) — ingest gate
15. [`SCORE_GATE1.md`](SCORE_GATE1.md) — GATE1 gated metrics (partial sync-fragility)
16. [`DIGESTION_GATE1.md`](DIGESTION_GATE1.md) — what GATE1 taught
17. [`SCORE_DRIFT1.md`](SCORE_DRIFT1.md) — DRIFT1 gated metrics
18. [`DIGESTION_DRIFT1.md`](DIGESTION_DRIFT1.md) — what DRIFT1 taught
19. [`SCORE_JOINT1.md`](SCORE_JOINT1.md) — JOINT1 gated metrics (prior Soften)
20. [`DIGESTION_JOINT1.md`](DIGESTION_JOINT1.md) — what JOINT1 taught
21. [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md) — SYNC1 gated metrics (prior Soften)
22. [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md) — what SYNC1 taught
23. [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md) — MULTIPATH1 gated metrics (prior Soften)
24. [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md) — what MULTIPATH1 taught
25. [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md) — #0 gated metrics
26. [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md) — what #0 taught
27. [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md) — Lab fog peek + later gates
28. [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md) — what the peek taught
29. [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md) — what the last string taught
30. [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) — decision log
31. [`notes.md`](notes.md) — one-line pointer
