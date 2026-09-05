# Named-gap ledger — Greer-style sync-pulse TDOA

Habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). One line per open gap. This is a problem-solving scoreboard, **not** a locator and **not** a product claim.

**Opened:** 2026-09-05 — Founder **CLAIM LOCK** opens a **new** Amb: Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA. Current framing: owner-requested **collaboration** (bibliographic; US10135667B1 custom-beacon substrate, not a carrier-mast Amb). **No claim-language copy.** Lab proposes first-pulse fog + 2–3 cheap checks. Method Operator gates.

**Last check:** 2026-09-05 — Operator **ADMIT GATE1 Soften** (Kill not triggered; aim B Succeed). Detect-only refuse OR (G1a_DRIFT1 residual ∨ G1b raw LORO): FA `σ≤3` drift0 ≈ **0.100**; FA +matched drift3 ≈ **0.080**; TD σ=10 ≈ **0.828**; TD unmatched drift3 = **1.000**; TD per_epoch σ=3 = **1.000**. Residual-alone misses σ=10; raw LORO carries it. Injection-calibrated → Soften not Harden. **DRIFT1 HARDEN** and **JOINT1 Soften** still stand. Write-up on disk: Founder [`GREER_WRITEUP.md`](GREER_WRITEUP.md) **PRIMARY** (**HOLD send** until user OK); Lab audit [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md). Score: [`SCORE_GATE1.md`](SCORE_GATE1.md). Digestion: [`DIGESTION_GATE1.md`](DIGESTION_GATE1.md). Prior DRIFT1: [`SCORE_DRIFT1.md`](SCORE_DRIFT1.md). Prior JOINT1: [`SCORE_JOINT1.md`](SCORE_JOINT1.md). Prior SYNC1: [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md). Prior MULTIPATH1: [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md). #0: [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md). Fog peek: [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md).

**What this is not:** This is **not** rithm. Skill-met is **not** claimed. Soften / HARDEN is **not** claim clearance, **not** a locator, **not** a multipath-robust 0.50 m, and **not** a free per-epoch realtime drift claim. Training is **not** started and is **not** established. Hardware **X** is **not** locked. Fingerprint / ML / RF invent is **not** a rescue. Patent claims are **not** copied. The cell-tower Amb is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED** and is **not** reopened here.

**Process:** Lab invents; Operator admits, rejects, or parks. Lab does **not** self-admit. After GATE1 Soften, **Lab HOLD invent** pending Greer criteria / user send OK. Write-up is on disk (**HOLD send**). Still **no RF / ML**. **No** fingerprint rescue. **Multipath later.** Hardware **X PARKED**.

