# Stand-in tape (not live CME)

Yahoo `CL=F` daily Open/Close used only after operator stipulation **L-STANDIN-Y-CLF**.

- `clf_yahoo_standin.csv` — columns `date,open,settle,front_id` (`settle` = Yahoo Close; `front_id` = `CL=F`)
- `clf_yahoo_standin_fetch.json` — fetch metadata
- `clf_yahoo_month_chain.csv` — live Yahoo NYMEX months stacked by delivery (**not** historical CL1–CL18)
- `clf_yahoo_month_chain_fetch.json` — month-chain fetch log (38 live / 22 404)
- `horse_scores.json` — H-LAG-WF vs 0 on last 500; H-KS-FTS not run

Do **not** treat this as official settlement.

Re-run baseline RMSE: `python3 ../scripts/cl_session_rmse.py clf_yahoo_standin.csv --holdout 500`  
Re-run horses: `python3 ../scripts/cl_horses.py`
