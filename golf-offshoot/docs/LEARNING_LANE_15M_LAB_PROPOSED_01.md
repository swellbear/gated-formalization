# Lab — PROPOSED 01: charge the documented fee, and read the hurdle it prints

**State:** **PROPOSED.** Awaiting `operator`. **Not** Softened, **not** admitted, **not** scheduled, **not** a board.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `lab` — `lab_admits=false`. Lab never admits its own candidate ([`.cursor/skills/gpf-lab/SKILL.md`](../../.cursor/skills/gpf-lab/SKILL.md)).
**Admit?** N · **Soften?** N · **Trading ARMED?** N · **Keys / orders / cash?** none
**Written:** 2026-09-07 20:05 EDT · **Evidence as-of:** 2026-09-07 20:02 EDT (`latest/journal.json` `generated_at`)

**Gate this was written under.** CoS re-stamped the honesty checklist **all-PASS** at 19:58 ET and Operator posted a residual at 18:30 ET ([`docs/agents/DESK.md`](../../docs/agents/DESK.md)). That is the trigger named in the Operator park row 8 ([`LEARNING_LANE_15M_METHOD_PARK.md`](LEARNING_LANE_15M_METHOD_PARK.md)). Founder's authorization for this turn is one PROPOSED cheap test tied to a residual, paper-only.

**What this is not.** Not a new named horse. Not a new board. Not a WC3+ reopen. It does not enter the Softened set, does not clear golf idle, does not touch golf θ / WC1 / WC2 / the Operator stamp / `phase1_dryrun/`, and does not expand past `KXBTC15M`. Golf idle stays **ON**.

Residual folded here: park row 9 (zero-edge fills). Spine: [`LEARNING_LANE_15M_SOURCE_DIGEST.md`](LEARNING_LANE_15M_SOURCE_DIGEST.md) §3f and §6.

---

## 1. The residual, in one paragraph

The 15m paper writer never selects anything, so its settled outcomes cannot become a hit rate or an edge. `paper_autobet_open_markets` takes the public mark — `paper_mark`, else `yes_ask` ([`paper.py:198`](../src/golf_offshoot/learning_lane_15m/paper.py), `:200`) — and writes it into the position as *both* sides of the comparison: `entry_edge=0.0` ([`:228`](../src/golf_offshoot/learning_lane_15m/paper.py)), `entry_model_p=yes_f` ([`:229`](../src/golf_offshoot/learning_lane_15m/paper.py)) and `entry_market_p=yes_f` ([`:230`](../src/golf_offshoot/learning_lane_15m/paper.py)) are the same number, `fill_price=yes_f` ([`:237`](../src/golf_offshoot/learning_lane_15m/paper.py)) fills at that same mark, and the movement records `model_win=yes_f` with `edge_w=0.0` and `posted_edge=0.0` ([`:254`–`:256`](../src/golf_offshoot/learning_lane_15m/paper.py)). `model_win` equals the mark, so **the model is the market**: every candidate window is bought YES at the posted price with zero recorded edge, and nothing is chosen over anything else. Whatever the settled win/lose split turns out to be, it is a sample of the market's own noise around its own price — so it cannot become a hit rate or an edge no matter how many windows join. I confirmed this by reading the file, not by trusting the digest.

One thing I found while confirming it, which is what this test is about. The lane *records* a fee regime but never charges it. `fee_type=quadratic` and `fee_multiplier=1` are pinned as metadata ([`data_feeds/kalshi_15m.py:54`–`:55`](../src/golf_offshoot/data_feeds/kalshi_15m.py)) and copied into every book's notes and every movement's `reason_technical` ([`paper.py:147`, `:264`](../src/golf_offshoot/learning_lane_15m/paper.py)) — but settle pays `payout = stake × decimal_odds` and books `pnl = payout − stake` with **no fee term anywhere** ([`settle.py:345`–`:346`](../src/golf_offshoot/learning_lane_15m/settle.py)). There is no fee formula in the codebase at all; grep finds no coefficient, no rounding rule, no fee function. So every pnl figure on disk — and the `-3.41` in `paper/ledger.json` — is a **zero-fee, mid-mark** number that describes a market no one can trade at.

