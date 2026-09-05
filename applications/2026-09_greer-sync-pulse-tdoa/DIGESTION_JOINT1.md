# Digestion — JOINT1 Soften (sync budget ≲ 3 ns under joint clocks)

A short plain note of what the path-shared joint-clock pulse taught. Habit: [`docs/DIGESTION_HABIT.md`](../../docs/DIGESTION_HABIT.md). Incoming SYNC1: [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md). Incoming MULTIPATH1: [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md). Incoming #0: [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md). Score: [`SCORE_JOINT1.md`](SCORE_JOINT1.md). This does **not** score a locator. It does **not** lock a hardware **X**. It does **not** claim a multipath-robust or drift-robust 0.50 m. It does **not** reopen cell-tower as live. It does **not** reopen BIA→weight.

**This pulse:** `2026-09_greer-sync-pulse-tdoa` JOINT1 — Method Operator **ADMIT Soften** (Kill **not** triggered). Aim A **partial**. Lab scratch was **not** on this fold VM; the gated fact set was copied from the Operator gate. Path-shared JOINT1 (shared-τ) under **fixed_trial** `σ_sync`.

**Standing (record all four):** **GEOM0 HARDEN** · **MULTIPATH1 Soften** · **SYNC1 Soften** (Chan-alone near-ideal) · **JOINT1 Soften**.

## What the pulse settled

Kill is **not** triggered. Provisional **sim X = 0.50 m** **remains**. Named sync Soften budget **widens** to **`σ_sync ≲ 3 ns` under JOINT1** + prior mild-NLOS.

- Path-shared JOINT1 restores X under fixed_trial `σ_sync` up to **≲ 3 ns**: **0.231 m** @ 1 ns; **0.439 m** @ 3 ns ≤ 0.50 m.
- Chan scrape at 1 ns is **restored** (SYNC1 Chan-alone 1 ns was **0.513 m**).
- `σ_sync` = **10 ns** fails (**1.816 m**).
- Drift **3 ns/path** still breaks X (JOINT1 **0.919 m**) — shared-τ is **misspecified vs a ramp**.
- Prior **MULTIPATH1 Soften** still stands (LOS + mild/intermittent NLOS only).
- **GEOM0 HARDEN** still stands (geometry not the bottleneck under ideal sync).
- **Median-not-p90** honesty remains (1 ns p90 ≈ **1.16 m** on the #0 board).
- **Not** a multipath-robust claim. **Not** a drift-robust claim.
- No fingerprint / ML / RF invent.

That is an **Amb Soften** of the named sync leftover (budget widened under joint clocks). It is **not** a locator. It is **not** claim clearance.

## Combined X scope (locked)

**Sim X = 0.50 m** stays. It is a **median @ 1 ns RX noise** and is only honest under **mild NLOS + `σ_sync ≲ 3 ns` under JOINT1** (path-shared / fixed_trial). Strong multipath still fails Chan alone. Drift 3 ns/path still fails shared-τ. Remaining live fog includes **drift** (shared-τ vs ramp) and **multipath** — **not** hyperbolic geometry, and **not** a cleared loose-sync claim on Chan alone.

**X is median-not-p90.** Hardware **X PARKED.**

US10135667B1 — owner-requested **collaboration framing** (bibliographic; custom-beacon substrate, **not** a carrier-mast Amb). **No claim-language copy.**

## What this string must do next (not this fold)

**DRIFT1** pulse is **named** (not run here). Still **no RF / ML**. Do **not** invent a fingerprint rescue. Do **not** treat JOINT1 as drift-compensation.

## What stays parked / closed

- **Hardware X** stays **PARKED**.
- **DRIFT1** is named next — **not** scored this fold.
- **Cell-tower geometry** stays **PARKED**. Do **not** reopen as live.
- **BIA→weight portfolio** stays **CLOSED**. Do **not** reopen human, poultry, cattle, sheep, or companion BIA apps.
- **Collatz playground** stays **done** (#45). Lab HOLD there.
- **Track B invent** stays **paused**.
- **llm-gwt R-REPL** stays **parked**.

This note does **not** authorize running DRIFT1 in this fold. It does **not** show a TDOA locator. It does **not** start training. It does **not** unpark hardware **X**.
