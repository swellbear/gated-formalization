# Lab — PROPOSED 02: skip a posted 2-to-1 YES favorite

**State:** **RUN-ONLY** by `operator` 2026-09-08 17:11 EDT. **Not** Softened, **not** admitted, **not** a board, **not** a dashboard figure. Decision: [`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md`](LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md). `execution=true` (paper only). Not scored. Promotion still requires the normal ADMIT gate.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `lab` — `lab_admits=false`. Lab never admits its own candidate ([`.cursor/skills/gpf-lab/SKILL.md`](../../.cursor/skills/gpf-lab/SKILL.md)).
**Admit?** N · **Soften?** N · **Trading ARMED?** N · **Keys / orders / cash?** none
**Written:** 2026-09-08 16:53 EDT
**Registry id:** `R-SKIP-2TO1-FAVORITE`
**Class:** `SKIP-2TO1-FAVORITE`

**Gate this was written under.** Desk Job 2026-09-08 14:58 ET: one PROPOSED selection rule after `decide()` is live. Honesty gate was open on the 14:18 ET restamp. Residual: method-park row 9 (zero-edge fills — the observation gap). Trigger named there: *a later PROPOSED that actually selects*.

**What this is not.** Not a revival of `R-SKIP-COINFLIP`. Not a retune of `(0.45, 0.55)`. Not PROPOSED 01 / FEE-AS-SIGNAL. Not a second fee hurdle. Not a golf board. It does not enter the Softened set, does not clear golf idle, does not touch golf θ / WC1 / WC2 / the Operator stamp / `phase1_dryrun/`, and does not expand past `KXBTC15M`. Golf idle stays **ON**.

---

## 1. The residual, in one paragraph

PROPOSED 01 priced the omitted fee and stopped there. The live loop still has only one *executing* behavior: fill every candidate at the posted mark with `entry_edge=0.0`. `R-SKIP-COINFLIP` is declared but `execution=false`, and its band is not verifiably pre-registered because those cuts already existed as informing marks on this tree. Park row 9 stays open until something **selects**. This PROPOSED is that selection rule. It is paper-only. It is not an edge.

---

## 2. Burned classes loaded

Loaded [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json) before naming the class. `class_is_burned` is **false** for `SKIP-2TO1-FAVORITE` and for `R-SKIP-2TO1-FAVORITE`. It is **true** for `RETUNE-COINFLIP-BAND`, `FEE-AS-SIGNAL`, `THRESH`, `LOGIT`, `FLIP`, `MAG`, and the other seeded oil / lane burns. This class is not a rename of any of those.

| Refused | Why |
|---|---|
| Revive `R-SKIP-COINFLIP` | Already declared; L1 cannot Establish it |
| Retune `(0.45, 0.55)` | Burned class `RETUNE-COINFLIP-BAND` |
| Skip cheap YES because the fee is larger there | Burned class `FEE-AS-SIGNAL` |
| A tape quantile, a fitted cut, or any posted_yes I read off this tree | Informing marks; that is how the coinflip band lost Established |

---

## 3. The one rule

**Skip the paper fill when posted YES is a 2-to-1 or better favorite. Otherwise fill at the posted mark with `entry_edge=0.0`.**

The free parameter is the integer prior **`favorite_odds = 2`**. The posted_yes cutoff is derived, not fitted:

\[
p \;=\; \frac{\text{odds}}{1 + \text{odds}} \;=\; \frac{2}{3}
\]

`decide()` computes that cutoff from `params.favorite_odds`. No posted_yes from this tree was read to choose `2`. `2` is the first integer odds strictly above evens. It is not a mark, not a quantile, and not a widening of `(0.45, 0.55)`.

Skip is one-sided and on the *high* side of posted YES. That is the opposite of fee-avoidance: the taker fee `k · stake · (1 − P)` is smallest where this rule skips, and largest where it still fills. FEE-AS-SIGNAL is not smuggled in under another name.

