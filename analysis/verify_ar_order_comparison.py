from __future__ import annotations

import numpy as np
from statsmodels.tsa.ar_model import AutoReg


SEED = 90210
N = 3328
MAX_ORDER = 20
HOLD_BACK = MAX_ORDER


def generate_ar1(
    n: int,
    rng: np.random.Generator,
) -> np.ndarray:
    burn_in = 2000
    total = n + burn_in

    x = np.zeros(
        total,
        dtype=np.float64,
    )

    noise = rng.standard_normal(
        total
    )

    for i in range(
        1,
        total,
    ):
        x[i] = (
            0.7 * x[i - 1]
            + noise[i]
        )

    return x[burn_in:]


def main() -> None:
    rng = np.random.default_rng(
        SEED
    )

    series = generate_ar1(
        N,
        rng,
    )

    expected_nobs = (
        N - HOLD_BACK
    )

    observed_nobs = set()

    for order in range(
        1,
        MAX_ORDER + 1,
    ):
        fit = AutoReg(
            series,
            lags=order,
            trend="c",
            hold_back=HOLD_BACK,
            old_names=False,
        ).fit()

        nobs = int(
            fit.nobs
        )

        if nobs != expected_nobs:
            raise SystemExit(
                "❌ Effective observation count mismatch: "
                f"order={order}, nobs={nobs}, "
                f"expected={expected_nobs}"
            )

        if not np.isfinite(
            float(fit.aic)
        ):
            raise SystemExit(
                f"❌ Non-finite AIC at order {order}."
            )

        observed_nobs.add(
            nobs
        )

    if observed_nobs != {
        expected_nobs
    }:
        raise SystemExit(
            "❌ Candidate AR models do not share "
            "the same effective observation count."
        )

    print(
        "✅ AR order-comparison integrity verified."
    )

    print(
        f"   max_order={MAX_ORDER}"
    )

    print(
        f"   hold_back={HOLD_BACK}"
    )

    print(
        f"   effective_nobs={expected_nobs}"
    )


if __name__ == "__main__":
    main()
