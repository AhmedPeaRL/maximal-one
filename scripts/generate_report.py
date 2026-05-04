import json
import argparse
import numpy as np
import random
import os
import traceback

from analysis.numerical_spectral_verification import estimate_alpha


def generate_series(rng, n=1024):
    x = rng.randn(n)

    for i in range(1, n):
        x[i] += 0.8 * x[i-1]

    return x


def stable_float(x, digits=10):
    return float(round(x, digits))


def enforce_determinism(seed=42):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    # منع threading randomness
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"

enforce_determinism(42)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--canonical", action="store_true")
    args = parser.parse_args()

    rng = np.random.RandomState(args.seed)  # 🔥 مهم جداً

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

        synthetic = generate_series(rng, n=len(real))

        if args.canonical:
            series = real
            generator_type = "pure_real"
        else:
            series = synthetic
            generator_type = "structured_chaotic_process"

        print("Real length:", len(real))
        print("Synthetic length:", len(synthetic))
        print("Series sample:", series[:5])

        noise_samples = []
        for i in range(10):
            local_rng = np.random.RandomState(args.seed + 999 + i)
            wn = local_rng.randn(len(series))
            noise_samples.append(estimate_alpha(wn))
       
        alpha = estimate_alpha(series)

        if not np.isfinite(alpha):
            raise SystemExit("❌ alpha invalid (NaN or Inf)")

        if alpha > 5:
            raise SystemExit(f"❌ Unphysical alpha detected: {alpha}")
    
        from analysis.falsification_tests import run_falsification

        falsification = run_falsification(series, rng)
     
        from analysis.numerical_spectral_verification import block_bootstrap

        boot = block_bootstrap(series, rng)

        from analysis.statistical_significance import monte_carlo_p_value

        stats = monte_carlo_p_value(series, alpha, rng)
        
        if stats["p_value"] > 0.05:
            raise SystemExit("❌ Not statistically significant")

        alpha_noise = float(np.mean(noise_samples))

        report = {
            "spectral_profile": {
                "estimated_alpha": stable_float(alpha),
                "bootstrap_mean": stable_float(boot["mean"]),
                "bootstrap_std": stable_float(boot["std"]),
                "falsification_tests": falsification,
                "ci_low": stable_float(boot["ci_low"]),
                "ci_high": stable_float(boot["ci_high"]),
                "noise_alpha": stable_float(alpha_noise)
            },
            "metadata": {
                "seed": args.seed,
                "generator": generator_type
            },
            "statistical_test": stats
        }

        if abs(falsification["original_alpha"] - falsification["shuffled_alpha"]) < 0.2:
            raise SystemExit("❌ Structure not real (shuffle invariant)")

        if abs(falsification["original_alpha"] - falsification["white_noise_alpha"]) < 0.2:
            raise SystemExit("❌ Indistinguishable from noise")

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
