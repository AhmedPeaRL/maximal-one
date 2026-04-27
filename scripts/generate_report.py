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


def bootstrap_alpha(series, num_boot=30, block_size=64):
    """
    Block bootstrap preserving temporal structure
    """
    n = len(series)
    alphas = []

    for _ in range(num_boot):
        blocks = []
        i = 0
        while i < n:
            start = np.random.randint(0, n - block_size)
            blocks.append(series[start:start+block_size])
            i += block_size

        sample = np.concatenate(blocks)[:n]
        alphas.append(estimate_alpha(sample))

    return float(np.mean(alphas)), float(np.std(alphas))


def stable_float(x, digits=10):
    return float(round(x, digits))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--canonical", action="store_true")
    args = parser.parse_args()

    os.makedirs("artifacts", exist_ok=True)

    try:
        if args.canonical:
            series = generate_series(args.seed)
        else:
            # 🔥 استخدام بيانات حقيقية
            import pandas as pd

            df = pd.read_csv("real-data/sunspots_global.csv")

            # unified column handling
            if "value" in df.columns:
                series = df["value"].values.astype(float)
            elif "Sunspots" in df.columns:
                series = df["Sunspots"].values.astype(float)
            else:
                raise ValueError("Dataset must contain 'value' or 'Sunspots' column")

        white_noise = np.random.randn(len(series))
        alpha_noise = estimate_alpha(white_noise)
        alpha = estimate_alpha(series)
        mean_alpha, std_alpha = bootstrap_alpha(series)
    
        report = {
            "spectral_profile": {
                "estimated_alpha": stable_float(alpha),
                "bootstrap_mean": stable_float(mean_alpha),
                "bootstrap_std": stable_float(std_alpha),
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
        fallback = {
            "status": "partial",
            "error": str(e),
            "trace": traceback.format_exc(),
            "timestamp": time.time()
        }

        with open("artifacts/canonical_report.json", "w") as f:
            json.dump(fallback, f)

        print("⚠️ Fallback report generated")


if __name__ == "__main__":
    main()
