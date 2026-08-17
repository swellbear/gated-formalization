# Stand-in tape (not live CME)

Yahoo `CL=F` daily Open/Close used only after operator stipulation **L-STANDIN-Y-CLF**.

- `clf_yahoo_standin.csv` — columns `date,open,settle,front_id` (`settle` = Yahoo Close; `front_id` = `CL=F`)
- `clf_yahoo_standin_fetch.json` — fetch metadata

Do **not** treat this as official settlement. Re-run RMSE: `python3 ../scripts/cl_session_rmse.py clf_yahoo_standin.csv --holdout 500`
