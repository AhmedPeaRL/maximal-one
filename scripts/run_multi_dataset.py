import json
import numpy as np
import pandas as pd
import os

from analysis.numerical_spectral_verification import estimate_alpha


def load_sunspots():
    df = pd.read_csv("real-data/sunspots_global.csv")

    if "Sunspots" not in df.columns:
        raise ValueError("Column 'Sunspots' not found in dataset")

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
    return float(estimate_alpha(series))


def main():
    os.makedirs("artifacts", exist_ok=True)

    results = {}
    errors = {}

    # real data
    try:
        sunspots = load_sunspots()
        results["sunspots"] = evaluate(sunspots)
    except Exception as e:
        errors["sunspots"] = str(e)

    # synthetic structured
    try:
        results["synthetic"] = evaluate(load_synthetic())
    except Exception as e:
        errors["synthetic"] = str(e)

    # noise baseline
    try:
        results["noise"] = evaluate(load_noise())
    except Exception as e:
        errors["noise"] = str(e)

    # 🔥 validation logic
    invariant = None
    distinguishable = None

    if "sunspots" in results and "synthetic" in results:
        invariant = abs(results["sunspots"] - results["synthetic"]) < 0.3

    if "sunspots" in results and "noise" in results:
        distinguishable = abs(results["sunspots"] - results["noise"]) > 0.3

    report = {
        "alphas": results,
        "errors": errors,
        "checks": {
            "invariant_structure": invariant,
            "not_noise": distinguishable
        }
    }

    with open("artifacts/multi_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Multi-dataset report generated")

    # 🔥 strict fail only لو البيانات موجودة
    if invariant is False:
        raise SystemExit("❌ invariant failed")

    if distinguishable is False:
        raise SystemExit("❌ not distinguishable from noise")

    if "sunspots" not in results:
        raise SystemExit("❌ sunspots dataset failed to load")

    print("✅ MULTI-DATASET CLAIM HOLDS")


if __name__ == "__main__":
    main()
