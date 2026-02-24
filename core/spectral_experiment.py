import numpy as np
from scipy.stats import zscore

def monte_carlo_threshold(n_samples=2048, n_trials=5000, alpha=0.01):
    """
    Estimate maximum z-score distribution under null hypothesis.
    Returns threshold corresponding to desired alpha.
    """
    max_vals = []

    for _ in range(n_trials):
        data = np.random.normal(0, 1, n_samples)
        fft_vals = np.fft.fft(data)
        power = np.abs(fft_vals) ** 2
        z = zscore(power)
        max_vals.append(np.max(z))

    return np.percentile(max_vals, 100 * (1 - alpha))


def run_spectral_test(data, alpha=0.01):

    fft_vals = np.fft.fft(data)
    power = np.abs(fft_vals) ** 2
    z = zscore(power)

    empirical_threshold = monte_carlo_threshold(
        n_samples=len(data),
        n_trials=2000,
        alpha=alpha
    )

    significant = np.max(z) > empirical_threshold

    return {
        "max_zscore": float(np.max(z)),
        "empirical_threshold": float(empirical_threshold),
        "significant": bool(significant)
    }
