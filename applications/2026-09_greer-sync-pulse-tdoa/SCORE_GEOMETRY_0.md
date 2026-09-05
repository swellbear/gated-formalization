# #0 geometry-bottleneck score — Chan 1994 2D WLS (Operator-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** #0 geometry-bottleneck — frozen Chan (1994) two-stage WLS under ideal simultaneous sync + Gaussian Δt only  
**Parent peek:** first-pulse fog naming **ADMITTED** (C1/C2/C3 SUCCEED; sim-only; hardware **X PARKED**) — [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master.

**What this is not:** A locator. Claim clearance. Hardware **X**. Skill-met. RF fingerprinting / ML. GPS/DGPS as the mobile fix. A product copied from US10135667B1. Reopening cell-tower as live. Reopening BIA→weight. Rithm.

---

## 0. Plain-language framing

**What this is:** A cheap planar TDOA geometry check. Frozen Chan (1994) 2D weighted least squares. Ideal clocks. Gaussian time-difference noise only. No multipath injected.

**What this settles:** Under those idealizations, planar geometry is **not** the bottleneck. Median Euclidean error tracks the `c · σ_t` scale. Operator **ADMIT HARDEN**. Provisional **sim X = 0.50 m** is locked (**median**-based @ 1 ns + margin). At 1 ns, p90 ≈ **1.16 m**. **X is median-not-p90.** Hardware **X** stays **PARKED**.

**What this is not:** Not a field locator. Not a hardware bar. Not claim clearance. Not a reason to invent RF or ML. Ideal sync is **assumed**. Multipath was **not** injected.

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Method | Chan 1994 two-stage WLS |
| Stack | numpy only |
| References | 5 refs |
| Path | L-path, **101** samples |
| Monte Carlo | **40** MC |
| Seed | **20260905** |
| Idealizations | simultaneous sync assumed; Gaussian Δt only; **no** multipath injected |
| GPS / DGPS | never the mobile fix (place/time refs only, if used at all) |

This fold does **not** re-run the sim. Numbers are the gated Lab summary.

---

## 2. Lab score (copied from the gate)

| Condition | Euclidean error |
|-----------|-----------------|
| Zero-noise sanity | median ~**1e-14 m** |
| `σ_t` = **1 ns** | median **0.361 m** (`σ_d` ≈ **0.300 m**); **p90 ≈ 1.16 m** |
| `σ_t` = **3 ns** | median **1.081 m** |
| Failures | **0** |

Median error tracks `c · σ_t`. At 1 ns the range-scale `σ_d ≈ 0.300 m` sits next to the 0.361 m median. That is the geometry-not-bottleneck bite.

**Honesty on X:** provisional **sim X = 0.50 m** is **median**-based @ 1 ns (0.361 m + margin). The same 1 ns board has **p90 ≈ 1.16 m**. **X is median-not-p90.** Do **not** read 0.50 m as a 90th-percentile bar.

**HARDEN (Operator):** Under ideal simultaneous sync + Gaussian Δt only, planar TDOA geometry with frozen Chan (1994) 2D WLS is **not** the bottleneck.

---

## 3. Operator gate (authoritative)

**HARDEN.** Geometry is not the bottleneck under the idealizations above.

**LOCK** provisional **sim X = 0.50 m** (**median**-based @ 1 ns + margin). **X is median-not-p90** (1 ns p90 ≈ **1.16 m**).

**PARK** hardware **X** until a sync / multipath gate.

**Honesty locks**

- Ideal sync **assumed**.
- Multipath **not** injected.
- GPS is **never** the mobile fix.
- This is **not** claim clearance.
- This is **not** a locator.
- This is **not** skill-met.
- **X** is a **median** bar, **not** a p90 bar.

**NEXT (named; not run in this fold):** **multipath / NLOS positive-bias injection** under the **same frozen Chan (1994) 2D WLS**. Still **no RF / ML**. Sync-imperfection stays **not** the named next pulse.

**HOLD** Lab invent of that named pulse — **not run** here.

US10135667B1 remains a **prior-art note only** — method practice / explore the idea; **not** copy claims for a product.

Cell-tower Amb stays **PARKED**. BIA→weight portfolio stays **CLOSED**.

---

## 4. Hard NO

- Do **not** treat **0.50 m** as a hardware bar, a field locator, or a **p90** bar.
- Do **not** run the named next pulse (multipath / NLOS positive-bias injection) in this fold.
- Do **not** invent RF / ML / fingerprint models.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / elevated language.
- Do **not** reopen `2026-09_cell-tower-geometry` as live.
- Do **not** reopen the BIA→weight portfolio.
- Do **not** invent a different next pulse (sync-imperfection stays unopened).

---

*Docs only. HARDEN ≠ claim clearance. Provisional sim X is median-not-p90. Provisional sim X ≠ hardware X. Not a locator. Not skill-met. Not a patent-product claim. Not rithm. Named next pulse (multipath/NLOS) is not run. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate.*
