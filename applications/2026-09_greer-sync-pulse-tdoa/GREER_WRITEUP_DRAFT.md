# DRAFT — Lab PROPOSED digest; Lab does not admit; Operator/Founder may edit before send

**Status:** PROPOSED technical summary of sim evidence under named budgets. **Sync-fragility evidence only** after abstract ingest — not a patent-hard-problem digest.  
**lab_admits:** false  
**Date:** 2026-09-05  
**Audience:** Greer (by his request) — collaboration technical digest  
**Not:** a patent write-up, product brief, or claim clearance. **HOLD send** until DIGEST + Founder fold. Suite **A1→A4 Soften** on record. **0.50 m** is perfect-ref scoped sim only (A1 Soften; A4 Soften X/σ_t as honest phase-flip). **RF bench PARKED.**

---

## 1. Purpose

You asked us to dig into the **sync fragility** of multi-reference TDOA on a laptop-feasible simulation. This note is an honest evidence digest of what Lab scored under named budgets. It is **not** a patent write-up, not a product pitch, and not an admission that any success bar is met outside the sim conditions below.

Operator/Founder may edit before send. Lab proposes only; Lab does not admit.

---

## 2. Setup in one paragraph

We simulated **five fixed reference nodes** at known planar coordinates in a **40 × 30 m** box — corners plus mid-bottom: `(0,0), (40,0), (40,30), (0,30), (20,0)`. The mobile walked a held-out **L-path** interior (horizontal then vertical; **101** samples). Timing noise was modeled as Gaussian range-difference noise with σ_d = c · σ_t (light ≈ 0.3 m/ns). The baseline estimator was textbook **Chan (1994)** two-stage weighted least squares; later pulses added joint relative-clock and linear path-drift estimators (still numpy / textbook-style batch WLS / Gauss–Newton — no trained models). In sim, reference positions are known; in a hardware story those would be GPS/DGPS-placed refs only. **GPS was never used as a mobile fix.** No RF hardware was built. No fingerprint / radio-map / ML training.

---

## 3. What “good” meant here

After the geometry pulse, Operator locked a **provisional sim median error target X = 0.50 m** (basis: GEOM0 median **0.361 m** at σ_t = 1 ns, rounded up with margin). That X is a **median** target under named scopes — not a p90 promise (GEOM0 p90 at 1 ns was ≈ **1.16 m**). Hardware X stays parked.

---

## 4. Findings by topic

### Geometry — not the bottleneck (GEOM0 Harden)

| σ_t | Median error (m) | Mean | p90 |
|-----|------------------|------|-----|
| 1 ns | **0.361** | 0.518 | 1.157 |
| 3 ns | **1.081** | 1.583 | 3.382 |

Zero-noise recovery ≈ numerical zero. Medians track timing-noise scale (~1.2 × σ_d), not a GDOP blow-up. **Geometry + Chan alone look feasible; remaining fog is sync / multipath / hardware.** (`PROPOSED_GEOM0.md`)

### Multipath — mild OK; strong persistent breaks X (MULTIPATH1 Soften)

Under σ_t = 1 ns + frozen Chan:

| Band | Example median (m) | ≤ X=0.50? |
|------|--------------------|-----------|
| Baseline (LOS) | **0.364** | yes |
| Mild (1 random link, bias 0.5 m) | **0.476** | yes |
| Intermittent (25% epochs, bias 1 m) | **0.452** | yes |
| Moderate persistent (bias ≥1 m) | **0.73–0.94** | no |
| Strong persistent (bias ≥2 m) | **1.4–4.7** | no |

**Soften, not Kill:** X stays poseable under LOS + mild/intermittent NLOS; **do not** read this as multipath-robust 0.50 m with Chan alone. (`PROPOSED_MULTIPATH1.md`)

### Bare Chan + sync offsets (SYNC1 Soften)

Primary **fixed_trial** offsets (τ held across the path), σ_t = 1 ns:

| σ_sync (ns) | Median (m) | ≤ X? |
|-------------|------------|------|
| 0 | **0.350** | yes |
| 0.3 | **0.382** | yes |
| 1 | **0.513** | scrapes over |
| 3 | **1.263** | no |
| 10 | **4.549** | no |

**Path drift 3 ns end-to-end alone** (even at σ_sync = 0): median **0.798 m** — breaks X if uncompensated. Honest bare-Chan sync budget on this grid: near-ideal **σ_sync ≲ 0.3 ns**. (`PROPOSED_SYNC1.md`)

### Joint relative-clock WLS (JOINT1 Soften)

Path-shared relative clocks + per-sample pose, scored on the **same** SYNC1 measurements:

| σ_sync (ns) | Chan median | JOINT1 median | JOINT1 ≤ X? |
|-------------|-------------|----------------|-------------|
| 0 | 0.350 | **0.204** | yes |
| 0.3 | 0.382 | **0.203** | yes |
| 1 | 0.513 | **0.231** | yes (restores) |
| 3 | 1.263 | **0.439** | yes |
| 10 | 4.549 | **1.816** | no |

Drift 3 ns/path @ σ_sync = 0: Chan **0.798** / JOINT1 **0.919** — shared-constant clocks are **misspecified** vs a linear ramp and can make drift **worse**. Soften: widen named sync budget under JOINT1 to **σ_sync ≲ 3 ns fixed_trial**; do **not** claim drift-fixed or 10 ns-fixed. (`PROPOSED_JOINT1.md`)

