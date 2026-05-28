import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def monte_carlo_p_value(series, observed_alpha, rng, trials=5000):
    null_alphas = []

    n = len(series)

    for _ in range(trials):
        from analysis.strong_null_model import generate_strong_null

        wn = generate_strong_null(n, rng)
        
        if len(wn) < 256:
            wn = np.pad(wn, (0, 256-len(wn)), mode='reflect')

        alpha = estimate_alpha(wn)

        if np.isfinite(alpha):
            null_alphas.append(alpha)

    null_alphas = np.array(null_alphas)

    if len(null_alphas) < 20:
        return {
            "observed_alpha": float(observed_alpha),
            "null_mean": np.nan,
            "null_std": np.nan,
            "p_value": 1.0
        }

    distance = np.abs(
        null_alphas - np.median(null_alphas)
    )

    observed_distance = abs(
        observed_alpha - np.median(null_alphas)
    )

    p_value = max(
        1e-6,
        float(
            np.mean(
                distance >= observed_distance
            )
        )
    )

    return {
        "observed_alpha": float(observed_alpha),
        "null_mean": float(np.mean(null_alphas)),
        "null_std": float(np.std(null_alphas)),
        "p_value": float(p_value),
        "null_samples": int(len(null_alphas))
    }
