from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from statsmodels.tsa.ar_model import AutoReg
from statsmodels.stats.diagnostic import acorr_ljungbox


PRIMARY_PATH = Path(
    "real-data/sunspots_full.csv"
)

ORDER_CAPS = [
    20,
    40,
    60,
]

# Use one common estimation sample for all candidate orders
# and all capacity caps in this diagnostic.
COMMON_HOLD_BACK = max(ORDER_CAPS)

LJUNG_BOX_LAGS = [
    10,
    20,
    40,
]

HASH_DECIMAL_PLACES = 10


def canonical_float(value):
    return float(
        np.round(
            float(value),
            HASH_DECIMAL_PLACES,
        )
    )


def load_primary():
    df = pd.read_csv(
        PRIMARY_PATH,
        sep=";",
        header=None,
        engine="python",
    )

    if df.shape[1] < 4:
        raise SystemExit(
            "Primary dataset has fewer than four columns."
        )

    x = pd.to_numeric(
        df.iloc[:, 3],
        errors="coerce",
    ).dropna().to_numpy(
        dtype=np.float64
    )

    if len(x) < 256:
        raise SystemExit(
            "Primary dataset is too short."
        )

    if not np.all(
        np.isfinite(x)
    ):
        raise SystemExit(
            "Primary dataset contains non-finite values."
        )

    return x


def stationary_fit(series, max_order, hold_back):
    candidates = []

    for order in range(1, max_order + 1):
        try:
            fit = AutoReg(
                series,
                lags=order,
                trend="c",
                hold_back=hold_back,
                old_names=False,
            ).fit()
        except Exception:
            continue

        roots = np.asarray(
            fit.roots,
            dtype=np.complex128,
        )

        stationary = bool(
            roots.size == order
            and np.all(np.abs(roots) > 1.0)
        )

        if not stationary:
            continue

        if not np.isfinite(float(fit.aic)):
            continue

        candidates.append(
            (float(fit.aic), order, fit)
        )

    if not candidates:
        raise RuntimeError(
            f"No stationary AR candidate for max_order={max_order}"
        )

    _, selected_order, selected_fit = min(
        candidates,
        key=lambda item: item[0],
    )

    return selected_order, selected_fit


def residual_diagnostics(fit, order):
    residuals = np.asarray(
        fit.resid,
        dtype=np.float64,
    )

    valid_lags = [
        lag
        for lag in LJUNG_BOX_LAGS
        if lag > order and lag < len(residuals)
    ]

    if not valid_lags:
        return {
            "status": "NOT_EVALUABLE",
            "reason": (
                "No requested lag has positive adjusted "
                "degrees of freedom for this AR order."
            ),
            "model_df": int(order),
            "requested_lags": LJUNG_BOX_LAGS,
            "evaluated_lags": [],
            "results": {},
        }

    lb = acorr_ljungbox(
        residuals,
        lags=valid_lags,
        model_df=int(order),
        return_df=True,
    )

    results = {}

    for lag in valid_lags:
        row = lb.loc[lag]

        results[str(lag)] = {
            "status": "EVALUATED",
            "statistic": canonical_float(
                row["lb_stat"]
            ),
            "p_value": canonical_float(
                row["lb_pvalue"]
            ),
            "adjusted_degrees_of_freedom": (
                int(lag - order)
            ),
        }

    return {
        "status": "EVALUATED",
        "model_df": int(order),
        "requested_lags": LJUNG_BOX_LAGS,
        "evaluated_lags": valid_lags,
        "results": results,
    }


def main():
    series = load_primary()

    results = []

    for max_order in ORDER_CAPS:

        selected_order, fit = (
            stationary_fit(
                series,
                max_order,
                COMMON_HOLD_BACK,
            )
        )

        residuals = np.asarray(
            fit.resid,
            dtype=np.float64,
        )

        results.append({
            "declared_max_order":
                int(max_order),

            "selected_aic_order":
                int(selected_order),

            "selected_at_boundary":
                bool(
                    selected_order
                    ==
                    max_order
                ),

            "aic": canonical_float(
                fit.aic
            ),
            "bic": canonical_float(
                fit.bic
            ),

            "stationary":
                True,

            "residual_std": canonical_float(
                np.std(residuals)
            ),

            "ljung_box":
                residual_diagnostics(
                    fit,
                    selected_order,
                )
        })

    boundary_count = sum(
        int(
            item["selected_at_boundary"]
        )
        for item in results
    )

    if boundary_count == len(
        results
    ):
        interpretation = (
            "AIC remains at the declared boundary "
            "through the entire 20/40/60 capacity audit. "
            "The finite AR short-memory null is therefore "
            "not sufficiently capacity-resolved for stronger "
            "confirmatory inference. A new null protocol "
            "must be prospectively declared before confirmation."
        )

    elif boundary_count > 0:
        interpretation = (
            "At least one declared AR capacity remains "
            "boundary-selected. Null-capacity sensitivity "
            "requires prospective protocol specification "
            "before confirmatory use."
        )

    else:
        interpretation = (
            "The observed AIC selection no longer reaches "
            "the tested capacity boundaries. This is a "
            "model-capacity diagnostic only and does not "
            "establish the scientific hypothesis."
        )

    report = {
        "status":
            "DIAGNOSTIC_ONLY",

        "scientific_claim_authority":
            False,

        "claim_support":
            False,

        "post_observation":
            True,

        "protocol": {
            "purpose":
                "null_model_capacity_audit",

            "order_caps":
                ORDER_CAPS,

            "common_hold_back": COMMON_HOLD_BACK,
            "same_effective_observations_across_caps": True,
            "ljung_box_model_df": "selected_AR_order",
            "non_evaluable_ljung_box_lags_are_not_interpreted": True,

            "criterion":
                "AIC",

            "trend":
                "constant",

            "stationarity_required":
                True,

            "primary_null_unchanged":
                True,
        },

        "primary": {
            "dataset":
                str(PRIMARY_PATH),

            "rows":
                int(len(series)),
        },

        "results":
            results,

        "interpretation":
            interpretation,

        "important_boundary":
            (
                "This audit must not be used to choose an "
                "AR order or null family after observing a "
                "desired inferential outcome. Any new "
                "confirmatory order range must be declared "
                "before fresh validation data are analyzed."
            ),
    }

    output = Path(
        "artifacts/null_order_capacity_audit.json"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            report,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
