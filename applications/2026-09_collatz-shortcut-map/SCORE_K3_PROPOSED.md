# K3 score — mod-16 table vs K2 packaging (PROPOSED; Operator-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_collatz-shortcut-map`  
**String:** leashed invent→test — finite-range steps-to-1 vs baseline + control  
**Check:** **K3** mod-16 table on **T1** (`N=10^4`; same T1 board as K1/K2)  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Control hygiene:** [`CONTROL_FIX.md`](CONTROL_FIX.md)  
**Sibling:** [`SCORE_K2_PROPOSED.md`](SCORE_K2_PROPOSED.md)  
**Protocol (short):** invent→test habit [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md); named-gap ledger [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Lab invents; Operator admits / rejects / parks. Lab does **not** self-admit. Hunt scripts are **not** on master.

This file **combines the Lab scores** (K3 vs K2-step; Control-C affine; Syracuse orbit-control) with the **Operator gate**.

**What this is not:** Collatz is **not** proved. This is **not** new dynamics. This is **not** K3 novelty. This is **not** “beats random affine.”

---

## 0. Plain-language framing

**What this is:** Lab ran a third ranked option (**K3**, a mod-16 lookup table) on the same T1 board. Operator gated whether it is a new shortcut or a packaging of K2.

**What this settles:** K3 T1 mean steps-to-1 is **28.705**, **identical** to K2, with **0 mismatches** vs the K2-step. That is **packaging of K2**, not a new map. Affine Control-C is **INCONCLUSIVE / park** (9999/9999 fail). vs Syracuse orbit-control 28.705 ≤ 56.770 is a **restatement** of the already-gated K2 > K1 compression ladder, **not** K3 novelty. C-limb HARDEN-TAG for K3 = **restatement of K2 only**.

**What this is not:** Not Collatz proved. Not new dynamics. Not a third distinct harden. Track B invent stays **paused**. llm-gwt R-REPL stays **parked**.

---

## 1. Lab score A — K3 vs K2-step (T1)

**Board:** T1 · **N:** `10^4`

| Map | Mean steps-to-1 | vs K2-step |
|-----|-----------------|------------|
| **K2** max 2-batching | 28.705 | — |
| **K3** mod-16 table | 28.705 | **0 mismatches** |

K3 is a **lookup packaging** of the same K2 step. It is **not** a new invent.

---

## 2. Lab score B — Control-C (random affine)

**Pool:** standing [`CONTROL_FIX.md`](CONTROL_FIX.md) — `(3,1)` excluded; matched control must not equal the candidate.

**Result:** **9999/9999 fail** (no faithful reach-1 random affine).

**Disposition:** **INCONCLUSIVE / park**. Do **not** fake beat-control.

---

## 3. Lab score C — vs Syracuse orbit-control

| Map | Mean steps-to-1 |
|-----|-----------------|
| Syracuse / K1 orbit-control | 56.770 |
| **K3** (≡ K2) | 28.705 |

K3 **28.705 ≤ 56.770**.

This is a **restatement** of the already-recorded **K2 > K1** compression ladder. It is **not** K3 novelty. C-limb HARDEN-TAG for K3 = **restatement of K2 only**.

---

## 4. Operator gate (authoritative)

**PARK novelty.**

Honesty, required on the record:

- K3 is **packaging of K2** (identical T1 mean; 0 mismatches vs K2-step).
- **Not** new dynamics.
- **Not** Collatz proved.
- **Not** a third distinct Amb HARDEN vs C.
- Affine Control-C: **INCONCLUSIVE / park** (9999/9999 fail).
- vs Syracuse orbit-control is **restatement of K2 only**, not K3 novelty.

---

## 5. Amb remainder (named)

| Piece | Status | Remainder |
|-------|--------|-----------|
| K3 vs K2 | **novelty parked** | Packaging, not invent. |
| Control-C (random affine) | **parked** (INCONCLUSIVE) | 9999/9999 fail. Do **not** fake beat-control. |
| vs Syracuse orbit-control | **restatement of K2** | K2 > K1 ladder already on [`SCORE_K2_PROPOSED.md`](SCORE_K2_PROPOSED.md) / [`SCORE_K1_PROPOSED.md`](SCORE_K1_PROPOSED.md). |
| C-limb HARDEN-TAG (K3) | **restatement of K2 only** | Do **not** count a second C-harden for K3. |

---

## 6. Unchanged strings

- **Track B** invent remains **paused**.
- **llm-gwt R-REPL** remains **parked**.
- Ordinary CPU only. Hunt scripts **not** merged.

---

*Docs only. Packaging ≠ invent. Restatement ≠ novelty. Affine parked ≠ “beats random affine.” Not Collatz proved. Lab does not self-admit.*
