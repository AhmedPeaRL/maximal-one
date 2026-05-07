import json
import numpy as np
import pandas as pd

from analysis.independent_validation import compare_methods
from analysis.deterministic_ops import (
    deterministic_seed,
    stable_smoothing,
    stable_fft_power,
    stable_log,
    stable_polyfit
)

deterministic_seed(42)

DATASET = "real-data/sunspots_global.csv"

WINDOWS = [
    (0.0, 1.0),
    (0.1, 0.9),
    (0.2, 0.8),
]

results = []

df = pd.read_csv(DATASET)
col = "Sunspots" if "Sunspots" in df.columns else "value"
x = df[col].values.astype(float)

for start_ratio, end_ratio in WINDOWS:

    start = int(len(x) * start_ratio)
    end = int(len(x) * end_ratio)

    segment = x[start:end]

    fft_alpha, welch_alpha = compare_methods(segment)

    results.append({
        "window": [start_ratio, end_ratio],
        "fft": float(fft_alpha),
        "welch": float(welch_alpha),
        "delta": float(abs(fft_alpha - welch_alpha))
    })

fft_vals = [r["fft"] for r in results]
welch_vals = [r["welch"] for r in results]

report = {
    "pipeline_sovereignty_score":
        float(1.0 / (1.0 + np.std(fft_vals + welch_vals))),

    "fft_std":
        float(np.std(fft_vals)),

    "welch_std":
        float(np.std(welch_vals)),

    "method_agreement":
        float(np.mean([r["delta"] for r in results])),

    "results":
        results
}

report["verdict"] = (
    "stable"
    if report["method_agreement"] < 1.0
    else "fragile"
)

with open("artifacts/pipeline_sovereignty.json", "w") as f:
    json.dump(report, f, indent=2)

print(json.dumps(report, indent=2))

if report["verdict"] != "stable":
    raise SystemExit("❌ PIPELINE FRAGILITY DETECTED")

print("✅ PIPELINE SOVEREIGNTY HOLDS")
