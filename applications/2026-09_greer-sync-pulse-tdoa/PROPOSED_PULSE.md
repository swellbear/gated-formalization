# First pulse — name fog + cheap checks (Operator-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**String:** first-pulse fog peek **ADMITTED** (Lab `PROPOSED_FOG_PEEK`); **#0 HARDEN**; **MULTIPATH1 Soften**; next = **sync-imperfection** (**not this fold**)  
**Named gap (this fold):** does positive range-bias kill the locked **0.50 m** sim bar, or only scope it?  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Peek digestion:** [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)  
**#0 score:** [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md)  
**MULTIPATH1 score:** [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md)  
**MULTIPATH1 digestion:** [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md)

Lab invented ranked peek / pulse probes. Lab does **not** self-admit. The fog-peek record below is the gated fact set copied from the Method Operator gate. **#0** later scored a numeric sim **X**. **MULTIPATH1** later **Soften**ed it with an NLOS scope. Lab scratch was **not** on this fold VM.

**What this is not:** A TDOA locator. Claim clearance. A multipath-robust 0.50 m. Training established. Skill-met. RF fingerprinting. Fingerprint rescue. GPS/DGPS as the mobile fix. Reopening cell-tower as live. Reopening BIA→weight. Rithm. A product copied from the named patent. Hardware **X**. A sync-imperfection run (not this fold).

---

## 0. Plain-language framing

**What this is:** Name the honest fog, then three cheap checks that ask whether the locked claim is even poseable. Public refs / sync assumptions / measurement availability. No estimator.

**What this settles (gated):** A laptop-feasible **sim-only** path is poseable. Hardware is **not** required to name a sim **X**. A clock story can be written (ideal simultaneous TX + Δt → Δd = c·Δt, ~0.3 m/ns). A held-out path can be scored with GPS/DGPS as refs only. Multipath stays on the fog list. Provisional **X = sim-geometry first**. Hardware **X** is **PARKED**. Peek succeed is **not** claim clearance.

**What this is not:** Not a locator. Not a reason to build radios this fold. Not a reason to paste patent claims. Not claim clearance. Not invent of a locator. Not a numeric **X**.

---

## 1. Lab peek (copied from the gate)

**Target:** whether a laptop-feasible sim/prototype path can be posed without hardware/spectrum; whether a simultaneous-sync / clock assumption can be named; whether a GPS-denied-box hold-out can be scored without using GPS as the mobile fix, with multipath kept honest.

**Result (gated):**

| Check | Result |
|-------|--------|
| C1 — Spectrum / hardware vs sim-only | **SUCCEED** — sim-only path poseable; hardware **not** required to name a sim **X** |
| C2 — Clock resolution / simultaneous-sync | **SUCCEED** — provisional ideal simultaneous TX + Δt → Δd = c·Δt (~0.3 m/ns) |
| C3 — Multipath + GPS-denied-box measurability | **SUCCEED** — scoring poseable with GPS refs-only; multipath stays on fog |

Peek succeed ≠ claim clearance. Hardware **X** is **PARKED**, not Soften-as-live.

---

## 2. C1 — spectrum / hardware vs sim-only (SUCCEED)

A laptop-feasible **sim-only** path can be posed from ordinary assumption language. Hardware / licensed spectrum is **not** required before a **sim** **X** can be named.

**LOCK:** live path = sim-only.  
**PARK:** hardware **X**. Do **not** treat a later radio kit as the way to freeze the first numeric bar.

This fold does **not** build radios and does **not** name a hardware campaign.

---

## 3. C2 — clock / simultaneous-sync (SUCCEED)

Provisional clock story (assumption, not a measured kit):

- Ideal **simultaneous TX** at the reference nodes.
- Observed time difference Δt maps to a range difference Δd = c·Δt.
- Order-of-magnitude conversion: **~0.3 m/ns** (c in air / vacuum, docs-level).

This makes ≥3-ref simultaneous-sync TDOA **poseable**. It is **not** a locator. It is **not** a claim that real clocks hold this ideal.

---

## 4. C3 — multipath + GPS-denied-box scoring (SUCCEED)

A held-out path inside a GPS-denied box can be **scored** while GPS/DGPS **place and time refs only**. GPS/DGPS are **never** the mobile fix.

**Multipath stays on the fog list.** A denied box is a hard radio environment. Do **not** silently drop multipath because C3 succeeded.

---

## 5. Operator gate (authoritative)

**ADMIT fog naming** from first pulse (Lab `PROPOSED_FOG_PEEK`):

