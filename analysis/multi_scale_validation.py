import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def multi_scale_alpha(series):

    series = np.asarray(series, dtype=np.float64)

    scales = [1, 2, 4, 8]
    results = []

    for s in scales:

        if s > 1:
            # downsample
            scaled = series[::s]
        else:
            scaled = series

        if len(scaled) < 64:
            continue

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

    alphas = [a for _, a in results]

    std = np.std(alphas)
    mean = np.mean(alphas)

    # 🔥 شرط مهم جداً
    invariant = std < 0.4

    return {
        "scales": results,
        "mean_alpha": float(mean),
        "std_alpha": float(std),
        "scale_invariant": bool(invariant)
    }
