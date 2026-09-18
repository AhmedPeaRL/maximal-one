from __future__ import annotations
import numpy as np

def detect_structure(series):
    x = np.asarray(
        series,
        dtype=np.float64,
    )

    if x.ndim != 1:
        return 0.0

    if len(x) < 50:
        return 0.0

    if not np.all(
        np.isfinite(x)
    ):
        return 0.0

    std = np.std(x)

    if not np.isfinite(std) or std < 1e-12:
        return 0.0

    # --------------------------------------------------
    # Lag-1 autocorrelation
    # --------------------------------------------------

    a = x[:-1]
    b = x[1:]

    a_std = np.std(a)
    b_std = np.std(b)

    if (
        a_std < 1e-12
        or b_std < 1e-12
    ):
        autocorr = 0.0
    else:
        autocorr = float(
            np.corrcoef(
                a,
                b,
            )[0, 1]
        )

        if not np.isfinite(
            autocorr
        ):
            autocorr = 0.0

    autocorr_component = min(
        1.0,
        abs(autocorr),
    )

    # --------------------------------------------------
    # Proper discrete histogram entropy
    # --------------------------------------------------

    hist, _ = np.histogram(
        x,
        bins=20,
    )

    total = np.sum(hist)

    if total <= 0:
        entropy_component = 0.0
    else:
        probabilities = (
            hist.astype(np.float64)
            /
            float(total)
        )

        probabilities = probabilities[
            probabilities > 0
        ]

        entropy = -np.sum(
            probabilities
            *
            np.log(
                probabilities
            )
        )

        max_entropy = np.log(20.0)

        normalized_entropy = (
            entropy
            /
            max_entropy
        )

        normalized_entropy = float(
            np.clip(
                normalized_entropy,
                0.0,
                1.0,
            )
        )

        entropy_component = (
            1.0
            -
            normalized_entropy
        )

    # --------------------------------------------------
    # Variance stability
    # --------------------------------------------------

    window = min(
        20,
        len(x) // 4,
    )

    if window < 2:
        variance_component = 0.0
    else:
        first_std = np.std(
            x[:window]
        )

        last_std = np.std(
            x[-window:]
        )

        if (
            first_std < 1e-12
            or
            last_std < 1e-12
        ):
            variance_component = 0.0
        else:
            log_ratio = abs(
                np.log(
                    last_std
                    /
                    first_std
                )
            )

            variance_component = float(
                np.exp(
                    -log_ratio
                )
            )

    score = (
        0.4 * autocorr_component
        +
        0.3 * entropy_component
        +
        0.3 * variance_component
    )

    return float(
        np.clip(
            score,
            0.0,
            1.0,
        )
    )
