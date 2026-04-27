import numpy as np
import pandas as pd
from statsmodels.tsa.arima_process import ArmaProcess
from analysis.numerical_spectral_verification import estimate_alpha


# =========================
# 🔹 DATA LOADER (UNIFIED)
# =========================
def load_series(path):
    df = pd.read_csv(path)

    if "value" in df.columns:
        return df["value"].values

    elif "Sunspots" in df.columns:
        return df["Sunspots"].values

    else:
        raise ValueError("Dataset must contain 'value' or 'Sunspots' column")


# =========================
# 🔹 NULL MODELS
# =========================

def generate_arima_like(series):
    ar = np.array([1, -0.9])
    ma = np.array([1])
    arma = ArmaProcess(ar, ma)
    return arma.generate_sample(nsample=len(series))


def generate_fbm_like(series):
    noise = np.random.normal(0, 1, len(series))
    return np.cumsum(noise)


def phase_randomize(series):
    fft = np.fft.rfft(series)
    magnitude = np.abs(fft)
    phase = np.angle(fft)

    random_phase = np.random.uniform(0, 2*np.pi, len(phase))
    fft_new = magnitude * np.exp(1j * random_phase)

    return np.fft.irfft(fft_new, n=len(series))


def block_shuffle(series, block_size=10):
    series = np.array(series)
    n = len(series)

    blocks = [series[i:i+block_size] for i in range(0, n, block_size)]
    np.random.shuffle(blocks)

    return np.concatenate(blocks)[:n]


# =========================
# 🔹 CORE TEST
# =========================

def compute_null_distribution(series, generator, n=100):
    alphas = []
    for _ in range(n):
        surr = generator(series)
        alphas.append(estimate_alpha(surr))
    return np.array(alphas)


def z_score(real, null):
    return (real - np.mean(null)) / (np.std(null) + 1e-12)


def advanced_null_test(series):

    real_alpha = estimate_alpha(series)

    null_generators = {
        "ARIMA_like": generate_arima_like,
        "FBM_like": generate_fbm_like,
        "Phase_randomized": phase_randomize,
        "Block_shuffled": block_shuffle
    }

    results = {}
    global_null = []

    for name, gen in null_generators.items():
        null_dist = compute_null_distribution(series, gen, n=100)

        z = z_score(real_alpha, null_dist)

        results[name] = {
            "mean": float(np.mean(null_dist)),
            "std": float(np.std(null_dist)),
            "z_score": float(z),
            "irreducible": bool(abs(z) > 2.5)
        }

        global_null.extend(null_dist)

    # =========================
    # 🔥 GLOBAL TEST (REAL WEAPON)
    # =========================

    global_null = np.array(global_null)

    global_z = z_score(real_alpha, global_null)

    verdict = {
        "global_mean": float(np.mean(global_null)),
        "global_std": float(np.std(global_null)),
        "global_z": float(global_z),
        "strong_irreducibility": bool(abs(global_z) > 3.0)
    }

    return real_alpha, results, verdict


# =========================
# 🔹 ENTRY POINT
# =========================

if __name__ == "__main__":

    series = load_series("real-data/sunspots_global.csv")

    real_alpha, res, verdict = advanced_null_test(series)

    print("=== ADVANCED NULL KILLER (FULL) ===")
    print("Real alpha:", real_alpha)

    for model, stats in res.items():
        print(f"\n[{model}]")
        print("mean:", stats["mean"])
        print("std:", stats["std"])
        print("z_score:", stats["z_score"])
        print("irreducible:", stats["irreducible"])

    print("\n=== GLOBAL VERDICT ===")
    print("mean:", verdict["global_mean"])
    print("std:", verdict["global_std"])
    print("z_score:", verdict["global_z"])
    print("strong_irreducibility:", verdict["strong_irreducibility"])

    print("=== END ===")
