# K2 score — max 2-batching vs classic C + Control-B (PROPOSED; Operator-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_collatz-shortcut-map`  
**String:** leashed invent→test — finite-range steps-to-1 vs baseline + control  
**Check:** **K2** max 2-batching on **T1** (`N=10^4`; same T1 board as K1, classic **C** mean 84.975)  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Control hygiene:** [`CONTROL_FIX.md`](CONTROL_FIX.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit. Hunt scripts are **not** on master.

This file **combines both Lab scores** (K2 vs classic **C**; Control-B affine + Control-B-orbit) with the **Operator gate**.

**What this is not:** Collatz is **not** proved. This is **not** new dynamics. This is **not** “beats random affine.” This is **not** slogan clearance.

---

## 0. Plain-language framing

**What this is:** Lab ran the second ranked shortcut (**K2**, max 2-batching on the Collatz orbit) on the same finite T1 board against classic **C**, then tried Control-B (random affine) and a same-orbit strip-1 control. Operator gated the set.

**What this settles:** On T1, K2 mean steps-to-1 is below classic **C** and under the pre-registered 0.90 ratio bar. That is an **Amb HARDEN vs C**. Honesty: K2 is **max 2-batching on the Collatz orbit** (forced halves grouped). Affine Control-B did not yield a faithful reach-1 random affine → **PARK** INCONCLUSIVE / wrong-piece. Same-orbit even strip-1 only (Control-B-orbit) is a **THIN** Amb bite: K2 28.705 ≤ 29.205. That is **not** “beats random affine.”

**What this is not:** Not Collatz proved. Not new dynamics. Not a reason to treat K3 as novelty. Track B invent stays **paused**. llm-gwt R-REPL stays **parked**.

---

## 1. Lab score A — K2 vs classic C (T1)

**Board:** T1 · **N:** `10^4` · **fails:** 0 on both sides · **C** matches the K1 T1 board

| Map | Mean steps-to-1 | Fail |
|-----|-----------------|------|
| Classic **C** | 84.975 | 0 |
| **K2** max 2-batching | 28.705 | 0 |

**Ratio** K2/C = **0.3378**.

This is a cheaper **count** of the same Collatz orbit (max two forced halves batched). It is **not** a new map family.

---

## 2. Lab score B — Control-B (random affine)

**Pool:** standing [`CONTROL_FIX.md`](CONTROL_FIX.md) — K1’s `(3,1)` **excluded**; matched control must not equal the candidate.

**Result:** all pool **fail smoke** / `ok_frac≈0.008`. No faithful reach-1 random affine.

**Disposition:** **PARK** as **INCONCLUSIVE / wrong-piece**. Do **not** fake beat-control.

---

## 3. Lab score C — Control-B-orbit (same orbit, even strip-1 only)

**Object:** same Collatz orbit; even strip-1 only (not random affine).

| Map | Mean steps-to-1 |
|-----|-----------------|
| Control-B-orbit (strip-1 only) | 29.205 |
| **K2** max 2-batching | 28.705 |

K2 **28.705 ≤ 29.205**.

This is a **THIN** Amb bite: max 2-batching vs strip-1 on the **same** orbit. It is **not** “beats random affine.”

---

## 4. Operator gate (authoritative)

**ADMIT Amb HARDEN vs C.**

Honesty, required on the record:

- This is **max 2-batching on the Collatz orbit**.
- **Not** new dynamics.
- **Not** Collatz proved.
- **Not** “beats random affine.”

**PARK** affine Control-B as **INCONCLUSIVE / wrong-piece** (all pool fail smoke / `ok_frac≈0.008`).

**ADMIT THIN** Amb bite on Control-B-orbit (max batching vs strip-1). Not a random-affine win.

K3 is recorded on its own score ([`SCORE_K3_PROPOSED.md`](SCORE_K3_PROPOSED.md)) — **not** self-admitted here.

---

## 5. Amb remainder (named)

| Piece | Status | Remainder |
|-------|--------|-----------|
| K2 vs classic **C** on T1 | **hardened-vs-C** | Max 2-batching vs C only. Does **not** clear new dynamics. Does **not** prove Collatz. |
| Control-B (random affine reach-1) | **parked** (INCONCLUSIVE / wrong-piece) | No faithful reach-1 random affine. Do **not** fake beat-control. |
| Control-B-orbit (strip-1) | **THIN** Amb bite | Max 2-batching slightly cheaper than strip-1 on the same orbit. Not “beats random affine.” |
| K3 | see [`SCORE_K3_PROPOSED.md`](SCORE_K3_PROPOSED.md) | Packaging / novelty parked on that board. |

---

## 6. Unchanged strings

- **Track B** invent remains **paused**.
- **llm-gwt R-REPL** remains **parked**.
- Ordinary CPU only. Hunt scripts **not** merged.

---

*Docs only. Amb HARDEN vs C ≠ new dynamics. Affine parked ≠ “beats random affine.” THIN orbit bite ≠ clearance. Not Collatz proved. Lab does not self-admit.*
