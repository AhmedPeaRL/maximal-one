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


def bootstrap_alpha(series, num_boot=30):
    alphas = []
    n = len(series)

    for _ in range(num_boot):
        idx = np.random.randint(0, n, n)
        sample = series[idx]
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
        series = generate_series(args.seed)

        alpha = estimate_alpha(series)
        mean_alpha, std_alpha = bootstrap_alpha(series)
    
        report = {
            "spectral_profile": {
                "estimated_alpha": stable_float(alpha),
                "bootstrap_mean": stable_float(mean_alpha),
                "bootstrap_std": stable_float(std_alpha)
            },
            "metadata": {
                "seed": args.seed,
                "generator": "structured_chaotic_process"
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
