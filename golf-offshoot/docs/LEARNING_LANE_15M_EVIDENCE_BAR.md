# 15m evidence bar (DRAFT — not binding)

**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Drafted:** 2026-09-08 08:30 EDT · Operator
**Binding?** **N.** A system that sets its own threshold does not have one.
**Admit?** N · **Edge established?** N · `lab_admits` false · Trading **NOT ARMED**

This draft becomes binding only after both:

1. the Soften Critic attacks it in writing, in a session that did not draft it, and Operator answers each objection in the admit pass, and
2. Founder reads it once and acknowledges.

Until then it is a proposed bar. Writing it is not an ADMIT. Scoring against it is not owed. `records[]` stays empty.

Machine copy: [`LEARNING_LANE_15M_EVIDENCE_BAR.json`](LEARNING_LANE_15M_EVIDENCE_BAR.json).
Burned classes: [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json).
Fee source: [`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`](LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md) (RUN-ONLY note only — those numbers do not go on the hub, in the digest, in `manifest.json`, or in `records[]`).

---

## Two verdicts, not one

The method already says a gate pass is not a claim: Amb ≠ clearance, print-match ≠ clearance, no soft clearances, establishment-stop drill (`workflow.md`, `templates/02_Gate_Scoring_Sheet.md`). This lane inherits that split.

| Verdict | What it answers | What it licenses | What it does not |
|---|---|---|---|
| **Admissible** | Is this rule well-posed and honestly testable under the gate sheet and this bar? | A dated-record ADMIT that the *test completed* and the rule may stay live as a candidate. Operator note / park row. | Edge. `records[]` as a track record. Skill-met. Productize. Arming. Lifting the HOLD. |
| **Established** | Did the rule clear the locked numerical bar as *edge*, after confirmation? | A method establishment verdict on this lane only, and only after the track has been promoted into the gated method. | Money, keys, series expansion, golf θ, usefulness Soften. **Edge Softened/established?** on an ops-beside stamp stays **N** until promotion has fired. |

An ops ADMIT on this lane, while the lane is still ops-beside-method, is a dated record. Per [`docs/operator_ops/OPS_BESIDE_METHOD.md`](../../docs/operator_ops/OPS_BESIDE_METHOD.md): it does **not** establish edge. **Edge Softened/established?** stays **N**. Observation ≠ edge.

Promotion into the gated method is a separate Founder-named conditional. This bar does not fire it. This bar being written does not fire it. This bar is not binding yet, so the promotion condition that requires a binding bar cannot hold yet.

---

## No peeking

Score a selection rule at **n = 40** eligible settled windows, not every tick. Continuous scoring against a threshold manufactures significance.

- First look: the first 40 eligible windows after `declared_at` (`close` strictly after declaration). Call this set **L1**.
- Do not compute the test at n = 1, 10, 20, or 39. Do not peek and then wait for a prettier n.
- **L2** (windows 41–80 after `declared_at`) is held out. The session that scores L1 must not read L2 marks, fills, or pnl.
- A later confirmation look on L2 is a second precommitted look, not a retry of L1.
- `072245` does not exist. Do not invent it. Do not put it in any denominator.

`R-SKIP-COINFLIP` was declared at `2026-09-08T05:56:00-04:00`. It is **not scored in the session that wrote this bar.** Eligible-window *counts* may be reported. Outcomes of windows that closed after declaration must not be read to choose or illustrate this bar.

---

## What "distinguishable" means

Contrast, on the **same** n eligible windows:

`d_i = pnl_rule_fee_adj_i − pnl_baseline_fee_adj_i`

- Baseline is `R-BASELINE-FILL-ALL` on window i (the recorded fill, then fee-adjusted).
- The rule side uses that rule's fill-or-skip. A skip contributes **0** pnl and **0** fee.
- On a window both sides fill, `d_i = 0` after the same fee. The contrast lives in the skips (or in any later rule that fills a different contract).
- Lineage A only. Do not sum, net, or average lineage B's published `+1.67` into this arithmetic.
- Recorded `settlement_pnl` on disk has **no fee term**. Fee-adjust before comparing. The fee-adjusted figures live in the score note only.

**Fee adjustment** (from the RUN-ONLY note, k = 0.07, $1 stake, ceil to the cent):

`fee_i = ceil_cent(0.07 × stake_i × (1 − posted_yes_i))`

`pnl_fee_adj_i = recorded_pnl_i − fee_i` on a fill; `0` on a skip.

Measured cost cited from that note, not restated here as a dashboard figure: mean **$0.039** per fill, **3.92%** of stake, on the first 24 lineage-A books. A later public schedule that names a different `k` or a `KXBTC15M` override makes this stale.

**Test at n = 40 (L1), one look:**

1. One-sided paired t-test, H0: mean(d) ≤ 0. Reject only if p < α.
2. **Multiplicity:** `α = 0.05 / (trials_to_date + 1)` using the registry counter *before* incrementing. Then increment `trials_to_date` by 1. A bar with no multiplicity term is incomplete. At ~96 windows/day a 40-window look resolves in ~10 hours; ~14 looks/week against a naive α = 0.05 expects a false survivor most weeks. Scarcity is being removed; this is the replacement.
3. **Effect floor:** mean(d) ≥ **δ = $0.28** per window.

