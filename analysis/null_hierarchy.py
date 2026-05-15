import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def white_noise_null(n, rng):
    return rng.normal(0, 1, n)

def random_walk_null(n, rng):
    return np.cumsum(rng.normal(0, 1, n))

def phase_randomized(series, rng):
    fft = np.fft.fft(series)
    mag = np.abs(fft)
    phase = rng.uniform(0, 2*np.pi, len(fft))
    return np.fft.ifft(mag * np.exp(1j * phase)).real

def evaluate_all_nulls(series, n=200, seed=42):
    rng = np.random.default_rng(seed)
    n_points = len(series)

    results = {}

    nulls = {
        "white_noise": [],
        "random_walk": [],
        "phase_randomized": []
    }

    for _ in range(n):
        nulls["white_noise"].append(
            estimate_alpha(white_noise_null(n_points, rng))
        )
        nulls["random_walk"].append(
            estimate_alpha(random_walk_null(n_points, rng))
        )
        nulls["phase_randomized"].append(
            estimate_alpha(phase_randomized(series, rng))
        )

    for k, v in nulls.items():
        v = np.array(v)
        v = v[np.isfinite(v)]

        results[k] = {
            "mean": float(np.mean(v)),
            "std": float(np.std(v)),
        }

    return results
