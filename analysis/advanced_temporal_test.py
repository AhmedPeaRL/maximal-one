import json
import numpy as np
import pathlib
from numpy.fft import fft, ifft

ART = pathlib.Path("artifacts")

def load_series(name):
    p = ART / name
    if p.exists():
        return np.array(json.loads(p.read_text()))
    return None

# ===== Surrogate generators =====

def shuffled(x):
    return np.random.permutation(x)

def phase_randomized(x):
    X = fft(x)
    phases = np.angle(X)
    mag = np.abs(X)

    rand_phases = np.random.uniform(0, 2*np.pi, len(phases))
    X_new = mag * np.exp(1j * rand_phases)

    return np.real(ifft(X_new))

def ar1_surrogate(x):
    phi = np.corrcoef(x[:-1], x[1:])[0,1]
    noise = np.random.normal(size=len(x))
    s = np.zeros_like(x)
    for i in range(1, len(x)):
        s[i] = phi * s[i-1] + noise[i]
    return s

# ===== metric =====

def autocorr(x, lag=1):
    return np.corrcoef(x[:-lag], x[lag:])[0,1]

def temporal_score(x, y, max_lag=50):
    ac_x = np.array([autocorr(x, l) for l in range(1, max_lag)])
    ac_y = np.array([autocorr(y, l) for l in range(1, max_lag)])
    return float(np.mean(np.abs(ac_x) - np.abs(ac_y)))

systems = ["sunspots"]

results = {}

for name in systems:
    real = load_series(f"{name}_real.json")

    if real is None or len(real) < 1000:
        continue

    tests = {
        "shuffled": shuffled(real),
        "phase_randomized": phase_randomized(real),
        "ar1": ar1_surrogate(real)
    }

    scores = {}

    for k, surr in tests.items():
        score = temporal_score(real, surr)
        scores[k] = score

    # 🔥 القرار الحقيقي
    strong = all(v > 0.01 for v in scores.values())

    results[name] = {
        "scores": scores,
        "nontrivial_temporal_structure": strong
    }

final = {
    "systems": results,
    "breaks_all_surrogates": any(
        v["nontrivial_temporal_structure"] for v in results.values()
    )
}

(ART / "advanced_temporal_test.json").write_text(json.dumps(final, indent=2))

print("==== ADVANCED TEMPORAL TEST ====")
print(json.dumps(final, indent=2))
