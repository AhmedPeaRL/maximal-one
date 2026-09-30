from __future__ import annotations

import numpy as np
from fbm import FBM

from analysis.early_warning_signal import (
    early_warning_indicator
)


def generate_null(
    n: int = 5000,
    hurst: float = 0.5,
) -> np.ndarray:
    if n < 256:
        raise ValueError(
            "n must be at least 256"
        )

    if not (
        0.0 < hurst < 1.0
    ):
        raise ValueError(
            "hurst must be between 0 and 1"
        )

    f = FBM(
        n=n,
        hurst=hurst,
        length=1,
        method="daviesharte",
    )

    series = np.asarray(
        f.fbm(),
        dtype=np.float64,
    )

    if not np.all(
        np.isfinite(series)
    ):
        raise ValueError(
            "generated null contains non-finite values"
        )

    return series


def null_distribution(
    runs: int = 50,
) -> np.ndarray:
    if runs < 1:
        raise ValueError(
            "runs must be positive"
        )

    results = []

    for _ in range(runs):
        series = generate_null()

        result = early_warning_indicator(
            series
        )

        slope = result[
            "trend_slope"
        ]

        if not np.isfinite(slope):
            raise ValueError(
                "null early-warning slope is non-finite"
            )

        results.append(
            float(slope)
        )

    return np.asarray(
        results,
        dtype=np.float64,
    )


def main() -> None:
    distribution = (
        null_distribution()
    )

    print(
        "Null mean slope:",
        float(
            np.mean(distribution)
        ),
    )

    print(
        "Null std:",
        float(
            np.std(distribution)
        ),
    )

    print(
        "Scientific role: "
        "synthetic/methodological diagnostic only"
    )


if __name__ == "__main__":
    main()
