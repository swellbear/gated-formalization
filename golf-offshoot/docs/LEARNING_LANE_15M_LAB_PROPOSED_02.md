# Lab — PROPOSED 02: skip an incomplete public book

**State:** **PROPOSED.** Not Softened, **not** admitted, **not** RUN-ONLY, **not** a board, **not** a dashboard figure. Operator decides.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `lab` — `lab_admits=false`. Lab never admits its own candidate ([`.cursor/skills/gpf-lab/SKILL.md`](../../.cursor/skills/gpf-lab/SKILL.md)).
**Admit?** N · **Soften?** N · **Trading ARMED?** N · **Keys / orders / cash?** none
**Written:** 2026-09-08 15:41 EDT · **Declared:** `2026-09-08T15:41:00-04:00` in [`LEARNING_LANE_15M_RULES.json`](LEARNING_LANE_15M_RULES.json)
**Rule id:** `R-SKIP-INCOMPLETE-BOOK` · `execution: false` · `selects: true`

**Gate this was written under.** Desk honesty checklist is open (14:18 ET restamp). CoS assigned this invent at 14:58 ET after `decide()` was live: one PROPOSED selection rule, KXBTC15M paper only, do not revive `R-SKIP-COINFLIP`. This is park row 9's trigger (a later PROPOSED that actually selects), **not** park row 8 (a new named horse / WC3+ board). Golf idle stays **ON**.

**Burned classes loaded** from [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json) before the class was named. `class_is_burned("R-SKIP-INCOMPLETE-BOOK")` is false. This is not `CROSS`, `SPREAD`, `THRESH`, `FEE-AS-SIGNAL`, `RETUNE-COINFLIP-BAND`, `BASELINE-AS-EDGE`, or `R-SKIP-COINFLIP`. Do not retune the `(0.45, 0.55)` band. Do not score. Do not bind.

---

## 1. The residual, in one paragraph

Park row 9 still holds: the paper writer records `entry_edge=0.0` and the model is the market. PROPOSED 01 priced the omitted fee. It did not select. `R-SKIP-COINFLIP` is a selection rule, but its band is not verifiably pre-registered, so it cannot Establish, and this turn does not revive it or flip it.

`public_mid_or_last` will still mint a `paper_mark` from `last` when `yes_bid` or `yes_ask` is missing ([`kalshi_15m.py`](../src/golf_offshoot/data_feeds/kalshi_15m.py) `public_mid_or_last`). A last print is a display price, not a two-sided book. Filling that print pretends a posted market that was not quoted. The residual this rule names is **book completeness**, not direction and not a fee-as-signal.

Lab did **not** open `paper/*.json`, `settlements/*.json`, or `latest/journal.json` to choose this class or its parameters. No post-declaration window outcome was read. No skip rate was computed.

---

## 2. The one rule

**Skip the paper fill when the public book is incomplete. Otherwise fill at the posted mark with `entry_edge=0.0`.**

Incomplete means any of: `yes_bid` missing, `yes_ask` missing, or not `yes_bid < yes_ask`. A locked book (`bid == ask`) is incomplete for a taker. A crossed book (`bid > ask`) is incomplete.

The rule does **not** inspect `posted_yes` to pick the window. It does not change the fill price. It does not choose YES vs NO. Valid-quote bounds already enforced by `is_paper_autobet_candidate` (`0 < mark < 1`) are inherited, not re-declared as free parameters.

### Parameters (first named in this registry entry)

| Parameter | Value | Why this is not an informing mark |
|---|---|---|
| `require_yes_bid` | `true` | Boolean book-integrity flag. Not a posted YES. |
| `require_yes_ask` | `true` | Boolean book-integrity flag. Not a posted YES. |
| `require_strict_bid_lt_ask` | `true` | The definition of an ordered two-sided book. Not a width band. |

No numeric mark threshold is declared. The `(0.45, 0.55)` band is not reused and is not moved.

`declared_at=2026-09-08T15:41:00-04:00` is the first timestamp that names these parameters. The commit SHA of the registry entry that first names them is the commit that lands this file. Because the free parameters are not mark thresholds, no window mark on this tree informed them.

