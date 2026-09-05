# A1 ref-floor honesty — score (Operator-gated Soften)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** A1 — reference-node (RN) survey / ref-floor honesty (absolute vs perfect-ref relative)  
**Parent pulses:** US10135667B1 **abstract ingest ADMITTED** as Amb spine ([`DIGESTION_ABSTRACT_INGEST.md`](DIGESTION_ABSTRACT_INGEST.md); patent-facing **≤1 m xy**; **DGPS ~0.4–0.5 m** absolute floor named) · first-pulse fog naming **ADMITTED** (C1/C2/C3 SUCCEED) · **#0 GEOM0 HARDEN** ([`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md); **median-not-p90**; 1 ns p90 ≈ **1.16 m**; **perfect-ref** assumed) · **MULTIPATH1 Soften** ([`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md); LOS + mild/intermittent NLOS only) · **SYNC1 Soften** ([`SCORE_SYNC_1.md`](SCORE_SYNC_1.md); Chan-alone near-ideal `σ_sync ≲ 0.3 ns`) · **JOINT1 Soften** ([`SCORE_JOINT1.md`](SCORE_JOINT1.md); `σ_sync ≲ 3 ns` **fixed offsets**) · **DRIFT1 HARDEN** ([`SCORE_DRIFT1.md`](SCORE_DRIFT1.md); named batch α restores SYNC1 drift breakers) · **GATE1 Soften** ([`SCORE_GATE1.md`](SCORE_GATE1.md); detect-only refuse belt)  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_A1.md`](DIGESTION_A1.md)  
**Ingest triad (prior):** [`ABSTRACT_INGEST_SUMMARY.md`](ABSTRACT_INGEST_SUMMARY.md) · [`PROPOSED_ABSTRACT_INGEST.md`](PROPOSED_ABSTRACT_INGEST.md) · [`SOURCE.md`](SOURCE.md)  
**Copy gate (prior):** [`COPY_GATE.md`](COPY_GATE.md)  
**Greer-facing write-up (Founder PRIMARY; HOLD send until suite digests):** [`GREER_WRITEUP.md`](GREER_WRITEUP.md)  
**Lab audit draft:** [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master.

**What this is not:** A locator. Claim clearance. Hardware **X**. Skill-met. RF fingerprinting / ML. GPS/DGPS as the mobile fix. A product copied from US10135667B1. A multipath-robust 0.50 m. A free per-epoch realtime drift claim. An absolute ≤0.50 m under the RN floor. A reason to Harden absolute **X**. A send to Greer. Reopening cell-tower as live. Reopening BIA→weight. Rithm. A p90 bar. Claim-language product copy.

---

## 0. Plain-language framing

**What this is:** A cheap honesty pulse on how well we know the reference-node positions. Prior GEOM0 locked **sim X = 0.50 m** under **perfectly known refs**. This pulse injects DGPS-class RN survey error (`σ_ref`) and scores **absolute** median error vs truth.

**What this settles:** **Soften** (Kill **not** triggered). Patent-facing **absolute ≤1 m** is poseable under DGPS-class RN survey error. **Absolute ≤0.50 m is not** under that RN floor. **X = 0.50 m** stays **perfect-ref scoped sim only**. JOINT1 can scrape under 0.50 m absolute while riding the floor — **do not Harden absolute X**. Silent perfect-ref “absolute ≤0.50” language from prior GEOM0 is **Softened**.

**What this is not:** Not a field locator. Not a hardware bar. Not a p90 bar. Not claim clearance. Not a multipath-robust claim. Not free per-epoch realtime. Not a reason to invent RF, ML, or fingerprints. Not a send to Greer (write-up is **HOLD** until the A2→A3→A4 suite digests).

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Method | Frozen Chan 1994 2D WLS; absolute median vs truth under RN survey error |
| RN survey injection | `σ_ref` (DGPS-class; **~0.4–0.5 m** named floor) |
| Timing noise | `σ_t` = **1 ns** (Chan abs rows) |
| Standing pulses | **abstract ingest ADMIT** · **GEOM0 HARDEN** (perfect-ref) · **MULTIPATH1 Soften** · **SYNC1 Soften** · **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) · **DRIFT1 HARDEN** · **GATE1 Soften** |
| X honesty | **X = 0.50 m** = **perfect-ref** scoped sim only (**median-not-p90**; 1 ns p90 ≈ **1.16 m**). **Not** an absolute bar under the RN floor |
| Patent-facing bar | **≤1 m xy** (stands) |
| GPS / DGPS | never the mobile fix (place/time refs only, if used at all). DGPS-class error here is the **RN survey floor**, not a mobile fix |

