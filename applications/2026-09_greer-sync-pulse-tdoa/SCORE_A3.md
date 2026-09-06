# A3 leading-edge residual bias — score (Operator-gated Soften)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** A3 — indoor / first-arrival / leading-edge residual bias (denied-box radio; **not** our additive mild-NLOS MULTIPATH1 Soften)  
**Parent pulses:** US10135667B1 **abstract ingest ADMITTED** as Amb spine ([`DIGESTION_ABSTRACT_INGEST.md`](DIGESTION_ABSTRACT_INGEST.md); patent-facing **≤1 m xy**; **DGPS ~0.4–0.5 m** absolute floor named) · **A1 Soften** ([`SCORE_A1.md`](SCORE_A1.md); RN floor; abs ≤1 m poseable; **X = 0.50 m** perfect-ref only) · **A2 Soften (conditional)** ([`SCORE_A2.md`](SCORE_A2.md); JOINT1 + differential ~**2.5 ns** F9T-class path-shared relative-clock; Kill bare Chan ~**1.14 m**; Kill commodity / common-view / absolute-only; Harden unsupported; 50 kHz `c/B` ~**6 km** = **resolution caution only**, **not** injected as fix error) · first-pulse fog naming **ADMITTED** (C1/C2/C3 SUCCEED) · **#0 GEOM0 HARDEN** ([`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md); **median-not-p90**; 1 ns p90 ≈ **1.16 m**; **perfect-ref** assumed) · **MULTIPATH1 Soften** ([`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md); LOS + mild/intermittent NLOS only; **not** A3) · **SYNC1 Soften** ([`SCORE_SYNC_1.md`](SCORE_SYNC_1.md); Chan-alone near-ideal `σ_sync ≲ 0.3 ns`) · **JOINT1 Soften** ([`SCORE_JOINT1.md`](SCORE_JOINT1.md); `σ_sync ≲ 3 ns` **fixed offsets**) · **DRIFT1 HARDEN** ([`SCORE_DRIFT1.md`](SCORE_DRIFT1.md); named batch α restores SYNC1 drift breakers) · **GATE1 Soften** ([`SCORE_GATE1.md`](SCORE_GATE1.md); detect-only refuse belt)  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_A3.md`](DIGESTION_A3.md)  
**A2 (prior Soften, conditional):** [`SCORE_A2.md`](SCORE_A2.md) · [`DIGESTION_A2.md`](DIGESTION_A2.md)  
**A1 (prior Soften):** [`SCORE_A1.md`](SCORE_A1.md) · [`DIGESTION_A1.md`](DIGESTION_A1.md)  
**Ingest triad (prior):** [`ABSTRACT_INGEST_SUMMARY.md`](ABSTRACT_INGEST_SUMMARY.md) · [`PROPOSED_ABSTRACT_INGEST.md`](PROPOSED_ABSTRACT_INGEST.md) · [`SOURCE.md`](SOURCE.md)  
**Copy gate:** [`COPY_GATE.md`](COPY_GATE.md)  
**Greer-facing write-up (Founder PRIMARY; HOLD send until Founder rewrite + user OK):** [`GREER_WRITEUP.md`](GREER_WRITEUP.md)  
**Suite DIGEST (ADMITTED Soften Amb):** [`DIGESTION_A1A4_SUITE.md`](DIGESTION_A1A4_SUITE.md)  
**Lab audit draft:** [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit.

Lab scratch was **not** on this fold VM. Metrics below are copied from the **Operator gate** (authoritative). Hunt scripts / Lab notebooks are **not** on master.

**What this is not:** A locator. Claim clearance. Hardware **X**. Skill-met. RF fingerprinting / ML. GPS/DGPS as the mobile fix. A product copied from US10135667B1. A multipath-robust 0.50 m. A free per-epoch realtime drift claim. An absolute ≤0.50 m under the RN floor. A Harden of indoor / first-arrival. A Kill of the patent-facing ≤1 m bar. A send to Greer. Reopening cell-tower as live. Reopening BIA→weight. Rithm. A p90 bar. Claim-language product copy. Injecting 50 kHz `c/B` ~6 km as fix error.

---

## 0. Plain-language framing

**What this is:** A cheap honesty pulse on indoor / first-arrival leftover. Frozen Chan on the **A1 RN stack** (`σ_ref = 0.5`). Leading-edge residual bias (`B_lb`) and dense multipath (`B_dense`) are injected so denied-box first-arrival is no longer silently dropped as if it were our additive mild-NLOS Soften.

**What this settles:** **Soften** (Kill **not** triggered wholesale). Only **mild / intermittent** leading-edge residual (~**0.5–1 m** bias, or intermittent `f≈0.25`) survives patent-facing **≤1 m** under Chan + RN `σ_ref=0.5`. Persistent `B_lb ≳ 2 m` and `B_dense` **fail ≤1 m**. **Harden unsupported.** Carry **A1 Soften** + **A2 Soften (conditional)**. 50 kHz `c/B` ~**6 km** stays a **resolution caution only** — **not** injected as fix error.

**What this is not:** Not a field locator. Not a hardware bar. Not a p90 bar. Not claim clearance. Not a multipath-robust claim. Not free per-epoch realtime. Not a reason to invent RF, ML, or fingerprints. Not a send to Greer (write-up is **HOLD** until Founder rewrite + user OK). Not a rewrite of MULTIPATH1.

---

## 1. Board (gated)

| Field | Gated record |
|-------|----------------|
| Method | Frozen Chan 1994 2D WLS; absolute median vs truth under the A1 RN stack + leading-edge residual |
| RN survey stack | `σ_ref = 0.5` (A1 Soften stack; DGPS-class floor) |
| Injection | Leading-edge residual `B_lb`; dense multipath `B_dense` |
| Standing pulses | **abstract ingest ADMIT** · **A1 Soften** · **A2 Soften (conditional)** · **A4 Soften X/σ_t** (already on record) · **GEOM0 HARDEN** (named 1 ns model) · **MULTIPATH1 Soften** (additive mild-NLOS; **not** this leftover) · **SYNC1 Soften** · **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) · **DRIFT1 HARDEN** · **GATE1 Soften** |
| A2 honesty (carried) | **JOINT1 + differential ~2.5 ns (F9T-class) path-shared relative-clock**; Kill bare Chan / commodity / common-view / absolute-only; 50 kHz `c/B` ~**6 km** = **resolution caution only**. **Not** injected as fix error on this board |
| X honesty | **X = 0.50 m** = **perfect-ref** scoped sim only (**median-not-p90**; 1 ns p90 ≈ **1.16 m**). **Not** an absolute bar under the RN floor |
| Patent-facing bar | **≤1 m xy** (stands; this pulse scopes when LE residual keeps it poseable) |
| GPS / DGPS | never the mobile fix (place/time refs only, if used at all) |

