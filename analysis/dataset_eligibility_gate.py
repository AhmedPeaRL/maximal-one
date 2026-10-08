from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.load_real_datasets import DATASETS, load_series
from analysis.numerical_spectral_verification import (
    DEFAULT_FREQ_MIN,
    DEFAULT_FREQ_MAX,
    CANONICAL_MIN_BINS,
    CANONICAL_NPERSEG,
)


CLAIM_PATH = Path("core-scientific/strict_claim.json")
OUTPUT_PATH = Path("artifacts/dataset_eligibility_gate.json")
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


def frequency_bin_count(
    nperseg: int,
    freq_min: float,
    freq_max: float,
) -> int:
    freqs = np.fft.rfftfreq(nperseg)

    return int(
        np.sum(
            (freqs > freq_min)
            & (freqs < freq_max)
        )
    )


def finite_array(x):
    x = np.asarray(
        x,
        dtype=np.float64,
    )

    return (
        x.ndim == 1
        and len(x) > 0
        and np.all(np.isfinite(x))
    )


def evaluate_dataset(
    name: str,
    path: str,
    policy: dict,
    freq_min: float,
    freq_max: float,
):
    try:
        series = load_series(path)

        if not finite_array(series):
            return {
                "name": name,
                "path": path,
                "eligible_for_measurement": False,
                "eligible_for_replication": False,
                "status": "INELIGIBLE",
                "reason": "nonfinite_or_invalid_series",
            }

        n = int(len(series))

        minimum_measurement_length = int(
            policy.get(
                "minimum_series_length",
                256,
            )
        )

        canonical_nperseg = int(
            policy.get(
                "canonical_nperseg",
                CANONICAL_NPERSEG,
            )
        )

        minimum_bins = int(
            policy.get(
                "minimum_frequency_bins",
                CANONICAL_MIN_BINS,
            )
        )

        measurement_length_ok = (
            n >= minimum_measurement_length
        )

        # IMPORTANT:
        # A dataset shorter than the canonical Welch segmentation
        # must NOT silently become a replication dataset merely
        # because estimate_alpha() can adapt nperseg downward.
        #
        # Measurement validity and replication eligibility are
        # deliberately different concepts.
        replication_length_ok = (
            n >= canonical_nperseg
        )

        effective_nperseg = min(
            canonical_nperseg,
            n,
        )

        available_bins = frequency_bin_count(
            effective_nperseg,
            freq_min,
            freq_max,
        )

        bins_ok = (
            available_bins >= minimum_bins
        )

        eligible_for_measurement = bool(
            measurement_length_ok
            and bins_ok
        )

        eligible_for_replication = bool(
            eligible_for_measurement
            and replication_length_ok
        )

        if not measurement_length_ok:
            reason = (
                "series_shorter_than_measurement_minimum"
            )
        elif not replication_length_ok:
            reason = (
                "series_shorter_than_canonical_nperseg; "
                "adaptive nperseg is not allowed to establish "
                "replication eligibility"
            )
        elif not bins_ok:
            reason = (
                "insufficient_frequency_bins"
            )
        else:
            reason = "eligible"

        return {
            "name": name,
            "path": path,
            "series_length": n,
            "minimum_measurement_length":
                minimum_measurement_length,
            "canonical_nperseg":
                canonical_nperseg,
            "effective_nperseg":
                effective_nperseg,
            "frequency_band": [
                float(freq_min),
                float(freq_max),
            ],
            "frequency_bins":
                int(available_bins),
            "minimum_frequency_bins":
                minimum_bins,
            "measurement_length_ok":
                bool(measurement_length_ok),
            "replication_length_ok":
                bool(replication_length_ok),
            "frequency_bins_ok":
                bool(bins_ok),
            "eligible_for_measurement":
                eligible_for_measurement,
            "eligible_for_replication":
                eligible_for_replication,
            "status": (
                "ELIGIBLE"
                if eligible_for_replication
                else "MEASUREMENT_ONLY"
                if eligible_for_measurement
                else "INELIGIBLE"
            ),
            "reason": reason,
        }

    except Exception as exc:
        return {
            "name": name,
            "path": path,
            "eligible_for_measurement": False,
            "eligible_for_replication": False,
            "status": "ERROR",
            "reason": str(exc),
        }


