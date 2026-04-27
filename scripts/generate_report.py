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


def bootstrap_alpha(series, num_boot=100, block_size=None):
    """
    Adaptive block bootstrap preserving temporal structure
    """

    n = len(series)

    # 🔥 حل جذري: block_size يتظبط حسب حجم الداتا
    if block_size is None:
        block_size = max(8, min(128, n // 2))

    if block_size >= n:
        block_size = max(4, n // 2)

    alphas = []

    for _ in range(num_boot):
        blocks = []
        i = 0

        while i < n:
            max_start = n - block_size
            if max_start <= 0:
                start = 0
            else:
                start = np.random.randint(0, max_start)

            blocks.append(series[start:start + block_size])
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
            synthetic = generate_series(args.seed)

        import pandas as pd
        df = pd.read_csv("real-data/sunspots_global.csv")

        if "value" in df.columns:
            real = df["value"].values
        elif "Sunspots" in df.columns:
            real = df["Sunspots"].values
        else:
            raise ValueError("No valid column")

        series = 0.7 * real + 0.3 * synthetic[:len(real)]

        print("Real length:", len(real))
        print("Synthetic length:", len(synthetic))
        print("Series sample:", series[:5])

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
        print("❌ CRITICAL FAILURE in generate_report")
        print(str(e))
        print(traceback.format_exc())
        raise SystemExit(1)


if __name__ == "__main__":
    main()
