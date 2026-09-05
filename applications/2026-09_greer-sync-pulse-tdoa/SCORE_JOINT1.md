# JOINT1 path-shared joint clocks — score (Operator-gated Soften)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** JOINT1 — path-shared joint clocks (shared-τ) under **fixed_trial** `σ_sync`; Aim A **partial**  
**Parent pulses:** first-pulse fog naming **ADMITTED** (C1/C2/C3 SUCCEED) · **#0 GEOM0 HARDEN** ([`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md); **median-not-p90**; 1 ns p90 ≈ **1.16 m**) · **MULTIPATH1 Soften** ([`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md); LOS + mild/intermittent NLOS only) · **SYNC1 Soften** ([`SCORE_SYNC_1.md`](SCORE_SYNC_1.md); Chan-alone near-ideal `σ_sync ≲ 0.3 ns`)  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_JOINT1.md`](DIGESTION_JOINT1.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master.

**What this is not:** A locator. Claim clearance. Hardware **X**. Skill-met. RF fingerprinting / ML. GPS/DGPS as the mobile fix. A product copied from US10135667B1. A multipath-robust 0.50 m. A drift-robust 0.50 m. Reopening cell-tower as live. Reopening BIA→weight. Rithm. A p90 bar.

---

## 0. Plain-language framing

**What this is:** A cheap joint-clock check after SYNC1 Soften. Path-shared JOINT1 estimates a **shared τ** on the same honesty board. Inter-reference error is **fixed_trial** `σ_sync` (one offset per trial, not a ramp). No RF. No ML. No fingerprint.

**What this settles:** Kill is **not** triggered. Aim A is **partial**. Path-shared JOINT1 **restores X** under fixed_trial `σ_sync` up to **≲ 3 ns**. The Chan-alone 1 ns scrape is **restored**. `σ_sync` = 10 ns **fails**. Drift 3 ns/path **still breaks X** — shared-τ is misspecified versus a ramp. Named sync Soften budget **widens** to **`σ_sync ≲ 3 ns` under JOINT1** + prior mild-NLOS. **GEOM0 HARDEN** still stands. **MULTIPATH1 Soften** still stands. **SYNC1 Soften** still stands as the Chan-alone near-ideal window. **Median-not-p90** honesty remains.

