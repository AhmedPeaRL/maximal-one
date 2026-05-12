import numpy as np
from scipy.signal import welch
from scipy.ndimage import uniform_filter1d

np.set_printoptions(precision=15)

FREEZE_DECIMALS = 8


def f(x):
    return float(np.round(float(x), FREEZE_DECIMALS))


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

        x = np.asarray(
            log_f[i:i + window],
            dtype=np.float64
        )

        y = np.asarray(
            log_psd[i:i + window],
            dtype=np.float64
        )

        if (
            not np.all(np.isfinite(x))
            or not np.all(np.isfinite(y))
        ):
            continue

        if np.std(y) < 1e-6:
            continue

        try:

            coeffs = np.polyfit(
                x,
                y,
                1
            )

            slope = f(coeffs[0])

        except Exception:
            continue

        if np.isfinite(slope):
            slopes.append(slope)

    slopes = np.asarray(
        slopes,
        dtype=np.float64
    )

    if len(slopes) < 8:
        return np.nan

    slopes = np.round(
        slopes,
        FREEZE_DECIMALS
    )

    median = f(np.median(slopes))

    mad = f(
        np.median(
            np.abs(slopes - median)
        ) + 1e-12
    )

    filtered = slopes[
        np.abs(slopes - median)
        < 2.5 * mad
    ]

    if len(filtered) < 4:
        filtered = slopes

    filtered = np.round(
        filtered,
        FREEZE_DECIMALS
    )

    q1 = f(
        np.percentile(filtered, 25)
    )

    q3 = f(
        np.percentile(filtered, 75)
    )

    core = filtered[
        (filtered >= q1)
        & (filtered <= q3)
    ]

    if len(core) < 4:
        core = filtered

    return f(np.mean(core))


def estimate_alpha(series):

    series = np.asarray(
        series,
        dtype=np.float64
    )

    if not np.all(np.isfinite(series)):
        return np.nan

    series = series - f(np.mean(series))

    n = len(series)

    if n < 64:
        return np.nan

    freqs, psd = welch(
        series,
        window="hann",
        detrend="constant",
        scaling="density",
        nperseg=min(128, n),
        average="median"
    )

    freqs = np.round(freqs, FREEZE_DECIMALS)
    psd = np.round(psd, FREEZE_DECIMALS)

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
        size=5,
        mode="nearest"
    )

    psd = np.round(
        psd,
        FREEZE_DECIMALS
    )

    psd = np.maximum(psd, 1e-12)

    log_f = np.round(
        np.log(freqs),
        FREEZE_DECIMALS
    )

    log_psd = np.round(
        np.log(psd),
        FREEZE_DECIMALS
    )

    slope = robust_local_slopes(
        log_f,
        log_psd,
        window=9
    )

    if not np.isfinite(slope):
        return np.nan

    alpha = f(max(0.0, -slope))

    if not np.isfinite(alpha):
        return np.nan

    if alpha > 5:
        return np.nan

    return f(alpha)


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
            alphas.append(f(alpha))

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
        "mean": f(np.mean(alphas)),
        "std": f(np.std(alphas)),
        "ci_low": f(np.percentile(alphas, 2.5)),
        "ci_high": f(np.percentile(alphas, 97.5))
        }
