from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from statsmodels.tsa.ar_model import AutoReg


SEED = 90210
N = 3328
OUTER = 50

ORDERS = [1, 2, 4, 8, 12, 16, 20]

# All candidate AR orders must be compared using the same
# effective observations. Using the maximum candidate order
# as hold_back makes the comparison invariant to candidate order.
COMPARISON_HOLD_BACK = max(ORDERS)


def simulate_ar(
    phi: list[float],
    rng: np.random.Generator,
) -> np.ndarray:
    burn = 1000
    total = N + burn

    x = np.zeros(
        total,
        dtype=float,
    )

    noise = rng.normal(
        size=total,
    )

    for t in range(
        len(phi),
        total,
    ):
        value = noise[t]

        for lag, coefficient in enumerate(
            phi,
            start=1,
        ):
            value += (
                coefficient
                * x[t - lag]
            )

        x[t] = value

    return x[burn:]


def selected_order(
    series: np.ndarray,
    criterion: str,
    max_order: int,
) -> tuple[int, dict]:
    best_order = None
    best_value = np.inf
    records = []

    for order in range(
        1,
        max_order + 1,
    ):
        try:
            model = AutoReg(
                series,
                lags=order,
                trend="c",
                hold_back=COMPARISON_HOLD_BACK,
                old_names=False,
            )

            result = model.fit()

            roots = np.asarray(
                result.roots,
                dtype=np.complex128,
            )

            stationary = bool(
                roots.size == order
                and np.all(
                    np.abs(roots) > 1.0
                )
            )

            value = float(
                getattr(
                    result,
                    criterion,
                )
            )

            nobs = int(
                result.nobs
            )

            record = {
                "order": int(order),
                "fit_valid": True,
                "stationary": stationary,
                "criterion": criterion,
                "criterion_value": (
                    value
                    if np.isfinite(value)
                    else None
                ),
                "nobs": nobs,
                "hold_back": COMPARISON_HOLD_BACK,
            }

            records.append(record)

            if (
                stationary
                and np.isfinite(value)
                and value < best_value
            ):
                best_value = value
                best_order = order

        except Exception as exc:
            records.append({
                "order": int(order),
                "fit_valid": False,
                "stationary": False,
                "criterion": criterion,
                "criterion_value": None,
                "nobs": None,
                "hold_back": COMPARISON_HOLD_BACK,
                "error": str(exc),
            })

    if best_order is None:
        raise RuntimeError(
            f"No valid stationary {criterion} fit found."
        )

    nobs_values = {
        item["nobs"]
        for item in records
        if item.get("fit_valid") is True
    }

    if len(nobs_values) != 1:
        raise RuntimeError(
            "AR candidates were not compared using "
            "identical effective observations."
        )

    return best_order, {
        "criterion": criterion,
        "hold_back": COMPARISON_HOLD_BACK,
        "effective_nobs": next(
            iter(nobs_values)
        ),
        "candidates": records,
    }


def evaluate_case(
    case: str,
    phi: list[float],
) -> dict:
    results = []

    # One deterministic series per outer replicate.
    # The same series is then evaluated at every sweep cap.
    rng = np.random.default_rng(
        SEED
        + sum(
            (index + 1) * int(
                round(abs(value) * 1000)
            )
            for index, value in enumerate(phi)
        )
    )

    series_replicates = [
        simulate_ar(
            phi,
            rng,
        )
        for _ in range(OUTER)
    ]

    for max_order in ORDERS:
        selected = []
        effective_nobs = []

        for series in series_replicates:
            order, metadata = selected_order(
                series,
                "aic",
                max_order,
            )

            selected.append(
                int(order)
            )

            effective_nobs.append(
                int(
                    metadata["effective_nobs"]
                )
            )

        if len(set(effective_nobs)) != 1:
            raise RuntimeError(
                "Effective observation count differs "
                "within a capacity-sweep condition."
            )

        boundary = (
            sum(
                order == max_order
                for order in selected
            )
            / OUTER
        )

        results.append({
            "max_order": int(max_order),
            "selected_orders": selected,
            "boundary_fraction": float(
                boundary
            ),
            "median_selected_order": float(
                np.median(selected)
            ),
            "criterion": "AIC",
            "hold_back": COMPARISON_HOLD_BACK,
            "effective_nobs": effective_nobs[0],
        })

    return {
        "case": case,
        "declared_order": len(phi),
        "outer_replicates": OUTER,
        "n": N,
        "results": results,
    }


def main() -> None:
    payload = {
        "audit": "ar_aic_capacity_sweep",
        "protocol_revision": (
            "ar_order_comparison_holdback_v1"
        ),
        "scientific_role": "diagnostic_only",
        "claim_support": False,
        "does_not_change_primary_null": True,
        "does_not_support_claim": True,
        "does_not_falsify_claim": True,
        "post_observation": True,
        "preregistered_confirmation": False,
        "historical_boundary_result_invalidated_for_comparison": True,
        "seed": SEED,
        "n": N,
        "orders_tested": ORDERS,
        "comparison_hold_back": COMPARISON_HOLD_BACK,
        "same_effective_observations_required": True,
        "cases": [
            evaluate_case(
                "ar1_phi_0_7",
                [0.7],
            ),
            evaluate_case(
                "ar2_phi_0_5_0_2",
                [0.5, 0.2],
            ),
        ],
    }

    output = Path(
        "artifacts/model_capacity_sweep.json"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            payload,
            f,
            indent=2,
            sort_keys=True,
        )

    print(
        f"Model-capacity sweep written: {output}"
    )


if __name__ == "__main__":
    main()
