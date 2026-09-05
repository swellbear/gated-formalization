# Residual-Branch Menu — Greer-style sync-pulse TDOA

**Open string after abstract ingest ADMIT (Amb spine) + prior GATE1 Soften.** Offering ≠ running. This is **not** a closeout menu, **not** a locator, and **not** a product claim.

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**Status:** abstract ingest **ADMITTED**; patent-facing **≤1 m xy**; scoped **sim X = 0.50 m** (ideal refs + named GEOM0 noise; **not** patent promise); **DGPS ~0.4–0.5 m** absolute floor; **A1 opened**; A2 then A3/A4 named; link/map **PARKED**; fog peek **ADMITTED**; **GEOM0 HARDEN** stands; prior SYNC/JOINT/DRIFT/GATE = **sync-fragility evidence (partial)**; hardware **X PARKED**; write-up = sync-fragility evidence only (**HOLD send** until ingest + preferably A1 or A1+A2); Lab **HOLD** invent except A1

**Glossary:** `docs/READER_GLOSSARY.md`  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**SOURCE:** [`SOURCE.md`](SOURCE.md)  
**Ingest summary:** [`ABSTRACT_INGEST_SUMMARY.md`](ABSTRACT_INGEST_SUMMARY.md)  
**Copy gate:** [`COPY_GATE.md`](COPY_GATE.md)  
**Ingest digestion:** [`DIGESTION_ABSTRACT_INGEST.md`](DIGESTION_ABSTRACT_INGEST.md)  
**Founder write-up (PRIMARY; sync-fragility evidence only; HOLD send):** [`GREER_WRITEUP.md`](GREER_WRITEUP.md)  
**Lab audit draft:** [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md)  
**GATE1 score:** [`SCORE_GATE1.md`](SCORE_GATE1.md)  
**GATE1 digestion:** [`DIGESTION_GATE1.md`](DIGESTION_GATE1.md)  
**DRIFT1 score (prior):** [`SCORE_DRIFT1.md`](SCORE_DRIFT1.md)  
**DRIFT1 digestion (prior):** [`DIGESTION_DRIFT1.md`](DIGESTION_DRIFT1.md)  
**JOINT1 score (prior):** [`SCORE_JOINT1.md`](SCORE_JOINT1.md)  
**JOINT1 digestion (prior):** [`DIGESTION_JOINT1.md`](DIGESTION_JOINT1.md)  
**SYNC1 score (prior):** [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md)  
**SYNC1 digestion (prior):** [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md)  
**MULTIPATH1 score (prior):** [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md)  
**MULTIPATH1 digestion (prior):** [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md)  
**#0 score:** [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md)  
**#0 digestion:** [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md)  
**Peek + gate:** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md)  
**Peek digestion:** [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)

---

## 0. Plain-language framing

**What we’re doing:** Recording abstract ingest as Amb spine. Patent-facing **≤1 m xy**. **0.50 m** stays the scoped sim bar only. **A1** (ref-floor honesty) is opened. Prior write-up is **sync-fragility evidence only**. Hardware **X** stays parked. **No RF / ML.**

**What we need from you:** Nothing to send. Lab may invent a cheap **A1** check. **A2 / A3 / A4 HOLD.** Send stays **HOLD** until preferably A1 (or A1+A2).