**Cell-tower geometry** is **PARKED** (Founder STOP / user pivot; peek #61 + X=300 m on record; A→B halted). This app does **not** reopen it as live.  
**BIA→weight portfolio** is **CLOSED** (human #59 ship demo + kill of the accurate-weight claim; animal parks stay). This app does **not** reopen it.  
**Collatz playground** is **done** (#45). Lab HOLD there (unchanged).  
**Track B invent** remains **paused** (unchanged).  
**llm-gwt R-REPL** remains **parked** (unchanged).

## Claim line (parent; sim X locked; JOINT1 fixed-offset + DRIFT1 batch α + GATE1 refuse-belt + NLOS scoped; hardware X PARKED)

`on a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) recovers mobile position with median error ≤ 0.50 m on a held-out path inside a GPS-denied box, without RF fingerprint training` → kill vs succeed: fail closed if the path is not laptop-feasible **or** GPS/DGPS is smuggled in as the mobile fix **or** the path is RF-fingerprint training **or** **X** is silently read as p90; succeed later would need a held-out **median** ≤ **0.50 m** under the lock **and** must not silently drop the honesty locks (`σ_sync ≲ 3 ns` under JOINT1 **fixed offsets**; named **DRIFT1** batch α, **not** free per-epoch realtime; GATE1 refuse-belt; LOS + mild/intermittent NLOS; **X is median-not-p90**) → last check: 2026-09-05 Operator **GATE1 Soften** — FA≈**0.100** / TD σ=10 ≈**0.828**; prior **DRIFT1 HARDEN** (drift=3 @ `σ=0` **0.221 m** / drift=10 **0.223 m**); prior **JOINT1 Soften** (`σ_sync` **0.231 m** @ 1 ns / **0.439 m** @ 3 ns); prior **SYNC1 Soften** (`σ_sync≲0.3 ns` **0.382 m**); prior **MULTIPATH1 Soften**; **GEOM0 HARDEN** still stands; 1 ns **p90 ≈ 1.16 m** → status: **open** (sim **X** remains, **scoped** to JOINT1 fixed-offset + named DRIFT1 batch α + GATE1 refuse-belt + mild NLOS; **median-not-p90**; **not** claim clearance; hardware **X PARKED**; write-up **HOLD send**; Lab **HOLD** invent)

## Geometry leftover (#0)

`planar TDOA geometry bottleneck (frozen Chan 1994 2D WLS; ideal simultaneous sync + Gaussian Δt only)` → kill vs harden: geometry blows the median off the `c · σ_t` scale vs median tracks `c · σ_t` with a frozen Chan estimator → last check: 2026-09-05 Operator **ADMIT HARDEN** — 1 ns median **0.361 m** / p90 ≈ **1.16 m**; 3 ns median **1.081 m**; 0 failures; geometry is **not** the bottleneck under those idealizations; **X is median-not-p90** → status: **hardened**

## Honest-fog lines

`spectrum / hardware vs sim-only` → kill vs succeed: a hardware **X** is required and no laptop-feasible sim/prototype path can be posed → sim-only (or hardware) must be named before **X**; a laptop-feasible sim/prototype path is poseable from public refs / assumptions → last check: 2026-09-05 **C1 SUCCEED** then **#0** locked **sim X = 0.50 m**; hardware **not** required to name a sim **X** → status: **hardened** (sim-only named)

`hardware X` → kill vs succeed: a later gate names a hardware / spectrum path that can carry its own **X** vs stay parked while the live path is sim-only → last check: 2026-09-05 Operator **PARK** hardware **X** (GATE1 Soften + write-up do **not** unpark it) → status: **paused** / **PARKED**

`clock resolution / simultaneous-sync assumption` → kill vs succeed: no public-ref / assumption statement can even pose ≥3-ref simultaneous-sync TDOA → **fail closed** or park; a named clock/sync assumption makes the estimator class poseable (still not a locator) → last check: 2026-09-05 **C2 SUCCEED** (story named) then **#0 assumed** that ideal simultaneous sync — leftover honesty about **imperfection** was later SYNC1 / JOINT1 / DRIFT1 → status: **hardened** (clock story named; still not a locator)

`sync-imperfection (SYNC1 Chan-alone)` → kill vs soften: injected clock / sync error blows the 0.50 m sim bar with no surviving named window vs a named near-ideal window keeps the bar (Kill not triggered) → last check: 2026-09-05 Operator **ADMIT Soften** — `σ_sync≲0.3 ns` median **0.382 m** ≤ X; `σ_sync`=1 ns scrapes **0.513 m**; `≥3 ns` / 3 ns path drift **fails X**; later **JOINT1** restored the 1 ns scrape and widened the named budget under joint clocks; later **DRIFT1** restored the path-drift breakers under batch α → status: **killed** / **Soften** (Chan-alone window still near-ideal)

`sync-imperfection (JOINT1 path-shared)` → kill vs soften: path-shared shared-τ fails to restore X under any named fixed_trial window vs a named window keeps the bar (Kill not triggered) → last check: 2026-09-05 Operator **ADMIT Soften** (Aim A **partial**) — fixed_trial `σ_sync ≲ 3 ns` restores X (**0.231 m** @ 1 ns; **0.439 m** @ 3 ns); 10 ns **1.816 m** fails; drift 3 ns/path **0.919 m** fails (shared-τ misspecified vs ramp; later **DRIFT1**); do **not** invent fingerprint / ML / RF → status: **killed** / **Soften** (bar remains; scoped to `σ_sync ≲ 3 ns` under JOINT1 **fixed offsets** + mild NLOS; **still stands**)

`clock drift vs shared-τ (DRIFT1)` → kill vs harden: a later drift pulse shows whether a ramp / path-drift model can keep the 0.50 m bar vs shared-τ stays misspecified → last check: 2026-09-05 Operator **ADMIT HARDEN** — batch path-shared τ + linear α; drift=3 @ `σ=0` **0.221 m**; drift=10 **0.223 m**; **α̂ recovers**; honesty = path-shared **batch**, **not** free per-epoch realtime → status: **hardened**

`refuse-belt (GATE1)` → kill vs soften: a detect-only residual∨LORO belt either blows in-band FA or misses out-of-budget cases vs a named belt keeps FA≈0.10 and high TD (Kill not triggered) → last check: 2026-09-05 Operator **ADMIT Soften** (aim B Succeed) — FA `σ≤3` drift0 ≈ **0.100**; TD σ=10 ≈ **0.828**; residual-alone misses σ=10; raw LORO carries it; **not** a repair → status: **killed** / **Soften**

`multipath in a GPS-denied box` → kill vs succeed: this is standing honesty, not a hunt — a denied box is a hard radio environment; do **not** silently drop multipath; Kill = 0.50 m not poseable even under LOS / mild NLOS vs Soften = 0.50 m stays with NLOS scope vs Harden = multipath-robust 0.50 m → last check: 2026-09-05 Operator **ADMIT Soften** — Kill **not** triggered; poseable under LOS + mild/intermittent NLOS; **not** poseable under strong persistent multipath with frozen Chan alone; **no** fingerprint rescue; **X** median-not-p90 → status: **restated** / **Soften** (NLOS-scoped; not multipath-robust; **later**)

`multipath / NLOS positive-bias injection (same frozen Chan)` → kill vs harden: inject positive NLOS / multipath bias under the **same** Chan 1994 and show whether the **median** 0.50 m bar survives → last check: 2026-09-05 Operator **ADMIT Soften** (Kill not triggered) — baseline **0.364 m**; mild/intermittent **0.476 m** / **0.452 m**; strong persistent **0.73–4.7+ m** → status: **restated** / **Soften** (scored; NLOS-scoped; **later**)

## First-pulse data / measurement line

`public refs + sync assumptions + measurement availability for a laptop-feasible sim/prototype path` → kill vs succeed: no usable public refs / assumptions / measurement story → **DATA-BLOCKED park** or sim-only Soften (must be said); a citable public-ref / assumption peek that names fog and whether **X** is sim-geometry vs hardware → peek succeed (**not** claim clearance) → last check: 2026-09-05 fog naming **ADMITTED** — C1/C2/C3 **SUCCEED**; **X** class = sim-geometry first → status: **killed** / **PASS** (peek succeed; **not** claim clearance)

## Scored pulses

`#0 geometry-bottleneck sim (GEOM0)` → kill vs succeed: a laptop, no-RF sim using **frozen textbook multilateration only** that can freeze a numeric sim **X** vs a pose that still cannot score a held-out path → last check: 2026-09-05 Operator **ADMIT HARDEN** — Chan 1994 2D WLS; numeric **sim X = 0.50 m** (**median**-based @ 1 ns; **median-not-p90**; 1 ns p90 ≈ **1.16 m**); geometry not the bottleneck → status: **hardened** (scored; **not** claim clearance; still stands)

`SYNC1 sync-imperfection` → kill vs soften: loose sync / path drift kills the 0.50 m bar with no named window vs a near-ideal window keeps the bar → last check: 2026-09-05 Operator **ADMIT Soften** — near-ideal `σ_sync≲0.3 ns` keeps median **0.382 m**; 1 ns scrapes; ≥3 ns / path drift fails; later JOINT1 restored the scrape under joint clocks; later DRIFT1 restored the path-drift breakers → status: **killed** / **Soften** (scored; Chan-alone window; **not** claim clearance)

`JOINT1 path-shared joint clocks` → kill vs soften: shared-τ fails to restore X under any named fixed_trial window vs a named window keeps the bar → last check: 2026-09-05 Operator **ADMIT Soften** (Aim A **partial**) — `σ_sync ≲ 3 ns` under JOINT1 restores X; 10 ns fails; drift still failed until DRIFT1 → status: **killed** / **Soften** (scored; **still stands**; **fixed offsets**)

`MULTIPATH1 multipath-bias` → kill vs soften: any NLOS kills the 0.50 m bar vs a named mild window keeps it → last check: 2026-09-05 Operator **MULTIPATH1 Soften** — LOS + mild/intermittent NLOS only → status: **restated** / **Soften** (prior; **not** claim clearance; **later**)

`DRIFT1 pulse` → kill vs harden: whether a ramp / path-drift model can keep the 0.50 m bar → last check: 2026-09-05 Operator **ADMIT HARDEN** — batch path-shared τ + linear α; drift=3 @ `σ=0` **0.221 m**; drift=10 **0.223 m**; **α̂ recovers** → status: **hardened** (scored; **not** claim clearance; **not** free per-epoch realtime)

`GATE1 pulse` → kill vs soften: refuse belt fails to catch out-of-budget cases without blowing in-band FA vs a named detect-only belt keeps FA≈0.10 and high TD (Kill not triggered) → last check: 2026-09-05 Operator **ADMIT Soften** (aim B Succeed) — G1a residual ∨ G1b raw LORO; FA `σ≤3` drift0 ≈ **0.100**; FA +matched drift3 ≈ **0.080**; TD σ=10 ≈ **0.828**; TD unmatched drift3 = **1.000**; TD per_epoch σ=3 = **1.000**; residual-alone misses σ=10; raw LORO carries it; injection-calibrated → Soften not Harden → status: **killed** / **Soften** (scored; refuse belt; **not** a repair; **not** claim clearance)