def main():
    if not CLAIM_PATH.exists():
        raise SystemExit(
            f"Missing claim specification: {CLAIM_PATH}"
        )

    claim = json.loads(
        CLAIM_PATH.read_text(
            encoding="utf-8"
        )
    )

    if not PROVENANCE_PATH.exists():
        raise SystemExit(
            f"Missing replication provenance registry: "
            f"{PROVENANCE_PATH}"
        )

    provenance_registry = json.loads(
        PROVENANCE_PATH.read_text(
            encoding="utf-8"
        )
    )

    if provenance_registry.get(
        "protocol"
    ) != "REPLICATION_PROVENANCE_REGISTRY_V1":
        raise SystemExit(
            "❌ Unexpected replication provenance registry protocol."
        )

    provenance_candidates = provenance_registry.get(
        "candidates",
        {}
    )

    dataset_policy = claim.get(
        "dataset",
        {},
    ).get(
        "eligibility_policy",
        {},
    )

    frequency_resolution = claim.get(
        "method",
        {},
    ).get(
        "frequency_resolution",
        {},
    )

    frequency_band = (
        claim.get(
            "scale_validation",
            {},
        ).get(
            "base_frequency_band",
            [
                0.01,
                0.05,
            ],
        )
    )

    freq_min = float(
        frequency_band[0]
    )

    freq_max = float(
        frequency_band[1]
    )

    primary_dataset_name = str(
        claim.get(
            "dataset",
            {},
        ).get(
            "primary",
            "sunspots_full.csv",
        )
    )

    required_replication_domains = int(
        claim.get(
            "dataset",
            {},
        ).get(
            "independent_replication",
            {},
        ).get(
            "minimum_domains",
            2,
        )
    )

    results = []

    for name, path in DATASETS.items():

        # The primary dataset can never count as a
        # secondary independent replication domain.
        primary = (
            name == "sunspots"
            or path.endswith(
                primary_dataset_name
            )
        )

        # Derived/extended data also cannot count as
        # independent replication.
        derived = name in {
            "extended",
        }

        item = evaluate_dataset(
            name=name,
            path=path,
            policy=dataset_policy,
            freq_min=freq_min,
            freq_max=freq_max,
        )

        provenance = provenance_candidates.get(
            name
        )

        item["provenance_review"] = (
            provenance
            if provenance is not None
            else {
                "status": "MISSING",
                "replication_eligible": False,
                "reason": (
                    "Dataset is absent from the "
                    "replication provenance registry."
                ),
            }
        )

        provenance_eligible = bool(
            provenance is not None
            and provenance.get(
                "replication_eligible"
            ) is True
        )

        item["provenance_replication_eligible"] = (
            provenance_eligible
        )

        if (
            item.get("eligible_for_replication")
            is True
            and not provenance_eligible
        ):
            item["eligible_for_replication"] = False
            item["replication_exclusion_reason"] = (
                "dataset_passed_structural_eligibility_but_failed_"
                "replication_provenance_eligibility"
            )

        item["primary_domain"] = bool(
            primary
        )

        item["derived_domain"] = bool(
            derived
        )

        if primary:
            item["eligible_for_replication"] = False
            item["replication_exclusion_reason"] = (
                "primary_domain_excluded_from_secondary_replication_count"
            )

        elif derived:
            item["eligible_for_replication"] = False
            item["replication_exclusion_reason"] = (
                "derived_or_related_domain_excluded"
            )

        results.append(item)

    eligible_replication_domains = [
        item
        for item in results
        if (
            item.get(
                "eligible_for_replication"
            )
            is True
            and item.get(
                "provenance_replication_eligible"
            )
            is True
            and item.get(
                "primary_domain"
            )
            is False
            and item.get(
                "derived_domain"
            )
              is False
        )
    ]

    report = {
        "status": (
            "ELIGIBILITY_VALIDATED"
            if len(eligible_replication_domains)
            >= required_replication_domains
            else "REPLICATION_ELIGIBILITY_INSUFFICIENT"
        ),
        "scientific_claim_authority": False,
        "promotion_authority": False,
        "scientific_role": (
            "dataset measurement and replication "
            "eligibility enforcement"
        ),
        "frequency_band": [
            freq_min,
            freq_max,
        ],
        "canonical_nperseg": int(
            dataset_policy.get(
                "canonical_nperseg",
                CANONICAL_NPERSEG,
            )
        ),
        "minimum_frequency_bins": int(
            dataset_policy.get(
                "minimum_frequency_bins",
                CANONICAL_MIN_BINS,
            )
        ),
        "minimum_measurement_length": int(
            dataset_policy.get(
                "minimum_series_length",
                256,
            )
        ),
        "minimum_replication_domains":
            required_replication_domains,
        "eligible_replication_domains": [
            item["name"]
            for item in eligible_replication_domains
        ],
        "eligible_replication_domain_count":
            len(eligible_replication_domains),
        "domains": results,
        "interpretation": (
            "Measurement eligibility is distinct from "
            "scientific replication. A series shorter than "
            "the canonical Welch segmentation may be measured "
            "diagnostically when otherwise valid, but adaptive "
            "nperseg does not make it eligible to establish "
            "replication under the canonical protocol."
        ),
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "=== DATASET ELIGIBILITY GATE ==="
    )

    print(
        "Eligible replication domains:",
        len(eligible_replication_domains),
        "/",
        required_replication_domains,
    )

    print(
        "Status:",
        report["status"],
    )


if __name__ == "__main__":
    main()
