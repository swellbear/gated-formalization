# Digestion — A1→A4 suite Soften wrap (scaffold)

A short plain suite write-up. Habit: [`docs/DIGESTION_HABIT.md`](../../docs/DIGESTION_HABIT.md). **Lab DIGEST was not on this VM.** This file is **scaffolded from the Operator gate**. Operator may follow-on when Lab DIGEST lands. It does **not** score a locator. It does **not** copy claims. It does **not** send to Greer.

**This wrap:** `2026-09_greer-sync-pulse-tdoa` A1→A4 — Method Operator **ADMIT** the suite Soften wrap. A4 this fold: **Soften X/σ_t**. Score: [`SCORE_A4.md`](SCORE_A4.md). A4 note: [`DIGESTION_A4.md`](DIGESTION_A4.md). A1 on disk: [`SCORE_A1.md`](SCORE_A1.md) · [`DIGESTION_A1.md`](DIGESTION_A1.md). A2 on disk: [`SCORE_A2.md`](SCORE_A2.md) · [`DIGESTION_A2.md`](DIGESTION_A2.md). A3 individual SCORE / DIGESTION: [`SCORE_A3.md`](SCORE_A3.md) · [`DIGESTION_A3.md`](DIGESTION_A3.md).

**Standing (record the suite):** **A1 Soften** · **A2 Soften-conditional** · **A3 Soften** · **A4 Soften X/σ_t** · abstract ingest **ADMITTED** · **GEOM0 HARDEN** (named 1 ns model) · **MULTIPATH1 Soften** · prior SYNC/JOINT/DRIFT/GATE = **partial** sync-fragility.

---

## Suite Soften wrap (A1→A4) — Operator gate (authoritative)

| Pulse | Gate | One-line |
|-------|------|----------|
| **A1 Soften** | Soften (Kill not triggered) | abs **≤1 m** under RN floor; **X=0.50** perfect-ref only; **DGPS floor named** |
| **A2 Soften-conditional** | Soften-conditional | **JOINT1+~2.5 ns** Soften; **Kill** bare Chan/commodity |
| **A3 Soften** | Soften | mild/intermittent LE (~**0.5–1 m** / `f≈0.25`) survives ≤1 m; persistent `B_lb ≳ 2 m` / `B_dense` fail (`b=2` → **1.34 / 1.52**; `b=5` → ~**3.9**) |
| **A4 Soften** | Soften X/σ_t | Soften **X/σ_t**; **RF PARKED** |

**A4 gate (this fold):**

> Honest 50 kHz phase-flip detection jitter ≫ GEOM0 1 ns (J_mid ~100–500 ns → tens of meters; J_stretch ~10 ns → ~3.8 m fails ≤1 m). JOINT1 does not cancel detection jitter. Not Kill wholesale (laptop model remains). Harden unsupported. RF bench PARKED.

**Greer send HOLD** until DIGEST + Founder fold. **No** claim-language product copy.

---

## A1 Soften (carried; on disk)

Operator **ADMIT Soften**. Kill **not** triggered. See [`SCORE_A1.md`](SCORE_A1.md) · [`DIGESTION_A1.md`](DIGESTION_A1.md).

- Absolute **≤1 m** poseable under DGPS-class RN survey error (Chan abs median **0.832 m** @ `σ_ref=0.5 m`, `σ_t=1 ns`).
- Absolute **≤0.50 m not** under that RN floor (**0.691 / 0.832** at 0.4 / 0.5).
- **X = 0.50 m** stays **perfect-ref scoped sim only**.
- JOINT1 scrape abs **0.449** @ `σ_ref=0.5` / `σ_sync=0` rides the floor — **do not Harden absolute X**.
- **DGPS ~0.4–0.5 m** absolute floor **named**.
- Silent GEOM0 absolute-≤0.50 **Softened**.

---

## A2 Soften-conditional (gate; individual file may follow-on)

Operator **ADMIT Soften-conditional**. See [`SCORE_A2.md`](SCORE_A2.md) · [`DIGESTION_A2.md`](DIGESTION_A2.md).

- **Soften** under **JOINT1 + differential ~2.5 ns (F9T-class)** path-shared relative-clock **named**.
- **Kill** bare Chan at ~2.5 ns (~**1.14 m** ≫ X).
- **Kill** commodity **20–50 ns** / common-view **~10 ns** / absolute-only **~5–15 ns** for **both** curves.
- **Harden unsupported** (public residuals **ns–tens-of-ns**, not `≪ 0.3 ns`).
- **Brutal lock:** patent simultaneous-via-DGPS-1PPS ≠ commercial 1PPS reality.

---