---

## 2. The one test

**Charge the documented quadratic fee against the settled books already on disk, and report the per-fill hurdle it prints.**

One question: *with `fee_type=quadratic × fee_multiplier=1` actually charged on entry, what exact cost does the current zero-fee book omit, and is that cost material against the `PAPER_UNIT = 1.0` stake ([`paper.py:29`](../src/golf_offshoot/learning_lane_15m/paper.py))?*

This is **deterministic arithmetic, not an outcome comparison.** It needs no n, no accumulation, and no waiting — which is precisely why it is the cheapest honest thing available here (§7 explains why the alternative is not).

### Steps

1. **Source the coefficient.** The quadratic form needs one number, `k`, and **`k` is not on this tree.** Read it from Kalshi's *public* fee schedule — public document read, no keys, no account, no private endpoint ([`kalshi_15m.py:20`](../src/golf_offshoot/data_feeds/kalshi_15m.py) is already public-read-only, and `assert_public_read_url` refuses trade/private paths). Record the exact URL and retrieval date. **If `k` cannot be read off a public document, stop here and invent nothing** (see the first falsifier).
2. **Compute the fee per settled fill,** read-only, from `paper/*.json` already on disk. For these fills the arithmetic collapses to one term. Each YES contract pays \$1, and `decimal_odds` is `1/mark` ([`paper.py:204`](../src/golf_offshoot/learning_lane_15m/paper.py)), so contract count is \(C = \text{stake}/P\) with \(P\) the mark. Substituting into the quadratic form:

   \[
   k \cdot C \cdot P (1-P) \;=\; k \cdot \frac{\text{stake}}{P} \cdot P (1-P) \;=\; k \cdot \text{stake} \cdot (1-P)
   \]

   The contract count cancels the mark. **Per-fill fee = \(k \times \text{stake} \times (1 - \text{mark})\), rounded up to the cent** — one multiplication per window, verifiable by hand. Whether the schedule also charges a settlement-side fee must be **sourced from the same public document, not assumed**; if the document is silent, report entry-side only and say so.
3. **Report only.** Per-fill fee, total fee, fee as a percent of total stake, and fee-accurate pnl beside recorded pnl. Write **nothing** into `paper/*.json`, `paper/ledger.json`, `settlements/*.json`, `manifest.json`, the digest or the park. The output is a note for `operator`, not a new column on the lane.

---

## 3. Prediction and falsifier

**Prediction.** The fee is a deterministic charge taken on entry regardless of outcome, so fee-accurate pnl is **strictly worse than recorded pnl on every settled window without exception** — never equal, never better. The charge is largest on cheap marks and smallest on marks near 1.0, and at the \$1.00 unit it lands in the low single-digit percent of stake. The honest consequence is a **hurdle number**: the per-fill cost that any future selection rule on this lane must beat before a positive paper pnl means anything at all.

**Falsifier — any one of these and the test says "no signal / not worth pursuing," and the line is dropped rather than built:**

| # | Result | Verdict |
|---|--------|---------|
| F1 | `k` cannot be read off a **public** Kalshi document (schedule is behind an account, or only reachable via a private/trade endpoint) | **Test dies.** No coefficient is invented, no fee-accurate number is published, no key is requested. This is the most likely way it dies |
| F2 | The computed fee rounds to **\$0.00 per fill** at the \$1.00 unit | The mid-vs-fee distinction is **cosmetic** at this stake. Do not build a fee path into the paper writer |
| F3 | Total fee is **< 1% of total stake** | **Immaterial.** Drop it; the omission is not what is wrong with this lane |
| F4 | Fee-accurate pnl is **not** strictly ≤ recorded pnl on some window | My model of the fee is **wrong**. Withdraw the test rather than reconcile it |

F1 is a real risk and it is the reason step 1 comes first: the test is designed so that it dies cheaply and publicly rather than quietly guessing a number. **A test with no falsifier is not a test**, and this one has four, one of which is likely.

---

## 4. What this does not claim

