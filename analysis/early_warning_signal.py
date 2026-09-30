from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from analysis.numerical_spectral_verification import estimate_alpha


def rolling_alpha(
    series: np.ndarray,
    window: int = 256,
) -> np.ndarray:
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1:
        raise ValueError(
            "series must be one-dimensional"
        )

    if len(series) <= window:
        raise ValueError(
            "series must contain more samples than window"
        )

    alphas = []

    for i in range(
        window,
        len(series),
    ):
        segment = series[
            i - window:i
        ]

        alpha = estimate_alpha(
            segment
        )

        if not np.isfinite(alpha):
            raise ValueError(
                "non-finite spectral exponent encountered"
            )

        alphas.append(
            float(alpha)
        )

    return np.asarray(
        alphas,
        dtype=np.float64,
    )


def early_warning_indicator(
    series: np.ndarray,
) -> dict:
    alpha_series = rolling_alpha(
        series
    )

    x = np.arange(
        len(alpha_series),
        dtype=np.float64,
    )

    trend = np.polyfit(
        x,
        alpha_series,
        1,
    )[0]

    variance = np.var(
        alpha_series
    )

    return {
        "trend_slope": float(trend),
        "variance": float(variance),
        "mean_alpha": float(
            np.mean(alpha_series)
        ),
        "window_count": int(
            len(alpha_series)
        ),
        "scientific_role":
            "diagnostic_only",
        "scientific_claim_authority":
            False,
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python analysis/early_warning_signal.py <csv>"
        )

    path = sys.argv[1]

    df = pd.read_csv(
        path
    )

    if df.shape[1] == 0:
        raise SystemExit(
            "CSV contains no columns"
        )

    series = pd.to_numeric(
        df.iloc[:, 0],
        errors="coerce",
    ).dropna().to_numpy(
        dtype=np.float64
    )

    if len(series) < 257:
        raise SystemExit(
            "CSV series is too short for the default window"
        )

    result = early_warning_indicator(
        series
    )

    print(result)


if __name__ == "__main__":
    main()
