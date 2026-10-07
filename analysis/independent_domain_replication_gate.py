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

from analysis.null_protocol import (
    load_null_protocol,
)


CLAIM_PATH = Path(
    "core-scientific/strict_claim.json"
)

OUTPUT = Path(
    "artifacts/independent_domain_replication_gate.json"
)

TRIALS = 1000
BASE_SEED = 42000


PRIMARY_DOMAIN_NAMES = {
    "sunspots",
}

DERIVED_DOMAIN_NAMES = {
    "extended",
}

EXCLUDED_DOMAIN_NAMES = (
    PRIMARY_DOMAIN_NAMES
    | DERIVED_DOMAIN_NAMES
)


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

    null_protocol = load_null_protocol()

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

        "estimator_minimum_length": int(
            eligibility.get(
                "estimator_minimum_series_length",
                512,
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

        "null_protocol_id":
            null_protocol[
                "protocol_id"
            ],

        "null_model_id":
            null_protocol[
                "model_id"
            ],

        "null_family":
            null_protocol[
                "null_family"
            ],

        "null_endpoint":
            null_protocol[
                "endpoint"
            ],

        "null_direction":
            null_protocol[
                "direction"
            ],

        "null_tail":
            null_protocol[
                "tail"
            ],
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


def candidate_domain_names():

    names = []

    for name in sorted(DATASETS):

        if name in EXCLUDED_DOMAIN_NAMES:
            continue

        names.append(name)

    return names


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

        if rows < policy[
            "measurement_minimum_length"
        ]:

            return {
                "name": name,
                "path": path,
                "rows": rows,
                "measurement_valid": False,
                "estimator_valid": False,
                "replication_eligible": False,
                "scientific_replication": False,
                "replication_status":
                    "INVALID_MEASUREMENT",
                "reason":
                    "Series is shorter than the declared "
                    "measurement minimum.",
            }

        if rows < policy[
            "estimator_minimum_length"
        ]:

            return {
                "name": name,
                "path": path,
                "rows": rows,
                "measurement_valid": True,
                "estimator_valid": False,
                "replication_eligible": False,
                "scientific_replication": False,
                "replication_status":
                    "INELIGIBLE_ESTIMATOR_DOMAIN",
                "reason":
                    "Measurement exists, but the series "
                    "is shorter than the declared canonical "
                    "estimator minimum required to provide "
                    "the minimum frequency-bin resolution.",
            }

        if rows < policy[
            "replication_minimum_length"
        ]:

            return {
                "name": name,
                "path": path,
                "rows": rows,
                "measurement_valid": True,
                "estimator_valid": True,
                "replication_eligible": False,
                "scientific_replication": False,
                "replication_status":
                    "INELIGIBLE_REPLICATION_DOMAIN",
                "reason":
                    "Measurement and estimator validity "
                    "are available, but the series is shorter "
                    "than the declared replication minimum.",
            }

        alpha = estimate_alpha(
            x
        )

        if not finite(alpha):

            return {
                "name": name,
                "path": path,
                "rows": rows,
                "measurement_valid": True,
                "estimator_valid": False,
                "replication_eligible": False,
                "scientific_replication": False,
                "replication_status":
                    "INVALID_ESTIMATOR",
                "reason":
                    "Canonical alpha is not finite.",
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
            policy[
                "null_model_id"
            ]

            and

            null_result.get(
                "null_protocol_id"
            )
            ==
            policy[
                "null_protocol_id"
            ]

            and

            null_result.get(
                "test_endpoint"
            )
            ==
            policy[
                "null_endpoint"
            ]

            and

            null_result.get(
                "alternative"
            )
            ==
            policy[
                "null_direction"
            ]

            and

            null_result.get(
                "tail"
            )
            ==
            policy[
                "null_tail"
            ]

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

            "alpha":
                float(alpha),

            "measurement_valid":
                True,

            "estimator_valid":
                True,

            "replication_eligible":
                True,

            "same_endpoint":
                bool(
                    null_result.get(
                        "test_endpoint"
                    )
                    ==
                    "canonical_primary_alpha"
                ),

            "same_null_family":
                bool(
                    null_result.get(
                        "null_model"
                    )
                    ==
                    policy[
                        "null_protocol_id"
                    ]
                ),

            "same_direction":
                bool(
                    null_result.get(
                        "alternative"
                    )
                    ==
                    "greater_than_null"
                ),

            "same_tail":
                bool(
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

                else

                "REPLICATION_NOT_ESTABLISHED"
            ),

            "null_result":
                null_result,

            "reason":
                (
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

            "measurement_valid":
                False,

            "estimator_valid":
                False,

            "replication_eligible":
                False,

            "scientific_replication":
                False,

            "replication_status":
                "INVALID_MEASUREMENT",

            "reason":
                str(exc),
        }


def main():

    policy = load_replication_policy()

    required_domains = int(
        policy[
            "minimum_domains"
        ]
    )

    candidate_names = (
        candidate_domain_names()
    )

    domains = []

    for index, name in enumerate(
        candidate_names
    ):

        domains.append(
            evaluate_domain(
                name,
                BASE_SEED + index,
                policy,
            )
        )

    measurement_valid = sum(
        1
        for item in domains
        if item.get(
            "measurement_valid"
        )
        is True
    )

    estimator_valid = sum(
        1
        for item in domains
        if item.get(
            "estimator_valid"
        )
        is True
    )

    replication_eligible = sum(
        1
        for item in domains
        if item.get(
            "replication_eligible"
        )
        is True
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

        else

        "REPLICATION_NOT_ESTABLISHED"
    )

    report = {

        "status":
            status,

        "scientific_claim_authority":
            False,

        "promotion_authority":
            False,

        "minimum_required":
            required_domains,

        "candidate_domains":
            candidate_names,

        "measurement_valid_independent_domains":
            measurement_valid,

        "estimator_valid_independent_domains":
            estimator_valid,

        "replication_eligible_independent_domains":
            replication_eligible,

        "passed_independent_domains":
            passed,

        "required_protocol": {

            "protocol_id":
                policy[
                    "null_protocol_id"
                ],

            "model_id":
                policy[
                    "null_model_id"
                ],

            "null_family":
                policy[
                    "null_family"
                ],

            "endpoint":
                policy[
                    "null_endpoint"
                ],

            "alternative":
                policy[
                    "null_direction"
                ],

            "tail":
                policy[
                    "null_tail"
                ],

            "trials":
                TRIALS,
        },

        "eligibility_policy": {

            "measurement_minimum_series_length":
                policy[
                    "measurement_minimum_length"
                ],

            "estimator_minimum_series_length":
                policy[
                    "estimator_minimum_length"
                ],

            "replication_minimum_series_length":
                policy[
                    "replication_minimum_length"
                ],

            "canonical_nperseg":
                policy[
                    "canonical_nperseg"
                ],

            "measurement_validity_is_not_replication":
                True,

            "estimator_validity_is_not_replication":
                True,

            "eligibility_is_not_scientific_replication":
                True,
        },

        "domains":
            domains,

        "interpretation":
            (
                "Independent real domains are evaluated "
                "from the declared dataset registry after "
                "excluding primary and derived domains. "
                "Measurement validity, estimator validity, "
                "replication eligibility, and scientific "
                "replication are separate states. No domain "
                "is counted as scientific replication merely "
                "because it has a finite alpha or sufficient "
                "length."
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
        "Candidate independent domains:",
        len(candidate_names),
    )

    print(
        "Measurement-valid independent domains:",
        measurement_valid,
    )

    print(
        "Estimator-valid independent domains:",
        estimator_valid,
    )

    print(
        "Replication-eligible independent domains:",
        replication_eligible,
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
        "Estimator eligibility is not scientific replication."
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
