# DRIFT1 path-drift α — score (Operator-gated HARDEN)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** DRIFT1 — batch path-shared τ + linear α nuisance on SYNC1 drift breakers  
**Parent pulses:** first-pulse fog naming **ADMITTED** (C1/C2/C3 SUCCEED) · **#0 GEOM0 HARDEN** ([`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md); **median-not-p90**; 1 ns p90 ≈ **1.16 m**) · **MULTIPATH1 Soften** ([`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md); LOS + mild/intermittent NLOS only) · **SYNC1 Soften** ([`SCORE_SYNC_1.md`](SCORE_SYNC_1.md); Chan-alone near-ideal `σ_sync ≲ 0.3 ns`) · **JOINT1 Soften** ([`SCORE_JOINT1.md`](SCORE_JOINT1.md); `σ_sync ≲ 3 ns` **fixed offsets**)  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_DRIFT1.md`](DIGESTION_DRIFT1.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master.

**What this is not:** A locator. Claim clearance. Hardware **X**. Skill-met. RF fingerprinting / ML. GPS/DGPS as the mobile fix. A product copied from US10135667B1. A multipath-robust 0.50 m. A **free per-epoch realtime** drift claim. Reopening cell-tower as live. Reopening BIA→weight. Rithm. A p90 bar.

---

## 0. Plain-language framing

**What this is:** A cheap path-drift check after JOINT1 Soften. Batch path-shared **τ** plus a **linear α** nuisance on the same honesty board. SYNC1 drift breakers (the ramps that broke Chan-alone and shared-τ-only) are the named target. No RF. No ML. No fingerprint.

**What this settles:** **HARDEN** under the named **DRIFT1** budget. Batch path-shared τ + linear α **restores median ≤ 0.50 m** on the SYNC1 drift breakers. **α̂ recovers.** **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) **still stands.**

**What this is not:** Not a field locator. Not a hardware bar. Not a p90 bar. Not claim clearance. Not a multipath-robust claim. Not a **free per-epoch realtime** drift model. Not a reason to invent RF, ML, or fingerprints.

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Method | Batch path-shared **τ** + linear **α** nuisance |
| Drift injection | SYNC1 drift breakers (path ramp); **σ = 0** on the reported restore rows |
| Standing pulses | **GEOM0 HARDEN** · **MULTIPATH1 Soften** (LOS + mild/intermittent NLOS only) · **SYNC1 Soften** (Chan-alone `σ_sync ≲ 0.3 ns`) · **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) |
| X honesty | **median-not-p90** (1 ns p90 ≈ **1.16 m** on the #0 board) |
| GPS / DGPS | never the mobile fix (place/time refs only, if used at all) |

This fold does **not** re-run the sim. Numbers are the gated Lab summary.

**JOINT1 reminder (prior Soften, not this pulse):** shared-τ-only drift 3 ns/path was **0.919 m** (fails X). DRIFT1 is the restore of those SYNC1 drift breakers under the named batch α budget.

---

## 2. Lab score (copied from the gate)

| Condition | Median Euclidean error vs **X = 0.50 m** |
|-----------|------------------------------------------|
| DRIFT1 **drift = 3** @ `σ = 0` (batch path-shared τ + linear α) | **0.221 m** ≤ X |
| DRIFT1 **drift = 10** (batch path-shared τ + linear α) | **0.223 m** ≤ X |
| **α̂** | **recovers** |

**HARDEN (Operator)** under the named **DRIFT1** budget.

Batch path-shared τ + linear α restores **median ≤ 0.50 m** on the SYNC1 drift breakers. **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) still stands. Do **not** claim multipath-robust. Do **not** claim free per-epoch realtime. Do **not** claim hardware.

---

## 3. Combined X scope (standing)

Provisional **sim X = 0.50 m** remains. It is honest only under:

