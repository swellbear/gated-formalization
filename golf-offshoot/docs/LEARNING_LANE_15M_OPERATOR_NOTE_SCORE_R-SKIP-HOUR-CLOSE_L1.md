# Operator note — L1 look of `R-SKIP-HOUR-CLOSE` (Admissible only)

**Verdict:** **PARK** on the registry falsifier · Operator · 2026-09-12 07:22 EDT · class **`crew`**
**Ceiling:** **Admissible** (test completed). **Not Established.**
**Not an ADMIT.** Not Softened. Not a dated record. Not a dashboard figure.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only · `lab_admits=false` · Trading **NOT ARMED**
**Rule:** `R-SKIP-HOUR-CLOSE` · look **L1** · `n=70` · card already written by clerical `score_rule` · this turn did **not** re-score
**Scorecard:** [`LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json`](LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json) · clerical commit `9051c54` at `2026-09-12T07:09:48-04:00` · `operator_look=PARK` at `2026-09-12T07:22:06-04:00`

This note is the only place these clause numbers may live with the look. They do not go in `manifest.json`, the digest, the hub, `records[]`, or any dated record. A scorecard is not an ADMIT.

`apply_operator_look` read the pushed card. `passes_every_binding_clause` is false → **PARK**. Execution on this selecting row dropped **true → false**. Tape was not invented. PaperWatch was not stopped. Baseline `R-BASELINE-FILL-ALL` still has `execution=true` and still fills.

---

## Ceiling

| | |
|---|---|
| **Admissible** | **Yes — test completed.** L1 was scored under the binding bar (`allow_nonbinding` on the clerical write). The falsifier fired. That is a complete outcome. |
| **Established** | **No.** Clauses (1), (4), and (5) fail. This look cannot Establish. |
| **Holdout honesty** | This look stamps a card that already existed. It does not peek L2 window outcomes. |

`R-SKIP-COINFLIP` was **not scored**. Its `execution` stays **false**. PARK'd `R-SKIP-2TO1-FAVORITE` was **not re-scored**.

---

## Window set (from the card only; L2 not peeked)

`declared_at` `2026-09-10T13:25:00-04:00`. Lived paper begins `2026-09-10T13:36:00-04:00` (RUN-ONLY flip). The registry row has no `lived_paper_begins_at` / replay interval fields; the clerical card labels every scored row `lived`. This turn does not re-label them.

| | |
|---|---|
| First scored | `KXBTC15M-26SEP101330` close `2026-09-10T17:30:00Z` |
| One skip | `KXBTC15M-26SEP101400` close `2026-09-10T18:00:00Z` · `posted_yes=0.455` · hour-ending minute 0 |
| 70th scored | `KXBTC15M-26SEP111245` close `2026-09-11T16:45:00Z` |
| `n` | **70** |
| `skip_count` | **1** |
| `072245` | not invented |
| `100315`–`100500` | not invented |

The skip's baseline fee-adj pnl is `-1.04`; the rule side is `0.0`. This turn does not invent any other window.

---

## Clauses (binding) — quoted from the card

From the card: `trials_to_date_before=2`, `α_k=0.0041667`, `δ=0.28`. Adjustment: `golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust`. Control: `matched_exposure_permutation` seed `20260908`, 10000 draws.

| Clause | Result |
|---|---|
| **(1)** H0 `mean(d) ≤ δ` | **FAIL.** `mean_d=0.014857`, `t=-17.846154`, `p=1.0`, not `< α_k`. |
| **(3)** | Absorbed into (1). |
| **(4)** `mean(pnl_rule_fee_adj) > 0` | **FAIL.** `mean_pnl_rule_fee_adj=-0.019143`. |
| **(5)** matched-exposure permutation | **FAIL.** `observed_mean_d=0.014857` does not exceed quantile `0.015`. `p_value=0.435756`. |
| **`passes_every_binding_clause`** | **false** |

`n=70`. `skip_count=1`. `skip_rate=0.014286`.

The one skip avoided a losing hour-ending fill on the recorded book (`d_i = +1.04` on that window; zeros on the other 69). `mean_d` is slightly positive and still far below `δ=0.28`. That is indistinguishable from, and on (5) worse than, abstaining at the same rate with no skill.

---

## PARK (successful outcome)

The registry falsifier: after the n the bar names (70), if selected-fill settlement_pnl cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows, **park this rule. Do not retune `skip_close_minute`.** Do not replace `0` with a tape-chosen slot.

**PARK.** Class **`crew`**. Closed on the falsifier. Not a failed turn.

`skip_close_minute` stays **0**. `R-SKIP-COINFLIP` is not revived and is not scored. PARK'd `R-SKIP-2TO1-FAVORITE` is not re-scored. `execution` on this row is now **false**. Binding is unchanged. Consult stays **off**. Trading **NOT ARMED**. HOLD stands. PaperWatch is not stopped.

**Wake name-clear (not a score):** `rule_reached_n R-SKIP-HOUR-CLOSE` (L1 already PARK; do not re-score) · `rule_reached_n R-SKIP-COINFLIP` (do not score) · `rule_reached_n R-SKIP-2TO1-FAVORITE` (L1 already PARK; do not re-score).

This scorecard is **not** an ADMIT. Soften Critic would attack a later proposed ADMIT; none is proposed.

---

## Omitted costs

Half-spread is **measured** (`LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json`) and is **omitted** from `fee_adjust`. Fee-adjusted figures remain optimistic. **Do not present any number here as full cost accounting.**

---

## What this turn did not do

- Re-score or invent tape
- Score `R-SKIP-COINFLIP`
- Re-score PARK'd `R-SKIP-2TO1-FAVORITE`
- Peek L2 window outcomes
- ADMIT, Establish, enable consult, arm trading, lift HOLD
- Stop PaperWatch
- Set `binding` or `trading_armed`
- Copy fee-accurate totals onto the hub, digest, `manifest.json`, `records[]`, or `LEARNING_CARD.md`
- Retune `skip_close_minute`
- Backfill `072245` or `100315`–`100500`
- Stamp `last_cos_*`
- Assign the next worker
