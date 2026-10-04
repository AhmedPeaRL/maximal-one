from __future__ import annotations

import numpy as np

from statsmodels.tsa.ar_model import AutoReg


SEED = 90210
N = 3328
MAX_ORDER = 20


def generate_ar1(
    n: int,
    phi: float,
    seed: int,
    burn_in: int = 2000,
) -> np.ndarray:
    rng = np.random.default_rng(seed)

    total = n + burn_in
    innovations = rng.standard_normal(total)

    x = np.zeros(total, dtype=np.float64)

    for i in range(1, total):
        x[i] = phi * x[i - 1] + innovations[i]

    return x[burn_in:]


def main() -> None:
    x = generate_ar1(
        n=N,
        phi=0.7,
        seed=SEED,
    )

    fits = []

    for order in range(1, MAX_ORDER + 1):
        fit = AutoReg(
            x,
            lags=order,
            trend="c",
            old_names=False,
            hold_back=MAX_ORDER,
        ).fit()

        fits.append(fit)

    effective_nobs = {
        int(fit.nobs)
        for fit in fits
    }

    if len(effective_nobs) != 1:
        raise SystemExit(
            "FAIL: AR candidates do not use the same effective observations."
        )

    expected_nobs = N - MAX_ORDER

    if effective_nobs != {expected_nobs}:
        raise SystemExit(
            "FAIL: unexpected effective observation count: "
            f"{effective_nobs}; expected {expected_nobs}."
        )

    aic_values = [
        float(fit.aic)
        for fit in fits
    ]

    if not all(np.isfinite(aic) for aic in aic_values):
        raise SystemExit(
            "FAIL: non-finite AIC encountered."
        )

    print(
        "PASS: all AR candidate orders use the same "
        f"effective observations ({expected_nobs})."
    )

    print(
        "PASS: AIC comparison is performed with fixed hold_back."
    )


if __name__ == "__main__":
    main()
