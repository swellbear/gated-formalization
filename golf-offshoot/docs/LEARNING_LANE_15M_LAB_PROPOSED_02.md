# Lab — PROPOSED 02: skip on-hour and half-hour closes

**State:** **PROPOSED.** Not Softened, not admitted, not RUN-ONLY, not a board, not a dashboard figure. Operator decides.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `lab` — `lab_admits=false`. Lab never admits its own candidate ([`.cursor/skills/gpf-lab/SKILL.md`](../../.cursor/skills/gpf-lab/SKILL.md)).
**Admit?** N · **Soften?** N · **Trading ARMED?** N · **Keys / orders / cash?** none
**Written:** 2026-09-08 16:39 EDT
**Registry id:** `R-SKIP-CLOSE-HH` · `execution: false` · `selects: true`
**Class:** `CLOSE-HH` (session filter on the product clock). Not a direction class.

**Gate this was written under.** Desk Job 2026-09-08 14:58 ET: one PROPOSED selection rule after `decide()` is live; do not revive `R-SKIP-COINFLIP`. Residual: park row 9 (zero-edge fills). Founder saved the 15m worker tick that runs this Job.

**What this is not.** Not a revival of `R-SKIP-COINFLIP`. Not a retune of `(0.45, 0.55)`. Not a new golf board. Not a WC3+ reopen. It does not enter the Softened set, does not clear golf idle, does not touch golf θ / WC1 / WC2 / the Operator stamp / `phase1_dryrun/`, and does not expand past `KXBTC15M`. Golf idle stays **ON**. `binding` stays false. `trading_armed` stays false.

---

## 0. Burned classes loaded

Loaded [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json) before naming a class. `class_is_burned` results for this invent:

| Name | Burned? |
|---|---|
| `CLOSE-HH` | **false** |
| `R-SKIP-CLOSE-HH` | **false** |
| `SESSION-HH` | **false** |
| `R-SKIP-COINFLIP` | **false** (existing rule; not revived, not retuned) |
| `RETUNE-COINFLIP-BAND` | **true** — this invent does not touch that band |
| `FEE-AS-SIGNAL` | **true** — this invent does not select on the fee |
| `BASELINE-AS-EDGE` | **true** — naming a fill is not this rule |
| `THRESH` / `MAG` / `SEAS-DIR` / `SPREAD` / `SHORT` / `PERSIST` | **true** — not this class |
| `H-SPOT-MOY-CONT` | **false** (FRAGILE, not a null) — not this class; not promoted |

`CLOSE-HH` is a **session filter**: skip exposure on two of the four product close minutes. It does not pick YES vs NO from a calendar, so it is not `SEAS-DIR` / `MOY-DIR`. It has no mark threshold, so it is not `THRESH` / `MAG`. It does not fade or catch a spread, so it is not `SPREAD`.

---

## 1. The residual, in one paragraph

Park row 9: `paper.py` still has a mechanical fill as the executing behavior (`R-BASELINE-FILL-ALL`, `entry_edge=0.0`). `R-SKIP-COINFLIP` selects on a posted-yes band, but that band is **not verifiably pre-registered** (marks on this tree informed it) and `execution` stays false. Established needs a selection rule declared **after** the execution flip, with parameters that are not informing marks. This PROPOSED is that rule. It selects. It does not score.

---

## 2. The one rule

**Skip the paper fill when the window's close minute is `00` or `30`. Otherwise fill at the posted mark with `entry_edge=0.0`.**

| | |
|---|---|
| Id | `R-SKIP-CLOSE-HH` |
| Kind | `selection` |
| Expression | `skip_close_minutes` |
| Parameters | `[0, 30]` |
| `execution` | **false** (Operator may flip; Lab does not) |
| Series | `KXBTC15M` only |

`decide()` dispatches on the declared `skip_close_minutes` list, not on `id == "R-SKIP-CLOSE-HH"`. `posted_yes` is not an input to the skip. A window that closed at or before `declared_at` is ineligible.

### Parameter source (not a mark)

1. **Product clock.** `KXBTC15M` windows close on a 15-minute grid. The adapter already encodes the four close minutes as a ticker suffix (`kalshi_15m.py` `_MARKET_TICKER_RE`: optional `-MM`). The free set of slots is `{0, 15, 30, 45}`. That grid is a published product property. It predates this tree's paper book.
2. **Which two.** `{0, 30}` is the on-hour / half-hour pair — the conventional hourly and 30-minute crypto print closes. That pairing is a clock convention, not a fit to any `paper_mark`, `posted_yes`, win/lose, or pnl on this tree.

**Pre-registration claim (for Operator to audit, not self-certify as proof).** These parameters first appear in the registry commit that lands this file. No earlier commit, desk line, or dated artifact on this tree names `skip_close_minutes` or `{0, 30}` as a selection parameter. Window *ids* on disk contain those minutes because the product does; those ids are not marks and were not used to choose the pair. A `note` field is not proof — the commit SHA of the registry row is.

