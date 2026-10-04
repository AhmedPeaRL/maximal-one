from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.load_real_datasets import load_series
from analysis.numerical_spectral_verification import estimate_alpha


CLAIM_PATH = Path(
    "core-scientific/strict_claim.json"
)

OUTPUT = Path(
    "artifacts/canonical_consensus.json"
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

    {
        "name": "sunspots_global_extended",
        "path": "real-data/sunspots_global_extended.csv",
        "role": "derived_real_control",
        "independent": False,
        "derived_from": "real-data/sunspots_full.csv",
    },

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


def load_eligibility_policy() -> dict:
    if not CLAIM_PATH.exists():
        raise SystemExit(
            f"Missing strict claim specification: {CLAIM_PATH}"
        )

    claim = json.loads(
        CLAIM_PATH.read_text(
            encoding="utf-8"
        )
    )

    dataset_policy = (
        claim
        .get("dataset", {})
        .get("eligibility_policy", {})
    )

    return {
        "minimum_series_length": int(
            dataset_policy.get(
                "minimum_series_length",
                256,
            )
        ),
        "replication_minimum_series_length": int(
            dataset_policy.get(
                "replication_minimum_series_length",
                1024,
            )
        ),
        "canonical_nperseg": int(
            dataset_policy.get(
                "canonical_nperseg",
                1024,
            )
        ),
    }


def evaluate_dataset(
    spec: dict,
    policy: dict,
) -> dict:

    entry = {
        "dataset": spec["path"],
        "name": spec["name"],
        "role": spec["role"],
        "independent": bool(
            spec["independent"]
        ),
        "derived_from": spec["derived_from"],

        # Legacy measurement-validity field.
        "valid": False,

        # Explicit semantic fields.
        "measurement_valid": False,
        "replication_eligible": False,

        "rows": 0,
        "alpha": None,
    }

    try:
        series = load_series(
            spec["path"]
        )

        rows = int(
            len(series)
        )

        entry["rows"] = rows

        alpha = estimate_alpha(
            series
        )

        if not np.isfinite(alpha):
            raise ValueError(
                "alpha is not finite"
            )

        entry["alpha"] = float(
            alpha
        )

        # Measurement validity means that the canonical
        # alpha measurement is available and finite.
        entry["measurement_valid"] = bool(
            rows
            >=
            policy["minimum_series_length"]
        )

        # Preserve the historical "valid" field only
        # as a measurement-validity compatibility alias.
        entry["valid"] = bool(
            entry["measurement_valid"]
        )

        if not entry["measurement_valid"]:
            entry["replication_exclusion_reason"] = (
                "series_length_below_measurement_minimum"
            )

            return entry

        # Replication eligibility is a dataset-level
        # protocol property, not a claim of replication.
        entry["replication_eligible"] = bool(
            rows
            >=
            policy["replication_minimum_series_length"]
        )

        if not entry["replication_eligible"]:
            entry["replication_exclusion_reason"] = (
                "series_length_below_replication_minimum"
            )

        return entry

    except Exception as exc:
        entry["error"] = str(
            exc
        )

        entry["measurement_valid"] = False
        entry["replication_eligible"] = False
        entry["valid"] = False

        return entry


def main():

    policy = load_eligibility_policy()

    results = [
        evaluate_dataset(
            spec,
            policy,
        )
        for spec in DATASETS
    ]

    primary_results = [
        r
        for r in results
        if (
            r["role"] == "primary_real"
            and r.get("measurement_valid") is True
        )
    ]

    measurement_valid_secondary_results = [
        r
        for r in results
        if (
            r["role"] == "independent_real"
            and r["independent"]
            and r.get("measurement_valid") is True
        )
    ]

    replication_eligible_secondary_results = [
        r
        for r in results
        if (
            r["role"] == "independent_real"
            and r["independent"]
            and r.get("replication_eligible") is True
        )
    ]

    excluded_secondary_real_domains = []

    for r in results:
        if (
            r["role"] != "independent_real"
            or not r["independent"]
        ):
            continue

        if r.get("measurement_valid") is not True:
            excluded_secondary_real_domains.append(
                {
                    "dataset": r["dataset"],
                    "name": r["name"],
                    "role": r["role"],
                    "independent": bool(
                        r["independent"]
                    ),
                    "measurement_valid": False,
                    "replication_eligible": False,
                    "reason": r.get(
                        "error",
                        r.get(
                            "replication_exclusion_reason",
                            "measurement_invalid",
                        ),
                    ),
                }
            )

        elif r.get("replication_eligible") is not True:
            excluded_secondary_real_domains.append(
                {
                    "dataset": r["dataset"],
                    "name": r["name"],
                    "role": r["role"],
                    "independent": bool(
                        r["independent"]
                    ),
                    "measurement_valid": True,
                    "replication_eligible": False,
                    "reason": r.get(
                        "replication_exclusion_reason",
                        "not_replication_eligible",
                    ),
                }
            )

    primary_alphas = np.asarray(
        [
            r["alpha"]
            for r in primary_results
        ],
        dtype=np.float64,
    )

    measurement_valid_secondary_alphas = np.asarray(
        [
            r["alpha"]
            for r in measurement_valid_secondary_results
        ],
        dtype=np.float64,
    )

    replication_eligible_secondary_alphas = np.asarray(
        [
            r["alpha"]
            for r in replication_eligible_secondary_results
        ],
        dtype=np.float64,
    )

    primary_available = (
        len(primary_alphas) >= 1
    )

    measurement_valid_secondary_domains = (
        len(
            measurement_valid_secondary_results
        )
    )

    replication_eligible_secondary_domains = (
        len(
            replication_eligible_secondary_results
        )
    )

    if measurement_valid_secondary_domains >= 2:
        secondary_domain_std = float(
            np.std(
                measurement_valid_secondary_alphas
            )
        )

        secondary_domain_median = float(
            np.median(
                measurement_valid_secondary_alphas
            )
        )
    else:
        secondary_domain_std = None
        secondary_domain_median = None

    summary = {
        "status": "evaluated",

        "datasets": results,

        "eligibility_policy": {
            "minimum_measurement_length": int(
                policy["minimum_series_length"]
            ),
            "replication_minimum_series_length": int(
                policy["replication_minimum_series_length"]
            ),
            "canonical_nperseg": int(
                policy["canonical_nperseg"]
            ),
            "measurement_validity_is_not_replication": True,
        },

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
            "measurement_valid_count": int(
                measurement_valid_secondary_domains
            ),
            "replication_eligible_count": int(
                replication_eligible_secondary_domains
            ),
            "measurement_valid_alphas": [
                float(r["alpha"])
                for r in measurement_valid_secondary_results
            ],
            "replication_eligible_alphas": [
                float(r["alpha"])
                for r in replication_eligible_secondary_results
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
            len(
                excluded_secondary_real_domains
            )
        ),

        # Backward compatibility ONLY.
        # This means measurement-valid domains.
        # It MUST NOT be interpreted as scientific replication.
        "valid_real_domains": int(
            measurement_valid_secondary_domains
        ),

        "measurement_valid_real_domains": int(
            measurement_valid_secondary_domains
        ),

        # This is the only field in this artifact
        # representing replication eligibility.
        # It still does NOT establish scientific replication.
        "replication_eligible_real_domains": int(
            replication_eligible_secondary_domains
        ),

        "real_domain_std": (
            secondary_domain_std
        ),

        "excluded_real_domains": (
            excluded_secondary_real_domains
        ),

        "independent_real_replication_required": True,

        "independent_real_domain_evaluation_complete": bool(
            primary_available
            and
            replication_eligible_secondary_domains
            >= 2
        ),

        "scientific_replication_established": False,

        "interpretation": (
            "The primary real dataset is evaluated separately "
            "from independent secondary real domains. "
            "Measurement validity and replication eligibility "
            "are explicitly separated. A measurement-valid "
            "domain is not automatically replication-eligible, "
            "and replication eligibility is not scientific "
            "replication. Scientific replication requires "
            "domain-level rejection of the same declared "
            "primary stochastic null using the same endpoint, "
            "direction, tail, and null family. Derived, shuffled, "
            "synthetic, and null datasets do not count. "
            "Independent secondary real datasets that fail "
            "measurement validity or replication eligibility "
            "are explicitly reported and are not silently "
            "substituted or repaired."
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

    print(
        "Measurement-valid independent secondary domains:",
        measurement_valid_secondary_domains,
    )

    print(
        "Replication-eligible independent secondary domains:",
        replication_eligible_secondary_domains,
    )

    print(
        "Scientific replication established by this artifact:",
        False,
    )

    if (
        replication_eligible_secondary_domains
        < 2
    ):
        print(
            "⚠️ Replication eligibility incomplete."
        )

    if excluded_secondary_real_domains:
        print(
            "ℹ️ Excluded independent secondary domains:"
        )

        for item in excluded_secondary_real_domains:
            print(
                f"   - {item['name']}: "
                f"{item['reason']}"
            )

    print(
        "✅ canonical consensus evaluated"
    )


if __name__ == "__main__":
    main()
