# Digestion — A3 Soften (mild LE bias; persistent B_lb fails ≤1 m)

A short plain note of what the leading-edge residual pulse taught. Habit: [`docs/DIGESTION_HABIT.md`](../../docs/DIGESTION_HABIT.md). Incoming A2: [`DIGESTION_A2.md`](DIGESTION_A2.md). Incoming A1: [`DIGESTION_A1.md`](DIGESTION_A1.md). Incoming ingest: [`DIGESTION_ABSTRACT_INGEST.md`](DIGESTION_ABSTRACT_INGEST.md). Incoming GATE1: [`DIGESTION_GATE1.md`](DIGESTION_GATE1.md). Incoming DRIFT1: [`DIGESTION_DRIFT1.md`](DIGESTION_DRIFT1.md). Incoming JOINT1: [`DIGESTION_JOINT1.md`](DIGESTION_JOINT1.md). Incoming SYNC1: [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md). Incoming MULTIPATH1: [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md). Incoming #0: [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md). Score: [`SCORE_A3.md`](SCORE_A3.md). Founder-polished send file: [`GREER_WRITEUP.md`](GREER_WRITEUP.md) (**HOLD send** until Founder rewrite + user OK). Suite DIGEST: [`DIGESTION_A1A4_SUITE.md`](DIGESTION_A1A4_SUITE.md). Lab audit: [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md). This does **not** score a locator. It does **not** lock a hardware **X**. It does **not** Harden indoor / first-arrival. It does **not** Kill ≤1 m wholesale. It does **not** authorize a send to Greer. It does **not** reopen cell-tower as live. It does **not** reopen BIA→weight.

**This pulse:** `2026-09_greer-sync-pulse-tdoa` A3 — Method Operator **ADMIT Soften** (Kill **not** triggered wholesale; Harden **unsupported**). Lab scratch was **not** on this fold VM; the gated fact set was copied from the Operator gate. Leading-edge residual (`B_lb`) / dense (`B_dense`) on the frozen Chan + RN `σ_ref=0.5` stack; absolute vs patent-facing **≤1 m**.

**Standing (record all):** **abstract ingest ADMIT** · **A1 Soften** · **A2 Soften (conditional)** · **A3 Soften** · **A4 Soften X/σ_t** · **GEOM0 HARDEN** (named 1 ns model; silent absolute-≤0.50 **Softened**) · **MULTIPATH1 Soften** (additive mild-NLOS; **not** this leftover) · **SYNC1 Soften** (Chan-alone near-ideal) · **JOINT1 Soften** (`σ_sync ≲ 3 ns` **fixed offsets**) · **DRIFT1 HARDEN** · **GATE1 Soften**.

## What the pulse settled

**Soften.** Kill is **not** triggered wholesale. **Harden unsupported.** Only **mild / intermittent** leading-edge residual (~**0.5–1 m** bias, or intermittent `f≈0.25`) survives patent-facing **≤1 m** under Chan + RN `σ_ref=0.5`. Persistent `B_lb ≳ 2 m` and `B_dense` **fail ≤1 m**.

- Mild / intermittent LE residual (~**0.5–1 m**, or `f≈0.25`) — **survives ≤1 m**.
- Persistent `B_lb ≳ 2 m` and `B_dense` — **fail ≤1 m**.
- Example `b=2` → abs **1.34 / 1.52**. Example `b=5` → ~**3.9**.
- Carry **A1 Soften** — Chan abs **0.832 m** @ `σ_ref=0.5`; **X = 0.50 m** perfect-ref only; do **not** Harden absolute **X**.
- Carry **A2 Soften (conditional)** — JOINT1 + differential ~**2.5 ns** F9T-class path-shared relative-clock; Kill bare Chan ~**1.14 m**; Kill commodity / common-view / absolute-only; Harden unsupported; brutal lock. 50 kHz `c/B` ~**6 km** = **resolution caution only**, **not** injected as fix error.
- Prior **GATE1 Soften** still stands (refuse belt; **not** a repair).
- Prior **DRIFT1 HARDEN** still stands (batch α; **not** free per-epoch realtime).
- Prior **JOINT1 Soften** still stands (`σ_sync ≲ 3 ns` **fixed offsets**).
- Prior **MULTIPATH1 Soften** still stands (LOS + mild/intermittent NLOS only on the perfect-ref sim **X**; **not** this leftover).
- **GEOM0 HARDEN** still stands as geometry-not-bottleneck under **perfect refs** + named noise.
- **Median-not-p90** honesty remains (1 ns p90 ≈ **1.16 m**).
- Honesty: path-shared **batch**, **not** free per-epoch realtime. **Not** multipath-robust. **Not** hardware.
- No fingerprint / ML / RF invent.
- **No claim-language product copy.**

