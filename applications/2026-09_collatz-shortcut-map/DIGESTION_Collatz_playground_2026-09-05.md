# Digestion — Collatz shortcut-map playground (2026-09-05)

A plain-English write-up of a finished playground string. This does **not** prove Collatz. It does **not** authorize new invent. Lab stays held.

**What this is:** A digestion of `2026-09_collatz-shortcut-map` — a leashed invent→test on whether a named shortcut reduces average steps-to-1 on a finite pre-registered range versus classic Collatz **C** and a control. Habit: [`docs/DIGESTION_HABIT.md`](../../docs/DIGESTION_HABIT.md). Incoming lesson from the last string stays on [`DIGESTION_FROM_LLM_GWT.md`](DIGESTION_FROM_LLM_GWT.md).

---

## What this playground tried

See whether a cheap, named rewrite of the Collatz step could lower the **average application count** (mean steps-to-1) on a finite T1 board (`N=10^4`) versus classic **C**, and versus a control that was supposed to be a distinct reach-1 map.

Lab invented ranked options (**K1** Syracuse / odd-orbit form, **K2** max 2-batching, **K3** a mod-16 table). Operator gated each. Lab does **not** self-admit.

It was **not** trying to prove the Collatz conjecture, clear an unbounded speedup, or reopen Track B / llm-gwt.

---

## What fog moved

On T1 (`N=10^4`), **K1** and **K2** reduce mean application count versus classic **C** by **Collatz-orbit compression** — counting the same orbit with forced halves folded in (K1) or with **max 2-batching** (K2).

| Check | Mean steps-to-1 | vs classic C (84.975) | Operator gate |
|-------|-----------------|------------------------|---------------|
| **K1** Syracuse | 56.770 | ratio **~0.67** (0.6681) | **ADMIT Amb HARDEN vs C only** |
| **K2** max 2-batching | 28.705 | ratio **~0.34** (0.3378) | **ADMIT Amb HARDEN vs C** |

Fails were **0** on those vs-C boards. Ambiguity **HARDEN** here means the finite-range vs-C comparison got tighter. It is **not** new dynamics. It is **not** Collatz proved.

Scores: [`SCORE_K1_PROPOSED.md`](SCORE_K1_PROPOSED.md) · [`SCORE_K2_PROPOSED.md`](SCORE_K2_PROPOSED.md).

---

## What was a counting artifact

- **Random affine controls mostly do not reach 1.** Control-A redraw, Control-B (`ok_frac≈0.008`), and Control-C (**9999/9999 fail**) are **INCONCLUSIVE / parked** as **wrong-piece**. Do **not** fake beat-control. Standing rule: [`CONTROL_FIX.md`](CONTROL_FIX.md).
- **Control-A once equaled K1.** First draw `(3,1)` is identical to K1 Syracuse. Thin. That pair is **permanently excluded** from later pools. Matched controls must **not** equal the candidate.
- **K3 was packaging, not invent.** Mod-16 table T1 mean **28.705**, **identical** to K2, **0 mismatches** vs the K2-step. **PARK novelty.** vs Syracuse 28.705 ≤ 56.770 is a **restatement** of the K2 > K1 compression ladder, not K3 novelty. C-limb HARDEN-TAG for K3 = **restatement of K2 only**. Score: [`SCORE_K3_PROPOSED.md`](SCORE_K3_PROPOSED.md).

---

## Thin orbit control

Same-orbit **even strip-1 only** (Control-B-orbit) mean **29.205**. K2 **28.705 ≤ 29.205**. Operator **ADMIT THIN** Amb bite: **max 2-batching slightly beats strip-1-only** on the **same** Collatz orbit.

That is a thin counting difference. It is **not** “beats random affine.” It is **not** new dynamics.

---

## What’s left / what we refuse

Park these clearly so they do not vanish:

- **Collatz is not proved.** Finite T1 compression is not the conjecture.
- **No unbounded claims.** No “faster for all n.” No slogan clearance.
- **Affine-control limb stays parked** as **wrong-piece / INCONCLUSIVE**. Random affines that fail reach-1 are not a lost horse and are not a win.
- **K3 novelty stays parked.** Packaging is not a third shortcut.
- **K1 / K2 vs C stays an Amb HARDEN only** — orbit compression, not new dynamics.
- **Track B invent stays paused.** This playground does **not** reopen it.
- **llm-gwt R-REPL stays parked.** This playground does **not** reopen it.

---

## Where invent sits now

**Playground invent is complete. Lab is HOLD.**

No new Collatz invent authorization lives in this note. Lab stays held for a **Founder real-problem discussion**. Do not mint a K4. Do not redraw another random affine to force a beat-control. Do not treat this write-up as a green light.

---

## Digestion lesson carried

The incoming lesson from llm-gwt still holds, and this playground did not break it:

- Stay **CPU-runnable**. No GPU. No weights. No API keys.
- **Do not invent checks that need infra we lack.** An infra-kill is not a hallmark fail and is not clearance.

This playground stayed on ordinary CPU. That part worked. The affine-control bar did **not** work as a reach-1 test. Honesty is to park that limb, not to pretend it lost.

---

## Pointers

| Record | What it is |
|--------|------------|
| [`SCORE_K1_PROPOSED.md`](SCORE_K1_PROPOSED.md) | K1 vs C HARDEN; Control-A parked |
| [`SCORE_K2_PROPOSED.md`](SCORE_K2_PROPOSED.md) | K2 vs C HARDEN; Control-B parked; THIN orbit bite |
| [`SCORE_K3_PROPOSED.md`](SCORE_K3_PROPOSED.md) | K3 novelty parked; Control-C parked; restatement of K2 |
| [`CONTROL_FIX.md`](CONTROL_FIX.md) | Permanent `(3,1)` exclusion; no fake beat-control |
| [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) | Scoreboard lines |
| [`DIGESTION_FROM_LLM_GWT.md`](DIGESTION_FROM_LLM_GWT.md) | Incoming CPU / no-infra lesson |

---

*Docs only. Playground invent complete. Lab HOLD. Not Collatz proved. Amb HARDEN ≠ new dynamics. Affine parked ≠ “beats random affine.” Packaging ≠ invent. Track B paused. llm-gwt R-REPL parked.*
