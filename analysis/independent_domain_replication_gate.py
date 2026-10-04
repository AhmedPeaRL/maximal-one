from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.load_real_datasets import (
    DATASETS,
    load_series,
)

from analysis.numerical_spectral_verification import (
    estimate_alpha,
)

from analysis.appropriate_stochastic_null import (
    parametric_short_memory_null,
)


CLAIM_PATH = Path(
    "core-scientific/strict_claim.json"
)

OUTPUT = Path(
    "artifacts/independent_domain_replication_gate.json"
)

REQUIRED_DOMAINS = [
    "co2",
    "cosmic_rays",
]

TRIALS = 1000
BASE_SEED = 42000


def load_replication_policy():
    if not CLAIM_PATH.exists():
        raise SystemExit(
            f"Missing strict claim specification: {CLAIM_PATH}"
        )

    claim = json.loads(
        CLAIM_PATH.read_text(
            encoding="utf-8"
        )
    )

    dataset = claim.get(
        "dataset",
        {},
    )

    replication = dataset.get(
        "independent_replication",
        {},
    )

    eligibility = dataset.get(
        "eligibility_policy",
        {},
    )

    return {
        "minimum_domains": int(
            replication.get(
                "minimum_domains",
                2,
            )
        ),
        "measurement_minimum_length": int(
            eligibility.get(
                "minimum_series_length",
                256,
            )
        ),
        "replication_minimum_length": int(
            eligibility.get(
                "replication_minimum_series_length",
                1024,
            )
        ),
        "canonical_nperseg": int(
            eligibility.get(
                "canonical_nperseg",
                1024,
            )
        ),
    }


def finite(x):
    try:
        return bool(
            np.isfinite(
                float(x)
            )
        )
    except Exception:
        return False


def evaluate_domain(
    name,
    seed,
    policy,
):
    path = DATASETS[name]

    rows = 0

    try:
        x = load_series(
            path
        )

        rows = int(
            len(x)
        )

        if rows < policy["measurement_minimum_length"]:
            return {
                "name": name,
                "path": path,
                "rows": rows,
                "measurement_valid": False,
                "replication_eligible": False,
                "scientific_replication": False,
                "replication_status":
                    "INVALID_MEASUREMENT",
                "reason": (
                    "Series is shorter than the declared "
                    "measurement minimum."
                ),
            }

        if rows < policy["replication_minimum_length"]:
            return {
                "name": name,
                "path": path,
                "rows": rows,
                "measurement_valid": True,
                "replication_eligible": False,
                "scientific_replication": False,
                "replication_status":
                    "INELIGIBLE_REPLICATION_DOMAIN",
                "reason": (
                    "Measurement is available, but the series "
                    "is shorter than the declared replication "
                    "minimum. Adaptive nperseg does not override "
                    "replication eligibility."
                ),
            }

        alpha = estimate_alpha(
            x
        )

        if not finite(alpha):
            return {
                "name": name,
                "path": path,
                "rows": rows,
                "measurement_valid": False,
                "replication_eligible": False,
                "scientific_replication": False,
                "replication_status":
                    "INVALID_MEASUREMENT",
                "reason":
                    "canonical alpha is not finite",
            }

        rng = np.random.default_rng(
            seed
        )

        null_result = (
            parametric_short_memory_null(
                x,
                float(alpha),
                rng,
                trials=TRIALS,
            )
        )

        protocol_match = bool(
            null_result.get(
                "null_model"
            )
            ==
            "stationary_gaussian_ar_p_aic"
            and
            null_result.get(
                "test_endpoint"
            )
            ==
            "canonical_primary_alpha"
            and
            null_result.get(
                "alternative"
            )
            ==
            "greater_than_null"
            and
            null_result.get(
                "tail"
            )
            ==
            "upper"
            and
            null_result.get(
                "permutation_null_is_primary"
            )
            is False
        )

        null_rejected = bool(
            null_result.get(
                "reject_at_0_05"
            )
            is True
        )

        replication = bool(
            protocol_match
            and
            null_result.get(
                "valid"
            )
            is True
            and
            null_result.get(
                "support_eligible"
            )
            is True
            and
            null_rejected
        )

        return {
            "name": name,
            "path": path,
            "rows": rows,
            "alpha": float(alpha),

            "measurement_valid": True,
            "replication_eligible": True,

            "same_endpoint": bool(
                null_result.get(
                    "test_endpoint"
                )
                ==
                "canonical_primary_alpha"
            ),

            "same_null_family": bool(
                null_result.get(
                    "null_model"
                )
                ==
                "stationary_gaussian_ar_p_aic"
            ),

            "same_direction": bool(
                null_result.get(
                    "alternative"
                )
                ==
                "greater_than_null"
            ),

            "same_tail": bool(
                null_result.get(
                    "tail"
                )
                ==
                "upper"
            ),

            "domain_level_null_rejected":
                null_rejected,

            "scientific_replication":
                replication,

            "replication_status": (
                "REPLICATION_ESTABLISHED"
                if replication
                else "REPLICATION_NOT_ESTABLISHED"
            ),

            "null_result":
                null_result,

            "reason": (
                "Independent replication requires "
                "domain-level rejection of the same "
                "declared primary stochastic null "
                "using the same endpoint, direction, "
                "tail, and null family."
            ),
        }

    except Exception as exc:
        return {
            "name": name,
            "path": path,
            "rows": rows,
            "measurement_valid": False,
            "replication_eligible": False,
            "scientific_replication": False,
            "replication_status":
                "INVALID_MEASUREMENT",
            "reason": str(exc),
        }


