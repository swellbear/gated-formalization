# MULTIPATH1 score — positive range-bias on frozen Chan (Operator-gated Soften)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** MULTIPATH1 — frozen Chan (1994) under `σ_t` = 1 ns + **positive range-bias** injection; same refs / L-path as #0  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md)  
**#0 geometry (prior HARDEN):** [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master.

**What this is not:** A locator. Claim clearance. Hardware **X**. A multipath-robust 0.50 m bar. Fingerprint rescue. Skill-met. RF fingerprinting / ML. GPS/DGPS as the mobile fix. A product copied from US10135667B1. Reopening cell-tower as live. Reopening BIA→weight. Rithm.

---

## 0. Plain-language framing

**What this is:** A cheap honesty pulse on the #0 board. Frozen Chan (1994). Same refs and L-path as #0. Clock noise held at `σ_t` = 1 ns. Positive range-bias is injected so multipath is no longer silently dropped.

**What this settles:** Operator **ADMIT Soften**. Kill did **not** fire. Provisional **sim X = 0.50 m** stays **LOCKED**, now with an **NLOS scope annotation**. The 0.50 m bar is poseable under LOS + mild / intermittent NLOS. It is **not** poseable under strong persistent multipath with frozen Chan alone. Do **not** claim a multipath-robust 0.50 m. **No** fingerprint rescue. **X** remains **median-not-p90**. Hardware **X** stays **PARKED**.

**What this is not:** Not a field locator. Not a hardware bar. Not claim clearance. Not a reason to invent RF or ML. Not a sync-imperfection pulse (that is next, **not this fold**).

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Method | Chan 1994 (frozen; same estimator class as #0) |
| Timing noise | `σ_t` = **1 ns** |
| Injection | **positive range-bias** (multipath honesty) |
| Geometry | **same refs / L-path as #0** |
| Metric | median Euclidean error ( **X** is median-not-p90 ) |
| GPS / DGPS | never the mobile fix (place/time refs only, if used at all) |

This fold does **not** re-run the sim. Numbers are the gated Lab summary copied from the Operator gate.

---

## 2. Lab score (copied from the gate)

| Condition | Median Euclidean error |
|-----------|-------------------------|
| Baseline (LOS @ 1 ns; this pulse) | **0.364 m** |
| Mild / intermittent — `random_k=1`, `b=0.5` | **0.476 m** |
| Mild / intermittent — `epoch_f=0.25`, `b=1` | **0.452 m** |
| Strong persistent — `b≥1–2 m` | **0.73–4.7+ m** |
| LOS p90 @ 1 ns (honesty; **not X**) | **≈ 1.16 m** |

**Soften (Operator).** Kill **not** triggered.

- **Poseable** under LOS + mild / intermittent NLOS (baseline **0.364 m**; `random_k=1` `b=0.5` → **0.476 m**; `epoch_f=0.25` `b=1` → **0.452 m**). Those medians stay under the locked **0.50 m** bar.
- **Not poseable** under strong persistent multipath (`b≥1–2 m` → **0.73–4.7+ m**) with **frozen Chan alone**.
- Do **not** claim a multipath-robust **0.50 m**. **No** fingerprint rescue.
- **X** remains **median-not-p90** (p90 ≈ **1.16 m** @ 1 ns LOS).

#0's 1 ns LOS median was **0.361 m**. This pulse's baseline is **0.364 m**. Both sit under **0.50 m**. Do **not** collapse them into one number.

---

## 3. Operator gate (authoritative)

**Soften.** Kill **not** triggered.

**LOCK** provisional **sim X = 0.50 m** remains, with **NLOS scope annotation**:

- Poseable under **LOS + mild / intermittent NLOS**.
- **Not** poseable under **strong persistent multipath** with frozen Chan alone.

**PARK** hardware **X**.

**NEXT (admitted as next pulse, not run in this PR):** **sync-imperfection**. Still **no RF / ML**. **No** fingerprint rescue.

**Honesty locks**

- Frozen Chan 1994. `σ_t` = 1 ns. Positive range-bias injection. Same refs / L-path as #0.
- Do **not** claim a multipath-robust 0.50 m.
- **X** is **median-not-p90**.
- GPS is **never** the mobile fix.
- This is **not** claim clearance.
- This is **not** a locator.
- This is **not** skill-met.

US10135667B1 remains a **prior-art note only** — method practice / explore the idea; **not** copy claims for a product.

Cell-tower Amb stays **PARKED**. BIA→weight portfolio stays **CLOSED**.

---

## 4. Hard NO

- Do **not** treat **0.50 m** as multipath-robust, as a hardware bar, or as a field locator.
- Do **not** invent RF / ML / fingerprint rescue.
- Do **not** silently drop strong persistent NLOS.
- Do **not** swap **X** to p90 (p90 ≈ 1.16 m @ 1 ns LOS is honesty, not the bar).
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / elevated language.
- Do **not** reopen `2026-09_cell-tower-geometry` as live.
- Do **not** reopen the BIA→weight portfolio.
- Do **not** run the sync-imperfection pulse in this fold.

---

*Docs only. Soften ≠ Kill. Soften ≠ claim clearance. NLOS-scoped sim X ≠ multipath-robust X. Not a locator. Not skill-met. Not a patent-product claim. Not rithm. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate.*
