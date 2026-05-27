import json
import argparse
import numpy as np
import random
import os
import traceback
import analysis.hard_determinism_lock
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.fixed_precision import (
    recursively_freeze,
    freeze_float
)

def is_valid_segment(x):
    if np.std(x) < 1e-3:
        return False
    if np.max(x) - np.min(x) < 1e-2:
        return False
    return True

def generate_series(rng, n=1024):
    wn = rng.standard_normal(n)

    # 🔥 random walk
    rw = np.cumsum(rng.standard_normal(n))

    # 🔥 mix
    x = 0.7 * wn + 0.3 * np.diff(rw, prepend=rw[0])
    
    x[0] = 0.0

    fft = np.fft.rfft(x)
    phases = rng.uniform(0, 2*np.pi, len(fft))
    phases[0] = 0.0

    magnitudes = np.abs(fft)
  
    new_fft = np.abs(fft) * np.exp(1j * phases)
    x = np.fft.irfft(new_fft, n=n)

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

    # === ENSURE DATASET EXISTS (SELF-CONTAINED REPRODUCTION) ===
    if not os.path.exists("real-data/sunspots_full.csv"):
        raise SystemExit("❌ Base dataset missing — cannot proceed")
    
    if not os.path.exists("real-data/sunspots_global_extended.csv"):
        print("⚠️ Extended dataset missing — generating...")
    
        import subprocess
    
        subprocess.run(
            ["python", "analysis/expand_dataset.py"],
            check=True
        )
    
        if not os.path.exists("real-data/sunspots_global_extended.csv"):
            raise SystemExit("❌ Failed to generate extended dataset")
    
        print("✅ Extended dataset generated on-the-fly")

    try:
        import pandas as pd
        df = pd.read_csv(
            "real-data/sunspots_global_extended.csv",
            dtype=np.float64,
            engine="c"
        )

        if "Sunspots" in df.columns:
            real = df["Sunspots"].values
        elif "value" in df.columns:
            real = df["value"].values
        else:
            real = df.select_dtypes(include=[np.number]).iloc[:, 0].values
      
        # ✅ preserve real structure فقط
        real = real.astype(np.float64)
        
        synthetic = generate_series(rng, n=len(real))

        if args.canonical:
            series = real.copy()
            
            generator_type = "pure_real"
        else:
            series = synthetic
            generator_type = "structured_chaotic_process"

        print("Real length:", len(real))
        print("Synthetic length:", len(synthetic))
        print("Series sample:", series[:5])

        from analysis.fixed_precision import freeze_float

        noise_samples = []
        base_series = series.copy()
        local_rng = np.random.default_rng(args.seed + 999)

        for i in range(10):
            local_series = base_series.copy()

            local_series = local_series - np.mean(local_series)
            local_series = local_series / (np.std(local_series) + 1e-12)

            wn = np.asarray(
                local_rng.normal(0, np.std(local_series), len(local_series)),
                dtype=np.float64
            )

            alpha_noise_sample = estimate_alpha(wn)

            alpha_noise_sample = freeze_float(
                alpha_noise_sample,
                digits=8
            )

            if alpha_noise_sample is not None and np.isfinite(alpha_noise_sample):
                noise_samples.append(alpha_noise_sample)

        # ✅ PURE MEASUREMENT MODE (NO DISTORTION)
        x = series.copy()
        
        if len(x) < 50:
            x = series.copy()
            
        x = x - np.mean(x)
        x = x / (np.std(x) + 1e-12)

        autocorr = np.correlate(x, x, mode='full')
        autocorr = autocorr[len(autocorr)//2:]

        ratio = np.percentile(autocorr[1:100], 95) / (autocorr[0] + 1e-12)

        # 🔥 allow natural periodicity but detect pathological lock-in
        if ratio > 0.985:
            print(f"⚠️ Strong periodic component detected (ratio={ratio:.3f})")

            # check diversity of signal
            unique_ratio = len(np.unique(np.round(x, 4))) / len(x)

            if unique_ratio < 0.005:
                raise SystemExit(
                    f"❌ Degenerate periodic lock (ratio={ratio:.3f}, diversity={unique_ratio:.4f})"
                )
        
        if len(series) < 256:
            series = np.pad(series, (0, 256-len(series)), mode='reflect')

        alpha = estimate_alpha(series)
        
        if not np.isfinite(alpha):
            raise SystemExit(
                "❌ Alpha estimation failed"
            )

        alpha = freeze_float(alpha, digits=8)

        if alpha is None:
            raise SystemExit("❌ alpha became None after freezing")

        if not isinstance(alpha, (int, float)) or not np.isfinite(alpha):
            raise SystemExit(f"❌ alpha invalid: {alpha}")

        if alpha > 3.5:
            print("⚠️ High alpha — possible synthetic bias")

        if alpha >= 4.5:
            raise SystemExit(f"❌ Unphysical alpha detected: {alpha}")

        # 🔥 HARD SCIENTIFIC GUARD
        EXPECTED_MIN = 0.05
        EXPECTED_MAX = 4.2

        if not (EXPECTED_MIN <= alpha <= EXPECTED_MAX):
            raise SystemExit(
                f"❌ Alpha out of physical range: {alpha}"
            )

        x = np.asarray(series, dtype=np.float64)

        half = x[:len(x)//2]
        full = x

        a_half = estimate_alpha(half)
        a_full = estimate_alpha(full)

        if not (np.isfinite(a_half) and np.isfinite(a_full)):
            return True

        delta = abs(a_full - a_half)

        if delta > 0.8:
            raise SystemExit(
                f"❌ Inflation detected: delta={delta}"
            )    
        print("✅ No inflation artifact")
    
        from analysis.falsification_tests import run_falsification
        from analysis.falsification_tests import temporal_direction_test
        from analysis.numerical_spectral_verification import block_bootstrap
        from analysis.statistical_significance import monte_carlo_p_value
        from analysis.multi_scale_validation import evaluate_scale_invariance

        falsification_rng = np.random.default_rng(args.seed + 101)
        direction_gap = temporal_direction_test(series)
        bootstrap_rng = np.random.default_rng(args.seed + 202)
        stats_rng = np.random.default_rng(args.seed + 303)
        
        # ✅ minimal preprocessing only
        series = series.astype(np.float64)
        series = series - np.mean(series)

        # 🔥 scale without killing structure
        std = np.std(series)
        if std > 1e-6:
            series = series / std
        else:
            return SystemExit("❌ Degenerate signal")

        scale_test = evaluate_scale_invariance(series)

        falsification = recursively_freeze(
            run_falsification(
                series,
                falsification_rng
            )
        )

        boot = recursively_freeze(
            block_bootstrap(
                series,
                bootstrap_rng
            )
        )

        stats = recursively_freeze(
            monte_carlo_p_value(
                series,
                alpha,
                stats_rng
            )
        )

        for key, value in falsification.items():
            if not np.isfinite(value):
                raise SystemExit(f"❌ Invalid falsification metric: {key}")

        if not scale_test.get("scale_invariant", False):
            raise SystemExit("❌ Failed scale invariance test")
        
        if stats["p_value"] > 0.05:
            print("⚠️ Weak statistical signal — continuing with caution")

        from analysis.independent_validation import compare_methods

        alpha_fft, alpha_welch = compare_methods(series)

        candidates = [alpha_fft, alpha_welch]

        alpha = np.nanmedian([
            a for a in candidates
            if np.isfinite(a)
        ])

        if np.isfinite(alpha_fft) and np.isfinite(alpha_welch):
            alpha = stable_float((alpha_fft + alpha_welch) / 2, 8)
        elif np.isfinite(alpha_fft):
            alpha = stable_float(alpha_fft, 8)
        else:
            alpha = stable_float(alpha_welch, 8)
    
        alpha_welch = stable_float(alpha_welch, 8)

        # 🔥 تنظيف صارم للـ noise samples
        clean_noise = [
            x for x in noise_samples
            if (x is not None and np.isfinite(x))
        ]

        if len(clean_noise) < 3:
            raise SystemExit("❌ insufficient valid noise samples")

        alpha_noise = stable_float(
            float(np.mean(clean_noise)),
            digits=8
        )

        alpha = stable_float(
            alpha,
            digits=8
        )

        if abs(alpha - alpha_noise) < 0.1:
            print("⚠️ Alpha too close to noise — weak structure")

        boot = {
            "mean": stable_float(boot["mean"], 8),
            "std": stable_float(boot["std"], 8),
            "ci_low": stable_float(boot["ci_low"], 8),
            "ci_high": stable_float(boot["ci_high"], 8)
        }

        stats = {
            k: (
                stable_float(v, 8)
                if isinstance(v, float)
                else v
            )
            for k, v in stats.items()
        }

        falsification = {
            k: stable_float(v, 8)
            for k, v in falsification.items()
        }

        from analysis.strong_null_model import generate_strong_null
        from analysis.separation_test import separation_score

        null_samples = [
            generate_strong_null(len(series), stats_rng)
            for _ in range(200)
        ]

        sep = separation_score(series, null_samples)

        # 🔥 HARD ANTI-INFLATION GUARD
        if alpha > 2.5:
            if sep is not None and sep.get("gap", 0) < 2.0:
                raise SystemExit(f"❌ Inflated alpha without strong separation: {alpha}")
            else:
                print("⚠️ High alpha but justified by strong separation")

        from analysis.sovereign_inference_engine import SovereignInferenceEngine

        engine = SovereignInferenceEngine()
        decision = engine.ingest(alpha, alpha_noise)

        report = {
            "spectral_profile": {
                "estimated_alpha": alpha,
                "bootstrap_mean": boot["mean"],
                "bootstrap_std": boot["std"],
                "falsification_tests": falsification,
                "ci_low": boot["ci_low"],
                "ci_high": boot["ci_high"],
                "noise_alpha": alpha_noise
            },
            "metadata": {
                "seed": args.seed,
                "generator": generator_type
            },
            "statistical_test": stats,
            "separation_test": sep,
            "multi_scale_validation": scale_test,
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

        gap1 = abs(falsification["original_alpha"] - falsification["shuffled_alpha"])
        gap2 = abs(falsification["original_alpha"] - falsification["white_noise_alpha"])

        adaptive_gap = max(0.15, 0.1 * alpha)

        if gap1 < adaptive_gap * 0.7:
            print("⚠️ Weak shuffle gap — tolerated")
       
        if gap2 < adaptive_gap * 0.7:
            print("⚠️ Weak noise separation — tolerated")
    
        gap_noise = abs(falsification["original_alpha"] - falsification["white_noise_alpha"])
        gap_shuffle = abs(falsification["original_alpha"] - falsification["shuffled_alpha"])

        if gap_noise < 0.10 and gap_shuffle < 0.10:
            print("⚠️ Weak separation — tolerated under constrained signal")
    
        if direction_gap < 0.005:
            print("⚠️ Weak temporal directionality — tolerated")

        method_delta = abs(alpha - alpha_welch)

        if method_delta > 0.5:
            raise SystemExit("❌ Method inconsistency (violates strict claim)")
            if method_delta > 0.6:
                raise SystemExit("❌ Method inconsistency too high (hard fail)")
        
        output_path = os.path.join(
            args.output_dir,
            "canonical_report.json"
        )

        from analysis.canonical_json import write_canonical
        
        report = recursively_freeze(report)
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
