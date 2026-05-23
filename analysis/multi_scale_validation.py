import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def downsample(series, factor):
    n = len(series) // factor
    return np.array([
        np.mean(series[i*factor:(i+1)*factor])
        for i in range(n)
    ], dtype=np.float64)

def multi_scale_alpha(series):
    series = np.asarray(series, dtype=np.float64)

    scales = [1, 2, 4, 8]
    results = []

    for s in scales:

        if s > 1:
            # downsample
            scaled = downsample(series, s)
        else:
            scaled = series

        if len(scaled) < 64:
            continue

        if len(scaled) < 256:
            scaled = np.pad(scaled, (0, 256-len(scaled)), mode='wrap')

        alpha = estimate_alpha(scaled)

        if np.isfinite(alpha):
            results.append((s, float(alpha)))

    return results

def evaluate_scale_invariance(series):
    results = multi_scale_alpha(series)

    if len(results) < 3:
        return {
            "valid": False,
            "reason": "insufficient_scales"
        }

    alphas = np.array([a for _, a in results])

    # 🔥 robust metric بدل std العادي
    median = np.median(alphas)
    mad = np.median(np.abs(alphas - median)) + 1e-12

    # 🔥 normalized dispersion
    dispersion = mad / (np.abs(median) + 1e-12)

    # 🔥 dynamic threshold based on scale count
    threshold = 0.25 + 0.1 * len(results)

    if any(a == 0.0 for _, a in results[1:]):
        return {
            "valid": False,
            "reason": "scale collapse detected"
        }

    return {
        "scales": results,
        "median_alpha": float(median),
        "mad_alpha": float(mad),
        "dispersion": float(dispersion),
        "scale_invariant": bool(dispersion < threshold)
    }
