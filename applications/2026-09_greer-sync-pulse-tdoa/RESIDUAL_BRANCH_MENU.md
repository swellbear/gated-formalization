# Residual-Branch Menu — Greer-style sync-pulse TDOA

**Open string after SYNC1 Soften.** Offering ≠ running. This is **not** a closeout menu, **not** a locator, and **not** a product claim.

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**Status:** fog peek **ADMITTED**; **GEOM0 HARDEN**; **MULTIPATH1 Soften**; **SYNC1 Soften**; provisional **sim X = 0.50 m** remains under **sync + NLOS** scope (**median**-not-p90); hardware **X PARKED**; Lab **HOLD**

**Glossary:** `docs/READER_GLOSSARY.md`  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**SYNC1 score:** [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md)  
**SYNC1 digestion:** [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md)  
**MULTIPATH1 score (prior):** [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md)  
**MULTIPATH1 digestion (prior):** [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md)  
**#0 score:** [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md)  
**#0 digestion:** [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md)  
**Peek + gate:** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md)  
**Peek digestion:** [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)

---

## 0. Plain-language framing

**What we’re doing:** Recording SYNC1 Soften after GEOM0 HARDEN and prior MULTIPATH1 Soften. Kill is **not** triggered. Sim **X** stays **0.50 m**, honest only under near-ideal sync (`σ_sync ≲ 0.3 ns`) and LOS / mild/intermittent NLOS. **X is median-not-p90** (1 ns p90 ≈ **1.16 m**). Hardware **X** stays parked. Lab holds. **No RF / ML.**

**What we need from you:** Nothing this fold. Lab **HOLD**. Optional later combined mild-NLOS + 0.3 ns sync, or drift-compensation textbook pulses, stay **parked** until Founder / user reopens.

**What this does *not* mean:** A TDOA locator. Claim clearance. A multipath-robust 0.50 m. Hardware **X**. Training started or established. Skill-met. RF fingerprinting. GPS/DGPS as the mobile fix. A product copied from US10135667B1. Auto-run of sync-imperfection. Reopening cell-tower as live. Reopening BIA→weight. Reopening Track B. Reopening llm-gwt R-REPL. Reopening Collatz invent (#45 playground is done; Lab HOLD there).

---

## 1. Named leftover (this string)

| ID | One-line | Class | Disposition |
|----|----------|-------|-------------|
| greer-tdoa-median-X | ≥3-ref simultaneous-sync TDOA, laptop-feasible sim-only, **median** error ≤ **0.50 m** on a held-out GPS-denied path; GPS/DGPS place/time refs only; no RF fingerprint training | Empirically posed on sim (**X** remains, **scoped** to near-ideal sync + mild NLOS; **median-not-p90**); succeed still requires a later held-out median ≤ X **without** dropping honesty locks | **open** / **HOLD** — last check: SYNC1 Soften; **sim X = 0.50 m** scoped; 1 ns p90 ≈ **1.16 m**; **not** claim clearance |
| spectrum-hardware-vs-sim | Can the path stay laptop-feasible sim-only, or must hardware/spectrum be named first? | Peek settled | **hardened** — last check: 2026-09-05 **C1 SUCCEED**; sim-only path poseable |
| hardware-X | A hardware / spectrum **X** on a later radio path | Parked — live path is sim-only | **paused** / **PARKED** — last check: 2026-09-05 Operator **PARK** hardware **X** (MULTIPATH1 does not unpark) |
| clock-resolution-sync | Can a simultaneous-sync / clock-resolution assumption be named from public refs? | Peek settled | **hardened** — last check: 2026-09-05 **C2 SUCCEED**; #0 + MULTIPATH1 assumed that idealization; still not a locator |
| sync-imperfection | Does the NLOS-scoped 0.50 m sim bar survive named clock / sync error? | Scored | **Soften** — last check: 2026-09-05 Operator **SYNC1 Soften**; `σ_sync≲0.3 ns` median **0.382 m** ≤ X; 1 ns scrapes **0.513 m**; ≥3 ns / path drift fails X |
| parked-textbook-followons | Combined mild-NLOS + 0.3 ns sync, or drift-compensation textbook pulses | Parked until Founder / user reopens | **paused** / **PARKED** — Lab **HOLD**; do not invent until reopened |
| multipath-denied-box | Multipath honesty + held-out path inside a GPS-denied box without GPS as the mobile fix | Scored Soften | **restated** / **Soften** — last check: 2026-09-05 MULTIPATH1; poseable under LOS + mild/intermittent NLOS; **not** poseable under strong persistent multipath with frozen Chan alone; no fingerprint rescue; **X** median-not-p90 |
| multipath-nlos-bias | Multipath / NLOS **positive-bias** injection under the **same frozen Chan (1994) 2D WLS** | Scored Soften | **restated** / **Soften** — last check: 2026-09-05 MULTIPATH1; Kill not triggered; NLOS-scoped 0.50 m |
| geometry-bottleneck-sim-0 | #0 geometry-bottleneck sim — laptop; no RF; frozen Chan (1994) 2D WLS | Scored | **hardened** — not the bottleneck; median tracks `c · σ_t`; **sim X = 0.50 m** (**median-not-p90**; 1 ns p90 ≈ **1.16 m**) |

No other empirically resolvable residuals on this fold.

---

## 2. Other strings (stay paused / closed / done)

| String | Disposition | Note |
|--------|-------------|------|
| Cell-tower geometry (`2026-09_cell-tower-geometry`) | **PARKED** (Founder STOP / user pivot) | Peek #61 + X=300 m on record; A→B halted; **not live**. This app does **not** reopen it as live |
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
| 2026-09-05 | Operator **ADMIT SYNC1 Soften** (Kill **not** triggered). Frozen Chan 1994; `σ_t`=1 ns; same refs/L-path. Near-ideal `σ_sync≲0.3 ns` → median **0.382 m** ≤ X; `σ_sync`=1 ns scrapes **0.513 m**; `≥3 ns` / 3 ns path drift **fails X**. Combined **X** scope = near-ideal sync + prior MULTIPATH1 NLOS scope. **GEOM0 HARDEN** still stands. Median-not-p90 honesty remains (1 ns p90 ≈ **1.16 m**). No fingerprint / ML / RF invent to rescue loose sync. **PARK** hardware **X**. **HOLD** — optional later combined mild-NLOS+0.3ns sync or drift-compensation textbook pulses parked until Founder/user reopens. Founder DIGEST recorded on [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md). US10135667B1 = custom-beacon substrate, not carrier-mast Amb. Cell-tower stays **PARKED**. BIA stays **CLOSED**. Soften ≠ claim clearance. Not a locator. Not skill-met. Not rithm. |

---

*Standing habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Invents that do not point at the ledger line do not run.*