This fold does **not** re-run the sim. Numbers are the gated Lab summary.

**Honesty vs MULTIPATH1:** MULTIPATH1 Soften is our **additive mild-NLOS** scope on the perfect-ref sim **X**. A3 is the abstract’s **indoor / first-arrival** leftover on the **Chan + RN `σ_ref=0.5`** stack vs patent **≤1 m**. Do **not** collapse them.

---

## 2. Lab score (copied from the gate)

| Condition | Absolute median vs patent-facing ≤1 m |
|-----------|----------------------------------------|
| Mild / intermittent leading-edge residual (~**0.5–1 m** bias, or intermittent `f≈0.25`) | **survives ≤1 m** under Chan + RN `σ_ref=0.5` |
| Persistent `B_lb ≳ 2 m` | **fails ≤1 m** |
| Persistent `B_dense` | **fails ≤1 m** |
| Example `b=2` | abs **1.34 / 1.52** — **fails ≤1 m** |
| Example `b=5` | ~**3.9** — **fails ≤1 m** |

**Soften (Operator). Kill not triggered wholesale. Harden unsupported.**

- Only **mild / intermittent** leading-edge residual (~**0.5–1 m** bias, or intermittent `f≈0.25`) keeps patent-facing **≤1 m** poseable under Chan + RN `σ_ref=0.5`.
- Persistent `B_lb ≳ 2 m` and `B_dense` **fail ≤1 m** (e.g. `b=2` → abs **1.34 / 1.52**; `b=5` → ~**3.9**).
- **Not Kill** of the leftover wholesale — a named mild window survives.
- **Harden unsupported** — persistent first-arrival / dense leftover still blows ≤1 m.
- Carry **A1 Soften** (RN floor; **X = 0.50 m** perfect-ref only; abs ≤1 m poseable under DGPS-class `σ_ref`).
- Carry **A2 Soften (conditional)**. 50 kHz `c/B` ~**6 km** = **resolution caution only**, **not** injected as fix error.