1. **DRIFT1 HARDEN** — batch path-shared τ + linear α nuisance restores SYNC1 drift breakers (**0.221 m** @ drift=3 / `σ=0`; **0.223 m** @ drift=10). **α̂ recovers.** This is a **path-shared batch** model, **not** free per-epoch realtime.
2. **`σ_sync ≲ 3 ns` under JOINT1** — path-shared joint clocks; **fixed_trial** / **fixed offsets** (1 ns → **0.231 m**; 3 ns → **0.439 m** ≤ X). **JOINT1 Soften still stands.**
3. Prior **MULTIPATH1 Soften** — **LOS + mild/intermittent NLOS only** (baseline **0.364 m**; `random_k=1` `b=0.5` → **0.476 m**; `epoch_f=0.25` `b=1` → **0.452 m**; strong persistent `b≥1–2 m` → **0.73–4.7+ m**, not poseable with Chan alone).
4. **Median-not-p90** honesty (the bar is a median, not a tail; 1 ns p90 ≈ **1.16 m**).
5. **GEOM0 HARDEN** still stands — planar geometry is not the bottleneck under ideal sync.
6. **SYNC1 Soften** still stands as the **Chan-alone** near-ideal window (`σ_sync ≲ 0.3 ns` → **0.382 m**; Chan 1 ns scrape **0.513 m** is restored under JOINT1).

**Fails / out of this budget (do not invent a rescue):**

- **Free per-epoch realtime** drift. DRIFT1 is a **path-shared batch** model.
- Strong multipath (beyond mild/intermittent NLOS). **Not multipath-robust.** **Multipath later.**
- Hardware / spectrum path. **Hardware X PARKED.**
- JOINT1 `σ_sync` = **10 ns** → **1.816 m** (fixed-offset leftover; JOINT1 Soften does **not** erase it).

Do **not** invent fingerprint / ML / RF to rescue loose sync, free-epoch drift, or strong multipath.

---

## 4. Operator gate (authoritative)

**Harden** under named **DRIFT1** budget.

**LOCK** provisional **sim X = 0.50 m** remains. Named DRIFT1 budget = batch path-shared τ + linear α nuisance restores median ≤ **0.50 m** on SYNC1 drift breakers. **X is median-not-p90.**

**PARK** hardware **X**.

**NEXT (named; not this fold):** **GATE1**, then a Greer-facing write-up. Still **no RF / ML**. **No** fingerprint rescue. **Multipath later.**

**Honesty locks**

- Path-shared **batch** model, **not** free per-epoch realtime.
- Median-not-p90 honesty remains (1 ns p90 ≈ **1.16 m**).
- **GEOM0 HARDEN** still stands.
- **MULTIPATH1 Soften** still stands (LOS + mild/intermittent NLOS only). **Not** a multipath-robust claim.
- **SYNC1 Soften** still stands as Chan-alone near-ideal.
- **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) **still stands.**
- GPS is **never** the mobile fix.
- This is **not** claim clearance.
- This is **not** a locator.
- This is **not** skill-met.
- This is **not** hardware.
- No fingerprint / ML / RF invent.

US10135667B1 — owner-requested **collaboration framing** (bibliographic; custom-beacon substrate, **not** a carrier-mast Amb). **No claim-language copy.** Not a product embodiment.

Cell-tower Amb stays **PARKED**. BIA→weight portfolio stays **CLOSED**.

---

## 5. Hard NO

- Do **not** treat **0.50 m** as a hardware bar, a field locator, a **p90** bar, a **multipath-robust** bar, or a **free per-epoch realtime** drift bar.
- Do **not** treat JOINT1 `σ_sync` = 10 ns (**1.816 m**) as a pass.
- Do **not** silently drop JOINT1 Soften — DRIFT1 HARDEN is the named **path-drift α** budget; JOINT1 still holds the **fixed-offset** window.
- Do **not** invent fingerprint / ML / RF to rescue loose sync, free-epoch drift, or strong multipath.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / elevated language.
- Do **not** reopen `2026-09_cell-tower-geometry` as live.
- Do **not** reopen the BIA→weight portfolio.
- Do **not** run **GATE1** or a Greer-facing write-up in this fold.
- Do **not** unpark hardware **X**. Multipath is **later**, not this fold.

---

*Docs only. HARDEN ≠ claim clearance. Path-shared batch α ≠ free per-epoch realtime. Provisional sim X is median-not-p90. Provisional sim X ≠ hardware X. Not skill-met. Not a patent-product claim. Not rithm. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate.*