- **C1 SUCCEED:** sim-only path poseable; hardware not required to name sim **X**
- **C2 SUCCEED:** provisional ideal simultaneous TX + Δt → Δd = c·Δt (~0.3 m/ns)
- **C3 SUCCEED:** scoring poseable with GPS refs-only; multipath stays on fog

**LOCK:** sim-only path; provisional **X = sim-geometry first**. **PARK** hardware **X**.

**NEXT (admitted here; scored later the same day):** **#0 geometry-bottleneck sim** — see [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md). Operator **ADMIT HARDEN**. Provisional **sim X = 0.50 m** (**median**-based @ 1 ns; **median-not-p90**; 1 ns p90 ≈ **1.16 m**). Hardware **X** stays **PARKED**. **Later:** **MULTIPATH1 Soften** — see [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md). **X** stays 0.50 m, **NLOS-scoped**.

**US10135667B1** = prior-art note only. Cell-tower **PARKED**. BIA **CLOSED**. Peek succeed ≠ claim clearance.

**Hard NO**

- Do **not** claim a multipath-robust 0.50 m or invent fingerprint rescue.
- Do **not** run sync-imperfection in this fold.
- Do **not** treat **sim X = 0.50 m** as a hardware bar or a **p90** bar.
- Do **not** train an RF fingerprint / radio-map model.
- Do **not** use GPS / DGPS as the mobile fix.
- Do **not** copy US10135667B1 claim language or treat this as a product embodiment of that patent.
- Do **not** commit large binary datasets or trained weights.
- Do **not** write skill-met / elevated language.
- Do **not** reopen `2026-09_cell-tower-geometry` as live.
- Do **not** reopen the BIA→weight portfolio.

---

## 6. Next pulse #0 (scored later the same day)

**#0 geometry-bottleneck sim** ran and was **HARDENED**. Metrics live on [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md).

- Ordinary **laptop**; **no RF**; **no** hardware campaign.
- Estimator class = frozen Chan (1994) two-stage WLS (textbook multilateration).
- **No** trained estimator invent. **No** fingerprint.
- GPS/DGPS **place/time refs only** — **never** the mobile fix.
- Provisional **sim X = 0.50 m** (**median**-based @ 1 ns: median **0.361 m** + margin). **X is median-not-p90** (1 ns p90 ≈ **1.16 m**). Hardware **X PARKED**.
- After #0: **MULTIPATH1 Soften** (same day). **X** stays 0.50 m, **NLOS-scoped**. Next leftover: **sync-imperfection**. Still **no RF / ML**.

---

## 6b. MULTIPATH1 (gated Soften — this fold)

Frozen Chan 1994; `σ_t` = 1 ns; **positive range-bias** injection; **same refs / L-path as #0**.

| Condition | Median Euclidean error |
|-----------|-------------------------|
| Baseline (LOS @ 1 ns; this pulse) | **0.364 m** |
| `random_k=1`, `b=0.5` | **0.476 m** |
| `epoch_f=0.25`, `b=1` | **0.452 m** |
| Strong persistent `b≥1–2 m` | **0.73–4.7+ m** |
| LOS p90 @ 1 ns (honesty; **not X**) | **≈ 1.16 m** |

**Soften.** Kill **not** triggered. Poseable under LOS + mild / intermittent NLOS. **Not** poseable under strong persistent multipath with frozen Chan alone. Do **not** claim a multipath-robust 0.50 m. **No** fingerprint rescue. **X** remains **median-not-p90**.

**LOCK** provisional **sim X = 0.50 m** remains, with **NLOS scope annotation**. **PARK** hardware **X**. Details: [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md).

**NEXT (admitted as next pulse, not run in this PR):** **sync-imperfection**. Still no RF / ML. No fingerprint rescue.

---

## 7. Unchanged strings

- Cell-tower geometry remains **PARKED** (Founder STOP / user pivot; peek #61 + X=300 m on record; A→B halted). **Not live.**
- BIA→weight portfolio remains **CLOSED** (human #59; animal parks stay).
- Collatz playground remains **done** (#45). Lab HOLD there.
- Track B invent remains **paused**.
- llm-gwt R-REPL remains **parked**.

---

*Docs only. Peek succeed / #0 HARDEN / MULTIPATH1 Soften ≠ claim clearance. NLOS-scoped sim X ≠ multipath-robust X. Not a locator. Not skill-met. Not a patent-product claim. Not rithm. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate.*