Do **not** claim hardware. Do **not** send the Greer write-up until Founder rewrite + user OK. Do **not** copy patent claim language.

---

## 3. Combined bars (standing)

Two bars stay distinct:

1. **Patent-facing ≤1 m xy** — **stands**, now **A3-scoped**: poseable under mild / intermittent leading-edge residual on the Chan + RN `σ_ref=0.5` stack. **Not** poseable under persistent `B_lb ≳ 2 m` or `B_dense`. **Not** hardware. **Not** claim copy.
2. **Sim X = 0.50 m** — **perfect-ref scoped sim only** (ideal-known refs + named GEOM0 noise + prior JOINT1 fixed-offset + named DRIFT1 batch α + GATE1 refuse-belt + mild NLOS; **median-not-p90**). **Not** an absolute bar under the RN floor. **Not** a patent promise. A3 does **not** restore absolute 0.50 m.

**Named RN floor (A1 Soften, carried):** **DGPS ~0.4–0.5 m** absolute. Chan abs **0.691 m** @ 0.4 and **0.832 m** @ 0.5 sit **above** 0.50 m and **below** 1 m.

**A2 Soften (conditional) (carried):** JOINT1 + differential ~**2.5 ns** F9T-class path-shared relative-clock. Commercial 1PPS does **not** carry either bar. 50 kHz `c/B` ~**6 km** = **resolution caution only**. Do **not** inject ~6 km as a ranging / fix error on this or later boards.

Prior scopes that still stand:

1. **A1 Soften** — abs ≤1 m poseable under DGPS-class RN survey error; abs ≤0.50 m **not**; **X = 0.50 m** perfect-ref only; JOINT1 scrape **0.449** rides the floor — **do not Harden absolute X**.
2. **A2 Soften (conditional)** — JOINT1 + ~2.5 ns F9T-class path-shared relative-clock; 50 kHz `c/B` ~6 km resolution caution only; **not** injected as fix error.
3. **GATE1 Soften** — detect-only refuse OR (G1a residual ∨ G1b raw LORO). **Not** a repair.
4. **DRIFT1 HARDEN** — batch path-shared τ + linear α. Path-shared **batch**, **not** free per-epoch realtime.
5. **`σ_sync ≲ 3 ns` under JOINT1** — path-shared joint clocks; **fixed offsets**.
6. Prior **MULTIPATH1 Soften** — **LOS + mild/intermittent NLOS only** on the perfect-ref sim **X**. **Not** this A3 leftover.
7. **Median-not-p90** honesty (1 ns p90 ≈ **1.16 m**).
8. **GEOM0 HARDEN** still stands as **geometry-not-bottleneck under perfect refs + named noise**. Silent perfect-ref **absolute-≤0.50** language remains **Softened**.
9. **SYNC1 Soften** still stands as the Chan-alone near-ideal window.

**Fails / out of this budget (do not invent a rescue):**

- Persistent `B_lb ≳ 2 m` and `B_dense` vs patent-facing ≤1 m (`b=2` → **1.34 / 1.52**; `b=5` → ~**3.9**).
- Treating A3 Soften as a Harden of indoor / first-arrival.
- Treating A3 as a Kill of ≤1 m wholesale.
- Injecting 50 kHz `c/B` ~6 km as fix error.
- Absolute **≤0.50 m** under DGPS-class `σ_ref`.
- Hardware / spectrum path. **Hardware X PARKED.**
- Free per-epoch realtime drift. Ingest realtime leftover is **not** Hardened (A4 Soften X/σ_t).

Do **not** invent fingerprint / ML / RF to rescue persistent first-arrival, the RN floor, loose sync, or free-epoch drift.

---

## 4. Operator gate (authoritative)

**Soften.** Kill **not** triggered wholesale. Harden **unsupported**.

**Copy (gate summary):**

