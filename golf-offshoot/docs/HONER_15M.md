# honer_15m — sibling search + exam lane

**Lane id:** `honer_15m`  
**Series:** `KXBTC15M` only. Not a HOLD lift.  
**Not** `learning_lane_15m`. Books do not merge. Trading **NOT ARMED**.

This is a Founder-authorized sibling. Lineage A, PaperWatch, `LEARNING_LANE_15M_RULES.json`, and `trials_to_date` stay sole owners of the live 70. Isolation is a **staging wall** so evidence stays clean, not a claim honer stays a toy. Destination: search → freeze photocopy → exam → machine score vs fill-all after fees → park dead or file-gate consult. Protocol: [`HONER_15M_PROMOTION.md`](HONER_15M_PROMOTION.md). Consult is **off** until freeze hash, dated fee-apply, surviving exam score, and honer invariants hold on **that** snapshot (`maybe_sync_and_enable`). Freeze bytes are the name. Lab does not retype θ. Replacement of the executing factory row is crew after consult has lived, not Founder. Founder is arm, cash, keys, HOLD lift, and golf C2/C4/WC3+.

## What it is

- **Search book:** YES-or-skip. Never buy NO. Family 1 is skip-rich-YES at live θ (start 0.75, clip [0.55, 0.90]).
- **Step rule `local_regret_v2`** (dated 2026-09-09 15:08 ET): step only if `|posted_yes − θ| ≤ 0.10`. Fill+NO tightens (θ − 0.02). Skip+YES loosens (θ + 0.02). Far tickets do not move the line. A deploy migrate keeps current θ and resets the freeze clock so v1 and v2 are not mixed.
- **Exam book:** lived fills at **frozen** knobs when freeze *f* fires. Own k (in `data/honer_15m/latest/trials.json`). n=70. One exam at a time. Not a keep.
- **Freeze f `in_band_v1`:** ≥20 **in-band** settled search windows, `|θ − last_declared_θ| ≥ 0.05` (or `|δ − last_declared_δ| ≥ 0.02` on the spread family, or `|γ − last_declared_γ| ≥ 0.02` on the thin-book family), **and** 5 consecutive **in-band** windows with no knob move. Far tickets increment an ignored counter only. Retired or spent vectors cannot freeze.
- **Quote bus:** PaperWatch is the sole Kalshi fetch. Honer subscribes to `data/quote_bus/latest/KXBTC15M.json`. Stale (>180s) or missing → skip, never HTTP.
- **Keep-lock:** `can_keep()` is false while fee is omitted, the bar is not binding, lab_admits, or trading is armed. A green exam is not a keep. A cite is not an apply. Dated honer fee-apply (`honer_15m.fee.apply_factory_fee`) cites the factory `founder_browser_bytes` pin and clears `fee_omitted` only after that apply. Keep stays closed while the honer bar is unbound. Founder read-once is not a keep gate.
- **Sidecar:** hub launches `python -m golf_offshoot honer-15m --watch` as its own process (not a second hub tree). Soft artifact refresh does not load new honer tick code.
- **8765 HTML and the local honer PNG share columns:** Near line / Spread / Wide-book / Thin-book. Freeze meter is in-band. Lineage A PNG is untouched.
- **Library:** `latest/library.json`. Outcomes are `parked`, `completed_dead`, `completed_unscored`, or `search_untestable`. Labels compound. Pnl does not rank. Not a score. `search_untestable` does **not** increment honer exam k. When `catalog_exhausted` is true **and** no next family is dated, **search is parked** (no new search fills). Exam stays closed. When a next family exists, that stamp is stale: search unparks and advances. `latest/family_amend.json` is the file doorbell that `HONER-FAMILY-AMEND` is owed (`catalog_exhausted` or exam `completed_dead`) until family 3 is dated. It does not read exam pnl. Gym Honer has no clip-grid.
- **Catalog:** [`HONER_15M_CATALOG.json`](HONER_15M_CATALOG.json). Three families. Family 3 `H-SKIP-THIN-BOOK` is dated from files (not a Lab ping; not factory civil skip). `H-SKIP-WIDE-SPREAD` and `H-SKIP-THIN-BOOK` activate after the previous family sits on the clip for 20 **in-band** windows **or** a second search-starvation, **and** ≥75% of the last 20 search decisions have a quote. Missing bid/ask → thin-book skip on family 3; on family 2 that is richness only. Amend protocol: [`HONER_15M_CATALOG_AMEND.md`](HONER_15M_CATALOG_AMEND.md).
- **Futility:** at n=20 and n=40, park if remaining windows as skips cannot pass (mean d≤0 or exam mean pnl≤0 at 70). At n=70 the same means label `completed_dead` vs `completed_unscored` — still not a keep.
- **Search starvation (honer only):** on the search clock `search_settled_since_freeze`, look at n=40 (starve if zero in-band visits) and n=70 (starve if in-band < 20). First family-1 starve retires the vector as `search_untestable` and resets θ to 75¢. Second family-1 starve retires then advances to wide-spread if quotes are ok (`advance_owed` retries without another 70 or a second reset). Family 2 is the same shape onto thin-book. Family 3 second starve exhausts the catalog. Not a factory rule. Not consult enable. Deploy does not zero the live search clocks.
- **Mark:** `paper_mark` else `yes_ask`. Same candidate filter as the public 15m adapter. Spread is a skip gate, never settle evidence.
- **Fee:** dated honer fee-apply at score time via factory `fee_adjust`, citing `founder_browser_bytes` pin `c326a69f…`. Search/exam ledgers stay gross. Do not print a fee-adjusted honer total on the hub, digest, or `records[]`. `fee_omitted` is false after apply; keep stays closed until bind.
- **δ / sd:** not copied from the live bar. Provisional until a sibling score. Permutation seed `20260909`. Binding false.

## Roots

`golf-offshoot/data/honer_15m/` only. Never `learning_lane_15m/` and never `/workspace/kalshi_15m_exports`.

CLI: `python -m golf_offshoot honer-15m` (one tick) or `--watch`.

Hub: labeled sandbox on `127.0.0.1:8765` when `lane=learning_lane_15m`. English standing plus local `honer_window_strip.png` (not Pages). 8765 freeze meter + English library (not registry ids); search/exam tables **and** the honer PNG show near-line / spread / wide-book / thin-book. No combined bankroll. No winner vs Lineage A. Soft artifact refresh does not load new honer tick code — the sidecar re-execs on honer sources; restart the existing 8765 tree once after sidecar/`app.py` land.

## Burned classes (do not revive)

FLIP, PERSIST, SEAS-DIR, SHRINK, LOGIT, RETUNE-COINFLIP-BAND, FEE-AS-SIGNAL, SUM-LINEAGES, BACKFILL-GAP, BASELINE-AS-EDGE.
