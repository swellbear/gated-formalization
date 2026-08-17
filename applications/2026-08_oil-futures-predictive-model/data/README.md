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

Do **not** treat this as official settlement.

Re-run baseline RMSE: `python3 ../scripts/cl_session_rmse.py clf_yahoo_standin.csv --holdout 500`  
Re-run horses: `python3 ../scripts/cl_horses.py`  
Re-run pretell hunt: `python3 ../scripts/cl_pretell_hunt.py`