## A3 Soften (scored)

Operator **ADMIT Soften**. Kill **not** wholesale. Harden **unsupported**. See [`SCORE_A3.md`](SCORE_A3.md) · [`DIGESTION_A3.md`](DIGESTION_A3.md).

- Mild / intermittent LE (~**0.5–1 m** bias, or intermittent `f≈0.25`) **survives ≤1 m** under Chan + RN `σ_ref=0.5`.
- Persistent `B_lb ≳ 2 m` and `B_dense` **fail ≤1 m** (`b=2` → abs **1.34 / 1.52**; `b=5` → ~**3.9**).
- 50 kHz `c/B` ~**6 km** = **resolution caution only**, **not** injected as fix error. Distinct from A4 honest 50 kHz **phase-flip detection jitter**.
- This is **not** a substitute for our earlier **MULTIPATH1** additive-NLOS Soften, and it is **not** a Harden of indoor first-arrival.

---

## A4 Soften X/σ_t (this fold)

Operator **ADMIT Soften X/σ_t**. Kill **not** wholesale. See [`SCORE_A4.md`](SCORE_A4.md) · [`DIGESTION_A4.md`](DIGESTION_A4.md).

- Honest **50 kHz** phase-flip detection jitter **≫ GEOM0 1 ns**.
- **J_mid ~100–500 ns → tens of meters.**
- **J_stretch ~10 ns → ~3.8 m fails ≤1 m.**
- **JOINT1 does not cancel detection jitter.**
- Laptop model **remains** (not wholesale Kill).
- **Harden unsupported.**
- **RF bench PARKED.**

GEOM0 **HARDEN** still stands as geometry-not-bottleneck under the **named 1 ns model**. Silent “1 ns is an honest phase-flip detector” is **Softened**.

---

## Combined bars after the suite

| Bar | After A1→A4 |
|-----|-------------|
| **≤1 m xy** | Patent-facing object. Poseable under A1 RN floor **and** A3 mild/intermittent LE. **Fails** A3 persistent B_lb. **Fails** A4 J_stretch ~10 ns (~3.8 m). Commercial 1PPS does **not** carry it (A2). |
| **sim X = 0.50 m** | **Perfect-ref** scoped sim @ named **σ_t = 1 ns**. **Softened** as honest phase-flip (A4). **Not** absolute under RN floor (A1). **Not** a patent promise. |
| **σ_t honesty** | **Soften X/σ_t.** 1 ns is the named GEOM0 model, not an honest 50 kHz phase-flip floor. |
| **RN floor** | **DGPS ~0.4–0.5 m** (A1). |
| **A2 window** | JOINT1 + ~2.5 ns F9T-class path-shared relative-clock. Bare Chan / commodity **killed**. |
| **A3 window** | Mild/intermittent LE only for ≤1 m. |

Hardware **X PARKED.** RF bench **PARKED.** Link/map **PARKED.** Ingest realtime leftover **not** Hardened (batch remains).

US10135667B1 — owner-requested **collaboration framing**. Published abstract is the Amb spine. **No claim-language copy.**

---

## What this string must do next (HOLD)

**Greer send HOLD** until DIGEST + Founder fold. [`GREER_WRITEUP.md`](GREER_WRITEUP.md) stays **sync-fragility evidence only**. This scaffold is **not** the Founder send file.

**Lab HOLD invent.** Still **no RF / ML**. Do **not** invent a fingerprint rescue. Do **not** copy claims. Do **not** unpark an RF bench.

If Lab DIGEST lands later, Operator may replace or append this scaffold. Do **not** treat this file as Lab-authored DIGEST.

## What stays parked / closed / hold

- **RF bench** **PARKED**.
- **Hardware X** stays **PARKED**.
- **Link/map** **PARKED**.
- **Send to Greer** stays **HOLD** until DIGEST + Founder fold.
- **Lab invent** stays **HOLD**.
- **SkyMirr MuLCAT** stays its own Amb.
- **Cell-tower geometry** stays **PARKED**.
- **BIA→weight portfolio** stays **CLOSED**.
- **Collatz playground** stays **done** (#45).
- **Track B invent** stays **paused**.
- **llm-gwt R-REPL** stays **parked**.

This note does **not** authorize a send. It does **not** show a TDOA locator. It does **not** start training. It does **not** Harden 1 ns. It does **not** unpark hardware **X**.

---

*Scaffold from the Operator gate. Lab DIGEST was not on this VM. Soften suite ≠ claim clearance. Soften X/σ_t ≠ 1 ns Harden. Not Kill wholesale ≠ locator. No claim-language product copy. Not skill-met. Not rithm. Lab does not self-admit.*
