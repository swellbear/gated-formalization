# Compare method (A vs B)

Parallel paper machines. **Never auto-bets. Never real money.** Lived St. Jude `{event}.json` is a museum: auto-apply later snapshots is allowed; `--lock-paper` is not.

Hashed constitution: `method_law_v1` in `golf_offshoot.compare.law`.

| Path | Ranking | Ticket bar | Paper file |
|------|---------|------------|------------|
| lived | current pipeline | EdgeW **and** vs-posted | `{event}.json` |
| A-replay / A-control | same θ as lived | EdgeW only | `{event}_a_replay.json` |
| B-guts | honest θ | EdgeW only | `{event}_b_guts.json` |
| B-nerves | A's θ | vs-posted (`1/d`) | `{event}_b_nerves.json` |
| B-full | honest θ | vs-posted | `{event}_b_full.json` |

Two Monte Carlos, not four: lived/A sim + B-guts sim, **same seed**. B-nerves and B-full are strategy-only.

Honesty in B-guts: no agronomy schema defaults in course demand; missing SG is NaN (not 0) in cosine; do not invent `recent_form_sg` from neighbors; park narrative and live tee pairing; health is WD-only.

Compare ledgers are independent **$250** books. They do not touch `ledger.json` / `working_bankroll`. Sells book P/L onto that path's own bankroll. Mode is frozen `stay_selective` + `conservative`. Threshold learner **keep_t** this week (`n=1`). Reject `copy_a_edgew_because_a_won`.

**Markets:** St. Jude (`401811962`) stays **Winner-only**. From the next event on, A/B also ticket **Top 5 / Top 10 / Top 20 when that coupon is actually listed**. Place is never synthesized from Winner odds. Score **Winner posted P/L** and **place posted P/L** as two lines, not one blended book.

```bash
python -m golf_offshoot live --event 401811962 --book bovada --compare-method
python -m golf_offshoot compare-replay --event 401811962
```

`compare-replay` walks existing snapshots into A-replay + B-nerves only. B-guts needs persisted `audit.extra["field"]` (new audits store field + market). This week's older snapshots do not have that field.

Default `live` auto-applies the **lived** paper book when the actionable advice set changes (HOLD-only does not re-apply). `--no-apply-paper` skips. `--compare-method` will not `--lock-paper` lived.

The **fights** page under `data/exports/{event}_fights_*.html` is the operator readout: who each path owns, where they disagree, and **why** (plain + technical: Winner vs place coupons, EdgeW vs vs-posted, honest theta vs A theta, with the 3pp numbers). `--compare-method` and `compare-replay` also write one **batch pack** under `data/exports/packs/{event}_{time}_{run}_batch/` with `00_full_readout.pdf` in this order: how to read (five-book legend), fights, ESPN leaderboard, model field, then lived / A-replay / B-guts / B-nerves / B-full tickets + why-bets, then lived bankroll. Each ticket page is titled with the book (A-control shares A-replay; there is not a second A book). Open that PDF in Edge, Chrome, or Adobe — not as source in the editor.

Leftover callout stays parked. Do not add agronomy / tee / injury feeds for this.
