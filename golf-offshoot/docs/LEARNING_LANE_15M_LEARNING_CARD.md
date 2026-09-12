# 15m learning card

Figures from files. Not a verdict. Operator notes remain the verdict SoT.

**As-of:** journal generated_at=2026-09-12T05:16:57.330715-04:00

## What the book is doing now

- `R-BASELINE-FILL-ALL` (`execution: true`, kind=baseline). Book followed R-BASELINE-FILL-ALL: 32 fills, 0 skips (rule_decisions.json).
- `R-SKIP-HOUR-CLOSE` (`execution: true`, kind=selection). Book followed R-SKIP-HOUR-CLOSE: 110 fills, 39 skips (rule_decisions.json).

## On trial

`R-SKIP-HOUR-CLOSE` — Skip the paper fill when close_at clock minute equals 0 (hour-ending slot; skip_close_minute=0). Otherwise fill at the posted mark with entry_edge=0.0.

## Why we tried it

> # Lab — PROPOSED 03: skip the hour-ending 15m close **State:** **RUN-ONLY** by `operator` 2026-09-10 13:36 EDT. **Not** Softened, **not** admitted, **not** a board, **not** a dashboard figure.

Source: golf-offshoot\docs\LEARNING_LANE_15M_LAB_PROPOSED_03.md

## Kill / falsifier

> After the n named by the evidence bar in force (currently looks.first_look_n = 70), if selected-fill settlement_pnl cannot be distinguished from R-BASELINE-FILL-ALL on those same windows, park this rule. Do not retune skip_close_minute. Do not replace 0 with a tape-chosen slot. The bar is the governing source.

Source: registry `falsifier`

## Verdict

RUN-ONLY

Source: golf-offshoot\docs\LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_03.md

## Implemented?

`execution: true` — # Operator note — RUN-ONLY of Lab PROPOSED 03 (skip the hour-ending 15m close) **Verdict:** **RUN-ONLY** · Operator · 2026-09-10 13:36 EDT **Not an ADMIT.** Not Softened.

## Sources

- `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` sha256=71bd2f57c70b0f4a5062df048bc359a462628827505c39d16e06b85e04075008
- `C:/Users/bearh/gated-formalization-master-hub/golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_03.md` sha256=d9cf238874b1133541303fc068e98776b8d2eaaedeb07bef416102c6064a563d
- operator note sha256=3196a7c59774984b478c40fc8b97d3a77194b4654e615ebd03db7d3214c7a037
- input_fp: 81065a9f901c67e29e7f7e86abdaf4d06327a4d3bd34ec9e8d7f0812fbd187ef
- See Operator note for any fee arithmetic. Not reprinted here.
