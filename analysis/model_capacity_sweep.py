from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from statsmodels.tsa.ar_model import AutoReg


SEED = 90210
N = 3328
OUTER = 50

ORDERS = [1, 2, 4, 8, 12, 16, 20]


def simulate_ar(phi: list[float], rng: np.random.Generator) -> np.ndarray:
    burn = 1000
    total = N + burn

    x = np.zeros(total, dtype=float)
    noise = rng.normal(size=total)

    for t in range(len(phi), total):
        value = noise[t]

        for lag, coefficient in enumerate(phi, start=1):
            value += coefficient * x[t - lag]

        x[t] = value

    return x[burn:]


def selected_order(
    series: np.ndarray,
    criterion: str,
    max_order: int,
) -> int:
    best_order = None
    best_value = np.inf

    for order in range(1, max_order + 1):
        try:
            model = AutoReg(
                series,
                lags=order,
                trend="c",
                old_names=False,
            )

            result = model.fit()

            value = getattr(result, criterion)

            if not np.isfinite(value):
                continue

            if value < best_value:
                best_value = float(value)
                best_order = order

        except Exception:
            continue

    if best_order is None:
        raise RuntimeError(
            f"No valid {criterion} fit found."
        )

    return best_order


def evaluate_case(
    case: str,
    phi: list[float],
) -> dict:
    results = []

    for max_order in ORDERS:
        selected = []

        for _ in range(OUTER):
            rng = np.random.default_rng(
                SEED + len(selected) + max_order * 1000
            )

            series = simulate_ar(phi, rng)

            order = selected_order(
                series,
                "aic",
                max_order,
            )

            selected.append(order)

        boundary = sum(
            order == max_order
            for order in selected
        ) / OUTER

        results.append(
            {
                "max_order": max_order,
                "selected_orders": selected,
                "boundary_fraction": boundary,
                "median_selected_order": float(
                    np.median(selected)
                ),
            }
        )

    return {
        "case": case,
        "declared_order": len(phi),
        "outer_replicates": OUTER,
        "results": results,
    }


def main() -> None:
    payload = {
        "audit": "ar_aic_capacity_sweep",
        "scientific_role": "diagnostic_only",
        "claim_support": False,
        "post_observation": True,
        "preregistered_confirmation": False,
        "seed": SEED,
        "n": N,
        "orders_tested": ORDERS,
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
