import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def generate_surrogate(series):
    """
    Phase randomized surrogate (preserves distribution, destroys structure)
    """
    fft = np.fft.rfft(series)
    phases = np.exp(1j * np.random.uniform(0, 2*np.pi, len(fft)))
    new_fft = np.abs(fft) * phases
    surrogate = np.fft.irfft(new_fft)
    return surrogate

def run_null_test(real_series, n=20):
    real_alpha = estimate_alpha(real_series)

    null_alphas = []

    for _ in range(n):
        surrogate = generate_surrogate(real_series)
        a = estimate_alpha(surrogate)
        null_alphas.append(a)

    null_alphas = np.array(null_alphas)

    mean_null = np.mean(null_alphas)
    std_null = np.std(null_alphas)

    z_score = (real_alpha - mean_null) / (std_null + 1e-8)

    print("Real alpha:", real_alpha)
    print("Null mean:", mean_null)
    print("Null std:", std_null)
    print("Z-score:", z_score)

    return {
        "real_alpha": real_alpha,
        "null_mean": mean_null,
        "null_std": std_null,
        "z_score": z_score,
        "pass": z_score > 2.0
    }
