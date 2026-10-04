from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.appropriate_stochastic_null import (
    _simulate_from_fit,
    _stationary_fit,
)

from analysis.numerical_spectral_verification import (
    estimate_alpha,
)


AUDIT_SEED = 90210

OUTER_REPLICATES = 50

INNER_SURROGATES = 200

BURN_IN = 2000

ALPHA_THRESHOLD = 0.05

MIN_VALID_SURROGATES = 200


AR_CASES = {
    "ar1_phi_0_7": [0.7],
    "ar2_phi_0_5_0_2": [0.5, 0.2],
}

def generate_ar_process(
    phi,
    n,
    rng,
    burn_in=BURN_IN,
):
    phi = np.asarray(
        phi,
        dtype=np.float64,
    )

    order = len(phi)

    total = (
        int(n)
        + int(burn_in)
    )

    innovations = rng.standard_normal(
        total
    )

    x = np.zeros(
        total,
        dtype=np.float64,
    )

    for i in range(
        order,
        total,
    ):
        x[i] = (
            np.dot(
                phi,
                x[
                    i - order:i
                ][::-1],
            )
            + innovations[i]
        )

    return x[burn_in:]

def summarize_orders(orders):
    orders = np.asarray(
        orders,
        dtype=np.int64,
    )

    if orders.size == 0:
        return {
            "count": 0,
            "median": None,
            "max": None,
            "boundary_fraction": None,
        }

    return {
        "count": int(orders.size),
        "median": float(
            np.median(orders)
        ),
        "max": int(
            np.max(orders)
        ),
        "boundary_fraction": float(
            np.mean(orders == 20)
        ),
    }

def summarize_p_values(p_values):
    values = np.asarray(
        p_values,
        dtype=np.float64,
    )

    values = values[
        np.isfinite(values)
    ]

    if values.size == 0:
        return {
            "count": 0,
            "q01": None,
            "q05": None,
            "q10": None,
            "q25": None,
            "q50": None,
            "q75": None,
            "q90": None,
            "q95": None,
            "q99": None,
        }

    return {
        "count": int(values.size),
        "q01": float(np.quantile(values, 0.01)),
        "q05": float(np.quantile(values, 0.05)),
        "q10": float(np.quantile(values, 0.10)),
        "q25": float(np.quantile(values, 0.25)),
        "q50": float(np.quantile(values, 0.50)),
        "q75": float(np.quantile(values, 0.75)),
        "q90": float(np.quantile(values, 0.90)),
        "q95": float(np.quantile(values, 0.95)),
        "q99": float(np.quantile(values, 0.99)),
    }

def run_case(
    name,
    phi,
    rng,
):
    observed_alphas = []
    fitted_orders = []
    surrogate_orders = []
    outer_failures = []

    for outer_index in range(
        OUTER_REPLICATES
    ):
        series = generate_ar_process(
            phi,
            n=3328,
            rng=rng,
        )

        observed_alpha = estimate_alpha(
            series
        )

        if not np.isfinite(
            observed_alpha
        ):
            outer_failures.append({
                "outer_index": outer_index,
                "reason": "nonfinite_observed_alpha",
            })
            continue

        try:
            selected_order, fitted = (
                _stationary_fit(series)
            )
        except Exception as exc:
            outer_failures.append({
                "outer_index": outer_index,
                "reason": "observed_fit_failure",
                "error": str(exc),
            })
            continue

        fitted_orders.append(
            int(selected_order)
        )

        null_alphas = []
        surrogate_failure_count = 0

        for surrogate_index in range(
            INNER_SURROGATES
        ):
            try:
                surrogate = _simulate_from_fit(
                    fitted,
                    len(series),
                    rng,
                )

                refit_order, _ = (
                    _stationary_fit(
                        surrogate
                    )
                )

                alpha = estimate_alpha(
                    surrogate
                )

                if not np.isfinite(alpha):
                    surrogate_failure_count += 1
                    continue

                null_alphas.append(
                    float(alpha)
                )

                surrogate_orders.append(
                    int(refit_order)
                )

            except Exception:
                surrogate_failure_count += 1

        if len(null_alphas) < MIN_VALID_SURROGATES:
            outer_failures.append({
                "outer_index": outer_index,
                "reason": (
                    "insufficient_valid_surrogates"
                ),
                "valid_surrogates": int(
                    len(null_alphas)
                ),
                "requested_surrogates": int(
                    INNER_SURROGATES
                ),
                "minimum_valid_surrogates": int(
                    MIN_VALID_SURROGATES
                ),
                "surrogate_failures": int(
                    surrogate_failure_count
                ),
            })
            continue

        null = np.asarray(
            null_alphas,
            dtype=np.float64,
        )

        exceedances = int(
            np.sum(
                null >= observed_alpha
            )
        )

        p_value = (
            exceedances + 1
        ) / (
            len(null) + 1
        )

        observed_alphas.append(
            {
                "outer_index": int(
                    outer_index
                ),
                "alpha": float(
                    observed_alpha
                ),
                "p_value": float(
                    p_value
                ),
                "valid_surrogates": int(
                    len(null)
                ),
                "surrogate_failures": int(
                    surrogate_failure_count
                ),
            }
        )

    p_values = [
        item["p_value"]
        for item in observed_alphas
    ]

    rejection_rate = (
        float(
            np.mean(
                np.asarray(p_values)
                <= 0.05
            )
        )
        if p_values
        else None
    )

    requested = int(
        OUTER_REPLICATES
    )

    valid = int(
        len(observed_alphas)
    )

    failed = int(
        len(outer_failures)
    )

    failure_rate = (
        float(failed / requested)
        if requested
        else None
    )

    return {
        "case": name,
        "phi": list(
            map(float, phi)
        ),
        "outer_replicates_requested":
            requested,
        "outer_replicates_valid":
            valid,
        "outer_replicates_failed":
            failed,
        "outer_replicate_failure_rate":
            failure_rate,
        "inner_surrogates_requested":
            int(INNER_SURROGATES),
        "minimum_valid_surrogates":
            int(MIN_VALID_SURROGATES),
        "observed_results":
            observed_alphas,
        "outer_failures":
            outer_failures,
        "rejection_rate_at_0_05":
            rejection_rate,
        "fitted_order_summary":
            summarize_orders(
                fitted_orders
            ),
        "surrogate_order_summary":
            summarize_orders(
                surrogate_orders
            ),
        "scientific_role":
            "null_calibration_audit_only",
        "claim_support":
            False,
        "interpretation":
            "This audit evaluates calibration behavior "
            "of the declared stochastic-null procedure "
            "on data generated from known stationary "
            "AR processes. It does not establish or "
            "refute the scientific claim.",
    }

