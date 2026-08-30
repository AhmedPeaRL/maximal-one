from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from analysis.load_real_datasets import (
    load_series,
)
from analysis.numerical_spectral_verification import (
    estimate_alpha,
)

DATASETS = [
    {
        "name": "sunspots",
        "path": "real-data/sunspots_full.csv",
        "role": "primary_real",
        "independent": True,
        "derived_from": None,
    },
    {
        "name": "co2",
        "path": "real-data/co2_atmospheric_clean.csv",
        "role": "independent_real",
        "independent": True,
        "derived_from": None,
    },
    {
        "name": "airline_passengers",
        "path": "real-data/airline_passengers.csv",
        "role": "independent_real",
        "independent": True,
        "derived_from": None,
    },
    {
        "name": "cosmic_rays",
        "path": "real-data/cosmic_rays_clean.csv",
        "role": "independent_real",
        "independent": True,
        "derived_from": None,
    },
    {
        "name": "temperature",
        "path": "real-data/temperature_global.csv",
        "role": "independent_real",
        "independent": True,
        "derived_from": None,
    },
    {
        "name": "sp500",
        "path": "real-data/sp500.csv",
        "role": "independent_real",
        "independent": True,
        "derived_from": None,
    },

    # Explicitly derived control.
    {
        "name": "sunspots_global_extended",
        "path": "real-data/sunspots_global_extended.csv",
        "role": "derived_real_control",
        "independent": False,
        "derived_from": "real-data/sunspots_full.csv",
    },

    # Null controls.
    {
        "name": "white_noise",
        "path": "real-data/white_noise.csv",
        "role": "null_white",
        "independent": False,
        "derived_from": None,
    },
    {
        "name": "random_walk",
        "path": "real-data/random_walk.csv",
        "role": "null_random_walk",
        "independent": False,
        "derived_from": None,
    },
    {
        "name": "shuffled_sunspots",
        "path": "real-data/shuffled_sunspots.csv",
        "role": "null_shuffle",
        "independent": False,
        "derived_from": "real-data/sunspots_full.csv",
    },
]

OUTPUT = Path(
    "artifacts/canonical_consensus.json"
)

def evaluate_dataset(spec):
    entry = {
        "dataset": spec["path"],
        "name": spec["name"],
        "role": spec["role"],
        "independent": bool(
            spec["independent"]
        ),
        "derived_from": spec["derived_from"],
        "valid": False,
        "alpha": None,
    }

    try:
        series = load_series(
            spec["path"]
        )

        alpha = estimate_alpha(
            series
        )

        if not np.isfinite(alpha):
            raise ValueError(
                "alpha is not finite"
            )

        entry["valid"] = True
        entry["rows"] = int(
            len(series)
        )
        entry["alpha"] = float(
            alpha
        )

    except Exception as exc:
        entry["error"] = str(exc)

    return entry

def main():
    results = [
        evaluate_dataset(spec)
        for spec in DATASETS
    ]

    real_results = [
        r
        for r in results
        if (
            r["independent"]
            and r["valid"]
            and r["role"]
            in {
                "primary_real",
                "independent_real",
            }
        )
    ]

    null_results = [
        r
        for r in results
        if (
            r["role"].startswith("null_")
            and r["valid"]
        )
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

    independent_real_domains = (
        len(real_alphas)
    )

    if independent_real_domains >= 2:
        real_domain_std = float(
            np.std(real_alphas)
        )
        real_domain_median = float(
            np.median(real_alphas)
        )
    else:
        real_domain_std = None
        real_domain_median = None

    summary = {
        "status": "evaluated",
        "datasets": results,

        "valid_real_domains": int(
            independent_real_domains
        ),

        "real_domain_alphas": [
            float(x)
            for x in real_alphas
        ],

        "real_domain_median": (
            real_domain_median
        ),

        "real_domain_std": (
            real_domain_std
        ),

        "valid_null_controls": int(
            len(null_alphas)
        ),

        "null_control_std": (
            float(np.std(null_alphas))
            if len(null_alphas) >= 2
            else None
        ),

        "real_domain_consensus": bool(
            independent_real_domains >= 2
        ),

        "null_controls_available": bool(
            len(null_alphas) >= 1
        ),

        "independent_real_replication_required": True,

        "independent_real_replication_complete": bool(
            independent_real_domains >= 2
        ),

        "interpretation": (
            "Only genuinely independent real datasets "
            "count toward cross-domain replication. "
            "Derived, shuffled, synthetic, and null "
            "datasets do not count."
        ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
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

    if independent_real_domains < 2:
        print(
            "⚠️ Independent real-domain replication incomplete."
        )
        print(
            "ℹ️ At least two genuinely independent real domains are required."
        )
    else:
        print(
            "✅ Independent real-domain replication available."
        )

    if len(null_alphas) == 0:
        print(
            "⚠️ No valid null controls available."
        )

    print(
        "✅ canonical consensus evaluated"
    )

if __name__ == "__main__":
    main()
