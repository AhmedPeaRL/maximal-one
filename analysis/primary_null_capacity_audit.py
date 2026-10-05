from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.appropriate_stochastic_null import (
    MAX_AR_ORDER,
    COMPARISON_HOLD_BACK,
    _as_series,
    _simulate_from_fit,
    _stationary_fit,
)

from analysis.numerical_spectral_verification import (
    estimate_alpha,
)


SEED = 90210
SURROGATES = 1000
BOUNDARY_THRESHOLD = 0.50

DATASET = Path(
    "real-data/sunspots_full.csv"
)

OUTPUT = Path(
    "artifacts/primary_null_capacity_audit.json"
)


def load_series(path: Path) -> np.ndarray:
    data = np.loadtxt(
        path,
        delimiter=",",
        skiprows=1,
    )

    if data.ndim == 1:
        series = data
    else:
        series = data[:, -1]

    return _as_series(series)


def main() -> None:
    rng = np.random.default_rng(
        SEED
    )

    x = load_series(
        DATASET
    )

    observed_alpha = float(
        estimate_alpha(x)
    )

    selected_order, fitted = (
        _stationary_fit(x)
    )

    selected_orders = []
    surrogate_alphas = []

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
            refit_order, _ = (
                _stationary_fit(
                    surrogate
                )
            )
        except Exception:
            refit_failures += 1
            continue

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

        selected_orders.append(
            int(refit_order)
        )

        surrogate_alphas.append(
            alpha
        )

    valid = len(
        selected_orders
    )

    if valid == 0:
        raise SystemExit(
            "❌ No valid surrogate refits."
        )

    orders = np.asarray(
        selected_orders,
        dtype=np.int64,
    )

    alphas = np.asarray(
        surrogate_alphas,
        dtype=np.float64,
    )

    boundary_count = int(
        np.sum(
            orders == MAX_AR_ORDER
        )
    )

    boundary_fraction = float(
        boundary_count / valid
    )

    review_triggered = bool(
        boundary_fraction
        >= BOUNDARY_THRESHOLD
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

    if review_triggered:
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

    output = {
        "audit":
            "primary_sunspot_null_capacity_audit",

        "dataset":
            str(DATASET),

        "sample_size":
            int(len(x)),

        "seed":
            SEED,

        "surrogates_requested":
            SURROGATES,

        "valid_surrogate_refits":
            valid,

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

        "review_triggered":
            review_triggered,

        "review_reasons":
            review_reasons,

        "surrogate_alpha_summary": {
            "mean":
                float(
                    np.mean(
                        alphas
                    )
                ),
            "std":
                float(
                    np.std(
                        alphas,
                        ddof=1,
                    )
                ),
            "median":
                float(
                    np.median(
                        alphas
                    )
                ),
            "minimum":
                float(
                    np.min(
                        alphas
                    )
                ),
            "maximum":
                float(
                    np.max(
                        alphas
                    )
                ),
        },

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
                "This audit evaluates capacity behavior of the "
                "declared primary sunspot AR(p) null using the "
                "same fixed-hold-back implementation as the "
                "primary stochastic-null procedure. It is "
                "diagnostic-only. A boundary warning does not "
                "establish or falsify the scientific hypothesis. "
                "Passing calibration on known AR processes does "
                "not establish adequacy of the primary sunspot "
                "null."
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
        valid,
    )


if __name__ == "__main__":
    main()