That is an **Amb Soften** of the named indoor / first-arrival leftover. It is **not** a locator. It is **not** claim clearance.

## Combined bars (locked)

Two bars stay distinct:

- **Patent-facing ≤1 m xy** **stands**, **A3-scoped** (mild / intermittent LE residual on Chan + RN `σ_ref=0.5`). Persistent `B_lb ≳ 2 m` and `B_dense` stay out of budget.
- **Sim X = 0.50 m** stays **perfect-ref scoped sim only** (ideal-known refs + named GEOM0 noise + prior JOINT1 / DRIFT1 / GATE1 / mild-NLOS scopes; **median-not-p90**). **Not** an absolute bar under the RN floor. **Not** a patent promise.

**Named RN floor (A1, carried):** **DGPS ~0.4–0.5 m** absolute.

**A2 Soften (conditional, carried):** JOINT1 + ~2.5 ns F9T-class path-shared relative-clock. Commercial 1PPS does **not** carry either bar. 50 kHz `c/B` ~**6 km** is **resolution caution only**. Do **not** inject it as fix error.

**X is median-not-p90.** Hardware **X PARKED.** Link/map **PARKED.**

US10135667B1 — owner-requested **collaboration framing** (bibliographic; custom-beacon substrate, **not** a carrier-mast Amb). Published abstract is the **Amb spine** (ingest ADMITTED). **No claim-language copy.**

## What this string must do next (locked)

**A4 Soften X/σ_t** is already on the record ([`DIGESTION_A4.md`](DIGESTION_A4.md)). Suite DIGEST Soften Amb **ADMITTED** ([`DIGESTION_A1A4_SUITE.md`](DIGESTION_A1A4_SUITE.md)). **Greer send HOLD** until Founder rewrite + user OK. Prior write-up = **sync-fragility evidence only**. **Lab HOLD invent** (no named next pulse). Still **no RF / ML**. Do **not** invent a fingerprint rescue. Do **not** Harden indoor / first-arrival. Do **not** Harden absolute **X**. Hardware **X** stays **PARKED**. RF bench **PARKED**.

- **A4 Soften X/σ_t** — scored (honest 50 kHz phase-flip detection jitter ≫ 1 ns; distinct from this fold’s `c/B` ~6 km resolution caution).
- Suite DIGEST Soften Amb **ADMITTED**. **HOLD send** until Founder rewrite + user OK.

## What stays parked / closed

- **Hardware X** stays **PARKED**.
- **Send to Greer** stays **HOLD** until Founder rewrite + user OK.
- **Lab invent** stays **HOLD**.
- **Link/map** GIS/CAD overlay stays **PARKED**.
- **RF bench** stays **PARKED**.
- **A4 Soften X/σ_t** is already scored; ingest realtime leftover is **not** Hardened.
- **MULTIPATH1 Soften** still stands (additive mild-NLOS; **not** this leftover).
- **Cell-tower geometry** stays **PARKED**. Do **not** reopen as live.
- **BIA→weight portfolio** stays **CLOSED**. Do **not** reopen human, poultry, cattle, sheep, or companion BIA apps.
- **SkyMirr MuLCAT** stays its own Amb. This fold does **not** reopen it.
- **Collatz playground** stays **done** (#45). Lab HOLD there.
- **Track B invent** stays **paused**.
- **llm-gwt R-REPL** stays **parked**.

This note does **not** authorize sending the write-up. It does **not** show a TDOA locator. It does **not** start training. It does **not** unpark hardware **X**. It does **not** Harden indoor / first-arrival. It does **not** skip A4.