`R-SKIP-COINFLIP`'s `(0.45, 0.55)` band is untouched.

---

## 3. Prediction and falsifier

**Prediction.** On a live 15-minute grid the rule skips about half the windows (the `:00` and `:30` closes) and fills the `:15` and `:45` closes. That is a selection. It is not an edge claim.

**Falsifier — any one of these and the test says "no / park," and the minute set is not retuned:**

| # | Result | Verdict |
|---|--------|---------|
| F1 | A commit, desk line, or dated artifact **predating this declaration** names `skip_close_minutes` or `{0, 30}` as a selection parameter | **Not pre-registered.** Park. Do not pretend the note was blind |
| F2 | At the n named by the evidence bar in force (`looks.first_look_n`, currently 70), the rule fails any binding clause (1)–(5) | **Park.** Do not retune `[0, 30]` |
| F3 | On that same L1 set, skip rate is **0** (never skips) or **1** (skip-all) | **Vacuous.** Park. Skip-all already fails clause (4) |
| F4 | Operator rules this is a burned class under another name (`SEAS-DIR`, `THRESH`, `SHORT`, …) | **Park.** Do not rename and re-propose |
| F5 | Operator rules `{0, 30}` was chosen from this tape's outcomes or marks | **Informing marks.** Park. Same defect as `R-SKIP-COINFLIP` |

This session does **not** evaluate F2, F3, or F5 against window outcomes. F1 was checked by search: no prior `skip_close_minutes` / `CLOSE-HH` / on-hour skip rule on this tree. F4 is Operator's.

---

## 4. Cheap test (expression only — not a score)

Read-only, synthetic `close_at` stamps. No `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no ledger, no mark, no pnl. `score_rule` was not called.

Rule under test: `declared_at=2026-09-08T16:39:00-04:00`, `skip_close_minutes=[0, 30]`, `selects=true`, `execution=false`.

| `close_at` | `posted_yes` | action |
|---|---:|---|
| `2026-09-08T16:45:00-04:00` | 0.20 | fill |
| `2026-09-08T16:45:00-04:00` | 0.80 | fill |
| `2026-09-08T17:00:00-04:00` | 0.20 | skip |
| `2026-09-08T17:00:00-04:00` | 0.80 | skip |
| `2026-09-08T17:15:00-04:00` | 0.50 | fill |
| `2026-09-08T17:30:00-04:00` | 0.50 | skip |
| `2026-09-08T16:30:00-04:00` (at/before declared_at) | 0.50 | ineligible |

Same action at 0.20 and 0.80 on the same close: the mark is not a parameter. That is the pre-registration point.

---

## 5. What this does not claim

- **Not an edge.** Not established, not banked, not measured, not implied.
- **Not a score.** No post-declaration window outcome was read. Eligible-window counts are not reported from live files.
- **Not an admit.** `lab_admits=false`. Operator decides.
- **Not a lived L2.** `execution` is false. Replay after `declared_at` may later support Admissible; Established still needs a lived flip that Lab does not make.
- **Not a fee signal.** Skipping `:00`/`:30` is not a claim about the fee or the spread.
- **Not a lineage merge.** Lineage B's published `+1.67` is untouched.
- **Not a HOLD lift.** `KXBTC15M` only.

---

## 6. Cost

| Need | Status |
|---|---|
| New data collection | **None** |
| Kalshi API keys / orders / cash | **None.** Trading NOT ARMED |
| New series | **None.** HOLD stands |
| Loop code | Generic `skip_close_minutes` dispatch in `decide()` so the declared parameters are expressible. Live executing rule remains `R-BASELINE-FILL-ALL` |
| Score | **Not run** |

---

## 7. Hard NOs honored

- Burned classes loaded; `R-SKIP-COINFLIP` not revived; band not retuned
- No Soften, Harden, Kill, ADMIT, self-admit
- No `execution: true`, no `binding: true`, no `trading_armed`, HOLD not lifted
- No score, no peek of L1/L2 outcomes, no post-declaration window file opened for marks or pnl
- No second series, no second hub, no golf θ, golf idle **ON**
- No Founder impersonation of `founder_read_once`

---

## 8. Handoff

→ **`operator`.** Operator admits, rejects, parks, or sets `execution: true` on this pre-registered row. Lab does not.

Three things for Operator, in order:

1. Whether `CLOSE-HH` / `[0, 30]` is a new class with parameters that are not informing marks (F1, F4, F5).
2. Whether to leave `execution: false` (replay OOS accumulates) or flip it before the first L2-eligible window closes (lived path). Lab does not flip.
3. Do not score in the same turn as a bar amendment that has not already been attacked-answered. This turn did not amend the bar.

Lab does not schedule a score and does not mark itself ADMITTED.
