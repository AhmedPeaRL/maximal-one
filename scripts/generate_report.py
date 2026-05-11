import json
import argparse
import numpy as np
import random
import os
import traceback

from analysis.numerical_spectral_verification import estimate_alpha
from analysis.deep_freeze import deep_freeze

def generate_series(rng, n=1024):
    x = rng.standard_normal(n)

    for i in range(1, n):
        x[i] += 0.8 * x[i-1]

    return x

def stable_float(x, digits=6):
    return float(round(x, digits))

def enforce_determinism(seed=42):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    # 🔒 Lock environment بالكامل
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["NUMEXPR_NUM_THREADS"] = "1"

enforce_determinism(42)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--canonical", action="store_true")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="artifacts"
    )
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    np.random.seed(args.seed)  # 🔥 مهم جداً

    os.makedirs(args.output_dir, exist_ok=True)

    try:
        import pandas as pd
        df = pd.read_csv(
            "real-data/sunspots_global.csv",
            dtype=np.float64,
            engine="c"
        )

        real = df.iloc[:, 0].astype(np.float64).values

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
            local_rng = np.random.default_rng(args.seed + 999 + i)
            wn = local_rng.standard_normal(len(series))
            noise_samples.append(estimate_alpha(wn))
       
        alpha = estimate_alpha(series)

        if not np.isfinite(alpha):
            raise SystemExit("❌ alpha invalid (NaN or Inf)")

        if alpha >= 5.0:
            raise SystemExit(f"❌ Unphysical alpha detected: {alpha}")
    
        from analysis.falsification_tests import run_falsification
        from analysis.numerical_spectral_verification import block_bootstrap
        from analysis.statistical_significance import monte_carlo_p_value

        falsification_rng = np.random.default_rng(args.seed + 101)
        bootstrap_rng = np.random.default_rng(args.seed + 202)
        stats_rng = np.random.default_rng(args.seed + 303)

        falsification = run_falsification(
            series,
            falsification_rng
        )

        boot = block_bootstrap(
            series,
            bootstrap_rng
        )

        stats = monte_carlo_p_value(
            series,
            alpha,
            stats_rng
        )

        for key, value in falsification.items():
            if not np.isfinite(value):
                raise SystemExit(f"❌ Invalid falsification metric: {key}")
        
        if stats["p_value"] > 0.05:
            raise SystemExit("❌ Not statistically significant")

        from analysis.independent_validation import estimate_alpha_welch

        alpha_welch = estimate_alpha_welch(series)

        alpha_noise = float(np.mean(noise_samples))

        from analysis.sovereign_inference_engine import SovereignInferenceEngine

        engine = SovereignInferenceEngine()
        decision = engine.ingest(alpha, alpha_noise)

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
            "statistical_test": stats,
            "cross_method_validation": {
                "fft_alpha": stable_float(alpha),
                "welch_alpha": stable_float(alpha_welch),
                "agreement": stable_float(abs(alpha - alpha_welch))
            },
            "sovereign_layer": {
                "decision": decision,
                "engine_summary": engine.summary(
                    alpha,
                    alpha_noise
                )
            }
        }

        if abs(falsification["original_alpha"] - falsification["shuffled_alpha"]) < 0.2:
            raise SystemExit("❌ Structure not real (shuffle invariant)")

        if abs(falsification["original_alpha"] - falsification["white_noise_alpha"]) < 0.2:
            raise SystemExit("❌ Indistinguishable from noise")

        if abs(alpha - alpha_welch) > 1.0:
            raise SystemExit("❌ Method inconsistency too high")

        output_path = os.path.join(
            args.output_dir,
            "canonical_report.json"
        )

        from analysis.canonical_json import write_canonical

        report = deep_freeze(report, digits=8)
        report = json.loads(
            json.dumps(
                report,
                sort_keys=True,
                separators=(",", ":")
            )
        )

        write_canonical(
            output_path,
            report
        )
            
        print("✅ Spectral report generated (stable & reproducible)")

    except Exception as e:
        print("❌ CRITICAL FAILURE in generate_report")
        print(str(e))
        print(traceback.format_exc())
        raise SystemExit(1)


if __name__ == "__main__":
    main()
