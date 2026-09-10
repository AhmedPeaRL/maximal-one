from __future__ import annotations
import numpy as np
from scipy.signal import welch

FREEZE_DECIMALS = 8

# ============================================================
# CANONICAL SPECTRAL PROTOCOL
# ============================================================
#
# This frequency band is the declared canonical band for the
# complete multi-scale protocol.
#
# It is intentionally restricted so that the same original
# physical band can be mapped through scales 1, 2, 4 and 8
# without crossing the normalized Nyquist limit.
#
# DO NOT change these values locally.
# Any scientific change requires a protocol amendment.
# ============================================================

DEFAULT_FREQ_MIN = 0.01
DEFAULT_FREQ_MAX = 0.05

CANONICAL_NPERSEG = 256
CANONICAL_WINDOW = "hann"
CANONICAL_DETREND = "linear"
CANONICAL_SCALING = "density"

def f(x):
    return float(
        np.round(
            float(x),
            FREEZE_DECIMALS,
        )
    )

def _validate_frequency_band(
    freq_min,
    freq_max,
):
    try:
        freq_min = float(freq_min)
        freq_max = float(freq_max)
    except (
        TypeError,
        ValueError,
    ):
        return None

    if not (
        np.isfinite(freq_min)
        and np.isfinite(freq_max)
    ):
        return None

    if not (
        0.0 < freq_min < freq_max < 0.5
    ):
        return None

    return (
        freq_min,
        freq_max,
    )

def _prepare_series(series):
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1:
        return None

    if len(series) < 256:
        return None

    if not np.all(
        np.isfinite(series)
    ):
        return None

    if np.std(series) < 1e-8:
        return None

    series = (
        series
        - np.mean(series)
    )

    std = np.std(series)

    if std < 1e-12:
        return None

    series = (
        series
        / std
    )

    return series

def estimate_alpha(
    series,
    freq_min=DEFAULT_FREQ_MIN,
    freq_max=DEFAULT_FREQ_MAX,
):
    """
    Canonical Welch PSD spectral exponent estimator.

    This is the single canonical primary estimator used by:

        - primary analysis
        - bootstrap
        - scale=1 validation
        - scale validation
        - cross-domain analysis

    No clipping.
    No forced agreement.
    No range correction.
    """

    frequency_band = _validate_frequency_band(
        freq_min,
        freq_max,
    )

    if frequency_band is None:
        return np.nan

    freq_min, freq_max = frequency_band

    series = _prepare_series(series)

    if series is None:
        return np.nan

    nperseg = min(
        CANONICAL_NPERSEG,
        len(series) // 2,
    )

    if nperseg < 128:
        return np.nan

    freqs, psd = welch(
        series,
        nperseg=nperseg,
        window=CANONICAL_WINDOW,
        detrend=CANONICAL_DETREND,
        scaling=CANONICAL_SCALING,
    )

    mask = (
        (freqs > freq_min)
        &
        (freqs < freq_max)
        &
        np.isfinite(freqs)
        &
        np.isfinite(psd)
        &
        (psd > 0)
    )

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 20:
        return np.nan

    log_f = np.log(freqs)
    log_psd = np.log(psd)

    if not (
        np.all(np.isfinite(log_f))
        and
        np.all(np.isfinite(log_psd))
    ):
        return np.nan

    try:
        coeffs = np.polyfit(
            log_f,
            log_psd,
            1,
        )
    except Exception:
        return np.nan

    slope = float(
        coeffs[0]
    )

    if not np.isfinite(slope):
        return np.nan

    alpha = -slope

    if not np.isfinite(alpha):
        return np.nan

    # Negative spectral exponents remain observable.
    # No scientific clipping is allowed.
    return f(alpha)

def block_bootstrap(
    series,
    rng,
    block_size=None,
    num_boot=100,
):
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if series.ndim != 1:
        return {
            "mean": np.nan,
            "std": np.nan,
            "ci_low": np.nan,
            "ci_high": np.nan,
        }

    n = len(series)

    if n < 256:
        return {
            "mean": np.nan,
            "std": np.nan,
            "ci_low": np.nan,
            "ci_high": np.nan,
        }

    if not np.all(
        np.isfinite(series)
    ):
        return {
            "mean": np.nan,
            "std": np.nan,
            "ci_low": np.nan,
            "ci_high": np.nan,
        }

    if block_size is None:
        block_size = max(
            64,
            n // 12,
        )

        block_size = min(
            block_size,
            n // 2,
        )

    if block_size < 8:
        return {
            "mean": np.nan,
            "std": np.nan,
            "ci_low": np.nan,
            "ci_high": np.nan,
        }

    alphas = []

    for _ in range(num_boot):

        sample = []

        while len(sample) < n:

            max_start = (
                n
                -
                block_size
            )

            if max_start <= 0:
                start = 0
            else:
                start = int(
                    rng.integers(
                        0,
                        max_start + 1,
                    )
                )

            block = series[
                start:
                start + block_size
            ]

            sample.extend(
                block.tolist()
            )

        sample = np.asarray(
            sample[:n],
            dtype=np.float64,
        )

        alpha = estimate_alpha(
            sample
        )

        if np.isfinite(alpha):
            alphas.append(
                f(alpha)
            )

    alphas = np.asarray(
        alphas,
        dtype=np.float64,
    )

    if len(alphas) < 8:
        return {
            "mean": np.nan,
            "std": np.nan,
            "ci_low": np.nan,
            "ci_high": np.nan,
        }

    return {
        "mean": f(
            np.mean(alphas)
        ),
        "std": f(
            np.std(alphas)
        ),
        "ci_low": f(
            np.percentile(
                alphas,
                2.5,
            )
        ),
        "ci_high": f(
            np.percentile(
                alphas,
                97.5,
            )
        ),
    }