This fold does **not** re-run the sim. Numbers are the gated Lab summary.

**Honesty on the floor:** A JOINT1 scrape under 0.50 m absolute at `σ_ref = 0.5` / `σ_sync = 0` **rides the floor**. That scrape is **not** a Harden of absolute **X**.

---

## 2. Lab score (copied from the gate)

| Condition | Absolute median Euclidean error |
|-----------|--------------------------------|
| Chan `σ_ref` = **0.4 m**, `σ_t` = 1 ns | **0.691 m** — **fails** absolute ≤0.50 m; **under** patent-facing ≤1 m |
| Chan `σ_ref` = **0.5 m**, `σ_t` = 1 ns | **0.832 m** — **fails** absolute ≤0.50 m; **under** patent-facing ≤1 m |
| JOINT1 scrape `σ_ref` = **0.5 m**, `σ_sync` = 0 | **0.449 m** — scrapes under 0.50 m; **rides the floor** — **do not Harden** absolute **X** |

**Soften (Operator). Kill not triggered.**

- **Absolute ≤1 m** is **poseable** under DGPS-class RN survey error (Chan abs median **0.832 m** @ `σ_ref = 0.5 m`, `σ_t` = 1 ns).
- **Absolute ≤0.50 m** is **not** under the RN floor (**0.691 / 0.832** at 0.4 / 0.5).
- **X = 0.50 m** stays **perfect-ref scoped sim only**.
- JOINT1 scrape abs **0.449** @ `σ_ref = 0.5` / `σ_sync = 0` rides the floor — **do not Harden absolute X**.
- **Not Kill.**

Do **not** claim hardware. Do **not** send the Greer write-up until the A2→A3→A4 suite digests. Do **not** copy patent claim language.

---

## 3. Combined X scope (standing)

Two bars stay distinct:

1. **Patent-facing ≤1 m xy** — **stands**. Poseable under DGPS-class RN survey error on this board (Chan abs **0.832 m** @ `σ_ref = 0.5 m`, `σ_t` = 1 ns).
2. **Sim X = 0.50 m** — **perfect-ref scoped sim only** (ideal-known refs + named GEOM0 noise + prior JOINT1 fixed-offset + named DRIFT1 batch α + GATE1 refuse-belt + mild NLOS; **median-not-p90**). **Not** an absolute bar under the RN floor. **Not** a patent promise.

**Named RN floor:** **DGPS ~0.4–0.5 m** absolute. Chan abs **0.691 m** @ 0.4 and **0.832 m** @ 0.5 sit **above** 0.50 m and **below** 1 m.

Prior scopes that still stand **under perfect-ref sim X = 0.50 m** (not as absolute):

1. **GATE1 Soften** — detect-only refuse OR (G1a residual ∨ G1b raw LORO). FA ≈ **0.10** in-band; TD high out-of-band. **Not** a repair.
2. **DRIFT1 HARDEN** — batch path-shared τ + linear α restores SYNC1 drift breakers. Path-shared **batch**, **not** free per-epoch realtime.
3. **`σ_sync ≲ 3 ns` under JOINT1** — path-shared joint clocks; **fixed offsets**.
4. Prior **MULTIPATH1 Soften** — **LOS + mild/intermittent NLOS only**.
5. **Median-not-p90** honesty (1 ns p90 ≈ **1.16 m**).
6. **GEOM0 HARDEN** still stands as **geometry-not-bottleneck under perfect refs + named noise**. Silent perfect-ref **absolute-≤0.50** language from that pulse is **Softened**.
7. **SYNC1 Soften** still stands as the Chan-alone near-ideal window.

**Fails / out of this budget (do not invent a rescue):**

- Absolute **≤0.50 m** under DGPS-class `σ_ref` (Chan **0.691 / 0.832** at 0.4 / 0.5).
- Treating the JOINT1 scrape (**0.449 m** @ `σ_ref = 0.5` / `σ_sync = 0`) as a Harden of absolute **X**.
- Strong multipath. **Not multipath-robust.** **A3** (indoor / first-arrival) is next-after-A2, not this fold.
- Hardware / spectrum path. **Hardware X PARKED.**
- Free per-epoch realtime drift. **A4** is later.

Do **not** invent fingerprint / ML / RF to rescue the RN floor, loose sync, free-epoch drift, or strong multipath.

---

## 4. Operator gate (authoritative)

**Soften.** Kill **not** triggered.

**Copy (gate summary):**

