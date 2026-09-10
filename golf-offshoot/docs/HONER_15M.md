# honer_15m — sibling search + exam lane

**Lane id:** `honer_15m`  
**Series:** `KXBTC15M` only. Not a HOLD lift.  
**Not** `learning_lane_15m`. Books do not merge. Trading **NOT ARMED**.

This is a Founder-authorized sibling. Lineage A, PaperWatch, `LEARNING_LANE_15M_RULES.json`, and `trials_to_date` stay sole owners of the live 70. Isolation is a **staging wall** so evidence stays clean, not a claim honer stays a toy. Destination: search → exam → earned AND-skip consult inside factory `decide()`. Protocol: [`HONER_15M_PROMOTION.md`](HONER_15M_PROMOTION.md). Consult is **off** until exam + score + later Critic exist and CoS assigns Systems to enable that snapshot.

## What it is

- **Search book:** YES-or-skip. Never buy NO. Family 1 is skip-rich-YES at live θ (start 0.75, clip [0.55, 0.90]).
- **Step rule `local_regret_v2`** (dated 2026-09-09 15:08 ET): step only if `|posted_yes − θ| ≤ 0.10`. Fill+NO tightens (θ − 0.02). Skip+YES loosens (θ + 0.02). Far tickets do not move the line. A deploy migrate keeps current θ and resets the freeze clock so v1 and v2 are not mixed.
- **Exam book:** lived fills at **frozen** knobs when freeze *f* fires. Own k (in `data/honer_15m/latest/trials.json`). n=70. One exam at a time. Not a keep.
- **Freeze f `in_band_v1`:** ≥20 **in-band** settled search windows, `|θ − last_declared_θ| ≥ 0.05` (or `|δ − last_declared_δ| ≥ 0.02` on the spread family), **and** 5 consecutive **in-band** windows with no knob move. Far tickets increment an ignored counter only. Retired or spent vectors cannot freeze.
- **Quote bus:** PaperWatch is the sole Kalshi fetch. Honer subscribes to `data/quote_bus/latest/KXBTC15M.json`. Stale (>180s) or missing → skip, never HTTP.
- **Keep-lock:** `can_keep()` is false while fee is omitted, the bar is not binding, lab_admits, or trading is armed. A green exam is not a keep. Citing the factory fee pin is not a dated fee-apply. Founder read-once is not a keep gate.
- **Sidecar:** hub launches `python -m golf_offshoot honer-15m --watch` as its own process (not a second hub tree). Soft artifact refresh does not load new honer tick code.
- **8765 HTML and the local honer PNG share columns:** Near line / Spread / Wide-book. Freeze meter is in-band. Lineage A PNG is untouched.
- **Library:** `latest/library.json`. Outcomes are `parked`, `completed_dead`, `completed_unscored`, or `search_untestable`. Labels compound. Pnl does not rank. Not a score. `search_untestable` does **not** increment honer exam k.
- **Catalog:** [`HONER_15M_CATALOG.json`](HONER_15M_CATALOG.json). Two families only. `H-SKIP-WIDE-SPREAD` activates after θ sits on the clip for 20 **in-band** windows **or** a second search-starvation, **and** ≥75% of the last 20 search decisions have a quote. Missing bid/ask → no spread skip (richness line only). Amend protocol: [`HONER_15M_CATALOG_AMEND.md`](HONER_15M_CATALOG_AMEND.md).
- **Futility:** at n=20 and n=40, park if remaining windows as skips cannot pass (mean d≤0 or exam mean pnl≤0 at 70). At n=70 the same means label `completed_dead` vs `completed_unscored` — still not a keep.
- **Search starvation (honer only):** on the search clock `search_settled_since_freeze`, look at n=40 (starve if zero in-band visits) and n=70 (starve if in-band < 20). First family-1 starve retires the vector as `search_untestable` and resets θ to 75¢. Second family-1 starve retires then advances to wide-spread if quotes are ok (`advance_owed` retries without another 70 or a second reset). Family 2 is symmetric; second starve exhausts the catalog. Not a factory rule. Not consult enable. Deploy does not zero the live search clocks.
- **Mark:** `paper_mark` else `yes_ask`. Same candidate filter as the public 15m adapter. Spread is a skip gate, never settle evidence.
- **Fee:** omitted until a dated honer fee-apply that cites the factory `schedule_sha256`. A cite is not an apply. Do not print a fee-adjusted total.
- **δ / sd:** not copied from the live bar. Provisional until a sibling score. Permutation seed `20260909`. Binding false.

## Roots

`golf-offshoot/data/honer_15m/` only. Never `learning_lane_15m/` and never `/workspace/kalshi_15m_exports`.

CLI: `python -m golf_offshoot honer-15m` (one tick) or `--watch`.

Hub: labeled sandbox on `127.0.0.1:8765` when `lane=learning_lane_15m`. English standing plus local `honer_window_strip.png` (not Pages). 8765 freeze meter + English library (not registry ids); search/exam tables **and** the honer PNG show near-line / spread / wide-book. No combined bankroll. No winner vs Lineage A. Soft artifact refresh does not load new honer tick code — the sidecar re-execs on honer sources; restart the existing 8765 tree once after sidecar/`app.py` land.

## Burned classes (do not revive)

FLIP, PERSIST, SEAS-DIR, SHRINK, LOGIT, RETUNE-COINFLIP-BAND, FEE-AS-SIGNAL, SUM-LINEAGES, BACKFILL-GAP, BASELINE-AS-EDGE.
