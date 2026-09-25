from __future__ import annotations

import numpy as np
from statsmodels.tsa.ar_model import AutoReg

from analysis.numerical_spectral_verification import estimate_alpha

MAX_AR_ORDER = 20
MIN_AR_ORDER = 1
BURN_IN = 1000
MIN_VALID_SURROGATES = 200

def _as_series(series):
    x = np.asarray(series, dtype=np.float64)

    if x.ndim != 1:
        raise ValueError("series must be one-dimensional")

    if len(x) < 256:
        raise ValueError(
            "series too short for stochastic-null inference"
        )

    if not np.all(np.isfinite(x)):
        raise ValueError(
            "series contains non-finite values"
        )

    return x

def _stationary_fit(series):
    x = _as_series(series)
    candidates = []

    max_order = min(
        MAX_AR_ORDER,
        max(MIN_AR_ORDER, len(x) // 10)
    )

    for order in range(
        MIN_AR_ORDER,
        max_order + 1
    ):
        try:
            fit = AutoReg(
                x,
                lags=order,
                trend="c",
                old_names=False,
            ).fit()
        except Exception:
            continue

        roots = np.asarray(
            fit.roots,
            dtype=np.complex128
        )

        if (
            roots.size != order
            or not np.all(np.abs(roots) > 1.0)
        ):
            continue

        if not np.isfinite(float(fit.aic)):
            continue

        candidates.append(
            (float(fit.aic), order, fit)
        )

    if not candidates:
        raise RuntimeError(
            "no stationary AR(p) candidate could be fitted"
        )

    _, order, fit = min(
        candidates,
        key=lambda item: item[0]
    )

    return order, fit

def _simulate_from_fit(
    fit,
    n,
    rng,
    burn_in=BURN_IN,
):
    params = np.asarray(
        fit.params,
        dtype=np.float64
    )

    order = int(
        fit.model._maxlag
    )

    intercept = float(
        params[0]
    )

    phi = np.asarray(
        params[1:1 + order],
        dtype=np.float64
    )

    sigma = float(
        np.sqrt(fit.sigma2)
    )

    total = int(n) + int(burn_in)

    eps = rng.normal(
        0.0,
        sigma,
        total
    )

    x = np.zeros(
        total,
        dtype=np.float64
    )

    denom = (
        1.0
        -
        float(np.sum(phi))
    )

    initial = (
        intercept / denom
        if abs(denom) > 1e-8
        else 0.0
    )

    x[:order] = initial

    for i in range(
        order,
        total
    ):
        x[i] = (
            intercept
            +
            np.dot(
                phi,
                x[i - order:i][::-1]
            )
            +
            eps[i]
        )

    return x[burn_in:]

def parametric_short_memory_null(
    series,
    observed_alpha,
    rng,
    trials=1000,
):
    x = _as_series(series)

    observed_alpha = float(
        observed_alpha
    )

    trials = int(trials)

    if not np.isfinite(
        observed_alpha
    ):
        raise ValueError(
            "observed_alpha must be finite"
        )

    if trials < MIN_VALID_SURROGATES:
        raise ValueError(
            f"trials must be >= "
            f"{MIN_VALID_SURROGATES}"
        )

    selected_order, fitted = (
        _stationary_fit(x)
    )

    null_alphas = []
    selected_orders = []

    for _ in range(trials):

        surrogate = _simulate_from_fit(
            fitted,
            len(x),
            rng
        )

        try:
            refit_order, _ = (
                _stationary_fit(
                    surrogate
                )
            )

            alpha = estimate_alpha(
                surrogate
            )

        except Exception:
            continue

        if np.isfinite(alpha):
            null_alphas.append(
                float(alpha)
            )

            selected_orders.append(
                int(refit_order)
            )

    null = np.asarray(
        null_alphas,
        dtype=np.float64
    )

    valid = int(
        null.size
    )

    if valid < MIN_VALID_SURROGATES:
        return {
            "valid": False,
            "reason":
                "insufficient_valid_surrogates",
            "scientific_role":
                "primary_stochastic_null_gate",
            "support_eligible": False,
            "null_model":
                "stationary_gaussian_ar_p_aic",
            "selected_order":
                int(selected_order),
            "max_order":
                int(MAX_AR_ORDER),
            "trials_requested":
                int(trials),
            "null_samples":
                valid,
            "observed_alpha":
                observed_alpha,
        }

    exceedances = int(
        np.sum(
            null >= observed_alpha
        )
    )

    p_value = float(
        (exceedances + 1)
        /
        (valid + 1)
    )

    return {
        "valid": True,
        "scientific_role":
            "primary_stochastic_null_gate",
        "support_eligible": True,
        "null_model":
            "stationary_gaussian_ar_p_aic",
        "null_hypothesis":
            "the observed series is adequately "
            "represented by a finite-order stationary "
            "short-memory Gaussian AR(p) process, "
            "with p selected by AIC over 1..20",
        "selection_rule": {
            "criterion": "AIC",
            "min_order":
                int(MIN_AR_ORDER),
            "max_order":
                int(MAX_AR_ORDER),
            "trend": "constant",
            "stationarity_required":
                True,
        },
        "selected_order":
            int(selected_order),
        "trials_requested":
            int(trials),
        "null_samples":
            valid,
        "exceedances":
            exceedances,
        "p_value_mc_add_one":
            p_value,
        "observed_alpha":
            observed_alpha,
        "null_mean":
            float(np.mean(null)),
        "null_median":
            float(np.median(null)),
        "null_std":
            float(
                np.std(
                    null,
                    ddof=1
                )
            ),
        "null_q05":
            float(
                np.quantile(
                    null,
                    0.05
                )
            ),
        "null_q50":
            float(
                np.quantile(
                    null,
                    0.50
                )
            ),
        "null_q95":
            float(
                np.quantile(
                    null,
                    0.95
                )
            ),
        "selected_order_median":
            float(
                np.median(
                    selected_orders
                )
            ),
        "selected_order_max":
            int(
                np.max(
                    selected_orders
                )
            ),
        "reject_at_0_05":
            bool(
                p_value <= 0.05
            ),
        "permutation_null_is_primary":
            False,
    }