> Soften: Absolute ≤1 m poseable under DGPS-class RN survey error (Chan abs median 0.832 m @ σ_ref=0.5 m, σ_t=1 ns). Absolute ≤0.50 m **not** under RN floor (0.691/0.832 at 0.4/0.5). X=0.50 stays perfect-ref scoped sim only. JOINT1 scrape abs 0.449 @ σ_ref=0.5 / σ_sync=0 rides floor — do not Harden absolute X. Not Kill.
>
> Locks: patent-facing ≤1 m stands; DGPS ~0.4–0.5 m absolute floor named; Soften silent perfect-ref absolute-≤0.50 language from prior GEOM0.
>
> Next locked (user override suite): GO A2 then A3 then A4; Soften/Harden each. Greer send HOLD until suite digests.

**LOCK**

- Patent-facing **≤1 m xy** **stands**.
- **DGPS ~0.4–0.5 m** absolute floor **named**.
- **X = 0.50 m** stays **perfect-ref scoped sim only**. Soften silent perfect-ref absolute-≤0.50 language from prior GEOM0.
- Do **not** Harden absolute **X**.

**NEXT (locked; user override suite):** **GO A2** then **A3** then **A4**. Soften/Harden each.

**PARK** hardware **X**. Link/map GIS/CAD overlay stays **PARKED**.

**HOLD** Lab invent except the locked A2→A3→A4 suite. **HOLD send** of [`GREER_WRITEUP.md`](GREER_WRITEUP.md) until the suite digests. Prior write-up = **sync-fragility evidence only**.

**Honesty locks**

- Absolute ≤1 m poseable under DGPS-class RN survey error. Absolute ≤0.50 m **not**.
- JOINT1 scrape abs **0.449** rides the floor — **not** a Harden of absolute **X**.
- **X = 0.50 m** is perfect-ref scoped sim only. **Not** a patent promise.
- Path-shared **batch** model, **not** free per-epoch realtime.
- Median-not-p90 honesty remains (1 ns p90 ≈ **1.16 m**).
- **GEOM0 HARDEN** still stands as geometry-not-bottleneck under perfect refs. Silent absolute-≤0.50 reading is **Softened**.
- **MULTIPATH1 Soften** still stands. **Not** a multipath-robust claim. **A3** later.
- **SYNC1 Soften** still stands as Chan-alone near-ideal.
- **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) **still stands.**
- **DRIFT1 HARDEN** still stands.
- **GATE1 Soften** still stands. **Not** a repair.
- GPS is **never** the mobile fix.
- This is **not** claim clearance.
- This is **not** a locator.
- This is **not** skill-met.
- This is **not** hardware.
- No fingerprint / ML / RF invent.
- **No claim-language product copy.**

US10135667B1 — owner-requested **collaboration framing** (bibliographic; custom-beacon substrate, **not** a carrier-mast Amb). Published abstract is the **Amb spine** (ingest ADMITTED). **No claim-language copy.** Not a product embodiment.

Cell-tower Amb stays **PARKED**. BIA→weight portfolio stays **CLOSED**. SkyMirr stays its own Amb.

---

## 5. Hard NO

- Do **not** treat **0.50 m** as an **absolute** bar, a hardware bar, a field locator, a **p90** bar, a **multipath-robust** bar, a **free per-epoch realtime** drift bar, or a patent promise.
- Do **not** Harden absolute **X** off the JOINT1 scrape (**0.449 m** @ `σ_ref = 0.5` / `σ_sync = 0`).
- Do **not** silently keep GEOM0’s perfect-ref reading as if it were absolute ≤0.50 m.
- Do **not** drop the patent-facing **≤1 m xy** bar, and do **not** treat it as cleared hardware.
- Do **not** invent fingerprint / ML / RF to rescue the RN floor, loose sync, free-epoch drift, or strong multipath.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / elevated language.
- Do **not** reopen `2026-09_cell-tower-geometry` as live.
- Do **not** reopen the BIA→weight portfolio.
- Do **not** send [`GREER_WRITEUP.md`](GREER_WRITEUP.md) until the A2→A3→A4 suite digests.
- Do **not** unpark hardware **X**. Do **not** unpark link/map. A2 is next; A3/A4 after. Lab invent otherwise is **HOLD**.

---

*Docs only. Soften ≠ claim clearance. RN floor ≠ locator. Perfect-ref sim X ≠ absolute X. Patent-facing ≤1 m stands; is not hardware. Provisional sim X is median-not-p90 and perfect-ref only. Provisional sim X ≠ hardware X. Not skill-met. Not a patent-product claim. Not rithm. No claim-language product copy. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate. Write-up HOLD send until A2→A3→A4 suite digests.*
