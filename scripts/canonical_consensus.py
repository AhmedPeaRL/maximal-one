from future import annotations
import json
from pathlib import Path
import numpy as np
from analysis.dataset_loader import load_numeric_series
from analysis.numerical_spectral_verification import estimate_alpha

DATASETS = [
    {
        "path": "real-data/sunspots_full.csv",
        "role": "primary_real",
        "independent": True,
        "derived_from": None,
    },
    {
    # This file is generated from sunspots_full.csv.
    # It MUST NOT count as an independent real domain.
        "path": "real-data/sunspots_global_extended.csv",
        "role": "derived_real_control",
        "independent": False,
        "derived_from": "real-data/sunspots_full.csv",
    },
    {
        "path": "real-data/white_noise.csv",
        "role": "null_white",
        "independent": False,
        "derived_from": None,
    },
    {
        "path": "real-data/random_walk.csv",
        "role": "null_random_walk",
        "independent": False,
        "derived_from": None,
    },
    {
        "path": "real-data/shuffled_sunspots.csv",
        "role": "null_shuffle",
        "independent": False,
        "derived_from": "real-data/sunspots_global_extended.csv",
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
        "independent": bool(spec["independent"]),
        "derived_from": spec["derived_from"],
        "valid": False,
        "alpha": None,
    }

    try:
        series = load_numeric_series(path)
        alpha = estimate_alpha(series)

        if not np.isfinite(alpha):
            raise ValueError("alpha is not finite")

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
        r
        for r in results
        if r["role"] in {
            "primary_real",
            "independent_real",
        }
        and r["valid"]
        and r["independent"]
    ]

    null_results = [
        r
        for r in results
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

    independent_real_domains = len(real_alphas)
    summary = {
        "status": "evaluated",
         "datasets": results,
         "valid_real_domains": int(
             independent_real_domains
         ),
         "valid_null_controls": int(
             len(null_alphas)
         ),
         "real_domain_std": (
             float(np.std(real_alphas))
             if independent_real_domains >= 2
             else None
         ),
         "null_control_std": (
             float(np.std(null_alphas))
             if len(null_alphas) >= 2
             else None
         ),
         "real_domain_consensus": bool(
             independent_real_domains >= 2
             and np.std(real_alphas) <= 1.2
         ),
         "null_controls_available": bool(
             len(null_alphas) >= 1
         ),
         "independent_real_replication_required": True,
         "independent_real_replication_complete": bool(
             independent_real_domains >= 2
         ),
         "interpretation": (
             "Only genuinely independent real datasets count "
             "toward cross-domain replication. Derived, shuffled, "
             "synthetic, and null datasets do not count."
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

    if independent_real_domains < 2:
        print(
            "⚠️ Independent real-domain replication incomplete."
        )
        print(
            "ℹ️ Derived and control datasets are explicitly excluded."
        )

    if len(null_alphas) == 0:
        print(
            "⚠️ No valid null controls available."
        )

    if (
        independent_real_domains >= 2
        and
        np.std(real_alphas) > 1.2
    ):
        raise SystemExit(
            "❌ Independent real-domain dispersion too high"
        )

    print(
        "✅ canonical consensus evaluated"
    )

if name == "main":
    main()
