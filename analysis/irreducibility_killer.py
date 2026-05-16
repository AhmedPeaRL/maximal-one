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
        a = estimate_alpha(s)
        if np.isfinite(a):
            surrogate_alphas.append(a)

    surrogate_alphas = np.array(surrogate_alphas)

    if len(surrogate_alphas) < 5:
        return {
            "real_alpha": real_alpha,
            "surrogate_mean": np.nan,
            "surrogate_std": np.nan,
            "z_score": np.nan,
            "irreducible": False
        }

    mean = np.mean(surrogate_alphas)
    std = np.std(surrogate_alphas)

    if not np.isfinite(real_alpha) or std < 1e-12:
        return {
            "real_alpha": real_alpha,
            "surrogate_mean": mean,
            "surrogate_std": std,
            "z_score": np.nan,
            "irreducible": False
        }

    z = (real_alpha - mean) / (std + 1e-12)

    threshold = 2.5

    return {
        "real_alpha": real_alpha,
        "surrogate_mean": mean,   # ✅ FIXED
        "surrogate_std": std,
        "z_score": z,
        "irreducible": abs(z) > threshold
    }

def extract_series(df):
    if "value" in df.columns:
        return df["value"].values
    elif "Sunspots" in df.columns:
        return df["Sunspots"].values
    else:
        raise ValueError("Dataset must contain 'value' or 'Sunspots'")

if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("real-data/sunspots_global_extended.csv")
    series = extract_series(df)

    r = irreducibility_test(series)

    print("=== IRREDUCIBILITY TEST ===")
    print("Real alpha:", r["real_alpha"])
    print("Surrogate mean:", r["surrogate_mean"])
    print("Z-score:", r["z_score"])

    if r["irreducible"]:
        print("✅ STRUCTURE IRREDUCIBLE TO SURROGATE")
    else:
        print("⚠️ Still explainable by surrogate")
