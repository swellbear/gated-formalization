# Named-gap ledger — Greer-style sync-pulse TDOA

Habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). One line per open gap. This is a problem-solving scoreboard, **not** a locator and **not** a product claim.

**Opened:** 2026-09-05 — Founder **CLAIM LOCK** opens a **new** Amb: Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA (contrast prior art US10135667B1 — method practice / explore the idea; not copy claims for product). Lab proposes first-pulse fog + 2–3 cheap checks. Method Operator gates.

**Last check:** 2026-09-05 — Operator **ADMIT #0 HARDEN** (after fog peek C1/C2/C3 SUCCEED). Under ideal simultaneous sync + Gaussian Δt only, planar TDOA geometry with frozen Chan (1994) 2D WLS is **not** the bottleneck. Provisional **sim X = 0.50 m** locked. Hardware **X PARKED**. Lab **HOLD** until Founder / Operator opens sync-imperfection or multipath-bias. Score: [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md). Digestion: [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md). Fog peek record: [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md).

**What this is not:** This is **not** rithm. Skill-met is **not** claimed. Peek succeed / #0 HARDEN is **not** claim clearance and is **not** a locator. Training is **not** started and is **not** established. Hardware **X** is **not** locked. Models are **not** invented this fold. Patent claims are **not** copied for a product. The cell-tower Amb is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED** and is **not** reopened here.

**Process:** Lab invents; Operator admits, rejects, or parks. Lab does **not** self-admit. After #0, Lab does **not** invent the next pulse until Founder / Operator opens sync-imperfection or multipath-bias. Still **no RF / ML**.

**Cell-tower geometry** is **PARKED** (Founder STOP / user pivot; peek #61 + X=300 m on record; A→B halted). This app does **not** reopen it as live.  
**BIA→weight portfolio** is **CLOSED** (human #59 ship demo + kill of the accurate-weight claim; animal parks stay). This app does **not** reopen it.  
**Collatz playground** is **done** (#45). Lab HOLD there (unchanged).  
**Track B invent** remains **paused** (unchanged).  
**llm-gwt R-REPL** remains **parked** (unchanged).

## Claim line (parent; sim X locked; hardware X PARKED)

`on a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) recovers mobile position with median error ≤ 0.50 m on a held-out path inside a GPS-denied box, without RF fingerprint training` → kill vs succeed: fail closed if the path is not laptop-feasible **or** GPS/DGPS is smuggled in as the mobile fix **or** the path is RF-fingerprint training; succeed later would need a held-out median ≤ **0.50 m** under the lock **and** must not silently drop the honesty locks (ideal sync assumed; multipath not injected) → last check: 2026-09-05 Operator **#0 HARDEN** — Chan 1994 2D WLS; 5 refs; L-path 101; 40 MC; seed 20260905; 1 ns median **0.361 m** (`σ_d`≈0.300 m); 3 ns median **1.081 m**; zero-noise ~1e-14 m; 0 failures; provisional **sim X = 0.50 m** (1 ns + margin) → status: **open** / **HOLD** (sim **X** locked; **not** claim clearance; hardware **X PARKED**)

## Geometry leftover (#0)

`planar TDOA geometry bottleneck (frozen Chan 1994 2D WLS; ideal simultaneous sync + Gaussian Δt only)` → kill vs harden: geometry blows the median off the `c · σ_t` scale vs median tracks `c · σ_t` with a frozen Chan estimator → last check: 2026-09-05 Operator **ADMIT HARDEN** — 1 ns → **0.361 m**; 3 ns → **1.081 m**; 0 failures; geometry is **not** the bottleneck under those idealizations → status: **hardened**

## Honest-fog lines

`spectrum / hardware vs sim-only` → kill vs succeed: a hardware **X** is required and no laptop-feasible sim/prototype path can be posed → sim-only (or hardware) must be named before **X**; a laptop-feasible sim/prototype path is poseable from public refs / assumptions → last check: 2026-09-05 **C1 SUCCEED** then **#0** locked **sim X = 0.50 m**; hardware **not** required to name a sim **X** → status: **hardened** (sim-only named)

`hardware X` → kill vs succeed: a later gate names a hardware / spectrum path that can carry its own **X** vs stay parked while the live path is sim-only → last check: 2026-09-05 Operator **PARK** hardware **X** → status: **paused** / **PARKED**

`clock resolution / simultaneous-sync assumption` → kill vs succeed: no public-ref / assumption statement can even pose ≥3-ref simultaneous-sync TDOA → **fail closed** or park; a named clock/sync assumption makes the estimator class poseable (still not a locator) → last check: 2026-09-05 **C2 SUCCEED** (story named) then **#0 assumed** that ideal simultaneous sync — leftover honesty about **imperfection** stays unopened → status: **hardened** (clock story named; still not a locator)

`sync-imperfection` → kill vs harden: a later pulse that injects clock / sync error and shows the 0.50 m sim bar does not survive vs a pulse that keeps the bar under named imperfection → last check: **not opened** — Operator **HOLD** until Founder / Operator opens this pulse → status: **paused** / **HOLD** (do not invent until opened)

`multipath in a GPS-denied box` → kill vs succeed: this is standing honesty, not a hunt — a denied box is a hard radio environment; do **not** silently drop multipath → last check: 2026-09-05 **C3 SUCCEED** (scoring poseable) then **#0 did not inject** multipath — leftover honesty stays open → status: **open** (constraint; next invent only if Founder / Operator opens multipath-bias)

## First-pulse data / measurement line

`public refs + sync assumptions + measurement availability for a laptop-feasible sim/prototype path` → kill vs succeed: no usable public refs / assumptions / measurement story → **DATA-BLOCKED park** or sim-only Soften (must be said); a citable public-ref / assumption peek that names fog and whether **X** is sim-geometry vs hardware → peek succeed (**not** claim clearance) → last check: 2026-09-05 fog naming **ADMITTED** — C1/C2/C3 **SUCCEED**; **X** class = sim-geometry first → status: **killed** / **PASS** (peek succeed; **not** claim clearance)

## #0 pulse (scored)

`#0 geometry-bottleneck sim` → kill vs succeed: a laptop, no-RF sim using **frozen textbook multilateration only** that can freeze a numeric sim **X** vs a pose that still cannot score a held-out path → last check: 2026-09-05 Operator **ADMIT HARDEN** — Chan 1994 2D WLS; numeric **sim X = 0.50 m**; geometry not the bottleneck → status: **hardened** (scored; **not** claim clearance)
