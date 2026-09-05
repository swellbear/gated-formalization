# GATE1 refuse-belt — score (Operator-gated Soften)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** GATE1 — detect-only refuse OR: **G1a_DRIFT1 residual ∨ G1b raw LORO**  
**Parent pulses:** first-pulse fog naming **ADMITTED** (C1/C2/C3 SUCCEED) · **#0 GEOM0 HARDEN** ([`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md); **median-not-p90**; 1 ns p90 ≈ **1.16 m**) · **MULTIPATH1 Soften** ([`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md); LOS + mild/intermittent NLOS only) · **SYNC1 Soften** ([`SCORE_SYNC_1.md`](SCORE_SYNC_1.md); Chan-alone near-ideal `σ_sync ≲ 0.3 ns`) · **JOINT1 Soften** ([`SCORE_JOINT1.md`](SCORE_JOINT1.md); `σ_sync ≲ 3 ns` **fixed offsets**) · **DRIFT1 HARDEN** ([`SCORE_DRIFT1.md`](SCORE_DRIFT1.md); named batch α restores SYNC1 drift breakers)  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_GATE1.md`](DIGESTION_GATE1.md)  
**Greer-facing write-up (Founder PRIMARY; HOLD send):** [`GREER_WRITEUP.md`](GREER_WRITEUP.md)  
**Lab audit draft:** [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master.

**What this is not:** A locator. Claim clearance. Hardware **X**. Skill-met. RF fingerprinting / ML. GPS/DGPS as the mobile fix. A product copied from US10135667B1. A multipath-robust 0.50 m. A free per-epoch realtime drift claim. A magic accuracy repair. A product UX. Reopening cell-tower as live. Reopening BIA→weight. Rithm. A p90 bar.

---

## 0. Plain-language framing

**What this is:** A cheap detect-only refuse belt after DRIFT1 HARDEN. Residual after the named DRIFT1 batch model **or** raw leave-one-ref-out (LORO) scatter. Injection-calibrated thresholds. No RF. No ML. No fingerprint.

**What this settles:** **Soften** (Kill **not** triggered; aim B **Succeed**). In-budget false alarm ≈ **0.10**. Out-of-budget catch is **high** (TD σ=10 ≈ **0.828**; unmatched drift3 = **1.000**; per-epoch σ=3 = **1.000**). Use: **widen the error bar or refuse a point fix** when the check fires. **Not** a magic accuracy repair.

**What this is not:** Not a field locator. Not a hardware bar. Not a p90 bar. Not claim clearance. Not a multipath-robust claim. Not free per-epoch realtime. Not a reason to invent RF, ML, or fingerprints. Not a send to Greer (write-up is **HOLD** until user OK).

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Method | Detect-only refuse **OR**: **G1a_DRIFT1 residual ∨ G1b raw LORO** |
| Thresholds | Injection-calibrated (Soften, **not** Harden) |
| Standing pulses | **GEOM0 HARDEN** · **MULTIPATH1 Soften** · **SYNC1 Soften** · **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) · **DRIFT1 HARDEN** |
| X honesty | **median-not-p90** (1 ns p90 ≈ **1.16 m** on the #0 board) |
| GPS / DGPS | never the mobile fix (place/time refs only, if used at all) |

This fold does **not** re-run the sim. Numbers are the gated Lab summary.

**Honesty on the OR:** DRIFT1 residual **alone misses** `σ_sync` = 10 ns (τ absorbs fixed_trial). Raw **LORO carries** the σ=10 detection. Do **not** drop the LORO leg.

---

## 2. Lab score (copied from the gate)

| Quantity | Rate |
|----------|------|
| FA `σ≤3` drift0 | ≈ **0.100** |
| FA +matched drift3 | ≈ **0.080** |
| TD `σ=10` | ≈ **0.828** |
| TD unmatched under drift3 | **1.000** |
| TD per_epoch `σ=3` | **1.000** |

**Soften (Operator). Kill not triggered. Aim B Succeed.**

Detect-only refuse belt. Injection-calibrated thresholds → Soften, **not** Harden. **JOINT1 Soften** (`σ_sync ≲ 3 ns`) and **DRIFT1 HARDEN** still stand. Do **not** claim a magic accuracy repair. Do **not** claim hardware. Do **not** send the Greer write-up until user OK.

---

## 3. Combined X scope (standing)

Provisional **sim X = 0.50 m** remains. It is honest only under:

1. **GATE1 Soften** — detect-only refuse OR (G1a residual ∨ G1b raw LORO). FA ≈ **0.10** in-band; TD high out-of-band. **Not** a repair.
2. **DRIFT1 HARDEN** — batch path-shared τ + linear α restores SYNC1 drift breakers (**0.221 m** @ drift=3 / `σ=0`; **0.223 m** @ drift=10). **α̂ recovers.** Path-shared **batch**, **not** free per-epoch realtime.
3. **`σ_sync ≲ 3 ns` under JOINT1** — path-shared joint clocks; **fixed_trial** / **fixed offsets** (1 ns → **0.231 m**; 3 ns → **0.439 m** ≤ X). **JOINT1 Soften still stands.**
4. Prior **MULTIPATH1 Soften** — **LOS + mild/intermittent NLOS only**.
5. **Median-not-p90** honesty (1 ns p90 ≈ **1.16 m**).
6. **GEOM0 HARDEN** still stands.
7. **SYNC1 Soften** still stands as the Chan-alone near-ideal window (`σ_sync ≲ 0.3 ns`).

**Fails / out of this budget (do not invent a rescue):**

- JOINT1 `σ_sync` = **10 ns** → **1.816 m**. GATE1 can **refuse**; it does **not** restore 0.50 m.
- Strong multipath (beyond mild/intermittent NLOS). **Not multipath-robust.** **Multipath later.**
- Hardware / spectrum path. **Hardware X PARKED.**
- Free per-epoch realtime drift.

Do **not** invent fingerprint / ML / RF to rescue loose sync, free-epoch drift, or strong multipath.

---

## 4. Operator gate (authoritative)

**Soften.** Kill **not** triggered. Aim B **Succeed**.

**LOCK** provisional **sim X = 0.50 m** remains. Named GATE1 budget = detect-only refuse OR (G1a_DRIFT1 residual ∨ G1b raw LORO). Injection-calibrated. **X is median-not-p90.**

**PARK** hardware **X**.

**HOLD** Lab invent. **HOLD send** of [`GREER_WRITEUP.md`](GREER_WRITEUP.md) until Founder / user OK. Ask Greer for criteria when send is authorized.

**Honesty locks**

- Detect-only refuse. **Not** a magic accuracy repair.
- DRIFT1 residual alone **misses** σ=10 (τ absorbs fixed_trial). Raw LORO **carries** σ=10.
- Injection-calibrated thresholds → Soften, **not** Harden.
- Path-shared **batch** model, **not** free per-epoch realtime.
- Median-not-p90 honesty remains (1 ns p90 ≈ **1.16 m**).
- **GEOM0 HARDEN** still stands.
- **MULTIPATH1 Soften** still stands. **Not** a multipath-robust claim. **Multipath later.**
- **SYNC1 Soften** still stands as Chan-alone near-ideal.
- **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) **still stands.**
- **DRIFT1 HARDEN** still stands.
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
- Do **not** treat GATE1 as a magic accuracy repair or product UX.
- Do **not** drop the LORO leg (residual-alone misses σ=10).
- Do **not** treat JOINT1 `σ_sync` = 10 ns (**1.816 m**) as a pass.
- Do **not** invent fingerprint / ML / RF to rescue loose sync, free-epoch drift, or strong multipath.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / elevated language.
- Do **not** reopen `2026-09_cell-tower-geometry` as live.
- Do **not** reopen the BIA→weight portfolio.
- Do **not** send [`GREER_WRITEUP.md`](GREER_WRITEUP.md) until Founder / user OK.
- Do **not** unpark hardware **X**. Multipath is **later**. Lab invent is **HOLD**.

---

*Docs only. Soften ≠ claim clearance. Refuse belt ≠ locator. Provisional sim X is median-not-p90. Provisional sim X ≠ hardware X. Not skill-met. Not a patent-product claim. Not rithm. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate. Write-up HOLD send until user OK.*
