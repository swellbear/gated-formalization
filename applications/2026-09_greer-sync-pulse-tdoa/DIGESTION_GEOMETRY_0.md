# Digestion — #0 geometry-bottleneck HARDEN (sim X = 0.50 m provisional)

A short plain note of what the geometry pulse taught. Habit: [`docs/DIGESTION_HABIT.md`](../../docs/DIGESTION_HABIT.md). Incoming fog peek: [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md). Incoming park lesson: [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md). Score: [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md). This does **not** score a locator. It does **not** lock a hardware **X**. It does **not** reopen cell-tower as live. It does **not** reopen BIA→weight.

**This pulse:** `2026-09_greer-sync-pulse-tdoa` #0 — the next pulse **admitted** after the fog peek. Method Operator **ADMIT HARDEN**. Lab scratch was **not** on this fold VM; the gated fact set was copied from the Operator gate. C2’s named clock story (ideal simultaneous TX + Δt → Δd = c·Δt, ~0.3 m/ns) is the idealization this pulse used.

## What the pulse settled

Under **ideal simultaneous sync + Gaussian Δt only**, planar TDOA geometry with frozen Chan (1994) 2D WLS is **not** the bottleneck. Median Euclidean error tracks the `c · σ_t` scale.

- Method: Chan 1994 two-stage WLS; numpy only; 5 refs; L-path **101** samples; **40** MC; seed **20260905**.
- `σ_t` = **1 ns** → median **0.361 m** (`σ_d` ≈ **0.300 m**); **p90 ≈ 1.16 m**.
- `σ_t` = **3 ns** → median **1.081 m**.
- Zero-noise sanity ~**1e-14 m**. **0** failures.

That is an **Amb HARDEN** of the geometry leftover. It is **not** a locator. It is **not** claim clearance.

## What was locked (provisional)

- **Sim X = 0.50 m** (**median**-based @ 1 ns + margin; **perfect-ref**). **X is median-not-p90** (1 ns p90 ≈ **1.16 m**). Sim-only. Ideal sync assumed. Multipath not injected. Later **A1 Soften** — [`DIGESTION_A1.md`](DIGESTION_A1.md) — Softens silent absolute-≤0.50 reading of this lock.
- **Hardware X PARKED** until a sync / multipath gate.
- GPS / DGPS, if used at all, **place and time refs only** — never the mobile fix.
- US10135667B1 stays a **prior-art note only**.

HARDEN is **not** clearance. A 0.50 m **median** sim bar is **not** a field locator, **not** a p90 bar, and (later A1) **not** an absolute bar under the RN floor. Skill-met is **not** claimed.

## What this string must do next (later gated)

**MULTIPATH1** later **Soften**ed the multipath leftover. **SYNC1** later **Soften**ed Chan-alone sync-imperfection. **JOINT1** later **Soften**ed path-shared joint clocks and **widened** the named sync budget to `σ_sync ≲ 3 ns` under JOINT1. **DRIFT1** later **HARDENED** path-drift α (batch τ + linear α; SYNC1 drift breakers restore). **X** stays 0.50 m under **JOINT1 fixed-offset + named DRIFT1 batch α + NLOS** scope. Next after DRIFT1 (not this note): **GATE1**, then a Greer-facing write-up. Still **no RF / ML**. **No** fingerprint rescue. See [`DIGESTION_DRIFT1.md`](DIGESTION_DRIFT1.md).

This #0 note does **not** re-score MULTIPATH1. Geometry under ideal sync + Gaussian Δt remains **not** the bottleneck. See [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md).

## What stays parked / closed

- **Hardware X** stays **PARKED**.
- **Cell-tower geometry** stays **PARKED**. Do **not** reopen as live.
- **BIA→weight portfolio** stays **CLOSED**. Do **not** reopen human, poultry, cattle, sheep, or companion BIA apps.
- **Collatz playground** stays **done** (#45). Lab HOLD there.
- **Track B invent** stays **paused**.
- **llm-gwt R-REPL** stays **parked**.

This note does **not** authorize the next invent. It does **not** show a TDOA locator. It does **not** start training. It does **not** unpark hardware **X**.