def main():

    policy = load_replication_policy()

    required_domains = int(
        policy["minimum_domains"]
    )

    domains = []

    for index, name in enumerate(
        REQUIRED_DOMAINS
    ):
        domains.append(
            evaluate_domain(
                name,
                BASE_SEED + index,
                policy,
            )
        )

    passed = sum(
        1
        for item in domains
        if item.get(
            "scientific_replication"
        )
        is True
    )

    status = (
        "REPLICATION_ESTABLISHED"
        if passed >= required_domains
        else "REPLICATION_NOT_ESTABLISHED"
    )

    report = {
        "status": status,

        "scientific_claim_authority": False,
        "promotion_authority": False,

        "minimum_required":
            required_domains,

        "passed_independent_domains":
            passed,

        "required_protocol": {
            "null_model":
                "stationary_gaussian_ar_p_aic",
            "endpoint":
                "canonical_primary_alpha",
            "alternative":
                "greater_than_null",
            "tail":
                "upper",
            "trials":
                TRIALS,
        },

        "eligibility_policy": {
            "measurement_minimum_series_length":
                policy["measurement_minimum_length"],
            "replication_minimum_series_length":
                policy["replication_minimum_length"],
            "canonical_nperseg":
                policy["canonical_nperseg"],
            "measurement_validity_is_not_replication":
                True,
        },

        "domains":
            domains,

        "interpretation": (
            "A valid alpha measurement is not "
            "scientific replication. A replication-eligible "
            "domain is also not scientific replication until "
            "that domain independently rejects the same "
            "declared primary stochastic null under the "
            "same endpoint, direction, tail, and null family."
        ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "=== INDEPENDENT DOMAIN REPLICATION GATE ==="
    )

    print(
        "Measurement-valid independent domains:",
        sum(
            1
            for item in domains
            if item.get(
                "measurement_valid"
            )
                is True
        ),
    )

    print(
        "Replication-eligible independent domains:",
        sum(
            1
            for item in domains
            if item.get(
                "replication_eligible"
            )
                is True
        ),
    )

    print(
        "Scientific replications established:",
        passed,
        "/",
        required_domains,
    )

    print(
        "Measurement eligibility is not scientific replication."
    )

    print(
        "Replication eligibility is not scientific replication."
    )

    print(
        "Status:",
        status,
    )


if __name__ == "__main__":
    main()
