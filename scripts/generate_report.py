import json
import argparse
import numpy as np
import os
import traceback
import time

from analysis.numerical_spectral_verification import estimate_alpha


def generate_series(seed, n=1024):
    np.random.seed(seed)

    # chaotic-like signal (not trivial random)
    x = np.random.randn(n)

    # introduce temporal structure
    for i in range(1, n):
        x[i] += 0.8 * x[i-1]

    return x


def bootstrap_alpha(series, num_boot=100):
    n = len(series)
    alphas = []

    for _ in range(num_boot):
        idx = np.random.randint(0, n, n)
        sample = series[idx]
        alphas.append(estimate_alpha(sample))

    alphas = np.array(alphas)

    return {
        "mean": float(np.mean(alphas)),
        "std": float(np.std(alphas)),
        "ci_low": float(np.percentile(alphas, 2.5)),
        "ci_high": float(np.percentile(alphas, 97.5))
    }


def stable_float(x, digits=10):
    return float(round(x, digits))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--canonical", action="store_true")
    args = parser.parse_args()
    np.random.seed(args.seed)
    white_noise = np.random.RandomState(args.seed + 999).randn(len(series))

    os.makedirs("artifacts", exist_ok=True)

    try:
        if args.canonical:
            series = real.copy()
        else:
            series = synthetic[:len(real)]

        import pandas as pd
        df = pd.read_csv("real-data/sunspots_global.csv")

        if "value" in df.columns:
            real = df["value"].values
        elif "Sunspots" in df.columns:
            real = df["Sunspots"].values
        else:
            raise ValueError("No valid column")

        series = real.copy()

        print("Real length:", len(real))
        print("Synthetic length:", len(synthetic))
        print("Series sample:", series[:5])

        white_noise = np.random.randn(len(series))
        alpha_noise = estimate_alpha(white_noise)
        alpha = estimate_alpha(series)
        boot = bootstrap_alpha(series)
    
        report = {
            "spectral_profile": {
                "estimated_alpha": stable_float(alpha),
                "bootstrap_mean": stable_float(boot["mean"]),
                "bootstrap_std": stable_float(boot["std"]),
                "ci_low": stable_float(boot["ci_low"]),
                "ci_high": stable_float(boot["ci_high"]),
                "noise_alpha": stable_float(alpha_noise)
            },
            "metadata": {
                "seed": args.seed,
                "generator": "structured_chaotic_process" if args.canonical else "real_sunspots"
            }
        }

        with open("artifacts/canonical_report.json", "w") as f:
            json.dump(report, f, sort_keys=True, separators=(',', ':'))

        print("✅ Spectral report generated (physically grounded)")

    except Exception as e:
        print("❌ CRITICAL FAILURE in generate_report")
        print(str(e))
        print(traceback.format_exc())
        raise SystemExit(1)


if __name__ == "__main__":
    main()
