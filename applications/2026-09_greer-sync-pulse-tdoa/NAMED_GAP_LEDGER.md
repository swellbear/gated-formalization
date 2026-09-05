# Named-gap ledger — Greer-style sync-pulse TDOA

Habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). One line per open gap. This is a problem-solving scoreboard, **not** a locator and **not** a product claim.

**Opened:** 2026-09-05 — Founder **CLAIM LOCK** opens a **new** Amb: Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA (contrast prior art US10135667B1 — method practice / explore the idea; not copy claims for product). Lab proposes first-pulse fog + 2–3 cheap checks. Method Operator gates.

**Last check:** 2026-09-05 — Founder / Operator **REOPEN** sync-fragility solve-target (not park forever). DIGEST baseline **preserved**. **GEOM0 HARDEN** still stands. **MULTIPATH1 Soften** still stands (LOS + mild/intermittent NLOS only). **SYNC1 Soften** still stands (`σ_sync ≲ 0.3 ns`). Hardware **X PARKED**. REOPEN digestion: [`DIGESTION_REOPEN_SYNC.md`](DIGESTION_REOPEN_SYNC.md). SYNC1 score: [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md). DIGEST baseline: [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md). Prior MULTIPATH1: [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md). #0: [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md). Fog peek: [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md).

**Founder DIGEST (baseline preserved):** Geometry+Chan is feasible under ideal sync; provisional sim X=0.50 m is median@1ns RX noise and only honest under mild NLOS + near-ideal inter-ref sync (σ_sync≲0.3 ns); strong multipath or σ_sync≳1 ns / path drift fail Chan alone; remaining live fog = sync fidelity + multipath (not hyperbolic geometry); contrast Greer US10135667B1 remains custom-beacon substrate, not carrier-mast Amb. Hardware X PARKED. The prior HOLD / “park until reopen” clause is what this fold **fires**.

**What this is not:** This is **not** rithm. Skill-met is **not** claimed. Soften / #0 HARDEN / REOPEN is **not** claim clearance, **not** a locator, and **not** a multipath-robust 0.50 m. This is **not** a remake of commercial RTLS. Training is **not** started and is **not** established. Hardware **X** is **not** locked. Fingerprint / ML / RF invent is **not** a rescue of loose sync. Patent claims are **not** copied for a product. The cell-tower Amb is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED** and is **not** reopened here.

**Process:** Lab invents; Founder / Operator admits, rejects, or parks. Lab does **not** self-admit. Founder / Operator **REOPEN** lifts Lab **HOLD** for the **invent board only**. First pulse after REOPEN (**not this fold**): Lab invents 2–3 cheap-check options for (A)/(B); Founder ranks. Multipath wave-2 after the sync string clears or parks. Still **no RF / ML**. **No** fingerprint rescue. **Not** a remake of commercial RTLS.

