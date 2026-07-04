import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.strong_null_model import generate_strong_null

def monte_carlo_p_value(
    series,
    observed_alpha,
    rng,
    trials=20000
):

    n = len(series)

    null_alphas = []

    for _ in range(trials):

        sample = generate_strong_null(
            n,
            rng
        )

        if len(sample) < 256:
            sample = np.pad(
                sample,
                (0, 256 - len(sample)),
                mode="reflect"
            )

        a = estimate_alpha(sample)

        if np.isfinite(a):
            null_alphas.append(float(a))

    null_alphas = np.asarray(
        null_alphas,
        dtype=np.float64
    )

    if len(null_alphas) < 20:

        return {
            "observed_alpha": float(observed_alpha),
            "null_mean": np.nan,
            "null_std": np.nan,
            "null_median": np.nan,
            "observed_gap": np.nan,
            "p_value": 1.0,
            "null_samples": 0
        }

    p_value = float(
        np.mean(
            null_alphas >= observed_alpha
        )
    )

    p_value = max(
        p_value,
        1.0 / len(null_alphas)
    )

    filtered_fraction = (
        len(null_alphas)
        / trials
    )

    return {

        "observed_alpha":
            float(observed_alpha),

        "null_mean":
            float(np.mean(null_alphas)),

        "null_std":
            float(np.std(null_alphas)),

        "null_median":
            float(np.median(null_alphas)),

        "observed_gap":
            float(
                observed_alpha
                - np.median(null_alphas)
            ),

        "p_value":
            float(p_value),

        "null_samples":
            int(len(null_alphas)),

        "filtered_fraction":
        float(filtered_fraction)
    }
