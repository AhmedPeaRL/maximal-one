import numpy as np
import pandas as pd
from statsmodels.tsa.arima_process import ArmaProcess
from analysis.numerical_spectral_verification import estimate_alpha


# =========================
# 🔹 DATA LOADER
# =========================
def load_series(path):
    df = pd.read_csv(path)

    for col in ["value", "Sunspots"]:
        if col in df.columns:
            series = df[col].values.astype(float)
            if len(series) < 20:
                raise ValueError("Series too short")
            return series

    raise ValueError("No valid column found")


# =========================
# 🔹 CORE UTILITIES
# =========================

def empirical_p_value(real, null):
    """
    two-sided empirical p-value
    """
    null = np.array(null)
    extreme = np.sum(np.abs(null) >= np.abs(real))
    return (extreme + 1) / (len(null) + 1)


def sanity_check(series):
    if np.std(series) < 1e-8:
        raise ValueError("Degenerate series (zero variance)")

    if len(series) < 30:
        raise ValueError("Too short for spectral inference")


# =========================
# 🔹 NULL MODELS (STRONG)
# =========================

def generate_arima_like(series):
    ar = np.array([1, -0.95])
    ma = np.array([1])
    arma = ArmaProcess(ar, ma)
    return arma.generate_sample(nsample=len(series))


def generate_fbm_like(series):
    noise = np.random.randn(len(series))
    return np.cumsum(noise)


def phase_randomize(series):
    fft = np.fft.rfft(series)
    magnitude = np.abs(fft)

    random_phase = np.random.uniform(0, 2*np.pi, len(magnitude))
    fft_new = magnitude * np.exp(1j * random_phase)

    return np.fft.irfft(fft_new, n=len(series))


def block_shuffle(series, block_size=None):
    n = len(series)

    if block_size is None:
        block_size = max(5, n // 10)

    blocks = [series[i:i+block_size] for i in range(0, n, block_size)]
    np.random.shuffle(blocks)

    return np.concatenate(blocks)[:n]


# 🔥🔥🔥 IAAFT (killer surrogate)
def iaaft_surrogate(series, iterations=50):
    sorted_series = np.sort(series)
    surrogate = np.random.permutation(series)

    target_fft = np.abs(np.fft.rfft(series))

    for _ in range(iterations):
        # enforce spectrum
        fft = np.fft.rfft(surrogate)
        fft = target_fft * np.exp(1j * np.angle(fft))
        surrogate = np.fft.irfft(fft, n=len(series))

        # enforce distribution
        ranks = np.argsort(np.argsort(surrogate))
        surrogate = sorted_series[ranks]

    return surrogate


# =========================
# 🔹 CORE ENGINE
# =========================

def compute_null_distribution(series, generator, n=200):
    alphas = []
    for _ in range(n):
        surr = generator(series)
        alphas.append(estimate_alpha(surr))
    return np.array(alphas)


def advanced_null_test(series):

    sanity_check(series)

    real_alpha = estimate_alpha(series)

    generators = {
        "ARIMA": generate_arima_like,
        "FBM": generate_fbm_like,
        "Phase": phase_randomize,
        "Block": block_shuffle,
        "IAAFT": iaaft_surrogate
    }

    results = {}
    global_null = []

    for name, gen in generators.items():

        null_dist = compute_null_distribution(series, gen)

        z = (real_alpha - np.mean(null_dist)) / (np.std(null_dist) + 1e-12)
        p = empirical_p_value(real_alpha, null_dist)

        results[name] = {
            "mean": float(np.mean(null_dist)),
            "std": float(np.std(null_dist)),
            "z_score": float(z),
            "p_value": float(p),
            "irreducible": bool(p < 0.01)
        }

        global_null.extend(null_dist)

    # =========================
    # 🔥 GLOBAL TEST
    # =========================

    global_null = np.array(global_null)

    global_z = (real_alpha - np.mean(global_null)) / (np.std(global_null) + 1e-12)
    global_p = empirical_p_value(real_alpha, global_null)

    # rank test
    rank = np.sum(global_null < real_alpha) / len(global_null)

    verdict = {
        "global_mean": float(np.mean(global_null)),
        "global_std": float(np.std(global_null)),
        "global_z": float(global_z),
        "global_p": float(global_p),
        "rank_position": float(rank),
        "strong_irreducibility": bool(global_p < 0.005 and (rank < 0.05 or rank > 0.95))
    }

    return real_alpha, results, verdict


# =========================
# 🔹 ENTRY
# =========================

if __name__ == "__main__":

    series = load_series("real-data/sunspots_global_extended.csv")

    real_alpha, res, verdict = advanced_null_test(series)

    print("=== ADVANCED NULL KILLER (HARDCORE) ===")
    print("Real alpha:", real_alpha)

    for k, v in res.items():
        print(f"\n[{k}]")
        for kk, vv in v.items():
            print(f"{kk}: {vv}")

    print("\n=== GLOBAL VERDICT ===")
    for k, v in verdict.items():
        print(f"{k}: {v}")

    print("=== END ===")
