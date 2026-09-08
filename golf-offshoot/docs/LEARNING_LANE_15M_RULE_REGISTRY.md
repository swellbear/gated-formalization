# 15m rule registry — declare before outcomes

**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Opened:** 2026-09-08 05:56 EDT
**Admit?** N · **Soften?** N · **lab_admits?** false · Trading **NOT ARMED**

A rule that is not dated before its windows close cannot use those windows as a clean out-of-sample test. Every hour collected before a declaration is an hour that cannot serve that rule. This file is the mechanic. The dated rows live in [`LEARNING_LANE_15M_RULES.json`](LEARNING_LANE_15M_RULES.json).

## How a rule is declared

1. Write a row in `LEARNING_LANE_15M_RULES.json` **before** the first window it may be scored on has closed.
2. `declared_at` is Eastern ISO-8601. It does not move. Restating the rule does not back-date it.
3. A window is eligible for that rule only when its `close_time` is **strictly after** `declared_at`.
4. Pre-declaration windows may be described as history. They are **in-sample for discovery, never OOS for that rule**.
5. Execution (`execution=true`) is separate from declaration. Dating starts at `declared_at` even if the loop is still filling every window. `execution=false` does **not** stall the OOS clock.
6. This is not an ADMIT. A live paper rule is still `entry_edge` arithmetic, not a claim.

## Replay is not a lived result

`R-SKIP-COINFLIP` is declared with `execution=false`. Every window that closes after `2026-09-08T05:56:00-04:00` is already a clean out-of-sample test of that rule **by replay**: the books are being collected without the rule acting on them, so it can be scored counterfactually against data it demonstrably could not have influenced. The declaration timestamp is what makes the data clean, not the execution flag. Wiring `paper.py` only blocks **live** behavior.

Write this down before anyone conflates them later: **a replayed result and a lived result are different evidence.** Replay assumes fills that live execution might not get. Skipping a bet changes nothing about the market and does change the fill sequence. Both are legitimate. They are not interchangeable.

## What the loop could not do until this file

`paper.py` fills every candidate at the posted mark with `entry_edge=0.0`. That is a behavior, not a declared rule. It could not express "skip this window" or "only these windows." `rules.py` is the expression half. The live loop still fills every window until a row sets `execution=true`.

## First dated rows (week still young)

See the JSON. Two rows were dated 2026-09-08 05:56 EDT:

- `R-BASELINE-FILL-ALL` — names the mechanical fill that has been running. Not a tested edge. Overnight 56 locked books are **not** OOS for a later-declared selection rule, and they are not an unbroken run (`072245` gap).
- `R-SKIP-COINFLIP` — first selection rule: skip when posted YES is inside `(0.45, 0.55)`. `execution=false` until the paper loop is wired to honor it. Windows that close after `declared_at` are the clean OOS set. Do not retune the band from last night's tape.

## Hard NOs

- Do not back-date `declared_at` after seeing a result
- Do not score a rule on a window that closed at or before `declared_at`
- Do not treat `R-BASELINE-FILL-ALL` as edge
- Do not sum lineage A and B to score a rule
- Do not invent a fill for `KXBTC15M-26SEP072245`
- Golf idle stays ON. Series HOLD stays `KXBTC15M` only
