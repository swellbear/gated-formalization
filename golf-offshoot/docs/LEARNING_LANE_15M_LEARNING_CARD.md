# 15m learning card

Figures from files. Not a verdict. Operator notes remain the verdict SoT.

**As-of:** journal generated_at=2026-09-12T07:46:56.793338-04:00

## What the book is doing now

- `R-BASELINE-FILL-ALL` (`execution: true`, kind=baseline). Book followed R-BASELINE-FILL-ALL: 34 fills, 0 skips (rule_decisions.json).

## On trial

`R-SKIP-CIVIL-BOUNDARIES` — Skip the paper fill when close_at clock minute is 0 or 30 (civil hour and half-hour walls; skip_close_minutes=[0, 30]). Otherwise fill at the posted mark with entry_edge=0.0.

## Why we tried it

> # Lab — PROPOSED 04: skip the civil hour and half-hour walls **State:** **PROPOSED.** **Not** Softened, **not** admitted, **not** a board, **not** a dashboard figure. `execution=false` this turn.

Source: golf-offshoot\docs\LEARNING_LANE_15M_LAB_PROPOSED_04.md

## Kill / falsifier

> After the n named by the evidence bar in force (currently looks.first_look_n = 70), if selected-fill settlement_pnl cannot be distinguished from R-BASELINE-FILL-ALL on those same windows, park this rule. Do not retune skip_close_minutes. Do not replace {0, 30} with a tape-chosen pair. The bar is the governing source.

Source: registry `falsifier`

## Verdict

not yet ruled.

Source: —

## Implemented?

`execution: false`

## Sources

- `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` sha256=be9e2dedc3ff93ea6ce92cd7fed19051db15110a7e0c70325aa6f5f0b835e048
- `C:/Users/bearh/gated-formalization-master-hub/golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_04.md` sha256=863cd99d1b7125a5b83ff6536e872e5a816a47ccc25e5455f80663a3b672478d
- input_fp: 68c16a09206f705754e645d6179d52eb30b2d90782b9547a408f6b28a56e4a65
- See Operator note for any fee arithmetic. Not reprinted here.