### Linear path-drift α + joint τ (DRIFT1 Harden lean)

Matched linear α (meters-of-range per path-fraction) + shared τ, batch Gauss–Newton:

| Case | Chan | JOINT1 | DRIFT1 | DRIFT1 ≤ X? |
|------|------|--------|--------|-------------|
| drift=3, σ_sync=0 | 0.798 | 0.919 | **0.221** | yes |
| drift=3, σ_sync=0.3 | 0.866 | 0.943 | **0.218** | yes |
| drift=3, σ_sync=1 | 0.963 | 0.914 | **0.222** | yes |
| drift=0 sanity | 0.350 | 0.204 | **0.224** | yes |
| drift=10 OOM | 4.232 | 6.815 | **0.223** | yes |

**Harden lean under a named matched-α budget** (Operator freeze required — Lab still does not admit). Caveats we are blunt about: this is **batch / path-shared**, not free per-epoch realtime clocks; unmatched skew shapes are not claimed. (`PROPOSED_DRIFT1.md`)

### Refuse-gate (GATE1 Soften belt)

Detect-only: residual after DRIFT1 **OR** leave-one-ref-out (raw LORO) scatter. Calibrated to FA ≤ 10% on in-budget σ_sync ≤ 3 ns:

| Quantity | Rate |
|----------|------|
| FA in-budget (σ≤3, drift0) | **~10%** (0.100) |
| FA including matched drift3 | **~8%** (0.080) |
| TD at σ_sync=10 | **~83%** (0.828) |
| TD unmatched model under drift3 | **100%** |
| TD per-epoch wild sync (σ=3) | **100%** |

Honesty: residual-after-DRIFT1 alone **does not** see absorbed fixed_trial σ=10 (clocks soak it); raw LORO carries that detection. **Soften belt, not Harden** — useful refuse companion, not a product UX and not claim insurance. (`PROPOSED_GATE1.md`)

---

## 5. Named budgets stack (honesty)

If Operator scopes stand, **provisional X = 0.50 m median** currently means roughly all of the following together:

- Laptop **sim only**; hardware X **parked**
- **5 refs / 40×30 m / L-path**; textbook Chan → later JOINT1 / DRIFT1 stack
- Timing noise band around **σ_t = 1 ns** (GEOM0 X basis)
- **LOS + mild/intermittent NLOS** only — not strong persistent multipath (`PROPOSED_MULTIPATH1.md` Soften)
- Bare Chan alone: near-ideal sync **σ_sync ≲ 0.3 ns** (`PROPOSED_SYNC1.md`)
- With path-shared JOINT1: fixed_trial **σ_sync ≲ 3 ns**; fails at **10 ns** (`PROPOSED_JOINT1.md`)
- With DRIFT1 matched linear α: SYNC1-style **path drift** (e.g. 3 ns/path) cleared on this grid — **batch / path-shared**, not free realtime (`PROPOSED_DRIFT1.md`)
- GATE1 Soften refuse when residual∪LORO fires out of that budget (`PROPOSED_GATE1.md`)
- **No** RF build, **no** fingerprint/ML, **no** GPS-as-mobile-fix

Drop any of those scopes and the 0.50 m story does not automatically travel with you.

---

## 6. What still fails / open

- **σ_sync ≳ 10 ns** without a better model — JOINT1 median ≈ **1.82 m**; GATE1 can refuse, not magically fix
- **Strong persistent multipath** — Chan alone cannot hold X; fingerprint rescue is forbidden here
- **Hardware X** — parked; no radios built
- **Unmatched realtime free per-epoch clocks** — single-epoch joint is underdetermined; DRIFT1/JOINT1 wins were path-batch shared nuisances
- **Your success criteria** may re-aim X and budgets when you say so; Founder rank stays provisional until then

---

## 7. What we did not do

- No RF hardware / spectrum build  
- No fingerprint, radio-map, or ML training  
- No patent claim-language mapping or product embodiment language  
- No product UX / locator pitch  
- No new sims for this note — numbers are from existing Lab pulses only  

---

## 8. Ask Greer (optional)

1. Does this match the **sync fragility** problem you care about (multi-ref TDOA under imperfect clocks / slow skew)?  
2. What success criteria should replace our provisional **X = 0.50 m** and the named Soften/Harden budgets above?  
3. Anything you want us to dig next — still sim-only, still no claim copy?

---

## Audit trail (Operator)

| Pulse | Board | Gate lean |
|-------|--------|-----------|
| Fog peek | `PROPOSED_FOG_PEEK.md` | Admit fog; lock sim-only |
| Geometry | `PROPOSED_GEOM0.md` | **Harden**; lock X=0.50 m |
| Multipath | `PROPOSED_MULTIPATH1.md` | **Soften** (mild NLOS scope) |
| Sync | `PROPOSED_SYNC1.md` | **Soften** (≲0.3 ns bare Chan) |
| Joint clocks | `PROPOSED_JOINT1.md` | **Soften** (≲3 ns with JOINT1) |
| Path drift | `PROPOSED_DRIFT1.md` | **Harden** lean (matched α) |
| Refuse gate | `PROPOSED_GATE1.md` | **Soften** belt |

Raw medians: `raw/*_metrics.json`.

---

*DRAFT — Lab PROPOSED. Lab does not admit. Not claim clearance. Operator/Founder may edit before send.*
