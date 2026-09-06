# Technical note: sync fragility in multi-beacon TDOA (simulation evidence)

**For:** Kerry Greer (at your request)  
**From:** swellbear / gated-formalization collaboration  
**Date:** 2026-09-05  
**Status:** **Sync-fragility evidence only.** Not the send-candidate. Not a patent-hard-problem digest. Not a product pitch. Not a patent filing. Not a claim that hardware performance is proven. Founder send-candidate is [`GREER_WRITEUP_SEND.md`](GREER_WRITEUP_SEND.md) (**Soften-admit**; **HOLD send** until user OK). Suite DIGEST **Soften Amb ADMITTED**. Patent-facing bar **≤1 m xy** stands as object — **A4 J_stretch ~10 ns → ~3.8 m fails it**. **0.50 m** is **perfect-ref scoped sim only** — **Soften X/σ_t** as honest 50 kHz phase-flip (not GEOM0 1 ns). **DGPS ~0.4–0.5 m** is the named absolute floor. **RF bench PARKED.**

---

## 1. Purpose

You asked us to dig into a hard part of GPS-denied locate with multiple reference beacons: **what happens when the beacons are not perfectly time-aligned**.

This note summarizes what we measured in simulation. We are not restating or practicing patent claim language as a product. We are reporting evidence on sync fragility and what textbook fixes do (and do not) buy.

---

## 2. Setup (one paragraph)

Five fixed beacons at known positions in a **40 × 30 m** area. A mobile walked a held-out L-shaped path (101 samples). Timing noise was modeled as Gaussian range-difference noise (about **0.3 m per nanosecond** of timing error). The baseline locator was textbook Chan (1994) least squares. Later we added estimators that also track relative beacon clock offsets and slow clock drift along the path — still ordinary numerical methods, **no machine learning and no fingerprint map**. Beacon positions are known in sim (in hardware they would be surveyed / GPS-placed). **GPS was never used to locate the mobile.** No radios were built.

---

## 3. What “good” meant here

We used a provisional target: **median location error ≤ 0.50 m** under the conditions named below. That is a **median**, not a “almost always” promise (at 1 ns receiver noise alone, the 90th percentile was already about **1.2 m**). It is also **perfect-ref scoped sim only** — under DGPS-class reference-node survey error the absolute median sits above 0.50 m and under the patent-facing **≤1 m** bar (A1). A hardware accuracy target is still open.

---

## 4. Findings

### Geometry is not the hard part

With perfect sync and only receiver timing noise:

| Receiver timing noise | Median error |
|-----------------------|--------------|
| 1 ns | **0.36 m** |
| 3 ns | **1.08 m** |

With zero noise, the locator recovers the true path. So the hyperbola math works; the fragile pieces are elsewhere.

### Bad reflections (multipath)

Mild / occasional positive range bias can stay under 0.50 m. Strong, stuck multipath pushes medians into **meters**. So **0.50 m is not “multipath-proof”** with the baseline locator alone.

### When beacons fall out of sync (baseline locator)

| Sync mess between beacons | Median error | Under 0.50 m? |
|---------------------------|--------------|---------------|
| none | 0.35 m | yes |
| 0.3 ns | 0.38 m | yes |
| 1 ns | 0.51 m | barely no |
| 3 ns | 1.26 m | no |
| 10 ns | 4.55 m | no |

Also: a slow **3 ns drift over one walk**, even with otherwise perfect sync, broke the bar (**~0.80 m** median) if left uncompensated.

### Fix 1 — also estimate relative beacon clocks while locating

| Sync mess | Baseline median | With clock estimates | Under 0.50 m? |
|-----------|-----------------|----------------------|---------------|
| 1 ns | 0.51 m | **0.23 m** | yes |
| 3 ns | 1.26 m | **0.44 m** | yes |
| 10 ns | 4.55 m | **1.82 m** | no |

That widens the usable sync band for **fixed** offsets to about **≤ 3 ns**. It does **not** fix walk-long drift (and can make drift worse if you only model a constant offset).

### Fix 2 — also estimate slow drift along the walk

Under the same **3 ns-per-walk** drift that broke things before:

| Estimator | Median error |
|-----------|--------------|
| Baseline | 0.80 m |
| Clocks only (constant) | 0.92 m |
| Clocks + linear drift | **0.22 m** |

So matched slow drift is recoverable in this batch simulation. Caveat: this used **path-batch** shared parameters — not a claim of free per-moment realtime clocks with no structure.

### Safety belt — refuse a fake precise point

We also tested a simple “does this look too inconsistent?” check (residuals + leave-one-beacon-out scatter):

- When sync is still in the good band: false alarm about **10%**
- When sync is badly out (10 ns) or the wrong model is used under drift: catch rate about **83–100%**

Use: **widen the error bar or refuse a point fix** when the check fires — not a magic accuracy repair.

---

## 5. Honest stack (what 0.50 m currently means — perfect-ref sim only)

All of these together, in simulation:

1. Laptop sim only (no radios built yet)  
2. This geometry / path / textbook estimator stack  
3. **Perfectly known** beacon positions (A1: under DGPS-class survey error, absolute median is not ≤0.50 m)  
4. About **1 ns** receiver timing noise as the X basis  
5. Mild multipath only — not strong stuck reflections  
6. With clock+drift estimators: fixed sync mess up to about **3 ns**; matched linear walk drift cleared on this grid  
7. Refuse-belt when measurements leave that band  
8. No fingerprinting / ML; GPS not used on the mobile  

Drop a condition and the half-meter story does not automatically follow. The patent-facing **≤1 m** bar is a different object.

---

## 6. Still open

- Very large sync mess (**~10 ns**) — refuse helps; it does not restore 0.50 m  
- Strong multipath — not solved here  
- Reference-node survey error — absolute ≤0.50 m is **not** under a DGPS-class RN floor; patent-facing **≤1 m** still looks poseable on that board  
- Real hardware accuracy — not measured  
- Free per-sample clocks with no batch structure — not claimed  
- **Your success criteria** — please confirm or replace our provisional 0.50 m (perfect-ref sim) and ≤1 m (patent-facing) bars  
- **Phase-flip detection jitter (A4)** — honest 50 kHz J_stretch ~10 ns is already ~3.8 m (fails ≤1 m); J_mid is tens of meters; JOINT1 does not cancel it; RF bench parked  


---

## 7. Questions for you

1. Is **sync fragility** (imperfect beacon timing / slow skew) the problem you wanted us on?  
2. What success bar should replace provisional **0.50 m median**?  
3. What should we dig next — still sim-only, or a cheap hardware path?

---

*Draft for your review before any send. Evidence only; not patent claim clearance.*
