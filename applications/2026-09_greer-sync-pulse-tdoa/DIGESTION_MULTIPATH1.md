# Digestion — MULTIPATH1 Soften (X = 0.50 m NLOS-scoped)

A short plain note of what the multipath-bias pulse taught. Habit: [`docs/DIGESTION_HABIT.md`](../../docs/DIGESTION_HABIT.md). Prior geometry lesson: [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md). Score: [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md). This does **not** score a locator. It does **not** lock a hardware **X**. It does **not** claim a multipath-robust 0.50 m. It does **not** reopen cell-tower as live. It does **not** reopen BIA→weight.

**This pulse:** `2026-09_greer-sync-pulse-tdoa` MULTIPATH1 — Method Operator **ADMIT Soften**. Kill **not** triggered. Lab scratch was **not** on this fold VM; the gated fact set was copied from the Operator gate.

## What the pulse settled

Frozen Chan (1994) on the same refs / L-path as #0, with `σ_t` = 1 ns and **positive range-bias** injection, is **poseable** under LOS + mild / intermittent NLOS. It is **not** poseable under strong persistent multipath with Chan alone.

- Baseline LOS median **0.364 m** (this pulse; #0's 1 ns LOS was **0.361 m**).
- Mild / intermittent: `random_k=1` `b=0.5` → **0.476 m**; `epoch_f=0.25` `b=1` → **0.452 m**.
- Strong persistent: `b≥1–2 m` → **0.73–4.7+ m**.
- LOS p90 @ 1 ns ≈ **1.16 m**. **X** stays **median-not-p90**.

That is an **Amb Soften** of the multipath leftover (scope named). It is **not** a Kill of the 0.50 m bar. It is **not** a locator. It is **not** claim clearance. It is **not** fingerprint rescue.

## What was locked (provisional; scoped)

- **Sim X = 0.50 m** remains **LOCKED**, now with an **NLOS scope annotation**: LOS + mild / intermittent NLOS only.
- Do **not** claim a multipath-robust **0.50 m**.
- **Hardware X PARKED**.
- GPS / DGPS, if used at all, **place and time refs only** — never the mobile fix.
- US10135667B1 stays a **prior-art note only**.

Soften is **not** clearance. A scoped 0.50 m sim bar is **not** a field locator. Skill-met is **not** claimed.

## What this string must do next (later the same day: SYNC1)

Lab later scored **SYNC1 Soften** then **JOINT1 Soften**. See [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md) and [`DIGESTION_JOINT1.md`](DIGESTION_JOINT1.md). **MULTIPATH1 Soften** still stands. Next after JOINT1 (not this note): **DRIFT1**. Still **no RF / ML**. **No** fingerprint rescue.

Clock / sync leftover is now **SYNC1 Soften** (Chan-alone near-ideal) plus **JOINT1 Soften** (`σ_sync ≲ 3 ns` under joint clocks). Strong persistent multipath stays named as **out of scope** for frozen Chan + the 0.50 m bar — do **not** silently drop it, and do **not** invent a fingerprint to rescue it.

Stay the **same Amb**. Do **not** unpark hardware **X**. Do **not** train. Do **not** copy patent claims.

## What stays parked / closed

- **Hardware X** stays **PARKED**.
- **Cell-tower geometry** stays **PARKED**. Do **not** reopen as live.
- **BIA→weight portfolio** stays **CLOSED**. Do **not** reopen human, poultry, cattle, sheep, or companion BIA apps.
- **Collatz playground** stays **done** (#45). Lab HOLD there.
- **Track B invent** stays **paused**.
- **llm-gwt R-REPL** stays **parked**.

This note does **not** authorize the next invent. It does **not** show a TDOA locator. It does **not** start training. It does **not** unpark hardware **X**.
