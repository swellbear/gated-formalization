# Lab — PROPOSED 02: skip last-only / incomplete public quotes

**State:** **PROPOSED.** Not RUN-ONLY. Not Softened. Not admitted. Not scored. `execution` stays **false**.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `lab` — `lab_admits=false`. Lab never admits its own candidate ([`.cursor/skills/gpf-lab/SKILL.md`](../../.cursor/skills/gpf-lab/SKILL.md)).
**Admit?** N · **Soften?** N · **Trading ARMED?** N · **Keys / orders / cash?** none
**Written:** 2026-09-08 16:12 EDT
**Registry:** [`LEARNING_LANE_15M_RULES.json`](LEARNING_LANE_15M_RULES.json) id `R-SKIP-LAST-ONLY` · class `LAST-ONLY-SKIP`
**Residual:** method park row 9 — zero-edge fills; PROPOSED 01 priced the omitted fee and did not select. [`LEARNING_LANE_15M_METHOD_PARK.md`](LEARNING_LANE_15M_METHOD_PARK.md)

---

## 0. Burned classes loaded (before the name)

Loaded [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json). This class is **not** any of them.

| Burned id / alias | Why this is not that class |
|---|---|
| `RETUNE-COINFLIP-BAND` / `R-SKIP-COINFLIP` | No mark band. Does not touch `(0.45, 0.55)`. Does not revive that rule |
| `FEE-AS-SIGNAL` | Does not select on the fee or the hurdle |
| `BASELINE-AS-EDGE` | Naming a skip is not an edge claim |
| `SPREAD` / `SPREAD-FADE` / `SPREAD-CATCH` | Oil Track B. This rule does not fade or catch a spread width |
| `CROSS` / `C-SPOT-CROSS` | Oil Track B direction class. This rule does not take a direction |
| `THRESH` / `FLIP` / `INV` / `MAG` / the rest of the oil board | Different domain, different horse |
| `SUM-LINEAGES` / `BACKFILL-GAP` | Not a bookkeeping merge and not a gap fill |

`LAST-ONLY-SKIP`, `R-SKIP-LAST-ONLY`, `INCOMPLETE-QUOTE`, `TWO-SIDED-QUOTE` are **absent** from the burned file. `H-SPOT-MOY-CONT` stays FRAGILE, not this.

---

## 1. The one selection rule

**Skip the paper fill when the public book is not two-sided. Fill only when both `yes_bid` and `yes_ask` are present and their mid is in (0, 1).**

That is the **mid branch** of `public_mid_or_last` ([`kalshi_15m.py:216–231`](../src/golf_offshoot/data_feeds/kalshi_15m.py)). The **last** fallback and the **ask-only** fallback are skips.

```
if yes_bid is not None and yes_ask is not None:
    mid = (yes_bid + yes_ask) / 2.0
    if 0.0 < mid < 1.0:
        FILL at the posted mark, entry_edge=0.0
SKIP   # last-only, ask-only, missing, or mid not in (0, 1)
```

**Parameters:** none. There is no free number. There is no band. There is no width cutoff. The predicate is the definition of a two-sided public quote already written in the mark constructor.

