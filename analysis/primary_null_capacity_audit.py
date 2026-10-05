from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.appropriate_stochastic_null import (
    MAX_AR_ORDER,
    COMPARISON_HOLD_BACK,
    _simulate_from_fit,
    _stationary_fit,
)

from analysis.load_real_datasets import (
    load_series,
)

from analysis.numerical_spectral_verification import (
    estimate_alpha,
)


SEED = 90210
SURROGATES = 1000
MIN_VALID_SURROGATES = 200
BOUNDARY_THRESHOLD = 0.50

DATASET = Path(
    "real-data/sunspots_full.csv"
)

OUTPUT = Path(
    "artifacts/primary_null_capacity_audit.json"
)


def main() -> None:
    if COMPARISON_HOLD_BACK != MAX_AR_ORDER:
        raise SystemExit(
            "❌ Primary-null capacity audit requires "
            "fixed hold-back equal to max candidate order."
        )

    rng = np.random.default_rng(
        SEED
    )

    # IMPORTANT:
    # Use the repository's canonical dataset loader.
    # This preserves the declared sunspot signal column
    # and normalization semantics.
    x = load_series(
        DATASET
    )

    observed_alpha = float(
        estimate_alpha(x)
    )

    selected_order, fitted = (
        _stationary_fit(x)
    )

    selected_orders: list[int] = []
    surrogate_alphas: list[float] = []

    refit_failures = 0
    alpha_failures = 0

    for _ in range(
        SURROGATES
    ):
        surrogate = _simulate_from_fit(
            fitted,
            len(x),
            rng,
        )

        try:
            refit_order, refit = (
                _stationary_fit(
                    surrogate
                )
            )
        except Exception:
            refit_failures += 1
            continue

        # Count successful AR refits independently
        # of the spectral-alpha calculation.
        selected_orders.append(
            int(refit_order)
        )

        try:
            alpha = float(
                estimate_alpha(
                    surrogate
                )
            )
        except Exception:
            alpha_failures += 1
            continue

        if not np.isfinite(
            alpha
        ):
            alpha_failures += 1
            continue

        surrogate_alphas.append(
            alpha
        )

    valid_refits = len(
        selected_orders
    )

    if valid_refits < MIN_VALID_SURROGATES:
        raise SystemExit(
            "❌ Fewer than "
            f"{MIN_VALID_SURROGATES} valid surrogate "
            "AR refits are available."
        )

    orders = np.asarray(
        selected_orders,
        dtype=np.int64,
    )

    boundary_count = int(
        np.sum(
            orders == MAX_AR_ORDER
        )
    )

    boundary_fraction = float(
        boundary_count / valid_refits
    )

    review_reasons = []

    if (
        selected_order
        == MAX_AR_ORDER
    ):
        review_reasons.append(
            {
                "scope": "observed_fit",
                "reason":
                    "observed_order_at_declared_maximum",
                "selected_order":
                    int(selected_order),
                "max_order":
                    int(MAX_AR_ORDER),
            }
        )

    if (
        boundary_fraction
        >= BOUNDARY_THRESHOLD
    ):
        review_reasons.append(
            {
                "scope": "surrogate_refits",
                "reason":
                    "surrogate_boundary_fraction_exceeds_threshold",
                "boundary_fraction":
                    boundary_fraction,
                "threshold":
                    BOUNDARY_THRESHOLD,
            }
        )

    review_triggered = bool(
        review_reasons
    )

    alpha_array = np.asarray(
        surrogate_alphas,
        dtype=np.float64,
    )

    if len(alpha_array) > 0:
        surrogate_alpha_summary = {
            "valid_alpha_estimates":
                int(len(alpha_array)),
            "mean":
                float(
                    np.mean(
                        alpha_array
                    )
                ),
            "std":
                float(
                    np.std(
                        alpha_array,
                        ddof=1,
                    )
                )
                if len(alpha_array) > 1
                else 0.0,
            "median":
                float(
                    np.median(
                        alpha_array
                    )
                ),
            "minimum":
                float(
                    np.min(
                        alpha_array
                    )
                ),
            "maximum":
                float(
                    np.max(
                        alpha_array
                    )
                ),
        }
    else:
        surrogate_alpha_summary = {
            "valid_alpha_estimates": 0,
            "mean": None,
            "std": None,
            "median": None,
            "minimum": None,
            "maximum": None,
        }

    unique_orders, order_counts = (
        np.unique(
            orders,
            return_counts=True,
        )
    )

    order_distribution = {
        str(int(order)):
            int(count)
        for order, count
        in zip(
            unique_orders,
            order_counts,
        )
    }

    output = {
        "audit":
            "primary_sunspot_null_capacity_audit",

        "dataset":
            str(DATASET),

        "sample_size":
            int(len(x)),

        "loader":
            "analysis.load_real_datasets.load_series",

        "seed":
            SEED,

        "surrogates_requested":
            SURROGATES,

        "minimum_valid_surrogate_refits":
            MIN_VALID_SURROGATES,

        "valid_surrogate_refits":
            valid_refits,

        "protocol_revision":
            "ar_order_comparison_holdback_v1",

        "comparison_hold_back":
            int(COMPARISON_HOLD_BACK),

        "max_order":
            int(MAX_AR_ORDER),

        "same_effective_observations_required":
            True,

        "observed_alpha":
            observed_alpha,

        "observed_selected_order":
            int(selected_order),

        "observed_selected_at_boundary":
            bool(
                selected_order
                == MAX_AR_ORDER
            ),

        "surrogate_boundary_count":
            boundary_count,

        "surrogate_boundary_fraction":
            boundary_fraction,

        "boundary_fraction_threshold":
            BOUNDARY_THRESHOLD,

        "order_distribution":
            order_distribution,

        "review_triggered":
            review_triggered,

        "review_reasons":
            review_reasons,

        "surrogate_alpha_summary":
            surrogate_alpha_summary,

        "failures": {
            "refit_failures":
                int(refit_failures),
            "alpha_estimation_failures":
                int(alpha_failures),
        },

        "scientific_role":
            "diagnostic_only",

        "claim_support":
            False,

        "preregistered_confirmation":
            False,

        "does_not_change_primary_null":
            True,

        "does_not_support_claim":
            True,

        "does_not_falsify_claim":
            True,

        "interpretation":
            (
                "This audit evaluates the capacity behavior "
                "of the declared primary sunspot AR(p) null "
                "using the same fixed-hold-back implementation "
                "as the primary stochastic-null procedure. "
                "It is diagnostic-only. A boundary warning "
                "does not establish or falsify the scientific "
                "hypothesis. Passing known-process AR calibration "
                "does not establish adequacy of the primary "
                "sunspot stochastic null. Any future null-family "
                "change requires a separately justified and "
                "prospectively declared validation protocol."
            ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Primary-null capacity audit written:",
        OUTPUT,
    )

    print(
        "Observed selected order:",
        selected_order,
    )

    print(
        "Maximum declared order:",
        MAX_AR_ORDER,
    )

    print(
        "Surrogate boundary fraction:",
        f"{boundary_fraction:.6f}",
    )

    print(
        "Review triggered:",
        review_triggered,
    )

    print(
        "Valid surrogate refits:",
        valid_refits,
    )

    print(
        "Valid surrogate alpha estimates:",
        len(alpha_array),
    )


if __name__ == "__main__":
    main()
