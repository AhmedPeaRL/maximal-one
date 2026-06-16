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
    series = np.asarray(series, dtype=np.float64)

    if len(series) < 256:
        return np.nan

    if not np.all(np.isfinite(series)):
        return np.nan

    if np.std(series) < 1e-8:
        return np.nan

    # 🔥 remove mean
    series = series - np.mean(series)

    # 🔥 detect integrated processes
    diff_std = np.std(np.diff(series))

    raw_std = np.std(series)

    integration_ratio = raw_std / (diff_std + 1e-12)

    # 🔥 adaptive detrending
    if integration_ratio > 8.0:
        alpha_raw = alpha_from_raw()
        alpha_diff = alpha_from_diff()
        alpha = min(
            alpha_raw,
            alpha_diff
        )

    # normalize
    std = np.std(series)

    if std < 1e-12:
        return np.nan

    series = series / std

    freqs, psd = welch(
        series,
        nperseg=min(256, len(series)//2),
        window="hann",
        detrend="linear",
        scaling="density"
    )

    mask = (
        (freqs > 0.01)
        & (freqs < 0.25)
        & np.isfinite(psd)
        & (psd > 0)
    )

    freqs = freqs[mask]
    psd = psd[mask]

    if len(freqs) < 20:
        return np.nan

    log_f = np.log(freqs)
    log_psd = np.log(psd)

    try:
        coeffs = np.polyfit(log_f, log_psd, 1)
        slope = coeffs[0]
    except Exception:
        return np.nan

    alpha = float(-slope)

    if not np.isfinite(alpha):
        return np.nan

    # numerical tolerance zone
    if alpha < 0:
        if alpha > -0.20:
            alpha = 0.0
        else:
            return np.nan

    alpha = min(alpha, 3.0)

    return float(alpha)
    
def block_bootstrap(
    series,
    rng,
    block_size=None,
    num_boot=100
):

    if block_size is None:
        block_size = max(
            256,
            len(series)//12
        )
        block_size = min(
            block_size,
            len(series)//2
        )

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

        if len(sample) < 256:
            sample = np.pad(sample, (0, 256-len(sample)), mode='reflect')

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
