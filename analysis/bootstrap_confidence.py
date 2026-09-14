import numpy as np
from analysis.independent_validation import (
    periodogram_alpha_estimation
)
from analysis.numerical_spectral_verification import (
    estimate_alpha,
    block_bootstrap
)

BOOTSTRAP_ITERATIONS = 128

def bootstrap_alpha(
    series,
    estimator,
    iterations=BOOTSTRAP_ITERATIONS,
    seed=42
):
    """
    IID bootstrap diagnostic.

    The estimator is supplied explicitly.

    This function is diagnostic only and does not replace
    the canonical estimator protocol.
    """

    rng = np.random.default_rng(seed)

    series = np.asarray(
        series,
        dtype=np.float64
    )

    n = len(series)

    if n < 256:
        return None

    if not np.all(
        np.isfinite(series)
    ):
        return None

    estimates = []

    for _ in range(iterations):

        idx = rng.choice(
            n,
            size=n,
            replace=True,
            shuffle=False
        )

        sample = series[idx]

        try:

            alpha = estimator(sample)

            if np.isfinite(alpha):
                estimates.append(
                    float(alpha)
                )

        except Exception:
            continue

    if len(estimates) < 8:
        return None

    estimates = np.asarray(
        estimates,
        dtype=np.float64
    )

    return {
        "mean": float(
            np.mean(estimates)
        ),
        "std": float(
            np.std(estimates)
        ),
        "ci_low": float(
            np.percentile(
                estimates,
                2.5
            )
        ),
        "ci_high": float(
            np.percentile(
                estimates,
                97.5
            )
        ),
        "count": int(
            len(estimates)
        ),
        "estimator": "FFT_periodogram",
        "bootstrap_type": "iid"
    }

def dual_bootstrap(series):
    """
    Return diagnostic confidence estimates for both
    independent spectral estimators.

    IMPORTANT:
    The labels correspond to the actual estimator used.

    - Welch -> block_bootstrap()
    - FFT   -> bootstrap_alpha(...periodogram_alpha_estimation)

    These are diagnostic uncertainty estimates and do not
    establish independent rerun reproducibility.
    """

    rng = np.random.default_rng(42)

    # block_bootstrap() internally calls the canonical
    # Welch estimator.
    welch_conf = block_bootstrap(
        series,
        rng,
        block_size=16,
        num_boot=128
    )

    if isinstance(welch_conf, dict):
        welch_conf = dict(welch_conf)
        welch_conf["estimator"] = "Welch_PSD"
        welch_conf["bootstrap_type"] = "block"

    # periodogram_alpha_estimation() is the independent
    # full-series FFT estimator.
    fft_conf = bootstrap_alpha(
        series,
        periodogram_alpha_estimation
    )

    return {
        "fft": fft_conf,
        "welch": welch_conf
    }
