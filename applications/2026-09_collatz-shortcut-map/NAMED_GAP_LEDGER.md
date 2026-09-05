# Named-gap ledger — Collatz shortcut map

Habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). One line per open gap. This is a problem-solving scoreboard, **not** a proof.

**Opened:** 2026-09-05 — Founder opens the **Collatz shortcut-map** leashed invent→test string. Lab invents ranked shortcuts. Operator gates.

**Last check:** **K1** Syracuse on T1 (`N=10^4`, seed `20260905`). Operator **ADMIT Amb HARDEN vs C only**. Control limb **PARK**ed (wrong-piece / inconclusive). Score: [`SCORE_K1_PROPOSED.md`](SCORE_K1_PROPOSED.md).

**What this is not:** Collatz is **not** proved. K1 is **not** new dynamics. This is **not** “beats random affine.” Hunt scripts are **not** merged.

**Process:** Lab invents 2–3 ranked options for this named gap (why / cost / kill-vs-harden). Operator admits, rejects, or parks. Lab does **not** self-admit. Invent→test: [`docs/INVENT_TEST_HABIT.md`](../../docs/INVENT_TEST_HABIT.md).

**Run constraint:** ordinary CPU only — no GPU, no weights, no API keys.

**Track B invent** remains **paused** (unchanged).  
**llm-gwt R-REPL** remains **paused** (unchanged).

## Lines

`shortcut reducing average stopping time / steps-to-1 on a finite pre-registered range vs baseline + control` → kill vs harden: a cheap pre-registered check that would drop the shortcut (no average-step reduction vs baseline and control) vs only tighten the finite-range comparison → last check: **K1** T1 (ratio K1/C = 0.6681 ≤ 0.90; 0 fail) → status: **hardened-vs-C** / **control-parked**

`Amb remainder — K1 vs C is odd-orbit compression only; Control-A random affine is not a faithful reach-1 control` → kill vs harden: a distinct reach-1 control (not identical to K1; not a timeout-heavy affine) vs only restating the T1 vs-C ratio → last check: Control-A first draw `(3,1)` identical to K1 (thin); redraw pool `{(5,1),(5,-1),(7,1)}` fail smoke or T1 mostly timeouts (`ok_frac≈0.0255` for `(5,1)`) → status: **wrong-piece** / **paused** (control limb)

`K2 / K3 ranked shortcuts` → kill vs harden: gated only if Operator unlocks; do not self-admit → last check: none this fold → status: **HOLD**
