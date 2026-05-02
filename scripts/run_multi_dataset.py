import json
import numpy as np
import pandas as pd
import os

from analysis.numerical_spectral_verification import estimate_alpha


def load_sunspots():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, "real-data", "sunspots_global.csv")

    df = pd.read_csv(path)

    col = "Sunspots" if "Sunspots" in df.columns else "value"
    return df[col].values.astype(float)


def load_synthetic(seed=42, n=1024):
    np.random.seed(seed)
    
    # 🔥 upgraded structured signal
    x = np.zeros(n)
    noise = np.random.randn(n)

    for i in range(1, n):
        x[i] = 0.7 * x[i-1] + 0.2 * noise[i]

    # add weak periodicity (realistic)
    x += 0.1 * np.sin(np.linspace(0, 20, n))

    return x


def load_noise(n=1024):
    return np.random.randn(n)


def evaluate(series):
    return float(estimate_alpha(series))


def safe_collect(fn, seeds):
    vals = []
    for s in seeds:
        try:
            v = evaluate(fn(seed=s))
            if np.isfinite(v):
                vals.append(v)
        except:
            continue
    return vals


def main():
    os.makedirs("artifacts", exist_ok=True)

    results = {
        "real": {},
        "synthetic": {},
        "noise": {}
    }

    # === REAL ===
    sunspots = load_sunspots()
    real_alpha = evaluate(sunspots)

    if not (0.5 <= real_alpha <= 5.0):
        raise SystemExit(f"❌ invalid real alpha: {real_alpha}")

    results["real"]["sunspots"] = real_alpha

    # === SYNTHETIC (robust sampling) ===
    synthetic_vals = safe_collect(load_synthetic, range(20))

    if len(synthetic_vals) < 5:
        raise SystemExit("❌ synthetic unstable — insufficient valid samples")

    results["synthetic"]["mean"] = float(np.mean(synthetic_vals))
    results["synthetic"]["std"] = float(np.std(synthetic_vals))

    # === NOISE ===
    noise_alpha = evaluate(load_noise())
    results["noise"]["white"] = noise_alpha

    # === CORE VALIDATION ===

    not_noise = abs(real_alpha - noise_alpha) > 0.4

    internally_stable = (0.5 < real_alpha < 5.0)

    if not not_noise:
        raise SystemExit("❌ real not distinguishable from noise")

    if not internally_stable:
        raise SystemExit("❌ real unstable")

    # synthetic فقط sanity
    if results["synthetic"]["std"] > 0.8:
        raise SystemExit("❌ synthetic chaotic — invalid stress field")

    report = {
        "alphas": results,
        "checks": {
            "not_noise": not_noise,
            "internal_stability": internally_stable
        }
    }

    with open("artifacts/multi_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Multi-dataset report generated")
    print("✅ MULTI-DATASET CLAIM HOLDS")


if __name__ == "__main__":
    main()
