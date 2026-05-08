import numpy as np
from scipy.signal import welch
from scipy.ndimage import uniform_filter1d

np.set_printoptions(precision=15)


def robust_local_slopes(
    log_f,
    log_psd,
    window=7
):

    slopes = []

    n = len(log_f)

    if n < (window + 3):
        return np.nan

    for i in range(n - window):

        x = log_f[i:i + window]
        y = log_psd[i:i + window]

        if (
            not np.all(np.isfinite(x))
            or not np.all(np.isfinite(y))
        ):
            continue

        # reject flat regions
        if np.std(y) < 1e-6:
            continue

        try:

            coeffs = np.polyfit(x, y, 1)

            slope = coeffs[0]

        except Exception:
            continue

        if np.isfinite(slope):
            slopes.append(float(slope))

    slopes = np.asarray(
        slopes,
        dtype=np.float64
    )

    if len(slopes) < 8:
        return np.nan

    median = np.median(slopes)

    mad = (
        np.median(
            np.abs(slopes - median)
        ) + 1e-12
    )

    filtered = slopes[
        np.abs(slopes - median)
        < 2.5 * mad
    ]

    if len(filtered) < 6:
        return np.nan

    # weighted center
    q1 = np.percentile(filtered, 25)
    q3 = np.percentile(filtered, 75)

    core = filtered[
        (filtered >= q1)
        & (filtered <= q3)
    ]

    if len(core) < 4:
        core = filtered

    return float(np.mean(core))


def estimate_alpha(series):

    series = np.asarray(
        series,
        dtype=np.float64
    )

    if not np.all(np.isfinite(series)):
        return np.nan

    series = series - np.mean(series)

    n = len(series)

    if n < 64:
        return np.nan

    freqs, psd = welch(
        series,
        window="hann",
        detrend="constant",
        scaling="density",
        nperseg=min(128, n)
    )

    mask = (
        (freqs > 0.02)
        & (freqs < 0.25)
    )

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 12:
        return np.nan

    psd = uniform_filter1d(
        psd,
        size=3
    )

    psd = np.maximum(psd, 1e-12)

    log_f = np.log(freqs)
    log_psd = np.log(psd)

    slope = robust_local_slopes(
        log_f,
        log_psd,
        window=5
    )

    if not np.isfinite(slope):
        return np.nan

    # بدل crash كامل
    if slope > 0:
        slope = -abs(slope)

    alpha = float(-slope)

    if not np.isfinite(alpha):
        return np.nan

    if alpha < 0:
        return np.nan

    if alpha > 8:
        return np.nan

    return float(alpha)


def block_bootstrap(
    series,
    rng,
    block_size=16,
    num_boot=100
):

    series = np.asarray(
        series,
        dtype=np.float64
    )

    n = len(series)

    alphas = []

    for _ in range(num_boot):

        sample = []

        while len(sample) < n:

            start = rng.integers(
                0,
                n - block_size
            )

            block = series[
                start:start + block_size
            ]

            sample.extend(block)

        sample = np.asarray(
            sample[:n],
            dtype=np.float64
        )

        alpha = estimate_alpha(sample)

        if np.isfinite(alpha):
            alphas.append(alpha)

    alphas = np.asarray(
        alphas,
        dtype=np.float64
    )

    if len(alphas) < 8:

        return {
            "mean": np.nan,
            "std": np.nan,
            "ci_low": np.nan,
            "ci_high": np.nan
        }

    return {
        "mean": float(np.mean(alphas)),
        "std": float(np.std(alphas)),
        "ci_low": float(np.percentile(alphas, 2.5)),
        "ci_high": float(np.percentile(alphas, 97.5))
    }
