from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg

from analysis.numerical_spectral_verification import (
    estimate_alpha
)


PRIMARY_PATH = Path(
    "real-data/sunspots_full.csv"
)

CANONICAL_REPORT = Path(
    "artifacts/canonical_report.json"
)

STRICT_CLAIM = Path(
    "core-scientific/strict_claim.json"
)

OUTPUT = Path(
    "artifacts/null_calibration_gate.json"
)

MIN_ORDER = 1
MAX_ORDER = 20


def finite(x):
    try:
        return bool(
            np.isfinite(float(x))
        )
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
        errors="coerce"
    ).dropna().to_numpy(
        dtype=np.float64
    )

    if len(x) < 256:
        raise ValueError(
            "primary series is too short"
        )

    if not np.all(
        np.isfinite(x)
    ):
        raise ValueError(
            "primary series contains non-finite values"
        )

    return x


def fit_scan(x):
    results = []

    max_order = min(
        MAX_ORDER,
        max(
            MIN_ORDER,
            len(x) // 10
        )
    )

    for order in range(
        MIN_ORDER,
        max_order + 1
    ):
        try:
            fit = AutoReg(
                x,
                lags=order,
                trend="c",
                old_names=False
            ).fit()

            roots = np.asarray(
                fit.roots,
                dtype=np.complex128
            )

            stationary = bool(
                roots.size == order
                and
                np.all(
                    np.abs(roots) > 1.0
                )
            )

            aic = float(
                fit.aic
            )

            results.append({
                "order": order,
                "aic": (
                    aic
                    if finite(aic)
                    else None
                ),
                "stationary": stationary
            })

        except Exception as exc:
            results.append({
                "order": order,
                "aic": None,
                "stationary": False,
                "error": str(exc)
            })

    valid = [
        item
        for item in results
        if (
            item["stationary"]
            and
            finite(item["aic"])
        )
    ]

    if not valid:
        raise RuntimeError(
            "No valid stationary AR order found."
        )

    best = min(
        valid,
        key=lambda item: item["aic"]
    )

    return {
        "scan_min_order": MIN_ORDER,
        "scan_max_order": max_order,
        "best_aic_order": int(
            best["order"]
        ),
        "best_aic": float(
            best["aic"]
        ),
        "best_at_boundary": bool(
            best["order"] == max_order
        ),
        "results": results
    }


def main():
    if not CANONICAL_REPORT.exists():
        raise SystemExit(
            "canonical_report.json is required before null calibration."
        )

    report = json.loads(
        CANONICAL_REPORT.read_text(
            encoding="utf-8"
        )
    )

    stochastic = report.get(
        "appropriate_stochastic_null"
    )

    if not isinstance(
        stochastic,
        dict
    ):
        raise SystemExit(
            "canonical primary stochastic-null result is missing."
        )

    x = load_primary()

    alpha = estimate_alpha(x)

    scan = fit_scan(x)

    diagnostic = (
        stochastic.get(
            "order_selection_diagnostic"
        )
        or {}
    )

    surrogate_boundary_fraction = diagnostic.get(
        "surrogate_boundary_fraction"
    )

    selected_order = stochastic.get(
        "selected_order"
    )

    observed_boundary = bool(
        selected_order == MAX_ORDER
    )

    surrogate_boundary_saturation = (
        finite(
            surrogate_boundary_fraction
        )
        and
        float(
            surrogate_boundary_fraction
        ) > 0.0
    )

    calibration_required = bool(
        observed_boundary
        or
        surrogate_boundary_saturation
    )

    report_out = {
        "status": (
            "CALIBRATION_REQUIRED"
            if calibration_required
            else "CALIBRATION_NOT_REJECTED"
        ),

        "scientific_claim_authority": False,
        "promotion_authority": False,

        "protocol": {
            "null_family":
                "stationary_gaussian_AR_p_aic",
            "min_order": MIN_ORDER,
            "max_order": MAX_ORDER,
            "criterion": "AIC",
            "stationarity_required": True,
            "endpoint": "canonical_primary_alpha",
            "direction": "greater_than_null",
            "tail": "upper"
        },

        "observed_primary_alpha": (
            float(alpha)
            if finite(alpha)
            else None
        ),

        "observed_order_scan": scan,

        "canonical_null_diagnostics": {
            "selected_order": (
                int(selected_order)
                if selected_order is not None
                else None
            ),
            "selected_at_boundary":
                observed_boundary,
            "surrogate_boundary_fraction": (
                float(
                    surrogate_boundary_fraction
                )
                if finite(
                    surrogate_boundary_fraction
                )
                else None
            ),
            "surrogate_boundary_saturation":
                surrogate_boundary_saturation
        },

        "interpretation": (
            "The declared finite-order AR(p) null is "
            "not treated as adequately calibrated when "
            "the selected order reaches the declared "
            "maximum or the surrogate refits show boundary "
            "saturation. This gate is conservative and "
            "does not constitute evidence against the "
            "scientific hypothesis."
        ),

        "fresh_calibration_required": True,

        "post_observation_amendment": True
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(
        json.dumps(
            report_out,
            indent=2,
            sort_keys=True
        ) + "\n",
        encoding="utf-8"
    )

    print(
        "=== NULL CALIBRATION GATE ==="
    )

    print(
        "Observed selected order:",
        selected_order
    )

    print(
        "Declared maximum:",
        MAX_ORDER
    )

    print(
        "Surrogate boundary fraction:",
        surrogate_boundary_fraction
    )

    print(
        "Status:",
        report_out["status"]
    )


if __name__ == "__main__":
    main()
