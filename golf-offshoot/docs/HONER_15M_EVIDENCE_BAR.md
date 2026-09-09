# honer_15m evidence bar (DRAFT — not binding)

**Lane:** `honer_15m` · series `KXBTC15M` only  
**Binding?** **N.** `founder_read_once` false.  
**Admit?** N · **Edge established?** N · Trading **NOT ARMED**

This is not the live 15m bar. Do not copy δ=$0.28 or sd=0.784 from that file. Compute δ/sd from the sibling **exam** sample at first score.

## Contrast

On the same exam windows:

`d_i = pnl_exam_i − pnl_fill_all_i`

Fill-all is a **counterfactual** always-YES at the same mark. Not Lineage A. Not a third ledger.

- Exam fill vs fill-all: `d_i = 0` (same ticket).
- Exam skip vs fill-all: `d_i = 0 − pnl_fill_all`.

The exam only differs on skips.

Fee-adj is **omitted** (zero-fee mid). Name that. Do not print a corrected total.

## Looks

- L1: first 70 exam settles after the snapshot `declared_at`.
- L2 (71–140) is named and **not scored in this build**.
- Futility at n=20 and n=40: remaining windows treated as skips (`d=+1` each, exam pnl 0). Park if mean(d)≤0 or exam mean pnl≤0 at 70 under that path.
- `α_k = 0.05 / (k(k+1))` with sibling `k` from `latest/trials.json` (increments on freeze).
- Permutation seed **20260909**.

## Pass clauses (non-binding)

1. t-test vs H0 mean(d)≤δ at α_k (δ from this exam sample, not the live bar).
4. Exam-side mean pnl > 0.
5. Permutation at seed 20260909.

Do not claim Established. Do not bind in this build.

## Keep-lock

`can_keep()` is false while any of: `fee_omitted`, `binding != true`, `founder_read_once != true`, `lab_admits`, trading armed.

A green exam (`classify_completed_exam` → `completed_unscored`) is a **library label**, not a keep. `permutation_mean_d` and `alpha_k` stay callable and unwired to keep.

Do not pin a fee sha256 placeholder. If the factory later pins `schedule_sha256`, honer may cite it and still omit fee from totals until a **dated honer fee-apply** (out of this build).

δ/sd stay provisional on this sibling exam sample. Do not copy live-bar 0.28 / 0.784.

