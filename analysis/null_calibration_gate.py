from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.ar_model import AutoReg

from analysis.numerical_spectral_verification import estimate_alpha

PRIMARY_PATH = Path("real-data/sunspots_full.csv")
CANONICAL_REPORT = Path("artifacts/canonical_report.json")
OUTPUT = Path("artifacts/null_calibration_gate.json")

MIN_ORDER = 1
MAX_ORDER = 40

# Declared engineering diagnostic threshold.
# This is NOT a universal statistical constant.
BOUNDARY_FRACTION_LIMIT = 0.10

LJUNG_BOX_LAGS = [10, 20, 40]

def finite(x):
    try:
        return bool(np.isfinite(float(x)))
    except Exception:
        return False

def load_primary():
    df = pd.read_csv(
        PRIMARY_PATH,
        sep=";",
        header=None,
        engine="python",
        on_bad_lines="skip",
    )

    if df.shape[1] < 4:
        raise ValueError(
            "sunspots_full.csv must contain at least four columns"
        )

    x = pd.to_numeric(
        df.iloc[:, 3],
        errors="coerce",
    ).dropna().to_numpy(dtype=np.float64)

    if len(x) < 256:
        raise ValueError("primary series is too short")

    if not np.all(np.isfinite(x)):
        raise ValueError(
            "primary series contains non-finite values"
        )

    return x

def fit_scan(x):
    results = []

    max_order = min(
        MAX_ORDER,
        max(MIN_ORDER, len(x) // 10),
    )

    for order in range(MIN_ORDER, max_order + 1):
        try:
            fit = AutoReg(
                x,
                lags=order,
                trend="c",
                old_names=False,
            ).fit()

            roots = np.asarray(
                fit.roots,
                dtype=np.complex128,
            )

            stationary = bool(
                roots.size == order
                and np.all(np.abs(roots) > 1.0)
            )

            aic = float(fit.aic)

            results.append(
                {
                    "order": order,
                    "aic": aic if finite(aic) else None,
                    "stationary": stationary,
                }
            )

        except Exception as exc:
            results.append(
                {
                    "order": order,
                    "aic": None,
                    "stationary": False,
                    "error": str(exc),
                }
            )

    valid = [
        r
        for r in results
        if r["stationary"] and finite(r["aic"])
    ]

    if not valid:
        raise RuntimeError(
            "No valid stationary AR order found"
        )

    best = min(
        valid,
        key=lambda r: r["aic"],
    )

    return {
        "scan_min_order": MIN_ORDER,
        "scan_max_order": max_order,
        "best_aic_order": best["order"],
        "best_aic": best["aic"],
        "best_at_boundary": (
            best["order"] == max_order
        ),
        "results": results,
    }

def residual_whiteness(x, order):
    try:
        fit = AutoReg(
            x,
            lags=order,
            trend="c",
            old_names=False,
        ).fit()

        residuals = np.asarray(
            fit.resid,
            dtype=np.float64,
        )

        residuals = residuals[
            np.isfinite(residuals)
        ]

        if len(residuals) < 100:
            return {
                "valid": False,
                "passed": False,
                "reason": "too_few_residuals",
                "lags": {},
            }

        max_lag = min(
            max(LJUNG_BOX_LAGS),
            max(1, len(residuals) // 5),
        )

        lags = [
            lag
            for lag in LJUNG_BOX_LAGS
            if lag <= max_lag
        ]

        if not lags:
            return {
                "valid": False,
                "passed": False,
                "reason": "no_valid_ljung_box_lag",
                "lags": {},
            }

        result = acorr_ljungbox(
            residuals,
            lags=lags,
            return_df=True,
        )

        values = {}

        for lag in lags:
            p = float(
                result.loc[
                    lag,
                    "lb_pvalue",
                ]
            )

            values[str(lag)] = {
                "p_value": p,
                "passed": bool(
                    finite(p) and p > 0.05
                ),
            }

        passed = all(
            item["passed"]
            for item in values.values()
        )

        return {
            "valid": True,
            "passed": passed,
            "lags": values,
        }

    except Exception as exc:
        return {
            "valid": False,
            "passed": False,
            "reason": str(exc),
            "lags": {},
        }

def load_surrogate_boundary_fraction():
    if not CANONICAL_REPORT.exists():
        return None

    try:
        report = json.loads(
            CANONICAL_REPORT.read_text(
                encoding="utf-8"
            )
        )

        value = (
            report
            .get("appropriate_stochastic_null", {})
            .get("order_selection_diagnostic", {})
            .get("surrogate_boundary_fraction")
        )

        return (
            float(value)
            if finite(value)
            else None
        )

    except Exception:
        return None

def main():
    x = load_primary()

    alpha = estimate_alpha(x)
    scan = fit_scan(x)

    best_order = int(
        scan["best_aic_order"]
    )

    residuals = residual_whiteness(
        x,
        best_order,
    )

    surrogate_boundary_fraction = (
        load_surrogate_boundary_fraction()
    )

    failures = []

    if scan["best_at_boundary"]:
        failures.append(
            "observed AIC order reaches calibration scan boundary"
        )

    if (
        surrogate_boundary_fraction is not None
        and surrogate_boundary_fraction
        > BOUNDARY_FRACTION_LIMIT
    ):
        failures.append(
            "primary surrogate order selection reaches "
            "the declared boundary too frequently"
        )

    if not residuals["valid"]:
        failures.append(
            "residual whiteness diagnostic is invalid"
        )
    elif not residuals["passed"]:
        failures.append(
            "best-fit residuals are not adequately white "
            "under the declared Ljung-Box diagnostic"
        )

    calibrated = len(failures) == 0

    report = {
        "status": (
            "CALIBRATION_NOT_REJECTED"
            if calibrated
            else "CALIBRATION_REQUIRED"
        ),
        "scientific_claim_authority": False,

        "primary_alpha": (
            float(alpha)
            if finite(alpha)
            else None
        ),

        "order_scan": scan,

        "residual_whiteness": residuals,

        "canonical_primary_null_diagnostic": {
            "surrogate_boundary_fraction":
                surrogate_boundary_fraction,
            "boundary_fraction_limit":
                BOUNDARY_FRACTION_LIMIT,
            "boundary_fraction_available":
                surrogate_boundary_fraction is not None,
        },

        "calibration_decision": {
            "calibrated":
                calibrated,
            "failures":
                failures,
        },

        "interpretation": (
            "This gate does not replace the declared stochastic "
            "null and does not create confirmation. It only "
            "determines whether the current finite-order "
            "short-memory null is sufficiently calibrated for "
            "stronger inferential use. If calibration fails, "
            "scientific claim support remains blocked."
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

    print("=== NULL CALIBRATION GATE ===")
    print("Best AIC order:", best_order)
    print("Scan maximum:", scan["scan_max_order"])
    print("Observed boundary:", scan["best_at_boundary"])
    print(
        "Surrogate boundary fraction:",
        surrogate_boundary_fraction,
    )
    print(
        "Residual whiteness:",
        residuals["passed"],
    )
    print("Status:", report["status"])
    print("Saved:", OUTPUT)

if __name__ == "__main__":
    main()