def main():
    rng = np.random.default_rng(
        AUDIT_SEED
    )

    results = []

    for name, phi in AR_CASES.items():
        results.append(
            run_case(
                name,
                phi,
                rng,
            )
        )

    required_outer_replicates = int(
        OUTER_REPLICATES
    )

    BOUNDARY_FRACTION_REVIEW_THRESHOLD = 0.50

    review_reasons = []

    for result in results:
        valid_outer = int(
            result.get(
                "outer_replicates_valid",
                0
            )
        )

        if valid_outer < required_outer_replicates:
            review_reasons.append(
                {
                    "case": result.get("case"),
                    "reason": "insufficient_valid_outer_replicates",
                    "outer_replicates_valid": valid_outer,
                    "outer_replicates_required":
                    required_outer_replicates,
                }
            )

        fitted_boundary = (
            result.get(
                "fitted_order_summary",
                {}
            ).get(
                "boundary_fraction"
            )
        )

        surrogate_boundary = (
            result.get(
                "surrogate_order_summary",
                {}
            ).get(
                "boundary_fraction"
            )
        )

        if (
            fitted_boundary is not None
            and float(fitted_boundary)
            >= BOUNDARY_FRACTION_REVIEW_THRESHOLD
        ):
            review_reasons.append(
                {
                    "case": result.get("case"),
                    "reason": "observed_fit_boundary_fraction_exceeds_review_threshold",
                    "boundary_fraction":
                        float(fitted_boundary),
                    "threshold":
                        BOUNDARY_FRACTION_REVIEW_THRESHOLD,
                }
            )

        if (
            surrogate_boundary is not None
            and float(surrogate_boundary)
            >= BOUNDARY_FRACTION_REVIEW_THRESHOLD
        ):
            review_reasons.append(
                {
                    "case": result.get("case"),
                    "reason": "surrogate_boundary_fraction_exceeds_review_threshold",
                    "boundary_fraction":
                        float(surrogate_boundary),
                    "threshold":
                        BOUNDARY_FRACTION_REVIEW_THRESHOLD,
                }
            )

    calibration_review_required = bool(
        review_reasons
    )

    output = {
        "audit": "stationary_ar_null_calibration",
        "seed": AUDIT_SEED,
        "outer_replicates_requested":
            required_outer_replicates,
        "inner_surrogates_requested":
            INNER_SURROGATES,
        "minimum_valid_surrogates":
            MIN_VALID_SURROGATES,
        "results": results,
        "calibration_review_required":
            calibration_review_required,

        "model_capacity_review": {
            "boundary_fraction_threshold":
                BOUNDARY_FRACTION_REVIEW_THRESHOLD,
            "review_triggered":
                bool(calibration_review_required),
            "review_reasons":
                review_reasons,
            "scientific_role":
                "diagnostic_only",
            "claim_support":
                False,
            "interpretation":
                (
                    "A high boundary fraction indicates that the declared "
                    "AR order range may be capacity-limited. This triggers "
                    "model-capacity review but does not itself establish "
                    "or falsify the scientific hypothesis."
                ),
        },
        
        "scientific_role":
            "diagnostic_only",
        "claim_support":
            False,
        "interpretation":
            (
                "Calibration diagnostics only. "
                "Any failed outer replicate is explicitly "
                "reported. Insufficient valid outer replicates "
                "block confirmation use but do not falsify "
                "the scientific hypothesis."
            ),
    }

    path = Path(
        "artifacts/null_calibration_audit.json"
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    print(
        "Null calibration audit written:"
    )

    print(
        path
    )

if __name__ == "__main__":
    main()
