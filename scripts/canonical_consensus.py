from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from analysis.load_real_datasets import load_series
from analysis.numerical_spectral_verification import estimate_alpha

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

    primary_results = [
        r
        for r in results
        if (
            r["role"] == "primary_real"
            and r["valid"]
        )
    ]

    secondary_real_results = [
        r
        for r in results
        if (
            r["role"] == "independent_real"
            and r["independent"]
            and r["valid"]
        )
    ]

    excluded_secondary_real_domains = [
        {
            "dataset": r["dataset"],
            "name": r["name"],
            "role": r["role"],
            "independent": bool(
                r["independent"]
            ),
            "valid": bool(
                r["valid"]
            ),
            "reason": r.get(
                "error",
                "excluded from independent secondary-domain replication",
            ),
        }
        for r in results
        if (
            r["role"] == "independent_real"
            and r["independent"]
            and not r["valid"]
        )
    ]

    primary_alphas = np.asarray(
        [
            r["alpha"]
            for r in primary_results
        ],
        dtype=np.float64,
    )

    secondary_real_alphas = np.asarray(
        [
            r["alpha"]
            for r in secondary_real_results
        ],
        dtype=np.float64,
    )

    primary_available = (
        len(primary_alphas) >= 1
    )

    independent_secondary_domains = (
        len(secondary_real_alphas)
    )

    if independent_secondary_domains >= 2:
        secondary_domain_std = float(
            np.std(secondary_real_alphas)
        )
        secondary_domain_median = float(
            np.median(secondary_real_alphas)
        )
    else:
        secondary_domain_std = None
        secondary_domain_median = None

    summary = {
        "status": "evaluated",

        "datasets": results,

        "primary_real_domain": {
            "available": bool(
                primary_available
            ),
            "count": int(
                len(primary_alphas)
            ),
            "alphas": [
                float(x)
                for x in primary_alphas
            ],
        },

        "independent_secondary_real_domains": {
            "count": int(
                independent_secondary_domains
            ),
            "alphas": [
                float(x)
                for x in secondary_real_alphas
            ],
            "median": (
                secondary_domain_median
            ),
            "std": (
                secondary_domain_std
            ),
        },

        "excluded_secondary_real_domains": (
            excluded_secondary_real_domains
        ),

        "excluded_secondary_real_domain_count": int(
            len(excluded_secondary_real_domains)
        ),

        "independent_real_replication_required": True,

        "independent_real_replication_complete": bool(
            primary_available
            and
            independent_secondary_domains >= 2
        ),

        "interpretation": (
            "The primary real dataset is evaluated separately "
            "from independent secondary real domains. "
            "Only genuinely independent secondary real datasets "
            "count toward replication of the primary result. "
            "Derived, shuffled, synthetic, and null datasets "
            "do not count. Independent secondary real datasets "
            "that fail the canonical alpha measurement are "
            "explicitly listed and are not silently substituted "
            "or repaired."
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

    if excluded_real_domains:
        print(
            "ℹ️ Excluded independent real domains:"
        )
        for item in excluded_real_domains:
            print(
                f"   - {item['name']}: "
                f"{item['reason']}"
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
