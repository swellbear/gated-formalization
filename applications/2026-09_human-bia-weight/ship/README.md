# Ship-A — human BIA→weight S1-B (method practice)

**Status:** **ADMITTED (Operator)** — method-practice demo of the S1 HARDEN (#56) Ridge map (#57). Parent string is **CLOSE**: claim *BIA wearable/sensor = accurate weight (bathroom or farm scale)* is **KILL**.  
**Model:** S1-B · Cycle C (2003–2004) · `StandardScaler` + `RidgeCV`  
**This is not a medical device.** Residual **~11 kg / ~25 lb RMSE ≠ bathroom scale or farm scale**. **Not clinical.** **No livestock transfer.** Animal parks stay. **Rithm archive only.** NHANES DUA: statistical analysis / **no re-identification**. The bundled example is **synthetic**.

Parent: [`../STATUS.md`](../STATUS.md) · ledger: [`../NAMED_GAP_LEDGER.md`](../NAMED_GAP_LEDGER.md) · holdout: [`../SCORE_S1_PROPOSED.md`](../SCORE_S1_PROPOSED.md)

---

## Install

```bash
pip install scikit-learn joblib
```

No network at predict time. Local `s1b_pipeline.joblib` only.

## How to run

From this `ship/` directory, or with paths as shown from the application folder:

```bash
python ship/predict.py ship/example_input.csv
python ship/predict.py ship/example_input.json
echo '{"BIXS050K":520.0,"BIXC050K":55.0,"BMXHT":170.0,"RIAGENDR":1,"RIDAGEYR":40}' | python ship/predict.py -
```

Prints one predicted weight (kg) per input row to stdout.

## One-prediction howto (dry-run)

Synthetic example (not a real NHANES row):

```bash
python ship/predict.py ship/example_input.csv
```

Expected stdout (also in `example_expected.txt`):

```
75.2460
```

## Features

| Name | Meaning |
|------|---------|
| `BIXS050K` | 50 kHz resistance (ohms) |
| `BIXC050K` | 50 kHz reactance (ohms) |
| `BMXHT` | Standing height (cm) |
| `RIAGENDR` | Sex code (NHANES: 1 = male, 2 = female) |
| `RIDAGEYR` | Age (years) |

Order is fixed. JSON object, JSON array of objects, or CSV with that header are accepted. `--csv` / `--json` force a parse.

## Holdout metrics (Cycle C; vs B1+)

Fit on the **train split only**, matching S1 HARDEN. n train **3420** / test **856**. `alpha` **3.1622776601683795**.

| Model | Test RMSE (kg) | notes |
|-------|----------------|--------|
| **B1+** | 14.655 | height + sex + age |
| **S1-B** | 11.271495752140735 | R50 + Xc50 + height + sex + age |

S1-B also: MAE **8.783979696023593** · R² **0.7363714213498394**. Ratio S1-B / B1+ = **0.769** (HARDEN bar). Full board: [`../SCORE_S1_PROPOSED.md`](../SCORE_S1_PROPOSED.md).

## Limitations (scope locks)

- **~11 kg / ~25 lb RMSE** is leftover honesty. This is **not** a bathroom scale and **not** a farm scale and **not** commercial continuous weighing solved. The scale-accuracy claim is **KILL** (see [`../DIGESTION_STRING_CLOSE.md`](../DIGESTION_STRING_CLOSE.md)).
- **Not clinical.** Not a medical device. Not a diagnosis or treatment tool.
- **No livestock transfer.** Poultry #47, cattle #49, sheep #51, companion #53 stay **parked**.
- **NHANES DUA:** statistical analysis / **no re-identification**. **Not CC-BY.**
- Example input is **synthetic**. Do not treat it as a person or a SEQN.
- Method-practice ship only. **Not** skill-met for farm weighing / rithm.

Machine record: [`meta.json`](meta.json).