> Soften: Only mild/intermittent leading-edge residual (~0.5–1 m bias, or intermittent f≈0.25) survives patent ≤1 m under Chan (+ RN σ_ref=0.5 stack). Persistent B_lb ≳2 m and B_dense fail ≤1 m (e.g. b=2 → abs 1.34/1.52; b=5 → ~3.9). Not Kill wholesale; Harden unsupported.
>
> Carry A1 Soften + A2 Soften-conditional. 50 kHz c/B ~6 km = resolution caution only, not injected as fix error.
>
> Next (user override suite): GO A4 then DIGEST suite. Greer send HOLD until suite digests.

**LOCK**

- Patent-facing **≤1 m xy** **stands**, **A3-scoped** to mild / intermittent leading-edge residual on the Chan + RN `σ_ref=0.5` stack.
- Persistent `B_lb ≳ 2 m` and `B_dense` stay **out of budget**.
- **Harden unsupported.**
- Carry **A1 Soften**. Carry **A2 Soften (conditional)**.
- 50 kHz `c/B` ~**6 km** = **resolution caution only**. **Not** injected as fix error.
- **X = 0.50 m** stays **perfect-ref scoped sim only**. Do **not** Harden absolute **X**.

**NEXT:** **A4 Soften X/σ_t** is already on the record ([`SCORE_A4.md`](SCORE_A4.md)). Suite DIGEST Soften Amb **ADMITTED**. Greer send **HOLD** until Founder rewrite + user OK.

**PARK** hardware **X**. Link/map GIS/CAD overlay stays **PARKED**.

**HOLD** Lab invent (no named next pulse). **HOLD send** of [`GREER_WRITEUP.md`](GREER_WRITEUP.md) until Founder rewrite + user OK. Suite DIGEST Soften Amb **ADMITTED**. Prior write-up = **sync-fragility evidence only**.

**Honesty locks**

- Mild / intermittent LE residual survives ≤1 m. Persistent `B_lb ≳ 2 m` and `B_dense` fail.
- **Not Kill** wholesale. **Harden unsupported.**
- **A1 Soften** still stands. **A2 Soften (conditional)** still stands.
- 50 kHz `c/B` ~6 km is **not** a ranging error to inject.
- **X = 0.50 m** is perfect-ref scoped sim only. **Not** a patent promise.
- Path-shared **batch** model, **not** free per-epoch realtime.
- Median-not-p90 honesty remains (1 ns p90 ≈ **1.16 m**).
- **GEOM0 HARDEN** still stands as geometry-not-bottleneck under perfect refs. Silent absolute-≤0.50 reading is **Softened**.
- **MULTIPATH1 Soften** still stands. **Not** a multipath-robust claim. **Not** this A3 leftover.
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
- Do **not** Harden indoor / first-arrival off the mild LE window.
- Do **not** Kill the patent-facing **≤1 m xy** bar wholesale.
- Do **not** treat persistent `B_lb ≳ 2 m` or `B_dense` (`b=2` → **1.34 / 1.52**; `b=5` → ~**3.9**) as a pass.
- Do **not** inject 50 kHz `c/B` ~6 km as fix error.
- Do **not** collapse A3 into MULTIPATH1.
- Do **not** Harden absolute **X** off the JOINT1 scrape (**0.449 m** @ `σ_ref = 0.5` / `σ_sync = 0`).
- Do **not** invent fingerprint / ML / RF to rescue persistent first-arrival, the RN floor, loose sync, or free-epoch drift.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language.
- Do **not** commit Lab scratch / hunt scripts as established.
- Do **not** write skill-met / elevated language.
- Do **not** reopen `2026-09_cell-tower-geometry` as live.
- Do **not** reopen the BIA→weight portfolio.
- Do **not** send [`GREER_WRITEUP.md`](GREER_WRITEUP.md) until Founder rewrite + user OK.
- Do **not** unpark hardware **X**. Do **not** unpark link/map. Do **not** unpark RF bench. Lab invent is **HOLD**.

---

*Docs only. Soften ≠ claim clearance. Mild LE window ≠ Harden. Persistent B_lb / B_dense ≠ pass. RN floor ≠ locator. Perfect-ref sim X ≠ absolute X. Patent-facing ≤1 m stands, A3-scoped; is not hardware. 50 kHz c/B ~6 km is resolution caution only. Provisional sim X is median-not-p90 and perfect-ref only. Provisional sim X ≠ hardware X. Suite DIGEST Soften Amb ADMITTED. Not skill-met. Not a patent-product claim. Not rithm. No claim-language product copy. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate. Write-up HOLD send until Founder rewrite + user OK.*
