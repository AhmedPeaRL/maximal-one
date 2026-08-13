from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from analysis.dataset_loader import load_numeric_series
from analysis.numerical_spectral_verification import estimate_alpha

DATASETS = [
    "real-data/sunspots_full.csv",
    "real-data/sunspots_global_extended.csv",
    "real-data/white_noise.csv",
    "real-data/random_walk.csv",
    "real-data/shuffled_sunspots.csv",
]

OUTPUT = Path(
    "artifacts/canonical_consensus.json"
)

def main():
    results = []
    valid_alphas = []

    for path in DATASETS:
        entry = {
            "dataset": path,
            "valid": False,
            "alpha": None,
        }

        try:
            series = load_numeric_series(path)

            alpha = estimate_alpha(series)

            if not np.isfinite(alpha):
                raise ValueError(
                    "alpha is not finite"
                )

            entry["valid"] = True
            entry["rows"] = int(len(series))
            entry["alpha"] = float(alpha)

            valid_alphas.append(float(alpha))

        except Exception as exc:
            entry["error"] = str(exc)

        results.append(entry)

    if len(valid_alphas) < 2:
        summary = {
            "status": "insufficient_valid_domains",
            "valid_domains": len(valid_alphas),
            "required_domains": 2,
            "datasets": results,
        }

        OUTPUT.write_text(
            json.dumps(
                summary,
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

        print(
            json.dumps(
                summary,
                indent=2,
            )
        )

        raise SystemExit(
            "❌ insufficient valid domains"
        )

    alphas = np.asarray(
        valid_alphas,
        dtype=np.float64,
    )

    dispersion = float(
        np.std(alphas)
    )

    summary = {
        "status": "evaluated",
        "valid_domains": len(valid_alphas),
        "cross_domain_std": dispersion,
        "alphas": results,
        "consensus_threshold": 1.8,
        "consensus_passed": bool(
            dispersion <= 1.8
        ),
    }

    OUTPUT.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            summary,
            indent=2,
        )
    )

    if dispersion > 1.8:
        raise SystemExit(
            "❌ cross-domain dispersion too high"
        )

    print(
        "✅ canonical consensus evaluated"
    )

if __name__ == "__main__":
    main()
