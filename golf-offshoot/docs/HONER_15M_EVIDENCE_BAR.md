# honer_15m evidence bar (DRAFT — not binding)

**Lane:** `honer_15m` · series `KXBTC15M` only  
**Binding?** **N.**  
**Admit?** N · **Edge established?** N · Trading **NOT ARMED**

This is not the live 15m bar. Do not copy δ=$0.28 or sd=0.784 from that file. Compute δ/sd from the sibling **exam** sample at first score.

## Contrast

On the same exam windows:

`d_i = pnl_exam_i − pnl_fill_all_i`

Fill-all is a **counterfactual** always-YES at the same mark. Not Lineage A. Not a third ledger.

- Exam fill vs fill-all: `d_i = 0` (same ticket).
- Exam skip vs fill-all: `d_i = 0 − pnl_fill_all`.

The exam only differs on skips.

Fee-adj is **applied at score time** via factory `fee_adjust` citing `founder_browser_bytes` pin `c326a69f596a11e8f8be2620402d39a8d4823920c21cc97c93a114d862699601`. Search/exam ledgers stay gross. Do not print a fee-adjusted honer total on the hub, digest, or `records[]`. Keep-lock stays closed while this bar is unbound.

## Looks

- L1: first 70 exam settles after the snapshot `declared_at`.
- L2 (71–140) is named and **not scored in this build**.
- Futility at n=20 and n=40: remaining windows treated as skips (`d=+1` each, exam pnl 0). Park if mean(d)≤0 or exam mean pnl≤0 at 70 under that path.
- Search starvation looks (honer search clock only, not this exam sample): n=40 zero in-band visits; n=70 in-band < freeze_min. Outcome `search_untestable` does not increment sibling k and is not a score.
- `α_k = 0.05 / (k(k+1))` with sibling `k` from `latest/trials.json` (increments on freeze).
- Permutation seed **20260909**.

## Pass clauses (non-binding)

1. t-test vs H0 mean(d)≤δ at α_k (δ from this exam sample, not the live bar).
4. Exam-side mean pnl > 0.
5. Permutation at seed 20260909.

Do not claim Established. Do not bind in this build.

## Keep-lock

`can_keep()` is false while any of: `fee_omitted`, `binding != true`, `lab_admits`, trading armed.

A green exam (`classify_completed_exam` → `completed_unscored`) is a **library label**, not a keep. `permutation_mean_d` and `alpha_k` stay callable and unwired to keep.

Do not pin a fee sha256 placeholder. Honer **cites and applies** the factory `schedule_sha256` (`honer_15m.fee.cite_factory_pin` then `apply_factory_fee`). A cite alone does not clear `fee_omitted`. After the dated apply, `fee_omitted` is false and `can_keep()` stays false until `binding` is true. This is not consult enable.

δ/sd stay provisional on this sibling exam sample. Do not copy live-bar 0.28 / 0.784.

