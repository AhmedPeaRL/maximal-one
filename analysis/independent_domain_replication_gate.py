from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.load_real_datasets import (
    DATASETS,
    load_series
)

from analysis.numerical_spectral_verification import (
    estimate_alpha
)

from analysis.appropriate_stochastic_null import (
    parametric_short_memory_null
)


OUTPUT = Path(
    "artifacts/independent_domain_replication_gate.json"
)

REQUIRED_DOMAINS = [
    "co2",
    "cosmic_rays"
]

MIN_REQUIRED = 2
TRIALS = 1000
BASE_SEED = 42000


def finite(x):
    try:
        return bool(
            np.isfinite(float(x))
        )
    except Exception:
        return False


def evaluate_domain(
    name,
    seed
):
    path = DATASETS[name]

    try:
        x = load_series(path)

        alpha = estimate_alpha(x)

        if not finite(alpha):
            return {
                "name": name,
                "path": path,
                "measurement_valid": False,
                "scientific_replication": False,
                "replication_status":
                    "INVALID_MEASUREMENT",
                "reason":
                    "canonical alpha is not finite"
            }

        rng = np.random.default_rng(
            seed
        )

        null_result = (
            parametric_short_memory_null(
                x,
                float(alpha),
                rng,
                trials=TRIALS
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
            ) is True
        )

        replication = bool(
            protocol_match
            and
            null_result.get(
                "valid"
            ) is True
            and
            null_result.get(
                "support_eligible"
            ) is True
            and
            null_rejected
        )

        return {
            "name": name,
            "path": path,
            "rows": int(len(x)),
            "alpha": float(alpha),
            "measurement_valid": True,

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

            "null_result": null_result,

            "reason": (
                "Independent replication requires "
                "domain-level rejection of the same "
                "declared primary stochastic null "
                "using the same endpoint, direction, "
                "tail, and null family."
            )
        }

    except Exception as exc:
        return {
            "name": name,
            "path": path,
            "measurement_valid": False,
            "scientific_replication": False,
            "replication_status":
                "INVALID_MEASUREMENT",
            "reason": str(exc)
        }


def main():
    domains = []

    for index, name in enumerate(
        REQUIRED_DOMAINS
    ):
        domains.append(
            evaluate_domain(
                name,
                BASE_SEED + index
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
        if passed >= MIN_REQUIRED
        else "REPLICATION_NOT_ESTABLISHED"
    )

    report = {
        "status": status,

        "scientific_claim_authority": False,
        "promotion_authority": False,

        "minimum_required":
            MIN_REQUIRED,

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
                TRIALS
        },

        "domains": domains,

        "interpretation": (
            "A valid alpha measurement is not "
            "scientific replication. Each independent "
            "real domain must independently reject the "
            "same declared primary stochastic null "
            "under the same endpoint and direction."
        )
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True
        ) + "\n",
        encoding="utf-8"
    )

    print(
        "=== INDEPENDENT DOMAIN REPLICATION GATE ==="
    )

    print(
        "Passed:",
        passed,
        "/",
        MIN_REQUIRED
    )

    print(
        "Status:",
        status
    )


if __name__ == "__main__":
    main()
