from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.appropriate_stochastic_null import (
    MAX_AR_ORDER,
    MIN_AR_ORDER,
    _stationary_fit,
)

from statsmodels.tsa.ar_model import AutoReg


SEED = 90210
N = 3328
OUTER_REPLICATES = 50


AR_CASES = {
    "ar1_phi_0_7": [0.7],
    "ar2_phi_0_5_0_2": [0.5, 0.2],
}


def generate_ar_process(
    phi,
    n,
    rng,
    burn_in=2000,
):
    phi = np.asarray(
        phi,
        dtype=np.float64,
    )

    order = len(phi)

    total = int(n) + int(burn_in)

    innovations = rng.standard_normal(total)

    x = np.zeros(
        total,
        dtype=np.float64,
    )

    for i in range(order, total):
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


def inspect_aic_path(series):
    x = np.asarray(
        series,
        dtype=np.float64,
    )

    max_order = min(
        MAX_AR_ORDER,
        max(
            MIN_AR_ORDER,
            len(x) // 10,
        ),
    )

    candidates = []

    for order in range(
        MIN_AR_ORDER,
        max_order + 1,
    ):
        try:
            fit = AutoReg(
                x,
                lags=order,
                trend="c",
                old_names=False,
                hold_back=max_order,
            ).fit()
        except Exception as exc:
            candidates.append({
                "order": order,
                "fit_valid": False,
                "reason": str(exc),
            })
            continue

        roots = np.asarray(
            fit.roots,
            dtype=np.complex128,
        )

        stationary = bool(
            roots.size == order
            and np.all(
                np.abs(roots) > 1.0
            )
        )

        aic = float(fit.aic)

        candidates.append({
            "order": int(order),
            "fit_valid": True,
            "stationary": stationary,
            "aic": (
                aic
                if np.isfinite(aic)
                else None
            ),
            "bic": (
                float(fit.bic)
                if np.isfinite(fit.bic)
                else None
            ),
            "hqic": (
                float(fit.hqic)
                if np.isfinite(fit.hqic)
                else None
            ),
            "hold_back": int(max_order),
            "effective_nobs": int(fit.nobs),
        })

    valid = [
        item
        for item in candidates
        if (
            item.get("fit_valid") is True
            and item.get("stationary") is True
            and item.get("aic") is not None
        )
    ]

    if not valid:
        raise RuntimeError(
            "No valid stationary AR candidate."
        )

    selected_aic = min(
        valid,
        key=lambda item: item["aic"],
    )

    selected_bic = min(
        [
            item
            for item in valid
            if item.get("bic") is not None
        ],
        key=lambda item: item["bic"],
    )

    selected_hqic = min(
        [
            item
            for item in valid
            if item.get("hqic") is not None
        ],
        key=lambda item: item["hqic"],
    )

    return {
        "comparison_protocol": {
            "criterion": "AIC",
            "same_effective_observations": True,
            "hold_back": int(max_order),
            "reason": (
                "All candidate AR orders are compared on the "
                "same effective observations."
            ),
        },
        "selected_aic": int(
            selected_aic["order"]
        ),
        "selected_bic": int(
            selected_bic["order"]
        ),
        "selected_hqic": int(
            selected_hqic["order"]
        ),
        "aic_path": candidates,
    }


def run_case(name, phi, rng):
    records = []

    for index in range(
        OUTER_REPLICATES
    ):
        series = generate_ar_process(
            phi,
            N,
            rng,
        )

        fit_order, _ = _stationary_fit(
            series
        )

        diagnostics = inspect_aic_path(
            series
        )

        records.append({
            "outer_index": index,
            "declared_order": len(phi),
            "current_protocol_order": int(
                fit_order
            ),
            **diagnostics,
        })

    def fraction(key):
        values = [
            item[key]
            for item in records
        ]

        return float(
            np.mean(
                np.asarray(
                    values
                ) == MAX_AR_ORDER
            )
        )

    return {
        "case": name,
        "declared_phi": list(
            map(float, phi)
        ),
        "n": N,
        "outer_replicates": OUTER_REPLICATES,
        "max_ar_order": MAX_AR_ORDER,
        "min_ar_order": MIN_AR_ORDER,
        "current_protocol": {
            "criterion": "AIC",
            "max_order": MAX_AR_ORDER,
            "min_order": MIN_AR_ORDER,
            "trend": "constant",
            "stationarity_required": True,
        },
        "boundary_fraction": {
            "aic": fraction(
                "selected_aic"
            ),
            "bic": fraction(
                "selected_bic"
            ),
            "hqic": fraction(
                "selected_hqic"
            ),
            "current_protocol_fit": fraction(
                "current_protocol_order"
            ),
        },
        "records": records,
    }


def main():
    rng = np.random.default_rng(
        SEED
    )

    results = [
        run_case(
            name,
            phi,
            rng,
        )
        for name, phi in AR_CASES.items()
    ]

    output = {
        "protocol_revision": "ar_order_comparison_holdback_v1",
        "post_observation_repair": True,
        "confirmatory": False,
        "historical_boundary_result_invalidated_for_comparison": True,
        "audit": "ar_model_capacity_diagnostic",
        "seed": SEED,
        "scientific_role": "diagnostic_only",
        "claim_support": False,
        "post_observation": True,
        "preregistered_confirmation": False,
        "does_not_change_primary_null": True,
        "does_not_support_claim": True,
        "does_not_falsify_claim": True,
        "results": results,
    }

    path = Path(
        "artifacts/model_capacity_diagnostic.json"
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
        ) + "\n",
        encoding="utf-8",
    )

    print(
        f"Model-capacity diagnostic written: {path}"
    )


if __name__ == "__main__":
    main()