**What this does *not* mean:** A TDOA locator. Claim clearance. A send to Greer. A patent promise of 0.50 m. A multipath-robust 0.50 m. A free per-epoch realtime drift claim. A GATE1 accuracy repair. Hardware **X**. Training started or established. Skill-met. RF fingerprinting. GPS/DGPS as the mobile fix. A product copied from US10135667B1. Reopening cell-tower as live. Reopening SkyMirr. Reopening BIA→weight. Reopening Track B. Reopening llm-gwt R-REPL. Reopening Collatz invent (#45 playground is done; Lab HOLD there).

---

## 1. Named leftover (this string)

| ID | One-line | Class | Disposition |
|----|----------|-------|-------------|
| greer-tdoa-median-X | ≥3-ref simultaneous-sync TDOA, laptop-feasible sim-only; GPS/DGPS place/time refs only; no RF fingerprint training | Two bars after ingest: patent-facing **≤1 m xy**; scoped **sim X = 0.50 m** under ideal refs + named GEOM0 noise (**median-not-p90**; **not** patent promise). **DGPS ~0.4–0.5 m** absolute floor | **open** — last check: abstract ingest ADMIT; **A1 opened**; write-up **HOLD send**; **not** claim clearance |
| A1-ref-floor | Ref-floor honesty (absolute vs relative; DGPS ~0.4–0.5 m vs ideal-known-refs sim) | Empirically poseable cheap check | **open** — Rank-1 next; Operator **opened**; not scored |
| A2-clock-count | Clock-count / TDOA-resolution honesty (abstract high-speed receiver clock; distinct from inter-ref sync string) | Named leftover | **paused** / **HOLD** — after A1 |
| A3-indoor-first-arrival | Indoor / first-arrival / denied-box radio (not our additive mild-NLOS Soften) | Named leftover | **paused** / **HOLD** — after A2 |
| A4-realtime-motion | Realtime / central-compute / motion (abstract realtime; our wins were path-batch) | Named leftover | **paused** / **HOLD** — after A2 (with A3) |
| link-map-overlay | GIS / CAD overlay | Parked | **paused** / **PARKED** |
| spectrum-hardware-vs-sim | Can the path stay laptop-feasible sim-only, or must hardware/spectrum be named first? | Peek settled | **hardened** — last check: 2026-09-05 **C1 SUCCEED**; sim-only path poseable |
| hardware-X | A hardware / spectrum **X** on a later radio path | Parked — live path is sim-only | **paused** / **PARKED** — last check: 2026-09-05 Operator **PARK** hardware **X** (GATE1 + write-up do not unpark) |
| clock-resolution-sync | Can a simultaneous-sync / clock-resolution assumption be named from public refs? | Peek settled | **hardened** — last check: 2026-09-05 **C2 SUCCEED**; #0 + MULTIPATH1 assumed that idealization; still not a locator |
| sync-imperfection | Does the NLOS-scoped 0.50 m sim bar survive named clock / sync error? | Scored Soften (Chan-alone + JOINT1) | **Soften** / **partial** sync-fragility evidence — last check: 2026-09-05 ingest reclassifies; Chan-alone SYNC1 `σ_sync≲0.3 ns` **0.382 m**; JOINT1 restores X to **≲ 3 ns** |
| joint1-path-shared | Path-shared joint clocks (shared-τ) under fixed_trial `σ_sync` | Scored Soften | **Soften** / **partial** — last check: 2026-09-05 ingest; Aim A partial; **fixed offsets** |
| drift1-pulse | Clock drift / ramp vs shared-τ | Scored HARDEN | **hardened** under named budget / **partial** vs patent set — last check: 2026-09-05 ingest; batch τ + α; **not** free per-epoch realtime; **not** A4 |
| gate1-pulse | Detect-only refuse OR (G1a_DRIFT1 residual ∨ G1b raw LORO) | Scored Soften | **Soften** / **partial** — last check: 2026-09-05 ingest; FA≈**0.100**; TD σ=10 ≈**0.828**; **not** a repair |
| multipath-denied-box | Multipath honesty + held-out path inside a GPS-denied box without GPS as the mobile fix | Scored Soften | **restated** / **Soften** — last check: 2026-09-05 MULTIPATH1; poseable under LOS + mild/intermittent NLOS; **not** poseable under strong persistent multipath with frozen Chan alone; no fingerprint rescue; **X** median-not-p90; **later** |
| multipath-nlos-bias | Multipath / NLOS **positive-bias** injection under the **same frozen Chan (1994) 2D WLS** | Scored Soften | **restated** / **Soften** — last check: 2026-09-05 MULTIPATH1; Kill not triggered; NLOS-scoped 0.50 m; **later** |
| geometry-bottleneck-sim-0 | #0 geometry-bottleneck sim — laptop; no RF; frozen Chan (1994) 2D WLS | Scored | **hardened** — not the bottleneck; median tracks `c · σ_t`; **sim X = 0.50 m** (**median-not-p90**; 1 ns p90 ≈ **1.16 m**) |

No other empirically resolvable residuals on this fold.

---

## 2. Other strings (stay paused / closed / done)

| String | Disposition | Note |
|--------|-------------|------|
| Cell-tower geometry (`2026-09_cell-tower-geometry`) | **PARKED** (Founder STOP / user pivot) | Peek #61 + X=300 m on record; A→B halted; **not live**. This app does **not** reopen it as live |
| SkyMirr MuLCAT (`2026-09_skymirr-mulcat-isolation`) | **separate Amb** | SURROGATE1 Soften on its own record. This app does **not** reopen it |
| BIA→weight portfolio (`2026-09_human-bia-weight` + animal parks) | **CLOSED** (#59 KILL; #47/#49/#51 DATA-BLOCKED; #53 Soften) | Human ship demo stays method-practice only. This app does **not** reopen any BIA app |
| Collatz playground (`2026-09_collatz-shortcut-map`) | **done** (#45) | Playground invent complete; Lab HOLD there; **not** a proof. This app does **not** reopen it |
| Track B invent (oil spot) | **paused** | Unchanged; this app does **not** reopen it |
| llm-gwt R-REPL | **parked** | Unchanged; do not chase GPU / weights / keys |

---

## 3. Operator decision log

| Date | Action |
|------|--------|
| 2026-09-05 | Founder **CLAIM LOCK** opens this string as a **new** Amb (Greer-style GPS-denied locate via dedicated sync-pulse refs + mobile TDOA; contrast US10135667B1 — method practice / explore the idea; not copy claims for product). Claim wording locked. **X** TBD. First pulse after admit = name fog + 2–3 cheap checks. **No invent models this fold.** Lab HOLD. Cell-tower Amb **PARKED** (not reopened as live). BIA→weight portfolio **CLOSED**. Collatz playground **done** (#45). Track B **paused**. llm-gwt R-REPL stays **parked**. Last check: none. TDOA locate is **not** established. Training is **not** established. Not skill-met. Not rithm. |
| 2026-09-05 | Method Operator **ADMIT** first-pulse fog naming (Lab `PROPOSED_FOG_PEEK`). **C1 SUCCEED** — sim-only path poseable; hardware not required to name sim **X**. **C2 SUCCEED** — provisional ideal simultaneous TX + Δt → Δd = c·Δt (~0.3 m/ns). **C3 SUCCEED** — scoring poseable with GPS refs-only; multipath stays on fog. **LOCK:** sim-only path; provisional **X = sim-geometry first**. **PARK** hardware **X**. Next (**admitted**, then scored the same day): **#0 geometry-bottleneck sim**. US10135667B1 = prior-art note only. Cell-tower stays **PARKED**. BIA stays **CLOSED**. Peek succeed ≠ claim clearance. TDOA locate is **not** established. Training is **not** established. Not skill-met. Not rithm. |
| 2026-09-05 | Operator **ADMIT #0 HARDEN**. Frozen Chan (1994) 2D WLS; numpy; 5 refs; L-path 101; 40 MC; seed 20260905. 1 ns median **0.361 m** (`σ_d`≈0.300 m); 1 ns **p90 ≈ 1.16 m**; 3 ns median **1.081 m**; zero-noise ~1e-14 m; 0 failures. Geometry is **not** the bottleneck under ideal simultaneous sync + Gaussian Δt. **LOCK** provisional **sim X = 0.50 m** (**median**-based @ 1 ns + margin; **median-not-p90**). **PARK** hardware **X**. Honesty: ideal sync assumed; multipath not injected; GPS never the mobile fix; not claim clearance; not a locator; not skill-met; **X** is not a p90 bar. US10135667B1 prior-art note only. Cell-tower stays **PARKED**. BIA stays **CLOSED**. |
| 2026-09-05 | Operator **ADMIT MULTIPATH1 Soften**. Kill **not** triggered. Frozen Chan 1994; `σ_t`=1 ns; positive range-bias injection; same refs/L-path as #0. Baseline median **0.364 m**; `random_k=1` `b=0.5` → **0.476 m**; `epoch_f=0.25` `b=1` → **0.452 m**; strong persistent `b≥1–2 m` → **0.73–4.7+ m**. **LOCK** provisional **sim X = 0.50 m** remains, with **NLOS scope annotation** (poseable under LOS + mild/intermittent NLOS; **not** poseable under strong persistent multipath with frozen Chan alone). Do **not** claim multipath-robust 0.50 m. **No** fingerprint rescue. **X** remains median-not-p90 (p90 ≈ **1.16 m** @ 1 ns LOS). **PARK** hardware **X**. Later the same day: **SYNC1 Soften**. US10135667B1 prior-art note only. Cell-tower stays **PARKED**. BIA stays **CLOSED**. Soften ≠ claim clearance. TDOA locate is **not** established. Training is **not** established. Not skill-met. Not rithm. |
| 2026-09-05 | Operator **ADMIT SYNC1 Soften** (Kill **not** triggered). Frozen Chan 1994; `σ_t`=1 ns; same refs/L-path. Near-ideal `σ_sync≲0.3 ns` → median **0.382 m** ≤ X; `σ_sync`=1 ns scrapes **0.513 m**; `≥3 ns` / 3 ns path drift **fails X**. Combined **X** scope = near-ideal sync + prior MULTIPATH1 NLOS scope. **GEOM0 HARDEN** still stands. Median-not-p90 honesty remains (1 ns p90 ≈ **1.16 m**). No fingerprint / ML / RF invent to rescue loose sync. **PARK** hardware **X**. Later the same day: **JOINT1 Soften**. Founder DIGEST recorded on [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md). Cell-tower stays **PARKED**. BIA stays **CLOSED**. Soften ≠ claim clearance. Not a locator. Not skill-met. Not rithm. |
| 2026-09-05 | Operator **ADMIT JOINT1 Soften** (Kill **not** triggered; Aim A **partial**). Path-shared joint clocks (shared-τ) under **fixed_trial** `σ_sync`. Restores X up to **≲ 3 ns**: **0.231 m** @ 1 ns; **0.439 m** @ 3 ns ≤ X. Chan scrape at 1 ns **restored**. `σ_sync`=10 ns fails (**1.816 m**). Drift 3 ns/path still broke X on this pulse (JOINT1 **0.919 m** — shared-τ misspecified vs ramp). Named sync Soften budget **widens** to **`σ_sync ≲ 3 ns` under JOINT1** + prior mild-NLOS. **GEOM0 HARDEN** + **MULTIPATH1 Soften** still stand. **Not** multipath-robust. Median-not-p90 honesty remains (1 ns p90 ≈ **1.16 m**). No fingerprint / ML / RF invent. **PARK** hardware **X**. Later the same day: **DRIFT1 HARDEN**. Owner-requested **collaboration framing**; **no claim-language copy**. US10135667B1 = custom-beacon substrate, not carrier-mast Amb. Cell-tower stays **PARKED**. BIA stays **CLOSED**. Soften ≠ claim clearance. Not a locator. Not skill-met. Not rithm. |
| 2026-09-05 | Operator **ADMIT DRIFT1 HARDEN** under the named budget. Batch path-shared τ + linear α restores median ≤ **0.50 m** on SYNC1 drift breakers (drift=3 @ `σ=0` → **0.221 m**; drift=10 → **0.223 m**; **α̂ recovers**). **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) **still stands**. Honesty: path-shared **batch** model, **not** free per-epoch realtime; **not** multipath-robust; **not** hardware. **GEOM0 HARDEN** + **MULTIPATH1 Soften** + **SYNC1 Soften** still stand. Median-not-p90 honesty remains (1 ns p90 ≈ **1.16 m**). No fingerprint / ML / RF invent. **PARK** hardware **X**. Later the same day: **GATE1 Soften**. Owner-requested **collaboration framing**; **no claim-language copy**. US10135667B1 = custom-beacon substrate, not carrier-mast Amb. Cell-tower stays **PARKED**. BIA stays **CLOSED**. HARDEN ≠ claim clearance. Not a locator. Not skill-met. Not rithm. |
| 2026-09-05 | Operator **ADMIT GATE1 Soften** (Kill **not** triggered; aim B **Succeed**). Detect-only refuse OR (G1a_DRIFT1 residual ∨ G1b raw LORO). FA `σ≤3` drift0 ≈ **0.100**; FA +matched drift3 ≈ **0.080**; TD σ=10 ≈ **0.828**; TD unmatched drift3 = **1.000**; TD per_epoch σ=3 = **1.000**. Residual-alone misses σ=10 (τ absorbs fixed_trial); raw LORO carries it. Injection-calibrated → Soften not Harden. Use: widen the error bar or refuse a point fix — **not** a magic accuracy repair. **DRIFT1 HARDEN** + **JOINT1 Soften** + **SYNC1 Soften** + **MULTIPATH1 Soften** + **GEOM0 HARDEN** still stand. Write-up on disk: Founder [`GREER_WRITEUP.md`](GREER_WRITEUP.md) **PRIMARY** — **HOLD send** until user OK. Lab audit [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md). **Lab HOLD invent** pending Greer criteria / user send OK. **PARK** hardware **X**. **Multipath later.** Owner-requested **collaboration framing**; **no claim-language copy**. Cell-tower stays **PARKED**. BIA stays **CLOSED**. Soften ≠ claim clearance. Not a locator. Not skill-met. Not rithm. |
| 2026-09-05 | Operator **ADMIT ingest** of US10135667B1 **published abstract** as Amb spine ([`SOURCE.md`](SOURCE.md); [`PROPOSED_ABSTRACT_INGEST.md`](PROPOSED_ABSTRACT_INGEST.md); [`ABSTRACT_INGEST_SUMMARY.md`](ABSTRACT_INGEST_SUMMARY.md)). Still **not** claim clearance. **No** claim-language product copy. Copy gate [`COPY_GATE.md`](COPY_GATE.md) **PASS**. Success-bar Soften/Harden: patent-facing **≤1 m xy**; keep **X = 0.50 m** only as scoped sim bar under ideal refs + named noise (GEOM0) — **not** a patent promise; name **DGPS ~0.4–0.5 m** absolute floor. Prior string Soften: SYNC/JOINT/DRIFT/GATE = sync-fragility evidence (**partial**). Soften the claim we fully understood the patent hard-problem set. **HARDEN:** geometry-not-bottleneck under our noise model **stands**. Rank-1 next **locked:** **A1** (ref-floor honesty) first, then **A2**, then **A3/A4**. Link/map **PARKED**. **Greer send HOLD** until ingest + preferably A1 (or A1+A2). Prior write-up = sync-fragility evidence only. **Lab invent HOLD** except **A1 opened**. Hardware **X PARKED**. Cell-tower **PARKED**. BIA **CLOSED**. Ingest ≠ claim clearance. Not a locator. Not skill-met. Not rithm. |

---

*Standing habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Invents that do not point at the ledger line do not run.*
