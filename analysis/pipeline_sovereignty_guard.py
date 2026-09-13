import json
import numpy as np
import pandas as pd
from analysis.independent_validation import compare_methods
from analysis.bootstrap_confidence import dual_bootstrap

deterministic_seed = None

from analysis.deterministic_ops import deterministic_seed

deterministic_seed(42)

DATASET = "real-data/sunspots_global_extended.csv"

WINDOWS = [
    (0.0, 1.0),
    (0.1, 0.9),
]

results = []

df = pd.read_csv(DATASET)

col = (
    "Sunspots"
    if "Sunspots" in df.columns
    else "value"
)

x = df[col].values.astype(float)

for start_ratio, end_ratio in WINDOWS:

    start = int(len(x) * start_ratio)
    end = int(len(x) * end_ratio)

    segment = x[start:end]

    if len(segment) < 256:
        continue

    method_result = compare_methods(segment)

    if not isinstance(method_result, dict):
        raise SystemExit(
            "❌ compare_methods() returned an unexpected object"
        )

    required_keys = {
        "welch_alpha",
        "fft_alpha",
        "delta",
        "finite",
        "agreement",
        "threshold",
    }

    missing = required_keys - set(method_result.keys())

    if missing:
        raise SystemExit(
            "❌ compare_methods() missing required fields: "
            + ", ".join(sorted(missing))
        )

    fft_alpha = float(
        method_result["fft_alpha"]
    )

    welch_alpha = float(
        method_result["welch_alpha"]
    )

    delta = float(
        method_result["delta"]
    )

    if not (
        np.isfinite(fft_alpha)
        and np.isfinite(welch_alpha)
        and np.isfinite(delta)
    ):
        raise SystemExit(
            "❌ Non-finite method comparison result"
        )

    confidence = dual_bootstrap(segment)

    results.append({

        "window": [
            start_ratio,
            end_ratio,
        ],

        "fft": fft_alpha,

        "welch": welch_alpha,

        "delta": delta,

        "confidence": confidence,
    })

fft_vals = [
    r["fft"]
    for r in results
    if np.isfinite(r["fft"])
]

welch_vals = [
    r["welch"]
    for r in results
    if np.isfinite(r["welch"])
]

deltas = [
    r["delta"]
    for r in results
    if np.isfinite(r["delta"])
]

if len(fft_vals) < 2:
    raise SystemExit(
        "Insufficient finite FFT estimates"
    )

if len(welch_vals) < 2:
    raise SystemExit(
        "Insufficient finite Welch estimates"
    )

if len(deltas) < 2:
    raise SystemExit(
        "Insufficient finite method-comparison estimates"
    )

report = {

    "pipeline_sovereignty_score":
        float(
            1.0
            /
            (
                1.0
                +
                np.std(
                    fft_vals + welch_vals
                )
            )
        ),

    "fft_std":
        float(
            np.std(fft_vals)
        ),

    "welch_std":
        float(
            np.std(welch_vals)
        ),

    "method_agreement":
        float(
            np.mean(deltas)
        ),

    "results":
        results,
}

# Keep this aligned with the canonical
# scientific method-agreement threshold.
MAX_DELTA = 0.30

MAX_STD = 1.8

stable = (
    report["method_agreement"] <= MAX_DELTA
    and
    report["fft_std"] < MAX_STD
    and
    report["welch_std"] < MAX_STD
)

report["verdict"] = (
    "stable"
    if stable
    else "fragile"
)

with open(
    "artifacts/pipeline_sovereignty.json",
    "w"
) as f:

    json.dump(
        report,
        f,
        indent=2
    )

print(
    json.dumps(
        report,
        indent=2
    )
)

if report["verdict"] != "stable":

    raise SystemExit(
        "❌ PIPELINE FRAGILITY DETECTED"
    )

print(
    "✅ PIPELINE SOVEREIGNTY HOLDS"
)
