# honer_15m — sibling search + exam lane

**Lane id:** `honer_15m`  
**Series:** `KXBTC15M` only. Not a HOLD lift.  
**Not** `learning_lane_15m`. Books do not merge. Trading **NOT ARMED**.

This is a Founder-authorized sibling. Lineage A, PaperWatch, `LEARNING_LANE_15M_RULES.json`, and `trials_to_date` stay sole owners of the live 70.

## What it is

- **Search book:** YES-or-skip at live θ. Start θ=0.75. After each **settled** search window: fill+loss → θ+=0.02; skip+Kalshi YES → θ-=0.02. Clip [0.55, 0.90]. Never buy NO.
- **Exam book:** lived fills at **frozen** θ when freeze *f* fires. Own k (in `data/honer_15m/latest/trials.json`). n=70. One exam at a time.
- **Freeze f:** `|θ − last_declared_θ| ≥ 0.05` AND ≥20 settled search windows. Inputs are search θ and search count only.
- **Futility:** at n=20 and n=40, park if remaining windows as skips cannot pass (mean d≤0 or exam mean pnl≤0 at 70).
- **Mark:** `paper_mark` else `yes_ask`. Same candidate filter as the public 15m adapter.
- **Fee:** omitted. Do not print a fee-adjusted total.
- **δ / sd:** not copied from the live bar. Provisional until a sibling score. Permutation seed `20260909`. Binding false.

## Roots

`golf-offshoot/data/honer_15m/` only. Never `learning_lane_15m/` and never `/workspace/kalshi_15m_exports`.

CLI: `python -m golf_offshoot honer-15m` (one tick) or `--watch`.

Hub: labeled sandbox on `127.0.0.1:8765` when `lane=learning_lane_15m`. No combined bankroll. No winner vs Lineage A.

## Burned classes (do not revive)

FLIP, PERSIST, SEAS-DIR, SHRINK, LOGIT, RETUNE-COINFLIP-BAND, FEE-AS-SIGNAL, SUM-LINEAGES, BACKFILL-GAP, BASELINE-AS-EDGE.