- **Not an edge.** Not established, not banked, not measured, not implied. A hurdle is a **cost**, not a signal.
- **Not a hit rate.** This test does not touch the win/lose split and does not make it mean anything. The §1 residual stands: with `entry_edge=0.0`, nothing is selected, so the split stays a sample of market noise. Charging a fee makes that noise *more expensive*; it does not make it *informative*.
- **Not an admit.** `lab_admits=false`. This artifact is **PROPOSED**. Lab does not Soften, Harden, Kill, or ADMIT, and does not mark itself ADMITTED. `operator` decides.
- **Not a settle, not a win, not a lose, not a pnl.** No fee-accurate figure is an official settle. Official settle stays Kalshi `result` matched to CF Benchmarks `BRTI` only. No paper fill, demo blob or win/lose split becomes an admit or a settle here.
- **Not a direction.** A *more* negative fee-accurate pnl is not evidence of a method, and a *less* negative one would not be either. Both are bookkeeping.
- **Not scheduled.** No tick owes this. It runs only if `operator` says so.
- **Not a lineage merge.** It touches lineage A settled books only. Lineage B's published `+1.67` is neither re-derived nor summed nor dropped.

---

## 5. Cost

| Need | Status |
|---|---|
| Settled paper books, marks, stakes, recorded pnl | **Already on disk** — `golf-offshoot/data/learning_lane_15m/paper/*.json` (18 settled books as of 20:02 EDT) |
| Official results | **Already on disk** — `settlements/*.json`, unchanged and unread-from for this test beyond the join already made |
| New data collection | **None.** No new ingest, no new poll, no new window, no waiting |
| The coefficient `k` | **One public document read** — Kalshi's public fee schedule. No keys, no account, no login |
| Kalshi API keys | **None.** Not needed, not requested |
| Orders / cash / deposit / withdraw / transfer | **None.** Trading NOT ARMED |
| New series | **None.** `KXBTC15M` only; the Founder HOLD is untouched and this is not evidence toward lifting it |
| New code | Only if `operator` approves. If code lands it goes with tests, keeping the suite green (447 pass now). This artifact adds **no code** |
| Compute | One multiplication per settled window |

Everything except the one public document read is a read of files this tree already has.

---

## 6. Cheap observations I measured while sizing this

Read-only measurements on files already on disk. Each carries its own **n**. These are **observations, not results about method quality**, and none of them is a settle, a win, a lose, a pnl or an edge.

### Observation A — settle latency is already tight (n = 18)

Window close (the second UTC bound in `window_id`) to Kalshi's own `settlement_ts`, across every `settle_status: settled` row in `settlements/*.json`. `settlement_ts` is a straight passthrough of Kalshi's field ([`kalshi_15m.py:334`](../src/golf_offshoot/data_feeds/kalshi_15m.py)) off the live public API ([`:20`](../src/golf_offshoot/data_feeds/kalshi_15m.py)) — nothing on this tree stamps it, so this is the exchange's number, not ours.

| | |
|---|---|
| n | **18** settled windows (`071545-45` … `072000-00`) |
| 16 of 18 | close **+5.505 s** to **+5.520 s** — a 15 ms spread |
| `071630-30` | close **+15.512 s** |
| `072000-00` | close **+55.512 s** |
| median | **+5.514 s** |

The two outliers sit at +15.51 s and +55.51 s against a +5.51 s mode — the fractional part is constant and the excess arrives in whole 10-second steps. Suggestive of a fixed stamp plus a retry cadence; **n = 2 outliers is far too few to call that a pattern**, and it is recorded here as a curiosity, not a finding.

**Separately, and it is a different quantity:** our own observation delay (`as_of` minus window close, same 18 rows) runs min **27.6 s**, median **92.8 s**, max **558.8 s**. That tracks *our poll cycle*, not Kalshi finalization. Conflating the two would be reading our own scheduler as an exchange property.

### Observation B — the settled split is already indistinguishable from zero (n = 18)

Per-window `settlement_pnl` across the 18 settled books, exactly as recorded (zero-fee):

| | |
|---|---|
| n | **18** |
| mean | **−0.1894** per fill |
| sd | **0.9846** |
| standard error | **0.2321** |
| \|t\| | **0.82** |

