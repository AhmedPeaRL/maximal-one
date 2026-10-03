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

    for _ in range(
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
            continue

        selected_order, fitted = (
            _stationary_fit(series)
        )

        fitted_orders.append(
            int(selected_order)
        )

        null_alphas = []

        for _ in range(
            INNER_SURROGATES
        ):
            surrogate = _simulate_from_fit(
                fitted,
                len(series),
                rng,
            )

            try:
                refit_order, _ = (
                    _stationary_fit(
                        surrogate
                    )
                )
            except Exception:
                continue

            alpha = estimate_alpha(
                surrogate
            )

            if not np.isfinite(alpha):
                continue

            null_alphas.append(
                float(alpha)
            )

            surrogate_orders.append(
                int(refit_order)
            )

        if len(null_alphas) < MIN_VALID_SURROGATES:
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
                "alpha": float(
                    observed_alpha
                ),
                "p_value": float(
                    p_value
                ),
                "valid_surrogates": int(
                    len(null)
                ),
            }
        )

    p_values = [
        item["p_value"]
        for item in observed_alphas
    ]

    p_summary = summarize_p_values(
        p_values
    )

    rejection_rate = (
        float(
            np.mean(
                np.asarray(p_values)
                <= ALPHA_THRESHOLD
            )
        )
        if p_values
        else None
    )

    return {
        "case": name,

        "phi": list(
            map(float, phi)
        ),

        "outer_replicates_requested":
            OUTER_REPLICATES,

        "outer_replicates_valid":
            len(observed_alphas),

        "inner_surrogates_requested":
            INNER_SURROGATES,

        "minimum_valid_surrogates":
            MIN_VALID_SURROGATES,

        "alpha_threshold":
            ALPHA_THRESHOLD,

        "observed_results":
            observed_alphas,

        "p_value_summary":
            p_summary,

        "rejection_rate_at_0_05":
            rejection_rate,

        "calibration_dataset":
            "synthetic_declared_ar_dgp",

        "null_family":
            "stationary_gaussian_AR_p",

        "selection_rule":
            "AIC_1_to_20",

        "boundary_rate":
            (
                float(
                    np.mean(
                        np.asarray(
                            surrogate_orders
                        )
                        == 20
                    )
                )
                if surrogate_orders
                else None
            ),

        "outer_replicates_failed":
            (
                OUTER_REPLICATES
                - len(observed_alphas)
            ),

        "outer_replicate_failure_rate":
            (
                float(
                    (
                        OUTER_REPLICATES
                        - len(observed_alphas)
                    )
                    / OUTER_REPLICATES
                )
            ),

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

        "decision":
            "CALIBRATION_REQUIRES_REVIEW",

        "interpretation":
            (
                "This audit evaluates calibration behavior "
                "of the declared stochastic-null procedure "
                "on data generated from known stationary "
                "AR processes. It does not establish or "
                "refute the scientific claim."
            ),
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

    output = {
        "audit":
            "stationary_ar_null_calibration",

        "protocol_version":
            "1.1",

        "seed":
            AUDIT_SEED,

        "max_ar_order":
            20,

        "outer_replicates":
            OUTER_REPLICATES,

        "inner_surrogates":
            INNER_SURROGATES,

        "alpha_threshold":
            ALPHA_THRESHOLD,

        "results":
            results,

        "scientific_role":
            "diagnostic_only",

        "claim_support":
            False,

        "promotion_authority":
            False,

        "interpretation":
            (
                "Calibration diagnostics only. "
                "No result from this audit may promote "
                "the scientific claim. Calibration failure "
                "blocks use of the tested procedure for "
                "future confirmation but does not falsify "
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
