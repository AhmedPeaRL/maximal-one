import os
import json
import pandas as pd
import numpy as np

VALID_COLUMNS = [
    "value",
    "Value",
    "Sunspots",
    "sunspots",
    "Close",
    "close"
]

def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing dataset: {path}"
        )

    # try comma first
    df = pd.read_csv(path)

    # if entire line became one column,
    # retry with semicolon
    if len(df.columns) == 1:
        col = str(df.columns[0])

        if ";" in col:
            df = pd.read_csv(
                path,
                sep=";",
                engine="python"
            )

    return df

def detect_series(df):
    for col in VALID_COLUMNS:
        if col in df.columns:
            return (
                pd.to_numeric(
                    df[col],
                    errors="coerce"
                )
                .dropna()
                .values
            )

    numeric = []

    for col in df.columns:
        values = pd.to_numeric(
            df[col],
            errors="coerce"
        ).dropna()

        if len(values) > 100:
            numeric.append(
                (
                    col,
                    values.values
                )
            )

    if numeric:
        numeric.sort(
            key=lambda x: len(x[1]),
            reverse=True
        )

        return numeric[0][1]

    raise ValueError(
        f"No usable numeric column found. "
        f"Columns={list(df.columns)}"
    )

def compute_signal(alpha):
    return 1 if alpha > 0.5 else -1

def evaluate_prediction(series):
    correct = 0
    total = 0

    for i in range(len(series) - 1):
        window = series[max(0, i-128):i+1]
        alpha = estimate_alpha(window)

        if not np.isfinite(alpha):
            continue

        pred = compute_signal(alpha)

        real = np.sign(
            series[i + 1] - series[i]
        )

        if pred == real:
            correct += 1

        total += 1

    return (
        correct / total
        if total > 0
        else 0
    )

def run():
    with open(
        "core-scientific/external_prediction_bridge.json"
    ) as f:
        cfg = json.load(f)

    results = {}

    for target in cfg["prediction_targets"]:

        df = load_data(
            target["source"]
        )

        series = detect_series(df)

        acc = evaluate_prediction(series)

        results[target["id"]] = {
            "accuracy": float(acc),
            "samples": int(len(series))
        }

    os.makedirs(
        "artifacts",
        exist_ok=True
    )

    with open(
        "artifacts/external_prediction.json",
        "w"
    ) as f:

        json.dump(
            results,
            f,
            indent=2
        )

    print(
        "External prediction evaluation complete:"
    )

    print(
        json.dumps(
            results,
            indent=2
        )
    )

if __name__ == "__main__":
    run()