δ was chosen from **pre-declaration residual scale only** (see below): paired-difference sd ≈ 0.66 ⇒ SE at n = 40 ≈ 0.104. 2.69 × SE ≈ 0.28, the normal critical value for a 14-look week at family α = 0.05. δ is also larger than the measured per-fill fee, so clearing the omitted cost by a rounding error is not distinguishable.

**Kill / park** (this is the numeric form of `R-SKIP-COINFLIP`'s existing falsifier): if at n = 40 the rule is not distinguishable under (1)–(3), **park it and do not retune the band.** A dead test is a complete outcome. Record the park on that falsifier.

**Positive side** (missing until this draft): a result that wants to be read as positive expectancy must also have mean(`pnl_rule_fee_adj`) **> 0** on those same 40 windows. Beating a losing baseline by skipping, and still booking ~0 after fees, is distinguishable-or-not; it is not a positive result that cleared the cost. Skip-all yields 0 and fails this clause.

---

## Replay versus lived

The registry already says these are different evidence. This bar says which verdict accepts which.

| Evidence | Admissible | Established |
|---|---|---|
| **Replay** (`execution=false`; books collected without the rule acting) | Yes — L1 may be scored by replay. Declaration time makes the data clean. | **No.** A replayed survivor is not a lived one. |
| **Lived** (`execution=true`; the loop honored `rules.decide()`) | Yes — also acceptable for L1 if the rule was live for those windows. | **Required** for L2 confirmation and for any establishment verdict. |

Replay assumes fills live execution might not get. Skipping a bet changes nothing about the market and does change the fill sequence. Both are legitimate. They are not interchangeable. Do not flip `R-SKIP-COINFLIP` to `execution=true` in order to make a replayed look look lived.

---

## Trials accounting

`trials_to_date` lives on [`LEARNING_LANE_15M_RULES.json`](LEARNING_LANE_15M_RULES.json). It starts at **0**. It increments once per first-look (L1) score of any *selection* rule on this lane. Baseline naming is not a trial.

The held-out L2 range is the other half of the protection: the scorer of L1 never sees it. Establishment cannot be claimed from L1 alone even if L1 passes.

---

## Burned classes

Prose in `logs/failure_mode_log.md` is not enforceable. Lab and any later proposer **must** load [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json) before naming a class.

Oil Track B direction classes are seeded there so they cannot be re-proposed under new 15m names. **`H-SPOT-MOY-CONT` is FRAGILE, not a null.** Do not burn it to empty a queue. Do not promote it.

Lane-local burned classes start as: fee-as-signal, retune-coinflip-band-after-tape, sum-lineages, backfill-gap, baseline-as-edge.

A class lands on this list when it is parked on a falsifier or rejected as a burned revival. Aliases are first-class. Re-naming MAG as "magnitude-gate" is still MAG.

---

## What an ADMIT on this lane does and does not authorize

While the lane is ops-beside-method:

- An ADMIT is a **dated record** of a frozen exit (PASS / FAIL / park / residual) under the named bar for that date.
- **Edge Softened/established?** stays **N**. Write N even if a paper-hit count exists.
- It does not arm trading, lift the series HOLD, clear golf idle, rewrite the golf Operator stamp, or put a fee-accurate figure on the hub.

After promotion fires (conditional, not this draft): establishment is adjudicated under the standing gated-method rules against *this* bar once binding. Operator issues that verdict without asking Founder. Promotion is not itself a verdict.

---

## Pre-declaration windows used to choose δ

**Used:** the 56 settled lineage-A paper books whose close is **at or before** `2026-09-08T05:56:00-04:00`: `KXBTC15M-26SEP071545-45` through `KXBTC15M-26SEP080545-45`, excluding the missing `KXBTC15M-26SEP072245`.

**Read from those books:** `movements[0].model_win` (posted YES) and recorded `settlement_pnl`, then the note's ceil-cent fee. Used only to estimate sd of the paired difference under a skip-inside-(0.45, 0.55) expression, so SE at n = 40 could be named before any OOS look.

**Not used:** any window that closed after `2026-09-08T05:56:00-04:00`. Those files were not opened for marks or pnl while drafting this bar.

**Not a score:** the in-sample mean contrast on those 56 books was inspected only to confirm δ was **not** fit so that history would pass. That mean is not a method result and is not printed here as one. Pre-declaration skip rate on that expression was 22/56. That rate is history, not OOS.

---

## Hard NOs (this bar)

- Do not treat this draft as binding
- Do not score `R-SKIP-COINFLIP` before 40 eligible windows, and not in the drafting session
- Do not peek L2 while scoring L1
- Do not put fee-accurate totals on the hub, digest, manifest, or `records[]`
- Do not revive a burned class under a new name
- Do not treat `H-SPOT-MOY-CONT` as a null
- Do not treat a replayed survivor as lived establishment
- Do not merge lineage A and B
- Do not backfill `072245`
