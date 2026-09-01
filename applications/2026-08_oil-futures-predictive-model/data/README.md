# Stand-in tape (not live CME)

Yahoo `CL=F` daily Open/Close used only after operator stipulation **L-STANDIN-Y-CLF**.

- `clf_yahoo_standin.csv` — columns `date,open,settle,front_id` (`settle` = Yahoo Close; `front_id` = `CL=F`)
- `clf_yahoo_standin_fetch.json` — fetch metadata
- `clf_yahoo_month_chain.csv` — live Yahoo NYMEX months stacked by delivery (**not** historical CL1–CL18)
- `clf_yahoo_month_chain_fetch.json` — month-chain fetch log (38 live / 22 404)
- `horse_scores.json` — H-LAG-WF, H-SPARSE-CAL, H-SPARSE-VOL vs 0; promote gates; H-KS-FTS not run
- `sparse_calendar.json` — pre-registered EIA/FOMC dates for H-SPARSE-CAL
- `tell_dxy.csv` / `tell_rbob.csv` / `tell_ho.csv` / `tell_spx.csv` / `tell_hg.csv` / `tell_tnx.csv` — Yahoo stand-in tells (**L-STANDIN-Y-TELLS**)
- `tell_yahoo_fetch.json` — tell fetch metadata
- `pretell_hunt_scores.json` — eight named tell horses; discovery F-CC all lose; no survivor; confirm skipped
- `gap_horse_scores.json` — H-GAP-FADE / H-GAP-CONT; FADE small F-DAY confirm; F-CC locked to 0; no promote
- `djt_oil_lexicon.json` — frozen oil-adjacent + bull/bear tokens (**L-HUNT-DJT**; do not retune)
- `djt_truth_posts.csv` — stripped Truth Social posts (CNN dump; **L-STANDIN-DJT-TRUTH**)
- `djt_truth_fetch.json` — fetch metadata
- `djt_hunt_scores.json` — H-DJT-WEEK / H-DJT-MONTH; discovery F-CC both tie 0; no survivor; confirm skipped
- `cftc_cl_mm_net.csv` — CFTC disagg futures-only MM net for 067651 (**L-STANDIN-CFTC-COT**)
- `cftc_cot_fetch.json` — COT fetch metadata
- `cot_hunt_scores.json` — H-COT-NET / H-COT-CHG; discovery F-CC both lose; no survivor; confirm skipped
- `eia_spot_wti.csv` / `eia_spot_brent.csv` — daily cash prints (**L-STANDIN-EIA-SPOT**; FRED EIA reprints this pulse)
- `eia_spot_fetch.json` — spot fetch metadata
- `spot_trend_hunt_scores.json` — H-SPOT-FLIP-HOLD / H-SPOT-REV; discovery both lose continuation; no survivor; confirm skipped
- `spot_trend_queue.json` — exploration register (FLIP/REV/INV burned both boards; B2W burned on WTI; LOGIT scored; named queue **empty**)
- `spot_inv_hunt_scores.json` — H-SPOT-INV-CONT / H-SPOT-INV-FADE; discovery both lose continuation; no survivor; confirm skipped
- `spot_cross_hunt_scores.json` — H-SPOT-CROSS-B2W / H-SPOT-CROSS-W2B; WTI no survivor; Brent W2B confirm point-beats (last-250 tiny); spot-trend not established
- `spot_logit_hunt_scores.json` — H-SPOT-LOGIT-FULL / H-SPOT-LOGIT-SIGN; discovery beat both boards; FULL confirm lose all windows both boards; queue empty
- `cl_inv_hunt_scores.json` — H-CL-INV-SURP / H-CL-INV-WOW; discovery F-CC both lose (0 = 0.026705; closest WOW 0.026803); no survivor; confirm skipped; do not pick least-bad
- `cl_seas_hunt_scores.json` — H-CL-SEAS-ANN / H-CL-SEAS-MON; discovery F-CC both lose (0 = 0.026705; closest ANN 0.026799); no survivor; confirm skipped; do not pick least-bad
- `cl_dow_hunt_scores.json` — H-CL-DOW-WD / H-CL-DOW-FRI; discovery F-CC both lose (0 = 0.026705; closest FRI 0.026775); no survivor; confirm skipped; do not pick least-bad
- `cl_yahoo_queue.json` — Yahoo CL exploration register (SEAS and DOW burned; named `next` **empty**)
- `eia_weekly_crude_exspr.csv` — EIA weekly US crude ex-SPR (**L-STANDIN-EIA-INV** / **L-STANDIN-EIA-INV-CL**)
- `eia_inv_fetch.json` — inventory fetch metadata

Do **not** treat this as official settlement.

Re-run baseline RMSE: `python3 ../scripts/cl_session_rmse.py clf_yahoo_standin.csv --holdout 500`  
Re-run horses: `python3 ../scripts/cl_horses.py`  
Re-run pretell hunt: `python3 ../scripts/cl_pretell_hunt.py`  
Re-run gap horses: `python3 ../scripts/cl_gap_horses.py`  
Re-run DJT hunt (from this application folder): `python3 scripts/fetch_djt_truth.py` then `python3 scripts/cl_djt_hunt.py`  
Re-run COT hunt (from this application folder): `python3 scripts/fetch_cftc_cot.py` then `python3 scripts/cl_cot_hunt.py`  
Re-run spot-trend hunt (from this application folder): `python3 scripts/fetch_eia_spot.py` then `python3 scripts/spot_trend_hunt.py --stage discovery`  
Re-run inventory overlay (from this application folder): `python3 scripts/fetch_eia_inventory.py` then `python3 scripts/spot_inv_hunt.py --stage discovery`  
Re-run cross-bench overlay (from this application folder): `python3 scripts/spot_cross_hunt.py --stage discovery` then (Brent survivor only) `python3 scripts/spot_cross_hunt.py --stage confirm`  
Re-run logistic overlay (from this application folder): `python3 scripts/spot_logit_hunt.py --stage discovery` then `python3 scripts/spot_logit_hunt.py --stage confirm`  
Re-run CL inventory overlay (from this application folder): `python3 scripts/cl_inv_hunt.py --phase discovery`  
Re-run CL season overlay (from this application folder): `python3 scripts/cl_seas_hunt.py --phase discovery`  
Re-run CL weekday overlay (from this application folder): `python3 scripts/cl_dow_hunt.py --phase discovery`
