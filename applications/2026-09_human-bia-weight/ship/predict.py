#!/usr/bin/env python3
"""Predict body weight (kg) from NHANES-style BIA + anthro features (S1-B).

Method-practice ship package (Operator ADMIT). Not a medical device.
No network. Local joblib only.

Example (JSON file):
  python predict.py example_input.json

Example (CSV file):
  python predict.py example_input.csv

Example (stdin JSON object):
  echo '{\"BIXS050K\":520.0,\"BIXC050K\":55.0,\"BMXHT\":170.0,\"RIAGENDR\":1,\"RIDAGEYR\":40}' \\
    | python predict.py -

Prints one predicted weight (kg) per input row to stdout.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

FEATURES = ["BIXS050K", "BIXC050K", "BMXHT", "RIAGENDR", "RIDAGEYR"]
SHIP_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL = SHIP_DIR / "s1b_pipeline.joblib"


def _load_pipeline(path: Path):
    try:
        import joblib
    except ImportError as e:
        raise SystemExit("joblib required: pip install joblib scikit-learn") from e
    return joblib.load(path)


def _row_from_dict(d: dict) -> list[float]:
    missing = [f for f in FEATURES if f not in d]
    if missing:
        raise SystemExit(f"missing features: {missing}; need {FEATURES}")
    return [float(d[f]) for f in FEATURES]


def _load_json(text: str) -> list[list[float]]:
    obj = json.loads(text)
    if isinstance(obj, dict):
        return [_row_from_dict(obj)]
    if isinstance(obj, list):
        return [_row_from_dict(item) for item in obj]
    raise SystemExit("JSON must be an object or array of objects")


def _load_csv(text: str) -> list[list[float]]:
    reader = csv.DictReader(text.strip().splitlines())
    if reader.fieldnames is None:
        raise SystemExit("CSV needs a header row with feature names")
    rows = []
    for row in reader:
        rows.append(_row_from_dict(row))
    if not rows:
        raise SystemExit("CSV has no data rows")
    return rows


def _read_source(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="S1-B BIA→weight predictor (method-practice; local only)."
    )
    p.add_argument("input", nargs="?", default="-", help="JSON/CSV path, or '-' for stdin")
    p.add_argument("--csv", action="store_true", help="Force CSV parse")
    p.add_argument("--json", action="store_true", help="Force JSON parse")
    p.add_argument("--model", type=Path, default=DEFAULT_MODEL, help="joblib path")
    args = p.parse_args(argv)

    text = _read_source(args.input)
    if not text.strip():
        raise SystemExit("empty input")

    as_csv = args.csv
    as_json = args.json
    if not as_csv and not as_json:
        if args.input != "-" and str(args.input).lower().endswith(".csv"):
            as_csv = True
        else:
            as_json = True

    rows = _load_csv(text) if as_csv else _load_json(text)
    pipe = _load_pipeline(args.model)
    import numpy as np

    X = np.asarray(rows, dtype=float)
    preds = pipe.predict(X)
    for yhat in preds:
        print(f"{float(yhat):.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
