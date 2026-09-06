# Technical note: pressure-testing the hard parts of sync-pulse indoor locate

**For:** Kerry Greer  
**Date:** 2026-09-05  

This is laptop simulation evidence plus public timing literature on the hard parts of multi-beacon sync-pulse locate — after reading your patent abstract and independent claims carefully. It is not a product pitch, not patent claim clearance, and not proof that hardware already hits meter-class accuracy under an ordinary 50 kHz waveform.

---

## 1. Purpose

I took the problem your patent is about — GPS-denied indoor locate with perimeter sync-pulse references, DGPS-placed refs, and mobile difference-only timing — and ran it through a research habit I’ve been building: state the claim clearly, name what’s still open, run early checks that could change the claim, then update from the evidence.

This note is what those checks found. I’m not restating claim language as a product. I’m reporting where the story holds in simulation, where it needs to be narrowed, and where it breaks if silent assumptions stay in place.

---

## 2. What “good” means here

| Target | How I’m using it |
|--------|------------------|
| About **1 m** horizontal | Your stated accuracy object from the patent |
| **0.50 m** median | An earlier, stricter simulation pressure bar I used only when reference positions were treated as perfect and timing noise was modeled at about **1 ns**. That is not what the patent promised. |
| Typical DGPS survey about **0.4–0.5 m** | A floor under absolute position. Absolute mobile error cannot honestly beat that without better reference survey. |

I always separate absolute error from error relative to the references. I do not claim absolute half-meter accuracy with DGPS-class references.

---

## 3. Simulation setup

Five fixed beacons in a **40 × 30 m** area. A mobile walked a held-out L-shaped path with 101 samples. The baseline locator was textbook Chan least squares. Later I added estimators that also track relative beacon clock offsets and slow clock drift along the path — ordinary numerical methods, no machine learning and no fingerprint map. Beacon positions are known in the simulation; in hardware they would be surveyed or GPS-placed. GPS was never used to locate the mobile. No radios were built.

---

## 4. Findings

### A. Reference survey floor

With about **0.5 m** random survey error on each reference:

- Absolute median error about **0.83 m** — clears about **1 m**, fails **0.50 m**
- Error relative to the references a bit tighter, about **0.71 m** — still not half-meter absolute honesty

So the old half-meter absolute story assumed perfect reference positions. With your own DGPS baseline named, about **1 m** absolute is the fair bar on this grid.

### B. “Simultaneous” sync after DGPS 1PPS

Public commercial 1PPS residual timing is **nanoseconds to tens of nanoseconds**, not effectively perfect.

| Public residual class | Baseline locator alone | Also estimating relative beacon clocks |
|-----------------------|------------------------|----------------------------------------|
| Best public differential about **2.5 ns** | Harsh; half-meter fails | Still usable in about a **3 ns** band |
| Ordinary commodity / uncorrected about **10–50 ns** | Broken | Broken |

Usable sync on this grid needs relative-clock estimation plus differential or timing-grade residual around **2.5–3 ns** — not the baseline locator plus ordinary absolute 1PPS. Slow drift over a walk is a separate problem: earlier sims showed a matched linear-drift fix helps, while modeling only a constant clock offset can make drift worse.

### C. Leading-edge multipath

Using only the first edge of the pulse does **not** erase indoor multipath at about 50 kHz channel bandwidth.

- Mild or occasional residual range bias can still clear about **1 m** on this grid
- Persistent residual bias around **2–3 m** already fails about **1 m**, and looks worse once the 0.5 m reference floor is included

So the claim only holds for mild, first-path-dominant, or intermittent cases — not “multipath solved.”

### D. Phase-flip detection jitter

A clock running at **1 GHz or faster** is a digitizer floor. It is not the same thing as detection jitter through an approximately **50 kHz** phase-flip channel. Honest detection jitter is still far larger than **1 ns** — tens to hundreds of nanoseconds. On the baseline locator:

- Even an optimistic about **10 ns** of timing noise → median about **3.8 m**, past the 1 m bar
- Mid-range about **200 ns** → tens of meters

Estimating relative beacon clocks does **not** cancel that per-link detection noise. The timing budget has to be narrowed; I have not opened a radio bench yet.

---

## 5. What is not claimed

All of these have to stay named together:

1. Laptop simulation and public timing references only — no radios built  
2. About **1 m** absolute as the main accuracy bar from the patent; **0.50 m** only under perfect references in sim  
3. DGPS-class reference survey about **0.4–0.5 m** always named  
4. Sync usable only with relative-clock estimation and about **2.5–3 ns** differential residual — not ordinary absolute 1PPS alone  
5. Multipath only for mild or intermittent leading-edge residual  
6. Ordinary 50 kHz phase-flip detection noise does **not** support a silent **1 ns** / about **1 m** story under the baseline locator  
7. No fingerprinting or machine learning; GPS not used on the mobile  

Drop a condition and the meter-class story does not automatically follow.

---

## 6. Still open

- A waveform or RF path that actually meets a named detection-jitter budget  
- Strong or persistent multipath  
- Free per-sample clocks with no batch structure  
- Your real success criteria — please confirm or replace the about **1 m** bar and scopes above  
- Hardware accuracy — not measured  

---

## 7. Questions for you

1. Is this the right set of hard problems — reference survey floor, residual sync after 1PPS, leading-edge multipath, waveform detection jitter — or did I still miss what you care about most?  
2. What success bar and conditions should replace the provisional about **1 m** target and the narrowed budgets above?  
3. What should come next — more simulation and literature, or a cheap hardware / waveform path?

---

*Simulation and public-reference evidence only. Not patent claim clearance.*
