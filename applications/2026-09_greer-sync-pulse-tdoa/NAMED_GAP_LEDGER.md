# Named-gap ledger — Greer-style sync-pulse TDOA

Habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). One line per open gap. This is a problem-solving scoreboard, **not** a locator and **not** a product claim.

**Opened:** 2026-09-05 — Founder **CLAIM LOCK** opens a **new** Amb: Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA (contrast prior art US10135667B1 — method practice / explore the idea; not copy claims for product). Lab proposes first-pulse fog + 2–3 cheap checks. Method Operator gates.

**Last check:** 2026-09-05 — Operator **ADMIT MULTIPATH1 Soften**. Kill **not** triggered. Provisional **sim X = 0.50 m** remains **LOCKED** with **NLOS scope annotation** (**median**-not-p90; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED**. Next pulse (**not this fold**): **sync-imperfection**. Score: [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md). Digestion: [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md). Prior #0 HARDEN: [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md). Fog peek: [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md).

**What this is not:** This is **not** rithm. Skill-met is **not** claimed. Peek succeed / #0 HARDEN / MULTIPATH1 Soften is **not** claim clearance, **not** a locator, and **not** a multipath-robust 0.50 m. Training is **not** started and is **not** established. Hardware **X** is **not** locked. Fingerprint rescue is **not** this fold. Patent claims are **not** copied for a product. The cell-tower Amb is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED** and is **not** reopened here.

**Process:** Lab invents; Operator admits, rejects, or parks. Lab does **not** self-admit. After MULTIPATH1, Lab does **not** run sync-imperfection unless that pulse is the live job. Still **no RF / ML**. **No** fingerprint rescue.

**Cell-tower geometry** is **PARKED** (Founder STOP / user pivot; peek #61 + X=300 m on record; A→B halted). This app does **not** reopen it as live.  
**BIA→weight portfolio** is **CLOSED** (human #59 ship demo + kill of the accurate-weight claim; animal parks stay). This app does **not** reopen it.  
**Collatz playground** is **done** (#45). Lab HOLD there (unchanged).  
**Track B invent** remains **paused** (unchanged).  
**llm-gwt R-REPL** remains **parked** (unchanged).

## Claim line (parent; sim X locked NLOS-scoped; hardware X PARKED)

`on a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) recovers mobile position with median error ≤ 0.50 m on a held-out path inside a GPS-denied box, without RF fingerprint training` → kill vs succeed: fail closed if the path is not laptop-feasible **or** GPS/DGPS is smuggled in as the mobile fix **or** the path is RF-fingerprint training **or** **X** is silently read as p90; succeed later would need a held-out **median** ≤ **0.50 m** under the lock **and** must not silently drop the honesty locks (ideal sync assumed; **X is median-not-p90**; NLOS scope = LOS + mild/intermittent only) → last check: 2026-09-05 Operator **MULTIPATH1 Soften** — frozen Chan 1994; `σ_t`=1 ns; positive range-bias; same refs/L-path as #0; baseline **0.364 m**; `random_k=1` `b=0.5` → **0.476 m**; `epoch_f=0.25` `b=1` → **0.452 m**; strong persistent `b≥1–2 m` → **0.73–4.7+ m** (not poseable with Chan alone); p90 ≈ **1.16 m** @ 1 ns LOS; provisional **sim X = 0.50 m** **NLOS-scoped** (**median**-not-p90) → status: **open** / **Soften** (sim **X** locked, NLOS-scoped, median-not-p90; **not** claim clearance; **not** multipath-robust; hardware **X PARKED**)

## Geometry leftover (#0)

`planar TDOA geometry bottleneck (frozen Chan 1994 2D WLS; ideal simultaneous sync + Gaussian Δt only)` → kill vs harden: geometry blows the median off the `c · σ_t` scale vs median tracks `c · σ_t` with a frozen Chan estimator → last check: 2026-09-05 Operator **ADMIT HARDEN** — 1 ns median **0.361 m** / p90 ≈ **1.16 m**; 3 ns median **1.081 m**; 0 failures; geometry is **not** the bottleneck under those idealizations; **X is median-not-p90** → status: **hardened**

## Honest-fog lines

`spectrum / hardware vs sim-only` → kill vs succeed: a hardware **X** is required and no laptop-feasible sim/prototype path can be posed → sim-only (or hardware) must be named before **X**; a laptop-feasible sim/prototype path is poseable from public refs / assumptions → last check: 2026-09-05 **C1 SUCCEED** then **#0** locked **sim X = 0.50 m**; hardware **not** required to name a sim **X** → status: **hardened** (sim-only named)

`hardware X` → kill vs succeed: a later gate names a hardware / spectrum path that can carry its own **X** vs stay parked while the live path is sim-only → last check: 2026-09-05 Operator **PARK** hardware **X** (MULTIPATH1 Soften does **not** unpark it) → status: **paused** / **PARKED**

`clock resolution / simultaneous-sync assumption` → kill vs succeed: no public-ref / assumption statement can even pose ≥3-ref simultaneous-sync TDOA → **fail closed** or park; a named clock/sync assumption makes the estimator class poseable (still not a locator) → last check: 2026-09-05 **C2 SUCCEED** (story named) then **#0 assumed** that ideal simultaneous sync — leftover honesty about **imperfection** stays unopened → status: **hardened** (clock story named; still not a locator)

`sync-imperfection` → kill vs harden: a later pulse that injects clock / sync error and shows the NLOS-scoped 0.50 m sim bar does not survive vs a pulse that keeps the bar under named imperfection → last check: 2026-09-05 Operator **ADMIT** as next pulse after MULTIPATH1 Soften; **not run** this fold → status: **open** / **admitted as next pulse, not run**

`multipath in a GPS-denied box` → kill vs succeed: this is standing honesty, not a hunt — a denied box is a hard radio environment; do **not** silently drop multipath; Kill = 0.50 m not poseable even under LOS / mild NLOS vs Soften = 0.50 m stays with NLOS scope vs Harden = multipath-robust 0.50 m → last check: 2026-09-05 Operator **ADMIT Soften** — Kill **not** triggered; poseable under LOS + mild/intermittent NLOS; **not** poseable under strong persistent multipath with frozen Chan alone; **no** fingerprint rescue; **X** median-not-p90 → status: **restated** / **Soften** (NLOS-scoped; not multipath-robust)

`multipath / NLOS positive-bias injection (same frozen Chan)` → kill vs harden: inject positive NLOS / multipath bias under the **same** Chan 1994 and show whether the **median** 0.50 m bar survives → last check: 2026-09-05 Operator **ADMIT Soften** (Kill not triggered) — baseline **0.364 m**; mild/intermittent **0.476 m** / **0.452 m**; strong persistent **0.73–4.7+ m** → status: **restated** / **Soften** (scored; NLOS-scoped)

## First-pulse data / measurement line

`public refs + sync assumptions + measurement availability for a laptop-feasible sim/prototype path` → kill vs succeed: no usable public refs / assumptions / measurement story → **DATA-BLOCKED park** or sim-only Soften (must be said); a citable public-ref / assumption peek that names fog and whether **X** is sim-geometry vs hardware → peek succeed (**not** claim clearance) → last check: 2026-09-05 fog naming **ADMITTED** — C1/C2/C3 **SUCCEED**; **X** class = sim-geometry first → status: **killed** / **PASS** (peek succeed; **not** claim clearance)

## #0 pulse (scored)

`#0 geometry-bottleneck sim` → kill vs succeed: a laptop, no-RF sim using **frozen textbook multilateration only** that can freeze a numeric sim **X** vs a pose that still cannot score a held-out path → last check: 2026-09-05 Operator **ADMIT HARDEN** — Chan 1994 2D WLS; numeric **sim X = 0.50 m** (**median**-based @ 1 ns; **median-not-p90**; 1 ns p90 ≈ **1.16 m**); geometry not the bottleneck → status: **hardened** (scored; **not** claim clearance)