**What this is not:** Not a field locator. Not a hardware bar. Not a p90 bar. Not claim clearance. Not a multipath-robust claim. Not a drift-robust claim. Not a reason to invent RF, ML, or fingerprints.

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Method | Path-shared **JOINT1** (shared-τ / joint clocks) |
| Sync injection | **fixed_trial** `σ_sync` (one offset per trial) |
| Standing pulses | **GEOM0 HARDEN** · **MULTIPATH1 Soften** (LOS + mild/intermittent NLOS only) · **SYNC1 Soften** (Chan-alone `σ_sync ≲ 0.3 ns`) |
| X honesty | **median-not-p90** (1 ns p90 ≈ **1.16 m** on the #0 board) |
| GPS / DGPS | never the mobile fix (place/time refs only, if used at all) |

This fold does **not** re-run the sim. Numbers are the gated Lab summary.

**Chan-alone reminder (SYNC1, not this pulse):** `σ_sync` = 1 ns scraped **0.513 m**. JOINT1 at 1 ns is the restore of that scrape.

---

## 2. Lab score (copied from the gate)

| Condition | Median Euclidean error vs **X = 0.50 m** |
|-----------|------------------------------------------|
| JOINT1 `σ_sync` = **1 ns** (fixed_trial) | **0.231 m** ≤ X — Chan scrape at 1 ns **restored** |
| JOINT1 `σ_sync` = **3 ns** (fixed_trial) | **0.439 m** ≤ X |
| JOINT1 `σ_sync` = **10 ns** (fixed_trial) | **1.816 m** — **fails X** |
| JOINT1 **drift 3 ns/path** | **0.919 m** — **fails X** (shared-τ misspecified vs ramp) |

**Soften (Operator). Kill not triggered. Aim A partial.**

Path-shared JOINT1 restores **X** under fixed_trial `σ_sync` up to **≲ 3 ns**. Named sync Soften budget **widens** to that window + prior mild-NLOS. Do **not** claim multipath-robust. Do **not** claim drift-robust.

---

## 3. Combined X scope (standing)

Provisional **sim X = 0.50 m** remains. It is honest only under:

1. **`σ_sync ≲ 3 ns` under JOINT1** — path-shared joint clocks; **fixed_trial** (1 ns → **0.231 m**; 3 ns → **0.439 m** ≤ X).
2. Prior **MULTIPATH1 Soften** — **LOS + mild/intermittent NLOS only** (baseline **0.364 m**; `random_k=1` `b=0.5` → **0.476 m**; `epoch_f=0.25` `b=1` → **0.452 m**; strong persistent `b≥1–2 m` → **0.73–4.7+ m**, not poseable with Chan alone).
3. **Median-not-p90** honesty (the bar is a median, not a tail; 1 ns p90 ≈ **1.16 m**).
4. **GEOM0 HARDEN** still stands — planar geometry is not the bottleneck under ideal sync.
5. **SYNC1 Soften** still stands as the **Chan-alone** near-ideal window (`σ_sync ≲ 0.3 ns` → **0.382 m**; Chan 1 ns scrape **0.513 m** is now restored under JOINT1).

**Fails the bar (do not invent a rescue):**

- JOINT1 `σ_sync` = **10 ns** → **1.816 m**.
- **Drift 3 ns/path** → JOINT1 **0.919 m** (shared-τ misspecified vs ramp). **Not drift-robust.**
- Strong multipath (beyond mild/intermittent NLOS). **Not multipath-robust.**

Do **not** invent fingerprint / ML / RF to rescue loose sync, drift, or strong multipath.

---

## 4. Operator gate (authoritative)

**Soften.** Kill **not** triggered. Aim A **partial**.

**LOCK** provisional **sim X = 0.50 m** remains. Named sync Soften budget **widens** to **`σ_sync ≲ 3 ns` under JOINT1** + prior mild-NLOS. **X is median-not-p90.**

**PARK** hardware **X**.

**NEXT (named; not this fold):** **DRIFT1** pulse. Still **no RF / ML**. **No** fingerprint rescue.

**Honesty locks**

- Median-not-p90 honesty remains (1 ns p90 ≈ **1.16 m**).
- **GEOM0 HARDEN** still stands.
- **MULTIPATH1 Soften** still stands (LOS + mild/intermittent NLOS only). **Not** a multipath-robust claim.
- **SYNC1 Soften** still stands as Chan-alone near-ideal.
- Drift 3 ns/path still breaks X. **Not** a drift-robust claim.
- GPS is **never** the mobile fix.
- This is **not** claim clearance.
- This is **not** a locator.
- This is **not** skill-met.
- No fingerprint / ML / RF invent.

US10135667B1 — owner-requested **collaboration framing** (bibliographic; custom-beacon substrate, **not** a carrier-mast Amb). **No claim-language copy.** Not a product embodiment.

Cell-tower Amb stays **PARKED**. BIA→weight portfolio stays **CLOSED**.

---

## 5. Hard NO

- Do **not** treat **0.50 m** as a hardware bar, a field locator, a **p90** bar, a **multipath-robust** bar, or a **drift-robust** bar.
- Do **not** treat JOINT1 `σ_sync` = 10 ns (**1.816 m**) or drift 3 ns/path (**0.919 m**) as a pass.
- Do **not** silently drop the Chan-alone SYNC1 window — JOINT1 widens the named budget **under joint clocks**, it does not erase Chan-alone scrape at 1 ns.
- Do **not** invent fingerprint / ML / RF to rescue loose sync, drift, or strong multipath.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / elevated language.
- Do **not** reopen `2026-09_cell-tower-geometry` as live.
- Do **not** reopen the BIA→weight portfolio.
- Do **not** run **DRIFT1** in this fold.

---

*Docs only. Soften ≠ claim clearance. Kill not triggered ≠ locator. Aim A partial ≠ drift-robust. Provisional sim X is median-not-p90. Provisional sim X ≠ hardware X. Not skill-met. Not a patent-product claim. Not rithm. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate.*