**Cell-tower geometry** is **PARKED** (Founder STOP / user pivot; peek #61 + X=300 m on record; A→B halted). This app does **not** reopen it as live.  
**BIA→weight portfolio** is **CLOSED** (human #59 ship demo + kill of the accurate-weight claim; animal parks stay). This app does **not** reopen it.  
**Collatz playground** is **done** (#45). Lab HOLD there (unchanged).  
**Track B invent** remains **paused** (unchanged).  
**llm-gwt R-REPL** remains **parked** (unchanged).

## Claim line (parent; sim X locked; sync + NLOS scoped; hardware X PARKED)

`on a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) recovers mobile position with median error ≤ 0.50 m on a held-out path inside a GPS-denied box, without RF fingerprint training` → kill vs succeed: fail closed if the path is not laptop-feasible **or** GPS/DGPS is smuggled in as the mobile fix **or** the path is RF-fingerprint training **or** **X** is silently read as p90; succeed later would need a held-out **median** ≤ **0.50 m** under the lock **and** must not silently drop the honesty locks (near-ideal sync; LOS + mild/intermittent NLOS; **X is median-not-p90**) → last check: 2026-09-05 Founder / Operator **REOPEN** after **SYNC1 Soften** — frozen Chan 1994; `σ_t`=1 ns; same refs/L-path; `σ_sync≲0.3 ns` median **0.382 m** ≤ X; `σ_sync`=1 ns scrapes **0.513 m**; `≥3 ns` / 3 ns path drift **fails X**; prior **MULTIPATH1 Soften** (baseline **0.364 m**; mild **0.476** / **0.452**; strong **0.73–4.7+ m**); **GEOM0 HARDEN** still stands; 1 ns **p90 ≈ 1.16 m** → status: **open** / **REOPEN** (sim **X** remains, **scoped** to near-ideal sync + mild NLOS; **median-not-p90**; sync-fragility solve-target live; **not** claim clearance; hardware **X PARKED**)

## Geometry leftover (#0)

`planar TDOA geometry bottleneck (frozen Chan 1994 2D WLS; ideal simultaneous sync + Gaussian Δt only)` → kill vs harden: geometry blows the median off the `c · σ_t` scale vs median tracks `c · σ_t` with a frozen Chan estimator → last check: 2026-09-05 Operator **ADMIT HARDEN** — 1 ns median **0.361 m** / p90 ≈ **1.16 m**; 3 ns median **1.081 m**; 0 failures; geometry is **not** the bottleneck under those idealizations; **X is median-not-p90** → status: **hardened**

## Honest-fog lines

`spectrum / hardware vs sim-only` → kill vs succeed: a hardware **X** is required and no laptop-feasible sim/prototype path can be posed → sim-only (or hardware) must be named before **X**; a laptop-feasible sim/prototype path is poseable from public refs / assumptions → last check: 2026-09-05 **C1 SUCCEED** then **#0** locked **sim X = 0.50 m**; hardware **not** required to name a sim **X** → status: **hardened** (sim-only named)

`hardware X` → kill vs succeed: a later gate names a hardware / spectrum path that can carry its own **X** vs stay parked while the live path is sim-only → last check: 2026-09-05 Operator **PARK** hardware **X** (MULTIPATH1 Soften does **not** unpark it) → status: **paused** / **PARKED**

`clock resolution / simultaneous-sync assumption` → kill vs succeed: no public-ref / assumption statement can even pose ≥3-ref simultaneous-sync TDOA → **fail closed** or park; a named clock/sync assumption makes the estimator class poseable (still not a locator) → last check: 2026-09-05 **C2 SUCCEED** (story named) then **#0 assumed** that ideal simultaneous sync — leftover honesty about **imperfection** stays unopened → status: **hardened** (clock story named; still not a locator)

`sync-imperfection (SYNC1)` → kill vs soften: injected clock / sync error blows the 0.50 m sim bar with no surviving named window vs a named near-ideal window keeps the bar (Kill not triggered) → last check: 2026-09-05 Operator **ADMIT Soften** — `σ_sync≲0.3 ns` median **0.382 m** ≤ X; `σ_sync`=1 ns scrapes **0.513 m**; `≥3 ns` / 3 ns path drift **fails X**; do **not** invent fingerprint / ML / RF to rescue loose sync → status: **killed** / **Soften** (bar remains; scoped to near-ideal sync; DIGEST baseline preserved)

`sync-fragility solve-target (REOPEN)` → kill vs harden: (A) a named Soften that keeps provisional **sim X = 0.50 m** when `σ_sync` goes **beyond 0.3 ns** / drift **without** fingerprint / ML invent **or** (B) a measurement-only detector that flags when sync left the near-ideal band and then Softens / widens **X** or **refuses a point fix** → last check: 2026-09-05 Founder / Operator **REOPEN** (solve framing; invent board **not run**) → status: **open** / **REOPEN** (Lab HOLD lifted for this invent board only)

`multipath wave-2` → kill vs succeed: a later textbook pulse after the sync string **clears or parks** vs start now and split the solve → last check: 2026-09-05 Founder / Operator **park until sync string clears or parks** → status: **paused** / **PARKED** (after sync)

`multipath in a GPS-denied box` → kill vs succeed: this is standing honesty, not a hunt — a denied box is a hard radio environment; do **not** silently drop multipath; Kill = 0.50 m not poseable even under LOS / mild NLOS vs Soften = 0.50 m stays with NLOS scope vs Harden = multipath-robust 0.50 m → last check: 2026-09-05 Operator **ADMIT Soften** — Kill **not** triggered; poseable under LOS + mild/intermittent NLOS; **not** poseable under strong persistent multipath with frozen Chan alone; **no** fingerprint rescue; **X** median-not-p90 → status: **restated** / **Soften** (NLOS-scoped; not multipath-robust)

`multipath / NLOS positive-bias injection (same frozen Chan)` → kill vs harden: inject positive NLOS / multipath bias under the **same** Chan 1994 and show whether the **median** 0.50 m bar survives → last check: 2026-09-05 Operator **ADMIT Soften** (Kill not triggered) — baseline **0.364 m**; mild/intermittent **0.476 m** / **0.452 m**; strong persistent **0.73–4.7+ m** → status: **restated** / **Soften** (scored; NLOS-scoped)

## First-pulse data / measurement line

`public refs + sync assumptions + measurement availability for a laptop-feasible sim/prototype path` → kill vs succeed: no usable public refs / assumptions / measurement story → **DATA-BLOCKED park** or sim-only Soften (must be said); a citable public-ref / assumption peek that names fog and whether **X** is sim-geometry vs hardware → peek succeed (**not** claim clearance) → last check: 2026-09-05 fog naming **ADMITTED** — C1/C2/C3 **SUCCEED**; **X** class = sim-geometry first → status: **killed** / **PASS** (peek succeed; **not** claim clearance)

## Scored pulses

`#0 geometry-bottleneck sim (GEOM0)` → kill vs succeed: a laptop, no-RF sim using **frozen textbook multilateration only** that can freeze a numeric sim **X** vs a pose that still cannot score a held-out path → last check: 2026-09-05 Operator **ADMIT HARDEN** — Chan 1994 2D WLS; numeric **sim X = 0.50 m** (**median**-based @ 1 ns; **median-not-p90**; 1 ns p90 ≈ **1.16 m**); geometry not the bottleneck → status: **hardened** (scored; **not** claim clearance; still stands)

`SYNC1 sync-imperfection` → kill vs soften: loose sync / path drift kills the 0.50 m bar with no named window vs a near-ideal window keeps the bar → last check: 2026-09-05 Operator **ADMIT Soften** — near-ideal `σ_sync≲0.3 ns` keeps median **0.382 m**; 1 ns scrapes; ≥3 ns / path drift fails → status: **killed** / **Soften** (scored; **not** claim clearance)

`REOPEN invent board — 2–3 cheap-check options for (A)/(B)` → kill vs succeed: Lab invents ranked cheap checks that could kill or harden the sync-fragility leftover; Founder ranks; **not** fingerprint / ML; **not** commercial RTLS remake → last check: 2026-09-05 Founder / Operator **authorized, not run** → status: **open** / **awaiting next pulse**

`MULTIPATH1 multipath-bias` → kill vs soften: any NLOS kills the 0.50 m bar vs a named mild window keeps it → last check: 2026-09-05 Operator **MULTIPATH1 Soften** — LOS + mild/intermittent NLOS only → status: **restated** / **Soften** (prior; **not** claim clearance)
