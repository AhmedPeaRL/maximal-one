from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.load_real_datasets import DATASETS, load_series
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.appropriate_stochastic_null import (
    parametric_short_memory_null,
)

OUTPUT = Path(
    "artifacts/independent_domain_replication_gate.json"
)

REQUIRED_DOMAINS = [
    "co2",
    "cosmic_rays",
]

MIN_REQUIRED = 2
TRIALS = 1000
SEED_BASE = 420000

def finite(x):
    try:
        return bool(np.isfinite(float(x)))
    except Exception:
        return False

def calibration_is_valid():
    path = Path(
        "artifacts/null_calibration_gate.json"
    )

    if not path.exists():
        return False

    data = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    return (
        data.get("status")
        == "CALIBRATION_NOT_REJECTED"
    )

def evaluate_domain(name, seed):
    path = DATASETS[name]

    try:
        x = load_series(path)

        alpha = estimate_alpha(x)

        if not finite(alpha):
            return {
                "name": name,
                "path": path,
                "rows": int(len(x)),
                "alpha": None,
                "measurement_valid": False,
                "scientific_replication": False,
                "replication_status":
                    "INVALID_MEASUREMENT",
                "reason":
                    "non-finite canonical alpha",
            }

        if not calibration_is_valid():
            return {
                "name": name,
                "path": path,
                "rows": int(len(x)),
                "alpha": float(alpha),
                "measurement_valid": True,
                "scientific_replication": False,
                "replication_status":
                    "BLOCKED_BY_NULL_CALIBRATION",
                "reason":
                    "The shared stochastic-null family has "
                    "not yet passed the calibration gate. "
                    "No domain may be promoted to scientific "
                    "replication before that gate passes.",
            }

        result = parametric_short_memory_null(
            x,
            float(alpha),
            np.random.default_rng(seed),
            trials=TRIALS,
        )

        rejected = bool(
            result.get("reject_at_0_05") is True
        )

        return {
            "name": name,
            "path": path,
            "rows": int(len(x)),
            "alpha": float(alpha),
            "measurement_valid": True,

            "null_family":
                "stationary_gaussian_AR_p_AIC",

            "endpoint":
                "canonical_primary_alpha",

            "direction":
                "greater_than_null",

            "p_value":
                result.get(
                    "p_value_mc_add_one"
                ),

            "null_rejected":
                rejected,

            "selected_order":
                result.get(
                    "selected_order"
                ),

            "surrogate_boundary_fraction":
                result.get(
                    "order_selection_diagnostic",
                    {},
                ).get(
                    "surrogate_boundary_fraction"
                ),

            "scientific_replication":
                rejected,

            "replication_status":
                (
                    "REPLICATED"
                    if rejected
                    else "NOT_REPLICATED"
                ),

            "reason":
                (
                    "Same endpoint, direction, and declared "
                    "stochastic-null family independently rejected."
                    if rejected
                    else "Domain did not independently reject "
                         "the same declared stochastic null."
                ),
        }

    except Exception as exc:
        return {
            "name": name,
            "path": path,
            "rows": None,
            "alpha": None,
            "measurement_valid": False,
            "scientific_replication": False,
            "replication_status":
                "INVALID_MEASUREMENT",
            "reason": str(exc),
        }

def main():
    calibration_valid = calibration_is_valid()

    domains = [
        evaluate_domain(
            name,
            SEED_BASE + i,
        )
        for i, name in enumerate(
            REQUIRED_DOMAINS
        )
    ]

    passed = sum(
        1
        for item in domains
        if item["scientific_replication"] is True
    )

    status = (
        "REPLICATION_ESTABLISHED"
        if (
            calibration_valid
            and passed >= MIN_REQUIRED
        )
        else "REPLICATION_NOT_ESTABLISHED"
    )

    report = {
        "status": status,
        "scientific_claim_authority": False,
        "minimum_required": MIN_REQUIRED,
        "passed_independent_domains": passed,

        "protocol": {
            "same_endpoint_required": True,
            "same_null_family_required": True,
            "same_direction_required": True,
            "domain_level_null_rejection_required": True,
            "measurement_validity_is_not_replication": True,
            "derived_domains_excluded": True,
            "null_domains_excluded": True,
            "synthetic_domains_excluded": True,
        },

        "null_calibration_valid":
            calibration_valid,

        "domains": domains,

        "interpretation": (
            "Independent real-domain replication requires "
            "independent rejection of the same declared "
            "primary stochastic null under the same endpoint "
            "and direction. A finite alpha, method agreement, "
            "or cross-domain similarity alone is never counted "
            "as replication."
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
        ) + "\n",
        encoding="utf-8",
    )

    print(
        "=== INDEPENDENT DOMAIN REPLICATION GATE ==="
    )

    print(
        "Null calibration valid:",
        calibration_valid,
    )

    print(
        "Passed independent domains:",
        passed,
    )

    print(
        "Required:",
        MIN_REQUIRED,
    )

    print(
        "Status:",
        status,
    )

    print(
        "Saved:",
        OUTPUT,
    )

if __name__ == "__main__":
    main()
