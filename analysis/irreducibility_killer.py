import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def generate_surrogate(series):
    """
    Phase randomization surrogate (preserves distribution, kills structure)
    """
    fft_vals = np.fft.rfft(series)
    phases = np.exp(1j * np.random.uniform(0, 2*np.pi, len(fft_vals)))
    new_fft = np.abs(fft_vals) * phases
    surrogate = np.fft.irfft(new_fft)
    return surrogate


def irreducibility_test(series, n=50):
    real_alpha = estimate_alpha(series)

    surrogate_alphas = []

    for _ in range(n):
        s = generate_surrogate(series)
        surrogate_alphas.append(estimate_alpha(s))

    surrogate_alphas = np.array(surrogate_alphas)

    mean = np.mean(surrogate_alphas)
    std = np.std(surrogate_alphas)

    z = (real_alpha - mean) / (std + 1e-12)

    return {
        "real_alpha": real_alpha,
        "surrogate_mean": mean,
        "surrogate_std": std,
        "z_score": z,
        "irreducible": abs(z) > 2.5
    }


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("real-data/sunspots_global.csv")
    series = df["value"].values

    r = irreducibility_test(series)

    print("=== IRREDUCIBILITY TEST ===")
    print("Real alpha:", r["real_alpha"])
    print("Surrogate mean:", r["surrogate_mean"])
    print("Z-score:", r["z_score"])

    if r["irreducible"]:
        print("✅ STRUCTURE IRREDUCIBLE TO SURROGATE")
    else:
        print("⚠️ Still explainable by surrogate")
