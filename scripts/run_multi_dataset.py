import json
import numpy as np
import pandas as pd
import os

from analysis.numerical_spectral_verification import estimate_alpha


def load_sunspots():
    df = pd.read_csv("real-data/sunspots_global.csv")
    return df["Sunspots"].values.astype(float)


def load_synthetic(seed=42, n=1024):
    np.random.seed(seed)
    x = np.random.randn(n)
    for i in range(1, n):
        x[i] += 0.8 * x[i-1]
    return x


def load_noise(n=1024):
    return np.random.randn(n)


def evaluate(series):
    alpha = estimate_alpha(series)
    return float(alpha)


def main():
    os.makedirs("artifacts", exist_ok=True)

    results = {}

    # real data
    try:
        sunspots = load_sunspots()
        results["sunspots"] = evaluate(sunspots)
    except Exception as e:
        results["sunspots_error"] = str(e)

    # synthetic structured
    results["synthetic"] = evaluate(load_synthetic())

    # noise baseline
    results["noise"] = evaluate(load_noise())

    # 🔥 invariant check
    invariant = abs(results["sunspots"] - results["synthetic"]) < 0.3
    distinguishable = abs(results["sunspots"] - results["noise"]) > 0.3

    report = {
        "alphas": results,
        "checks": {
            "invariant_structure": invariant,
            "not_noise": distinguishable
        }
    }

    with open("artifacts/multi_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Multi-dataset report generated")

    if not invariant:
        raise SystemExit("❌ invariant failed")

    if not distinguishable:
        raise SystemExit("❌ not distinguishable from noise")

    print("✅ MULTI-DATASET CLAIM HOLDS")


if __name__ == "__main__":
    main()
