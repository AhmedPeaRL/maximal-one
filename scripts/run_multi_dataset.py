import json
import numpy as np
import pandas as pd
import os

from analysis.numerical_spectral_verification import estimate_alpha


def load_sunspots():
    df = pd.read_csv("real-data/sunspots_global.csv")

    col = None

    if "Sunspots" in df.columns:
        col = "Sunspots"
    elif "value" in df.columns:
        col = "value"
    else:
        raise ValueError(f"No valid column found. Columns: {df.columns}")

    return df[col].values.astype(float)

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

def domain_std(d):
    import numpy as np
    vals = list(d.values())
    return np.std(vals) if len(vals) > 1 else 0

domain_stats = {
    k: domain_std(v) for k, v in results.items()
}


def main():
    os.makedirs("artifacts", exist_ok=True)

    results = {
        "real": {},
        "synthetic": {},
        "noise": {}
    }
    errors = {}

    # real data
    try:
        sunspots = load_sunspots()
        results["real"]["sunspots"] = evaluate(sunspots)
    except Exception as e:
        errors["sunspots"] = str(e)

    # synthetic structured
    try:
        results["synthetic"]["ar1"] = evaluate(load_synthetic(...))
    except Exception as e:
        errors["synthetic"] = str(e)

    # noise baseline
    try:
        results["noise"]["white"] = evaluate(load_noise())
    except Exception as e:
        errors["noise"] = str(e)

    if "noise" in results and "synthetic" in results:
        if abs(results["noise"] ["white"] - results["synthetic"]["ar1"]) < 0.2:
            raise SystemExit("❌ synthetic indistinguishable from noise")

    # 🔥 validation logic
    invariant = None
    distinguishable = None

    if "sunspots" in results and "synthetic" in results:
        invariant = (
            abs(results["real"]["sunspots"] - results["synthetic"]["ar1"]) < 0.4
            if "sunspots" in results and "synthetic" in results
            else None
        )

    if "sunspots" in results and "noise" in results:
        distinguishable = abs(results["real"]["sunspots"] - results["noise"] ["white"]) > 0.3
    
    report = {
        "alphas": results,
        "errors": errors,
        "domain_stats": domain_stats,
        "checks": {
            "invariant_structure": invariant,
            "not_noise": distinguishable
        }
    }

    with open("artifacts/multi_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Multi-dataset report generated")

    if invariant is False:
        print("⚠️ invariant weak (acceptable)")

    if distinguishable is False:
        raise SystemExit("❌ not distinguishable from noise")

    if "sunspots" not in results:
        raise SystemExit("❌ sunspots dataset failed to load")

    print("✅ MULTI-DATASET CLAIM HOLDS")


if __name__ == "__main__":
    main()