**Why that matters for pre-registration.** The evidence bar disqualifies a parameter that was informed by marks already on this tree (`R-SKIP-COINFLIP`'s `(0.45, 0.55)`). A rule with no free parameter cannot have been fitted from those marks. The commit that first names this predicate in the registry is the pre-registration. A `note` field is not offered as proof.

**What `decide()` can and cannot do today.** `rules.decide()` takes `posted_yes` and `close_at` only. `posted_yes` is already the *collapsed* mark — mid, else last, else ask. The information this rule selects on is destroyed before `decide()` sees it. Lab does **not** extend that signature (Systems, and only if Operator wants a live expression). `execution` stays **false**. Until the signature carries `yes_bid` / `yes_ask` (or a `mark_source` tag from the constructor), `decide()` must return `no expression` for this id. That is honest, not a defect in the PROPOSED.

Paper only. `KXBTC15M` only. Founder HOLD untouched.

---

## 2. Cheap test (code, not tape)

Invent-test habit: one cheap check under the frozen protocol. **No window outcomes were read. No skip rate. No pnl. No score.**

| # | Check | Source | Result |
|---|---|---|---|
| C1 | Public market objects carry `yes_bid` and `yes_ask` as separate fields | `DISPLAY_ONLY_FIELDS` and `parse_market` in `kalshi_15m.py` | **Holds.** Fields exist in the schema |
| C2 | `public_mid_or_last` has a last fallback and an ask-only fallback | `kalshi_15m.py:227–230` | **Holds.** The mid branch is not the only branch, so this rule is not `R-BASELINE-FILL-ALL` in disguise |
| C3 | Synthetic constructor cases (not live windows): two-sided → mid; bid/ask missing + last → last; ask only → ask; nothing → None | same function, invented floats `0.48/0.52/0.99/0.61` | mid `0.50`; last fallback `0.61`; ask fallback `0.61`; empty `None` |
| C4 | Proposed names are not burned | `LEARNING_LANE_15M_BURNED_CLASSES.json` | **Holds.** See §0 |

C3 uses numbers I typed for the constructor, not marks copied from `paper/` or the RUN-ONLY fee table. I did not open those files for this test.

---

## 3. Prediction and falsifier

**Prediction (not a claim of edge).** A fill taken only on a two-sided public quote is the only fill whose `paper_mark` is a mid. Last-only and ask-only marks are a different object. Selecting on quote completeness is a selection. It may still lose to baseline at n. That is what the falsifier is for.

**Falsifier — any one and the test dies or parks, rather than being retuned:**

| # | Result | Verdict |
|---|---|---|
| F1 | The public schema does not carry `yes_bid` and `yes_ask` separately | **Test dies.** No field is invented |
| F2 | `public_mid_or_last` has no last/ask fallback (mid is the only branch) | **Test dies.** The rule selects nothing; it is the baseline |
| F3 | After the n named by the evidence bar in force (currently `first_look_n = 70`), selected-fill settlement_pnl cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows | **Park.** Do not add a numeric band. Do not retune a threshold this rule does not have |
| F4 | Anyone implements this by adding a `posted_yes` band or a spread-width cutoff | **Park as a different class** (`RETUNE-COINFLIP-BAND` or burned `SPREAD`). This PROPOSED is not that |

F1 and F2 were the cheap test. Neither fired on the code read. F3 is Operator's later look, **not this turn**. Lab does not score. F4 is a class guard.

---

## 4. What this does not claim

- **Not an edge.** Not established, not banked, not measured, not implied.
- **Not a score.** No eligible count. No post-declaration outcome file. `score_rule` was not called.
- **Not an admit.** `lab_admits=false`. Operator decides RUN-ONLY / PARK / (later) ADMIT.
- **Not `execution:true`.** Operator flips that, and only on a pre-registered survivor, and not in a scoring turn.
- **Not a revival or retune of `R-SKIP-COINFLIP`.**
- **Not fee-as-signal, not a lineage merge, not a backfill.**
- **Not loop code.** This artifact plus the registry row. No hub start/kill. No `decide()` signature change.
- **Not a golf invent.** Golf idle stays **ON**. No θ retune. No WC3+.
- **Not binding the bar.** `binding` stays false. `founder_read_once` stays false. Trading **NOT ARMED**.

---

## 5. Cost

| Need | Status |
|---|---|
| New data collection | **None** |
| Live window marks / pnl | **Unread** |
| Kalshi keys / orders / cash | **None** |
| New series | **None.** HOLD stands |
| New loop code | **None this turn.** Expression is owed to Systems only if Operator wants one |
| Compute | The cheap test was four constructor calls and a JSON load |

---

## 6. Hard NOs honored

- No Soften / Harden / Kill / ADMIT / self-admit
- No score of this rule or of `R-SKIP-COINFLIP`
- No `execution:true`, no `binding` true, no `trading_armed`, HOLD not lifted
- No second series, no second hub, no placeholder fee hash
- No invented win / lose / pnl
- Burned classes loaded; none revived under a new name

---

## 7. Handoff

→ **`operator`.** Operator sustains, overrules, RUN-ONLY, or parks. Lab does not.

Three things for Operator, in order:

1. Whether this is a selection rule at all (I say yes: it skips a constructor path the baseline fills).
2. Whether the empty parameter set is accepted as pre-registered on the registry commit that first names it, or whether Operator wants a different class.
3. Whether Systems may later extend `decide()` to see `yes_bid` / `yes_ask`. Lab does not do that in this fire.

Do not score in the same turn as any bar amendment that has not already been attacked-answered.
