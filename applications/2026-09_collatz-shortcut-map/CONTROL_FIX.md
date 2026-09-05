# Control fix (permanent) — Collatz shortcut-map playground

**Date:** 2026-09-05  
**Application:** `2026-09_collatz-shortcut-map`  
**Standing rule** for this string. Lab copy was **not** on this fold VM (`/workspace/collatz_lab/CONTROL_FIX.md` missing). Record below is the Operator-gated fix.

This is a **control hygiene** rule. It does **not** prove Collatz. It does **not** clear a shortcut. It does **not** authorize invent.

---

## 0. Plain-language framing

**What this is:** A permanent rule about what counts as a matched control on this playground.

**What this settles:** A control that is the same map as the candidate is **not** a control. A random affine that does not reach 1 is **not** a lost horse — that limb is **INCONCLUSIVE** and gets parked. Do **not** fake a beat-control.

**What this is not:** Not a reason to say a shortcut “beats random affine.” Not Collatz proved. Not new dynamics.

---

## 1. Permanent pool exclusion

**Control-A pool permanently excludes K1’s `(3,1)`.**

K1 Syracuse is the affine `(3,1)` on the odd branch. Drawing `(3,1)` as Control-A is **identical to the candidate**. That draw was **thin**. It stays out of every later Control-A / random-affine pool on this string.

---

## 2. Matched-control rule

A matched control **must not equal the candidate**.

If a draw is the same map (same pair, same orbit rewrite, same packaging), it is **thin**. It does **not** count as beating a distinct control. Redraw or park. Do **not** score it as a win.

---

## 3. Reach-1 failure → INCONCLUSIVE / park

If a random affine **fails to reach 1** (smoke fail, timeout-heavy board, `ok_frac` near zero, all-n fail):

- that limb is **INCONCLUSIVE**
- **park** it as **wrong-piece**
- do **not** treat the miss as “candidate beats control”
- do **not** invent a fake beat-control by dropping the reach-1 requirement

Tried affine pools on this playground (see score files) did not yield a faithful reach-1 random affine. That is a **parked limb**, not a cleared control bar.

---

## 4. What still may be scored (thin, named)

Same-orbit **strip** controls (for example even strip-1 only, vs max 2-batching on the **same** Collatz orbit) are a **different** object from random affine. They may take a **THIN** Amb bite if the Operator gates them. They are **not** “beats random affine.”

---

## 5. Unchanged strings

- **Track B** invent remains **paused**.
- **llm-gwt R-REPL** remains **parked**.
- Ordinary CPU only.

---

*Docs only. Identical-to-candidate ≠ control. Reach-1 fail ≠ beat-control. Not Collatz proved.*
