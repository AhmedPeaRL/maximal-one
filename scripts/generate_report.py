import json
import argparse
import numpy as np
import os
import traceback

from analysis.numerical_spectral_verification import estimate_alpha


def generate_series(seed, n=1024):
    np.random.seed(seed)

    x = np.random.randn(n)

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

    os.makedirs("artifacts", exist_ok=True)

    try:
        import pandas as pd
        df = pd.read_csv("real-data/sunspots_global.csv")

        if "value" in df.columns:
            real = df["value"].values
        elif "Sunspots" in df.columns:
            real = df["Sunspots"].values
        else:
            raise ValueError("No valid column")

        # 🔥 ALWAYS generate synthetic (حل جذري)
        synthetic = generate_series(args.seed, n=len(real))

        if args.canonical:
            series = real + 0.05 * synthetic
            generator_type = "hybrid_real_synthetic"
        else:
            series = synthetic
            generator_type = "structured_chaotic_process"

        print("Real length:", len(real))
        print("Synthetic length:", len(synthetic))
        print("Series sample:", series[:5])

        noise_samples = []
        for i in range(10):
            wn = np.random.RandomState(args.seed + 999 + i).randn(len(series))
            noise_samples.append(estimate_alpha(wn))

        alpha_noise = float(np.mean(noise_samples))
        alpha = estimate_alpha(series)
        
        if estimated_alpha > 5:
            raise ValueError("Unphysical alpha detected")
     
        from analysis.numerical_spectral_verification import block_bootstrap

        boot = block_bootstrap(series)

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
                "generator": generator_type
            }
        }

        with open("artifacts/canonical_report.json", "w") as f:
            json.dump(report, f, sort_keys=True, separators=(',', ':'))

        print("✅ Spectral report generated (stable & reproducible)")

    except Exception as e:
        print("❌ CRITICAL FAILURE in generate_report")
        print(str(e))
        print(traceback.format_exc())
        raise SystemExit(1)


if __name__ == "__main__":
    main()
