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
        "name": "passengers",
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

PROVENANCE_PATH = Path(
    "protocol/REPLICATION_PROVENANCE_REGISTRY_V1.json"
)

REQUIRED_PROVENANCE_FIELDS = (
    "source_identifier",
    "source_url_or_citation",
    "physical_domain",
    "observation_variable",
    "sampling_cadence",
    "sampling_regularness",
    "timestamp_presence",
    "time_order",
    "observation_window",
    "missingness_policy",
    "preprocessing_policy",
    "known_shared_nuisance_with_primary",
)


def provenance_value_present(value):
    """Accept explicit False where meaningful, but reject missing values."""
    if value is None:
        return False

    if isinstance(value, str):
        return bool(value.strip())

    if isinstance(value, (list, dict)):
        return bool(value)

    return True


def load_eligibility_policy() -> dict:
    if not CLAIM_PATH.exists():
        raise SystemExit(
            f"Missing strict claim specification: {CLAIM_PATH}"
        )

    claim = json.loads(
        CLAIM_PATH.read_text(encoding="utf-8")
    )

    dataset_policy = (
        claim.get("dataset", {})
        .get("eligibility_policy", {})
    )

    frequency_band = (
        claim.get("scale_validation", {})
        .get("base_frequency_band", [0.01, 0.05])
    )

    if (
        not isinstance(frequency_band, list)
        or len(frequency_band) != 2
    ):
        raise SystemExit(
            "Invalid canonical frequency band in strict_claim.json"
        )

    freq_min = float(frequency_band[0])
    freq_max = float(frequency_band[1])

    if not (0.0 < freq_min < freq_max < 0.5):
        raise SystemExit(
            "Invalid canonical frequency band bounds."
        )

    return {
        "minimum_series_length": int(
            dataset_policy.get("minimum_series_length", 256)
        ),
        "estimator_minimum_series_length": int(
            dataset_policy.get(
                "estimator_minimum_series_length", 512
            )
        ),
        "replication_minimum_series_length": int(
            dataset_policy.get(
                "replication_minimum_series_length", 1024
            )
        ),
        "minimum_frequency_bins": int(
            dataset_policy.get("minimum_frequency_bins", 20)
        ),
        "canonical_nperseg": int(
            dataset_policy.get("canonical_nperseg", 1024)
        ),
        "freq_min": freq_min,
        "freq_max": freq_max,
    }


def evaluate_dataset(
    spec: dict,
    policy: dict,
) -> dict:
    entry = {
        "dataset": spec["path"],
        "name": spec["name"],
        "role": spec["role"],
        "independent": bool(spec["independent"]),
        "derived_from": spec["derived_from"],
        "valid": False,
        "measurement_valid": False,
        "replication_eligible": False,
        "rows": 0,
        "alpha": None,
    }

    try:
        series = load_series(spec["path"])
        rows = int(len(series))
        entry["rows"] = rows

        if rows < policy["minimum_series_length"]:
            entry["replication_exclusion_reason"] = (
                "series_length_below_measurement_minimum"
            )
            return entry

        if rows < policy["estimator_minimum_series_length"]:
            entry["replication_exclusion_reason"] = (
                "series_length_below_estimator_minimum"
            )
            return entry

        nperseg = min(
            policy["canonical_nperseg"],
            rows,
        )

        frequencies = np.fft.rfftfreq(nperseg)

        available_bins = int(
            np.sum(
                (frequencies > policy["freq_min"])
                & (frequencies < policy["freq_max"])
            )
        )

        entry["frequency_bins"] = available_bins
        entry["minimum_frequency_bins"] = (
            policy["minimum_frequency_bins"]
        )

        if available_bins < policy["minimum_frequency_bins"]:
            entry["replication_exclusion_reason"] = (
                "insufficient_frequency_bins"
            )
            return entry

        alpha = estimate_alpha(
            series,
            freq_min=policy["freq_min"],
            freq_max=policy["freq_max"],
        )

        if not np.isfinite(alpha):
            entry["replication_exclusion_reason"] = (
                "nonfinite_alpha"
            )
            return entry

        entry["alpha"] = float(alpha)

        entry["measurement_valid"] = True
        entry["valid"] = True

        entry["replication_eligible"] = bool(
            rows >= policy["replication_minimum_series_length"]
        )

        if not entry["replication_eligible"]:
            entry["replication_exclusion_reason"] = (
                "series_length_below_replication_minimum"
            )

        return entry

    except Exception as exc:
        entry["error"] = str(exc)
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
  
    if not PROVENANCE_PATH.exists():
        raise SystemExit(
            f"Missing replication provenance registry: "
            f"{PROVENANCE_PATH}"
        )

    provenance_registry = json.loads(
        PROVENANCE_PATH.read_text(encoding="utf-8")
    )

    if provenance_registry.get("protocol") != (
        "REPLICATION_PROVENANCE_REGISTRY_V1"
    ):
        raise SystemExit(
            "Unexpected replication provenance registry protocol."
        )

    candidates = provenance_registry.get("candidates", {})

    for result in results:
        # Preserve the original computational eligibility for auditing.
        structural_eligible = (
            result.get("replication_eligible") is True
        )
        result["structural_replication_eligible"] = (
            structural_eligible
        )

        candidate = candidates.get(result["name"])
        missing_fields = []

        if candidate is not None:
            missing_fields = [
                field
                for field in REQUIRED_PROVENANCE_FIELDS
                if not provenance_value_present(
                    candidate.get(field)
                )
            ]

        provenance_eligible = bool(
            candidate is not None
            and candidate.get("path") == result["dataset"]
            and candidate.get("replication_eligible") is True
            and not missing_fields
        )

        result["provenance_replication_eligible"] = (
            provenance_eligible
        )
        result["provenance_missing_fields"] = missing_fields

        independent_real_domain = bool(
            result.get("role") == "independent_real"
            and result.get("independent") is True
            and result.get("derived_from") is None
        )

        final_eligible = bool(
            structural_eligible
            and independent_real_domain
            and provenance_eligible
        )

        result["replication_eligible"] = final_eligible

        exclusion_reasons = []

        if not independent_real_domain:
            exclusion_reasons.append(
                "not_an_independent_real_domain"
            )

        if not structural_eligible:
            exclusion_reasons.append(
                result.get(
                    "replication_exclusion_reason",
                    "structural_replication_eligibility_failed",
                )
            )

        if candidate is None:
            exclusion_reasons.append(
                "missing_provenance_registry_entry"
            )
        else:
            if candidate.get("path") != result["dataset"]:
                exclusion_reasons.append(
                    "provenance_path_mismatch"
                )

            if missing_fields:
                exclusion_reasons.append(
                    "incomplete_provenance_metadata"
                )

            if candidate.get("replication_eligible") is not True:
                exclusion_reasons.append(
                    "provenance_not_approved_for_replication"
                )

        # Preserve every known exclusion cause for auditability.
        result["replication_exclusion_reasons"] = (
            exclusion_reasons
        )

        result["replication_exclusion_reason"] = (
            exclusion_reasons[0]
            if exclusion_reasons
            else None
        )
            

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
