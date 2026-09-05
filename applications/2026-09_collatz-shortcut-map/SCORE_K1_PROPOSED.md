# K1 score — Syracuse vs classic C + Control-A (PROPOSED; Operator-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_collatz-shortcut-map`  
**String:** leashed invent→test — finite-range steps-to-1 vs baseline + control  
**Check:** **K1 Syracuse** on **T1** (`N=10^4`, seed `20260905`)  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit. Hunt scripts are **not** on master.

This file **combines both Lab scores** (K1 vs classic **C**; Control-A) with the **Operator gate**. Small-number summary: [`k1_t1_summary.json`](k1_t1_summary.json).

**What this is not:** Collatz is **not** proved. This is **not** new dynamics. This is **not** “beats random affine.” This is **not** slogan clearance.

---

## 0. Plain-language framing

**What this is:** Lab ran the first ranked shortcut (**K1**, the Syracuse / odd-orbit form) on a finite pre-registered T1 board against classic Collatz **C**, then tried Control-A (random affine). Operator gated the pair.

**What this settles:** On T1, K1 mean steps-to-1 is below classic **C** and under the pre-registered 0.90 ratio bar. That is an **Amb HARDEN vs C only**. Honesty: K1 is **Collatz odd-orbit compression** (the forced half is folded into the odd branch). Control-A’s first draw was **identical to K1** (thin). The redraw pool did not yield a faithful reach-1 random affine → control limb **parked**.

**What this is not:** Not Collatz proved. Not new dynamics. Not “beats random affine.” Later K2/K3 gates are on their own score files. Track B invent stays **paused**. llm-gwt R-REPL stays **parked**.

---

## 1. Lab score A — K1 vs classic C (T1)

**Board:** T1 · **N:** `10^4` · **seed:** `20260905` · **fails:** 0 on both sides

| Map | Mean steps-to-1 | Median | Max | Fail |
|-----|-----------------|--------|-----|------|
| Classic **C** | 84.975 | 73 | 261 | 0 |
| **K1** Syracuse | 56.770 | 50 | 165 | 0 |

**Ratio** K1/C = **0.6681** ≤ **0.90** bar.

This is a cheaper **count** of the same odd orbit (forced halves folded in). It is **not** a new map family.

---

## 2. Lab score B — Control-A (random affine)

**First draw:** `(3,1)` — **identical to K1**. Thin. Does **not** show that K1 beats a distinct random affine.

**Redraw excluding `(3,1)`:** pool `{(5,1), (5,-1), (7,1)}`

| Pair | Read |
|------|------|
| `(5,1)` | smoke/T1 mostly timeouts; `ok_frac≈0.0255` |
| `(5,-1)` | fail smoke or T1 mostly timeouts |
| `(7,1)` | fail smoke or T1 mostly timeouts |

**No faithful reach-1 random affine** in that pool. Later standing rule: [`CONTROL_FIX.md`](CONTROL_FIX.md) — `(3,1)` permanently excluded; reach-1 fail → INCONCLUSIVE / park; do not fake beat-control.

---

## 3. Operator gate (authoritative)

**ADMIT Amb HARDEN vs C only.**

Honesty, required on the record:

- This is **Collatz odd-orbit compression** (forced half folded into the odd branch).
- **Not** new dynamics.
- **Not** Collatz proved.
- **Not** “beats random affine.”

**PARK control limb** as **wrong-piece / inconclusive.** First draw thin; redraw pool has no faithful reach-1 random affine.

**K2 / K3:** ungated on the K1 fold; later gated on [`SCORE_K2_PROPOSED.md`](SCORE_K2_PROPOSED.md) / [`SCORE_K3_PROPOSED.md`](SCORE_K3_PROPOSED.md) (K2 Amb HARDEN vs C; K3 novelty parked).

---

## 4. Amb remainder (named)

| Piece | Status | Remainder |
|-------|--------|-----------|
| K1 vs classic **C** on T1 | **hardened-vs-C** | Compression vs C only. Does **not** clear new dynamics. Does **not** prove Collatz. |
| Control-A (random affine reach-1) | **control-parked** (wrong-piece / inconclusive) | No faithful reach-1 random affine in the tried pool. Named gap still asked for a **control**; that limb is parked, not met. |
| K2 / K3 | later gated | See K2 / K3 score files. Not gated on this K1 board. |

---

## 5. Unchanged strings

- **Track B** invent remains **paused**.
- **llm-gwt R-REPL** remains **parked**.
- Ordinary CPU only. Hunt scripts **not** merged.

---

*Docs only. Amb HARDEN vs C ≠ new dynamics. Control parked ≠ “beats random affine.” Not Collatz proved. Lab does not self-admit.*
