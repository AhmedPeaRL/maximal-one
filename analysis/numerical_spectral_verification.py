import numpy as np
from scipy import stats

def estimate_alpha(series):
    """
    Estimate spectral scaling exponent alpha
    using log-log regression of FFT amplitude spectrum.
    """

    n = len(series)
    freqs = np.fft.rfftfreq(n)[1:]
    spectrum = np.abs(np.fft.rfft(series))[1:]

    log_freqs = np.log(freqs)
    log_spec = np.log(spectrum)

    slope, intercept, r_value, p_value, std_err = stats.linregress(log_freqs, log_spec)

    alpha = -slope
    return alpha


def generate_reference_series(n=5000, seed=42):
    np.random.seed(seed)
    return np.random.normal(0, 1, n)


if __name__ == "__main__":

    series = generate_reference_series()
    alpha = estimate_alpha(series)

    result = {
        "estimated_alpha": float(alpha),
        "reference_half": 0.5
    }

    print("==== SPECTRAL PROFILE ====")
    print(result)