Expression (paper only; **`execution=false` here is the proposing-turn state at 16:53**. Operator flipped `execution=true` at 17:11, commit `0daae90`. The live flag is the registry row, not this sentence):

- `posted_yes >= 2/3` → **skip**
- `posted_yes < 2/3` → **fill** at the posted mark, `entry_edge=0.0`
- window `close_time` ≤ `declared_at` → **ineligible** (history, not OOS)

`R-SKIP-COINFLIP`'s id-dispatch and band are untouched.

---

## 4. Prediction and falsifier

**Prediction.** Selecting away from posted 2-to-1 YES favorites changes the paper book relative to `R-BASELINE-FILL-ALL` by more than noise-plus-δ, under the bar in force, on the first look the bar names.

**Falsifier.** After the n named by the evidence bar in force (currently `looks.first_look_n = 70`), if selected-fill `settlement_pnl` cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows, **park this rule**. Do not retune `favorite_odds`. Do not replace `2/3` with a tape quantile. The bar is the governing source.

This turn **does not score**. n is not counted here. No post-declaration outcome file was opened to write this.

---

## 5. Pre-registration statement

The bar's pre-registration test (not a `note` field's self-certification) needs (1) the commit SHA and timestamp of the registry row that first names the parameter, and (2) that this timestamp predates the earliest window whose mark informed the parameter.

**No window mark informed `favorite_odds=2`.** The parameter is an integer prior, not a posted_yes cutoff read from `paper/`, the RUN-ONLY fee table, the digest, the manifest, or any other file on this tree. I did not open those mark tables to choose it. The first naming is this declaration; the commit that lands `LEARNING_LANE_15M_RULES.json` with this id is the SHA the bar asked for.

This is the statement the bar requires. It is not itself the proof — the commit record is.

`R-SKIP-COINFLIP` remains not verifiably pre-registered. This row does not repair that.

---

## 6. What this does not claim

- **Not an edge.** Not established, not banked, not measured, not implied.
- **Not an admit.** `lab_admits=false`. Operator decides RUN-ONLY / PARK / (later) ADMIT.
- **Not lived at proposal.** `execution=false` was the proposing-turn state (16:53). Operator flipped `execution=true` at 17:11 (`0daae90`). Replay of windows that closed after `declared_at` and at or before that flip is still replay. Lived paper begins at the flip. Replay is not a lived result.
- **Not a score.** `score_rule` is not called. No scorecard is opened.
- **Not a bind, not an arm.** `binding` stays false. `trading_armed` stays false. The HOLD stands.
- **Not a lineage merge.** Lineage A only, if and when anyone scores. Lineage B's published `+1.67` is neither re-derived nor summed.
- **Not a second series.** `KXBTC15M` only.

---

## 7. Cost

| Need | Status |
|---|---|
| New data collection | **None** |
| New series | **None** |
| Kalshi keys / orders / cash | **None.** Trading NOT ARMED |
| Loop code | Expression only, in `rules._express_selection`, dispatched from declared `params.favorite_odds`. `paper.py` already consults `decide()`. This turn does not flip `execution` |
| Score | **Forbidden this turn** |

---

## 8. Hard NOs honored

- Burned classes loaded; `R-SKIP-COINFLIP` not revived; `(0.45, 0.55)` not retuned
- No Soften, no Harden, no Kill, no ADMIT, no self-admit
- No score, no scorecard, no post-declaration outcome file opened for results
- `execution` left false; `binding` not touched; `trading_armed` not touched; HOLD not lifted
- No golf θ, no WC3+, no second series, no second hub, no placeholder fee hash
- No Founder impersonation of arm or HOLD. Do not add `founder_read_once` as a bind condition

---

## 9. Handoff

→ **`operator`.** Operator sustains or overrules, and may set `execution=true` on this pre-registered row if it survives. Lab does not.
