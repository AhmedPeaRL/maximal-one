from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from analysis.dataset_loader import load_numeric_series
from analysis.numerical_spectral_verification import estimate_alpha

DATASETS = [
    {
        "path": "real-data/sunspots_full.csv",
        "role": "primary_real",
    },
    {
        "path": "real-data/sunspots_global_extended.csv",
        "role": "real_auxiliary",
    },
    {
        "path": "real-data/white_noise.csv",
        "role": "null_white",
    },
    {
        "path": "real-data/random_walk.csv",
        "role": "null_random_walk",
    },
    {
        "path": "real-data/shuffled_sunspots.csv",
        "role": "null_shuffle",
    },
]

OUTPUT = Path(
    "artifacts/canonical_consensus.json"
)

def evaluate_dataset(spec):
    path = spec["path"]

    entry = {
        "dataset": path,
        "role": spec["role"],
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

    except Exception as exc:
        entry["error"] = str(exc)

    return entry

def main():
    results = [
        evaluate_dataset(spec)
        for spec in DATASETS
    ]

    real_results = [
        r for r in results
        if r["role"] in {
            "primary_real",
            "real_auxiliary",
        }
        and r["valid"]
    ]

    null_results = [
        r for r in results
        if r["role"].startswith("null_")
        and r["valid"]
    ]

    real_alphas = np.asarray(
        [
            r["alpha"]
            for r in real_results
        ],
        dtype=np.float64,
    )

    null_alphas = np.asarray(
        [
            r["alpha"]
            for r in null_results
        ],
        dtype=np.float64,
    )

    summary = {
        "status": "evaluated",
        "datasets": results,
        "valid_real_domains": int(
            len(real_alphas)
        ),
        "valid_null_controls": int(
            len(null_alphas)
        ),
        "real_domain_std": (
            float(np.std(real_alphas))
            if len(real_alphas) >= 2
            else None
        ),
        "null_control_std": (
            float(np.std(null_alphas))
            if len(null_alphas) >= 2
            else None
        ),
        "real_domain_consensus": (
            bool(
                len(real_alphas) >= 2
                and
                np.std(real_alphas) <= 1.8
            )
        ),
        "null_controls_available": bool(
            len(null_alphas) >= 1
        ),
        "interpretation": (
            "real-domain replication requires "
            "at least two independent real datasets; "
            "shuffle and synthetic controls are not "
            "counted as independent domains"
        ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

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

    if len(real_alphas) < 2:
        print(
            "⚠️ Real-domain replication incomplete."
        )
        print(
            "ℹ️ Controls are not counted as independent domains."
        )

    if len(null_alphas) == 0:
        print(
            "⚠️ No valid null controls available."
        )

    if (
        len(real_alphas) >= 2
        and
        np.std(real_alphas) > 1.8
    ):
        raise SystemExit(
            "❌ Real-domain dispersion too high"
        )

    print(
        "✅ canonical consensus evaluated"
    )

if __name__ == "__main__":
    main()