At \|t\| = 0.82 the settled split is **statistically indistinguishable from zero**. That is the §1 residual measured instead of asserted: this is what "the model is the market" looks like in the numbers. It is **not** a result about method quality — there is no method to be right or wrong about, which is the whole point.

Live ledger for the same set: `starting_bankroll` 100.00 → `bankroll` 96.59, `betting_pnl` −3.41, 38 entries, 18 events. (The digest's 18:03 EDT snapshot recorded −3.41 at 10 events; the figure is coincidentally the same at 18 events. Same book, later read — **not** a second book and not a discrepancy.)

### Observation C — coefficient-free fee base (n = 18)

Summing the coefficient-free term \(C \cdot P(1-P) = \text{stake}(1-P)\) over the 18 settled fills gives **8.4015** on **\$18.00** staked. So the total entry fee is exactly \(k \times 8.4015\) before per-fill cent rounding — the sizing is done, and only `k` is missing. **No `k` is asserted here.**

---

## 7. Why I did not propose the settle-latency test instead

Founder named two candidates, and I picked the other one deliberately.

Settle latency is **already answered by the files on disk** at n = 18 (Observation A): 16 of 18 windows finalize in a 15 ms band around close +5.51 s. Spending the one PROPOSED slot on a test whose answer is already sitting in `settlements/*.json` would produce a tidy-looking tick and no new information. It is also the *less* honest choice on this lane, because latency is an ops property of the exchange — it says nothing about the §1 residual, which is that nothing is being selected.

The fee question is the cheaper and more honest one because it is **deterministic**. Observation B is the reason this matters: with per-fill noise at sd 0.9846, distinguishing a fee-sized effect (order of \$0.02–0.05 per fill) from that noise by *outcomes* would need roughly **1,500 to 17,000 windows** — 16 to 180 days of unbroken 15-minute cadence, depending on `k`. So the fee must be settled as **arithmetic**, which costs one multiplication per window and no waiting, rather than as a statistical comparison, which this lane cannot afford. That sample-size figure is a statement about **measurement cost**, not about method quality, and not a plan to accumulate windows.

---

## 8. Hard NOs honored

- No Soften, no Harden, no Kill, no ADMIT, no self-admit; `lab_admits=false` and this hands to `operator`
- No paper fill, demo blob or win/lose split called an admit or a settle; no invented win, lose or pnl anywhere a file does not record one
- Official settle stays Kalshi `result` matched to CF Benchmarks `BRTI`; no DIY CFB average; display prices are not settle evidence
- No new named horse, no new board, no WC3+ reopen, golf idle **not** cleared
- No golf θ retune, nothing touched in golf / WC1 / WC2 / the Operator stamp / `phase1_dryrun/`
- No expansion past `KXBTC15M`; the Founder HOLD stands and this is not evidence toward lifting it
- No edge established / banked edge / skill-met / productize claim
- Trading NOT ARMED — no Kalshi keys, orders, cash, deposit, withdraw or transfer
- Nothing edited in `manifest.json` (systems), hub HTML/CSS/JS (hub-ui), the digest (digestor) or the park (operator); this is a new Lab-owned file
- Nothing committed; the running hub on 127.0.0.1:8765 untouched, no second hub started
- No question put to Founder

---

## 9. Handoff

→ **`operator`.** Operator admits, rejects or parks this PROPOSED test. Lab does not.

Three things for Operator to rule on, in order:

1. Whether the test runs at all.
2. If yes — whether reading Kalshi's **public** fee schedule for `k` is inside the public-read-only posture (I believe it is; it is a documentation read, not an API call, and no key or account is involved). **If Operator says no, F1 fires and the test dies with nothing invented.**
3. Whether a fee-accurate figure, if produced, may be *displayed* anywhere. My recommendation: **not yet** — it should live in an Operator note until Operator decides whether it is a hurdle worth publishing, because a fee-accurate pnl on a dashboard is very easy for a later bot to misread as a result about method.

Lab does not schedule this and does not run step 1 without Operator.
