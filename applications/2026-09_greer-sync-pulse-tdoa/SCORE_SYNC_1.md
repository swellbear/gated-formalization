# SYNC1 sync-imperfection score — Chan 1994 2D WLS (Operator-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** SYNC1 sync-imperfection — frozen Chan (1994) two-stage WLS; `σ_t` = 1 ns; same refs / L-path as #0  
**Parent pulses:** first-pulse fog naming **ADMITTED** (C1/C2/C3 SUCCEED) · **#0 GEOM0 HARDEN** ([`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md); **median-not-p90**; 1 ns p90 ≈ **1.16 m**) · prior **MULTIPATH1 Soften** ([`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md); LOS + mild/intermittent NLOS only)  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master.

**What this is not:** A locator. Claim clearance. Hardware **X**. Skill-met. RF fingerprinting / ML. GPS/DGPS as the mobile fix. A product copied from US10135667B1. Reopening cell-tower as live. Reopening BIA→weight. Rithm. A rescue of loose sync by fingerprint / ML / RF invent. A p90 bar.

---

## 0. Plain-language framing

**What this is:** A cheap sync-imperfection check on the same frozen Chan board as #0. Receiver noise stays `σ_t` = 1 ns. Same refs / L-path. Inter-reference sync error (`σ_sync`) and path drift are injected. No new estimator.

**What this settles:** Kill is **not** triggered. Provisional **sim X = 0.50 m** **remains**, scoped (on this pulse) to **near-ideal Chan-alone sync + NLOS**. Near-ideal `σ_sync ≲ 0.3 ns` keeps the **median** **≤ X**. `σ_sync` = 1 ns scrapes over. `≥ 3 ns` / 3 ns path drift **fails X**. Later **JOINT1** restored the 1 ns scrape under joint clocks — see [`SCORE_JOINT1.md`](SCORE_JOINT1.md). **GEOM0 HARDEN** still stands. Prior **MULTIPATH1 Soften** still stands (LOS + mild/intermittent NLOS only). **Median-not-p90** honesty remains (1 ns p90 ≈ **1.16 m** on the #0 board).

**What this is not:** Not a field locator. Not a hardware bar. Not a p90 bar. Not claim clearance. Not a reason to invent RF, ML, or fingerprints to rescue loose sync. Strong multipath and loose sync still fail Chan alone.

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Method | Frozen Chan 1994 two-stage WLS (same class as #0) |
| Receiver noise | `σ_t` = **1 ns** |
| Geometry | same refs / L-path as #0 |
| Standing pulses | **GEOM0 HARDEN** · prior **MULTIPATH1 Soften** (LOS + mild/intermittent NLOS only) |
| X honesty | **median-not-p90** (1 ns p90 ≈ **1.16 m** on the #0 board) |
| GPS / DGPS | never the mobile fix (place/time refs only, if used at all) |

This fold does **not** re-run the sim. Numbers are the gated Lab summary.

---

## 2. Lab score (copied from the gate)

| Condition | Median Euclidean error vs **X = 0.50 m** |
|-----------|------------------------------------------|
| Near-ideal sync `σ_sync ≲ 0.3 ns` | **0.382 m** ≤ X |
| `σ_sync` = **1 ns** | **0.513 m** — scrapes over X |
| `σ_sync` **≥ 3 ns** / **3 ns path drift** | **fails X** |

**Soften (Operator). Kill not triggered.** The 0.50 m **median** bar stays, but only under the combined **sync + NLOS** scope below.

---

## 3. Combined X scope (standing)

Provisional **sim X = 0.50 m** remains. It is honest only under:

1. **Near-ideal inter-ref sync** — `σ_sync ≲ 0.3 ns` (median **0.382 m** ≤ X).
2. Prior **MULTIPATH1 Soften** — **LOS + mild/intermittent NLOS only** (baseline **0.364 m**; `random_k=1` `b=0.5` → **0.476 m**; `epoch_f=0.25` `b=1` → **0.452 m**; strong persistent `b≥1–2 m` → **0.73–4.7+ m**, not poseable with Chan alone).
3. **Median-not-p90** honesty (the bar is a median, not a tail; 1 ns p90 ≈ **1.16 m**).
4. **GEOM0 HARDEN** still stands — planar geometry is not the bottleneck under ideal sync.

**Fails the bar (Chan alone; do not invent a rescue):**

- `σ_sync` = 1 ns scrapes (**0.513 m**).
- `σ_sync ≥ 3 ns` / **3 ns path drift** fails X.
- Strong multipath (beyond mild/intermittent NLOS) fails Chan alone.

Do **not** invent fingerprint / ML / RF to rescue loose sync.

---

## 4. Operator gate (authoritative)

**Soften.** Kill **not** triggered.

**LOCK** provisional **sim X = 0.50 m** remains, scoped to **sync + NLOS** (near-ideal sync + LOS / mild/intermittent NLOS). **X is median-not-p90.**

**PARK** hardware **X**.

**Honesty locks**

- Median-not-p90 honesty remains (1 ns p90 ≈ **1.16 m**).
- **GEOM0 HARDEN** still stands (geometry not the bottleneck under ideal sync).
- Prior **MULTIPATH1 Soften** still stands (LOS + mild/intermittent NLOS only).
- Frozen Chan 1994; `σ_t` = 1 ns; same refs / L-path.
- GPS is **never** the mobile fix.
- This is **not** claim clearance.
- This is **not** a locator.
- This is **not** skill-met.
- No fingerprint / ML / RF invent to rescue loose sync.

**LATER THE SAME DAY:** **JOINT1 Soften** widened the named sync budget under path-shared joint clocks. See [`SCORE_JOINT1.md`](SCORE_JOINT1.md). **SYNC1 Soften** still stands as the Chan-alone near-ideal window. Still **no RF / ML**.

US10135667B1 — owner-requested **collaboration framing** (bibliographic; custom-beacon substrate, **not** a carrier-mast Amb). **No claim-language copy.**

Cell-tower Amb stays **PARKED**. BIA→weight portfolio stays **CLOSED**.

---

## 5. Hard NO

- Do **not** treat **0.50 m** as a hardware bar, a field locator, or a **p90** bar.
- Do **not** treat `σ_sync` = 1 ns (0.513 m scrape) as a pass.
- Do **not** invent fingerprint / ML / RF to rescue loose sync or strong multipath.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / elevated language.
- Do **not** reopen `2026-09_cell-tower-geometry` as live.
- Do **not** reopen the BIA→weight portfolio.
- Do **not** erase the Chan-alone SYNC1 window when reading JOINT1. JOINT1 widens the named budget **under joint clocks**.

---

*Docs only. Soften ≠ claim clearance. Kill not triggered ≠ locator. Provisional sim X is median-not-p90. Provisional sim X ≠ hardware X. Not skill-met. Not a patent-product claim. Not rithm. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate.*
