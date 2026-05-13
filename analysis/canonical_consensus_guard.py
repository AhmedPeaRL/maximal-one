import json
import numpy as np
import pandas as pd

from analysis.numerical_spectral_verification import (
    estimate_alpha
)

DATASETS = [
    "real-data/sunspots_global.csv",
    "real-data/sunspots_global_extended.csv"
    "real-data/white_noise.csv",
    "real-data/random_walk.csv",
    "real-data/shuffled_sunspots.csv"
]

VALID_COLUMNS = ["value", "Sunspots"]

alphas = []

report = []

for path in DATASETS:

    try:

        df = pd.read_csv(path)

        col = None

        for c in VALID_COLUMNS:
            if c in df.columns:
                col = c
                break

        if col is None:
            raise ValueError(
                f"No valid column in {path}"
            )

        series = (
            df[col]
            .astype(np.float64)
            .values
        )

        alpha = estimate_alpha(series)

        if not np.isfinite(alpha):
            alpha = -1.0

        report.append({
            "dataset": path,
            "alpha": float(alpha)
        })

        if alpha > 0:
            alphas.append(alpha)

    except Exception as e:

        report.append({
            "dataset": path,
            "alpha": -1.0,
            "error": str(e)
        })

if len(alphas) < 2:
    raise SystemExit(
        "❌ insufficient valid domains"
    )

dispersion = float(np.std(alphas))

summary = {
    "alphas": report,
    "cross_domain_std": dispersion,
    "valid_domains": len(alphas)
}

with open(
    "artifacts/canonical_consensus.json",
    "w"
) as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))

if dispersion > 1.8:
    raise SystemExit(
        "❌ cross-domain dispersion too high"
    )

print(
    "✅ canonical consensus holds"
)