### Expression

`rules.decide()` currently dispatches the selection kind by `id == "R-SKIP-COINFLIP"`. For this id it returns `action=unknown` / `no expression`. That is honest. **Operator must not set `execution:true` until Systems dispatches on these parameters and `paper.py` passes `yes_bid` / `yes_ask` into `decide()`.** Lab does not edit the running loop and does not flip execution.

---

## 3. Prediction and falsifier

**Prediction.** On windows with a two-sided ordered book the rule agrees with `R-BASELINE-FILL-ALL`. On windows whose public book is last-only, one-sided, locked, or crossed, the rule skips and writes no position and no pnl. A skip is not a loss.

**Falsifier — any one of these and the test says "no signal / not worth pursuing," and the line is parked on that falsifier rather than retuned:**

| # | Result | Verdict |
|---|--------|---------|
| F1 | After the n named by the evidence bar in force (currently `looks.first_look_n = 70`), selected-fill settlement_pnl cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows | **Park.** Do not retune the predicate into a spread-width band or a `posted_yes` band |
| F2 | Systems cannot express the rule from the declared parameters without adding a numeric mark threshold | **The class died as specified.** Do not substitute `R-SKIP-COINFLIP`'s band |
| F3 | A later read shows the parameters were chosen from a mark or pnl table on this tree that predates `declared_at` | **Not pre-registered.** L1 cannot Establish. Park rather than back-date |

F1 is the same kill shape the bar already names for a selection rule. This turn does **not** compute it.

---

## 4. What this does not claim

- **Not an edge.** Not established, not banked, not measured, not implied.
- **Not a hit rate.** Skipping an incomplete book does not make the remaining win/lose split a method result.
- **Not an admit.** `lab_admits=false`. Operator decides.
- **Not a revival of `R-SKIP-COINFLIP`.** The band stays `(0.45, 0.55)`. `execution` on that row stays false.
- **Not `CROSS` / `SPREAD` / `THRESH`.** Those are burned oil-track direction classes. This rule does not fade a spread or take a direction when a level is crossed. Do not retune it into a width.
- **Not `FEE-AS-SIGNAL`.** Completeness is not a hurdle and not a fee-avoidance rule.
- **Not a lineage merge, not a backfill, not a new series.** `KXBTC15M` only. HOLD stands.
- **Not lived.** `execution: false`. Replay OOS starts at `declared_at`. Replay is not Established.

---

## 5. Cheap test that is not a score

Read-only, no window outcomes:

1. `class_is_burned("R-SKIP-INCOMPLETE-BOOK") is False`
2. `class_is_burned("CROSS")`, `SPREAD`, `THRESH`, `FEE-AS-SIGNAL`, `RETUNE-COINFLIP-BAND` stay True
3. Registry row exists with `execution is False`, `selects is True`, `kind == "selection"`
4. `decide()` on this id with only `posted_yes` / `close_at` returns `action == "unknown"` (no expression yet)
5. `trials_to_date` incremented by `record_trial` on this declaration (baseline naming is not a trial; `R-SKIP-COINFLIP` is not backfilled)

No paper book was opened. No pnl was computed. `score_rule` was not called.

---

## 6. Hard NOs honored

- No Soften, no Harden, no Kill, no ADMIT, no self-admit
- No score, no bind, no `execution:true`, no `trading_armed`, no HOLD lift
- No second hub, no series add, no golf θ, golf idle **ON**
- No placeholder fee hash
- Nothing edited in `manifest.json`, the digest, the park, or the evidence bar

---

## 7. Handoff

→ **`operator`.** Operator admits, rejects, parks, or RUN-ONLY. Lab does not.

Three things for Operator to rule on, in order:

1. Whether this declaration stands as a dated selection rule (paper only).
2. Whether Systems is owed the parameter dispatch + book-side arguments before any execution flip.
3. Whether `execution:true` waits for that expression. Lab's recommendation: **yes — wait.** Flipping first would make every window `unknown` and therefore not fill.

Lab does not flip execution. Lab does not score. Lab does not schedule Systems.
