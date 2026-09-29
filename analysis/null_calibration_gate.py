from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg

from analysis.numerical_spectral_verification import estimate_alpha

PRIMARY_PATH = Path("real-data/sunspots_full.csv")
OUTPUT = Path("artifacts/null_calibration_gate.json")

MIN_ORDER = 1
MAX_ORDER = 40

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
    ).dropna().to_numpy(
        dtype=np.float64
    )

    if len(x) < 256:
        raise ValueError(
            "primary series is too short"
        )

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

    for order in range(
        MIN_ORDER,
        max_order + 1,
    ):
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
        if (
            r["stationary"]
            and finite(r["aic"])
        )
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

def main():
    x = load_primary()

    alpha = estimate_alpha(x)

    scan = fit_scan(x)

    boundary = scan["best_at_boundary"]

    report = {
        "status": (
            "CALIBRATION_REQUIRED"
            if boundary
            else "CALIBRATION_NOT_REJECTED"
        ),
        "scientific_claim_authority": False,
        "primary_alpha": (
            float(alpha)
            if finite(alpha)
            else None
        ),
        "order_scan": scan,
        "boundary_policy": {
            "boundary_fraction_limit": BOUNDARY_FRACTION_LIMIT,
            "current_single_fit_boundary": boundary,
            "claim_support_blocked_if_boundary": True,
        },
        "interpretation": (
            "A finite-order short-memory null is not treated "
            "as adequately calibrated when order selection "
            "reaches the declared maximum. The current result "
            "must remain non-confirmatory until the null family "
            "and order-selection protocol are independently "
            "calibrated."
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
    print("Best AIC order:", scan["best_aic_order"])
    print("Scan maximum:", scan["scan_max_order"])
    print("Boundary:", boundary)
    print("Status:", report["status"])
    print("Saved:", OUTPUT)

if __name__ == "__main__":
    main()
