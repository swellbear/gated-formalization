# Operator note — L1 score of `R-SKIP-2TO1-FAVORITE` (Admissible only)

**Verdict:** **PARK** on the registry falsifier · Operator · 2026-09-10 10:40 EDT · class **`crew`**
**Ceiling:** **Admissible** (test completed). **Not Established.**
**Not an ADMIT.** Not Softened. Not a dated record. Not a dashboard figure.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only · `lab_admits=false` · Trading **NOT ARMED**
**Rule:** `R-SKIP-2TO1-FAVORITE` · look **L1** · `n=70` · `score_rule(..., look="L1")` · `allow_nonbinding` not set
**Scorecard:** [`LEARNING_LANE_15M_SCORECARD_R-SKIP-2TO1-FAVORITE_L1.json`](LEARNING_LANE_15M_SCORECARD_R-SKIP-2TO1-FAVORITE_L1.json) · arithmetic commit `516a66c` at `2026-09-10T10:41:17-04:00`

This note is the only place these clause numbers may live with the score. They do not go in `manifest.json`, the digest, the hub, `records[]`, or any dated record. A scorecard is not an ADMIT.

---

## Ceiling

| | |
|---|---|
| **Admissible** | **Yes — test completed.** L1 was scored under the binding bar. The falsifier fired. That is a complete outcome. |
| **Established** | **No.** `favorite_odds=2` is not verifiably pre-registered (bar face: first naming `e9fab5a` 19h 06m after the published RUN-ONLY fee table). L1 cannot Establish this rule even if every clause had passed. |
| **Holdout honesty** | This L1 note is committed **after** the 71st eligible window already closed (`KXBTC15M-26SEP091500-00`, close `2026-09-09T15:00:00-04:00`). It is **not** a valid holdout for Established. The machine invariant `l1_committed_before_l2` only checks that `commit_sha` and `committed_at` exist on the L1 card. |

`R-SKIP-COINFLIP` was **not scored**. Its `execution` stays **false**.

---

## Window set (L1 only; L2 not peeked)

`declared_at` `2026-09-08T16:53:00-04:00`. Lived paper begins `2026-09-08T17:11:00-04:00`. Replay interval `(declared_at, 17:11]` was excluded; `score_rule` labels every scored row `lived`.

Eligible = close strictly after `declared_at`, lived, not a named hole, and either a paper book with recorded `settlement_pnl` or a skip with `recorded_pnl=0`, plus an official settle.

| | |
|---|---|
| First eligible | `KXBTC15M-26SEP081715-15` close `2026-09-08T17:15:00-04:00` |
| 70th eligible | `KXBTC15M-26SEP091445-45` close `2026-09-09T14:45:00-04:00` |
| 71st (closed; not scored) | `KXBTC15M-26SEP091500-00` close `2026-09-09T15:00:00-04:00` |
| `n` | **70** |
| `072245` | not invented |
| `100315`–`100500` | not invented (those closes are after this L1 span anyway) |

Two lived skip-decision rows in this span have **no** paper book, **no** settle file, and **no** journal official result on this tree: `KXBTC15M-26SEP090015-15` and `KXBTC15M-26SEP091245-45`. They are **not** in the denominator. A skip is not a loss; `recorded_pnl=0` is what would have been passed if they had an official settle. They do not. Do not invent a Kalshi result for them.

`KXBTC15M-26SEP082100-00` (close 21:00 EDT Sep 8) has a lived paper fill at `posted_yes=0.735`. `score_rule` re-expresses **skip** (`≥ 2/3`). That is the card's `skip_count=1`. Baseline uses the recorded fill; the rule side is 0.

---

## Clauses (binding)

From `score_rule` under `trials_to_date=1` so `k=2`, `α_k=0.008333`, `δ=0.28`. Adjustment: `golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust`. Control: `matched_exposure_permutation` seed `20260908`, 10000 draws.

| Clause | Result |
|---|---|
| **(1)** H0 `mean(d) ≤ δ` | **FAIL.** `mean_d=-0.004857`, `p=1.0`, not `< α_k`. |
| **(3)** | Absorbed into (1). |
| **(4)** `mean(pnl_rule_fee_adj) > 0` | **FAIL.** `mean_pnl_rule_fee_adj=-0.078714`. |
| **(5)** matched-exposure permutation | **FAIL.** `observed_mean_d=-0.004857` does not exceed quantile `0.015286`. `p_value=0.548845`. |
| **`passes_every_binding_clause`** | **false** |

`n=70`. `skip_count=1`. `skip_rate=0.014286`.

The one skip was a winning favorite on the recorded book. Skipping it produced `d_i < 0` on that window and zeros on the other 69 (same fill as baseline). That is indistinguishable from, and on (1) and (5) worse than, abstaining at the same rate with no skill.

---

## PARK (successful outcome)

The registry falsifier: after the n the bar names (70), if selected-fill settlement_pnl cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows, **park this rule. Do not retune `favorite_odds`.** Do not replace 2/3 with a tape quantile.

**PARK.** Class **`crew`**. Closed on the falsifier. Not a failed turn.

`favorite_odds` stays **2**. `R-SKIP-COINFLIP` is not revived and is not scored. `execution` on the coinflip row stays **false**. Binding is unchanged. Consult stays **off**. Trading **NOT ARMED**. HOLD stands.

This scorecard is **not** an ADMIT. Soften Critic would attack a later proposed ADMIT; none is proposed.

---

## Omitted costs

Half-spread is **measured** (`LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json`, **n=624**, mean **0.00385**) and is **omitted** from `fee_adjust`. Fee-adjusted figures remain optimistic. **Do not present any number here as full cost accounting.**

---

## What this turn did not do

- Score `R-SKIP-COINFLIP`
- Peek L2 window outcomes (windows 71+)
- Set `allow_nonbinding`
- ADMIT, Establish, enable consult, arm trading, lift HOLD
- Copy fee-accurate totals onto the hub, digest, `manifest.json`, `records[]`, or `LEARNING_CARD.md`
- Retune `favorite_odds`
- Backfill `072245` or `100315`–`100500`
- Change `last_cos_*` or `AGENT_LEAVE_OFF.md`
