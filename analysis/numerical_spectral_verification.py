from __future__ import annotations
import numpy as np
from scipy.signal import welch

FREEZE_DECIMALS = 8

def f(x):
    return float(np.round(float(x), FREEZE_DECIMALS))

def estimate_alpha(series):
    """
    Estimate spectral exponent alpha from a PSD power-law region.

    IMPORTANT:
    This function measures alpha.
    It does NOT clip, force, or otherwise alter a valid estimate
    to make it fit an expected scientific range.
    """

    series = np.asarray(series, dtype=np.float64)

    if series.ndim != 1:
        return np.nan

    if len(series) < 256:
        return np.nan

    if not np.all(np.isfinite(series)):
        return np.nan

    if np.std(series) < 1e-8:
        return np.nan

    series = series - np.mean(series)

    std = np.std(series)

    if std < 1e-12:
        return np.nan

    series = series / std

    nperseg = min(256, len(series) // 2)

    if nperseg < 128:
        return np.nan

    freqs, psd = welch(
        series,
        nperseg=nperseg,
        window="hann",
        detrend="linear",
        scaling="density",
    )

    mask = (
        (freqs > 0.01)
        & (freqs < 0.25)
        & np.isfinite(freqs)
        & np.isfinite(psd)
        & (psd > 0)
    )

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 20:
        return np.nan

    log_f = np.log(freqs)
    log_psd = np.log(psd)

    if not (
        np.all(np.isfinite(log_f))
        and np.all(np.isfinite(log_psd))
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

    slope = float(coeffs[0])

    if not np.isfinite(slope):
        return np.nan

    alpha = -slope

    if not np.isfinite(alpha):
        return np.nan

    # Tiny negative numerical excursions may be treated as zero.
    if alpha < 0:
        if alpha > -0.20:
            alpha = 0.0
        else:
            return np.nan

    # NO SCIENTIFIC CLIPPING.
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

    if not np.all(np.isfinite(series)):
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
            max_start = n - block_size

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
                start:start + block_size
            ]

            sample.extend(block.tolist())

        sample = np.asarray(
            sample[:n],
            dtype=np.float64,
        )

        alpha = estimate_alpha(sample)

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
        "mean": f(np.mean(alphas)),
        "std": f(np.std(alphas)),
        "ci_low": f(np.percentile(alphas, 2.5)),
        "ci_high": f(np.percentile(alphas, 97.5)),
    }
