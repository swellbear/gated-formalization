# Residual-Branch Menu — Greer-style sync-pulse TDOA

**Open string after #0.** Offering ≠ running. This is **not** a closeout menu, **not** a locator, and **not** a product claim.

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**Status:** fog peek **ADMITTED**; **#0 geometry HARDEN**; provisional **sim X = 0.50 m**; hardware **X PARKED**; Lab **HOLD**

**Glossary:** `docs/READER_GLOSSARY.md`  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**#0 score:** [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md)  
**#0 digestion:** [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md)  
**Peek + gate:** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md)  
**Peek digestion:** [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)

---

## 0. Plain-language framing

**What we’re doing:** Recording the #0 HARDEN after the fog peek. Geometry under ideal sync + Gaussian Δt is **not** the bottleneck. Sim **X** is locked at **0.50 m**. Hardware **X** stays parked. Lab holds until Founder / Operator opens sync-imperfection or multipath-bias. **No RF / ML.**

**What we need from you:** Nothing this fold. Lab **HOLD**. Next invent only if you open sync-imperfection or multipath-bias.

**What this does *not* mean:** A TDOA locator. Claim clearance. Hardware **X**. Training started or established. Skill-met. RF fingerprinting. GPS/DGPS as the mobile fix. A product copied from US10135667B1. Auto-admit. Reopening cell-tower as live. Reopening BIA→weight. Reopening Track B. Reopening llm-gwt R-REPL. Reopening Collatz invent (#45 playground is done; Lab HOLD there).

---

## 1. Named leftover (this string)

| ID | One-line | Class | Disposition |
|----|----------|-------|-------------|
| greer-tdoa-median-X | ≥3-ref simultaneous-sync TDOA, laptop-feasible sim-only, median error ≤ **0.50 m** on a held-out GPS-denied path; GPS/DGPS place/time refs only; no RF fingerprint training | Empirically posed on sim (provisional **X** locked); succeed still requires a later held-out median ≤ X **without** dropping honesty locks | **open** / **HOLD** — last check: #0 HARDEN; **sim X = 0.50 m**; **not** claim clearance |
| spectrum-hardware-vs-sim | Can the path stay laptop-feasible sim-only, or must hardware/spectrum be named first? | Peek settled | **hardened** — last check: 2026-09-05 **C1 SUCCEED**; sim-only path poseable |
| hardware-X | A hardware / spectrum **X** on a later radio path | Parked until sync/multipath gate | **paused** / **PARKED** — last check: 2026-09-05 Operator **PARK** hardware **X** |
| clock-resolution-sync | Can a simultaneous-sync / clock-resolution assumption be named from public refs? | Peek settled | **hardened** — last check: 2026-09-05 **C2 SUCCEED**; #0 assumed that idealization; still not a locator |
| sync-imperfection | Does the 0.50 m sim bar survive named clock / sync error? | Empirically resolvable **after** Operator opens this pulse | **paused** / **HOLD** — not opened; do not invent until opened |
| multipath-denied-box | Multipath honesty + held-out path inside a GPS-denied box without GPS as the mobile fix | Peek settled as poseable; #0 did not inject; multipath stays fog | **open** (constraint) — last check: 2026-09-05 **C3 SUCCEED** then #0 no-inject; next invent only if Operator opens multipath-bias |
| geometry-bottleneck-sim-0 | #0 geometry-bottleneck sim — laptop; no RF; frozen Chan (1994) 2D WLS | Scored | **hardened** — not the bottleneck; median tracks `c · σ_t`; **sim X = 0.50 m** |

No other empirically resolvable residuals on this fold. Lab does **not** invent clock or multipath pulses until they are opened.

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
| 2026-09-05 | Operator **ADMIT #0 HARDEN**. Frozen Chan (1994) 2D WLS; numpy; 5 refs; L-path 101; 40 MC; seed 20260905. 1 ns median **0.361 m** (`σ_d`≈0.300 m); 3 ns median **1.081 m**; zero-noise ~1e-14 m; 0 failures. Geometry is **not** the bottleneck under ideal simultaneous sync + Gaussian Δt. **LOCK** provisional **sim X = 0.50 m** (1 ns + margin). **PARK** hardware **X** until sync/multipath gate. Honesty: ideal sync assumed; multipath not injected; GPS never the mobile fix; not claim clearance; not a locator; not skill-met. **HOLD** next Lab invent until Founder / Operator opens sync-imperfection or multipath-bias (still no RF / ML). US10135667B1 prior-art note only. Cell-tower stays **PARKED**. BIA stays **CLOSED**. |

---

*Standing habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Invents that do not point at the ledger line do not run.*
