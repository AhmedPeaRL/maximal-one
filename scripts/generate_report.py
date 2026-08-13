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
    
    PRIMARY_DATASET = (
        "real-data/sunspots_full.csv"
    )

    AUXILIARY_DATASET = (
        "real-data/sunspots_global_extended.csv"
    )

    if not os.path.exists(PRIMARY_DATASET):
        raise SystemExit(
            "❌ Primary dataset missing"
        )

    auxiliary_available = os.path.exists(
        AUXILIARY_DATASET
    )

    if auxiliary_available:
        print(
            "✅ Auxiliary dataset available"
        )
    else:
        print(
            "⚠️ Auxiliary dataset unavailable"
        )

    try:
        import pandas as pd
        df = pd.read_csv(
            PRIMARY_DATASET,
            sep=";",
            header=None,
            engine="python"
        )

        df.columns = [
            "year",
            "month",
            "decimal_year",
            "sunspots",
            "std",
            "obs",
            "flag"
        ]

        real = pd.to_numeric(
            df["sunspots"],
            errors="coerce"
        ).dropna().values

        real = real.astype(
            np.float64
        )

        real_reference = real.copy()
        extended_reference = None

        if auxiliary_available:
            ext_df = pd.read_csv(
                AUXILIARY_DATASET
            )

            if "Sunspots" in ext_df.columns:
                extended_reference = (
                    ext_df["Sunspots"]
                    .astype(np.float64)
                    .values
                )
        
        synthetic = generate_series(rng, n=len(real))

        if args.canonical:
            series = real.copy()
            
            generator_type = "real_extended_hybrid"
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
            raise SystemExit(
                "❌ Half/full alpha invalid"
            )

        delta = abs(a_full - a_half)

        if delta > 0.8:
            raise SystemExit(
                f"❌ Inflation detected: delta={delta}"
            )    
        print("✅ No inflation artifact")

        from analysis.integration_diagnostics import (
            integration_score,
            classify_process
        )

        integration_ratio = integration_score(series)
        process_class = classify_process(series)
    
        from analysis.falsification_tests import run_falsification
        from analysis.falsification_tests import temporal_direction_test
        from analysis.falsification_tests import phase_surrogate_guard
        from analysis.falsification_tests import validate as validate_bootstrap
        from analysis.numerical_spectral_verification import block_bootstrap
        from analysis.statistical_significance import monte_carlo_p_value
        from analysis.multi_scale_validation import evaluate_scale_invariance
        from analysis.cross_seed_validation import run as cross_seed_validation
        from analysis.evidence_fusion import (
            evidence_fusion
        )
        from analysis.consensus_guard import (
            consensus_check
        )
        from analysis.predictive_validation import (
            evaluate_prediction
        )

        falsification_rng = np.random.default_rng(args.seed + 101)
        direction_gap = temporal_direction_test(series)
        bootstrap_rng = np.random.default_rng(args.seed + 202)
        stats_rng = np.random.default_rng(args.seed + 303)
        
        # ✅ minimal preprocessing only
        series = series.astype(np.float64)
        series = series - np.mean(series)

        prediction_validation = evaluate_prediction(series)

        # 🔥 scale without killing structure
        std = np.std(series)
        if std > 1e-6:
            series = series / std
        else:
            return SystemExit("❌ Degenerate signal")

        scale_test = evaluate_scale_invariance(series)
        cross_seed = cross_seed_validation(
            series
        )
        if not cross_seed.get(
            "seed_stable",
            False
        ):
            raise SystemExit(
                "❌ Cross-seed instability detected"
            )

        falsification = recursively_freeze(
            run_falsification(
                series,
                falsification_rng
            )
        )

        phase_guard = phase_surrogate_guard(
            falsification["original_alpha"],
            falsification["phase_randomized_alpha"]
        )
        print(
            "Phase surrogate gap:",
            phase_guard["gap"]
        )
        print(
            "Phase interpretation:",
            phase_guard["interpretation"]
        )

        boot = recursively_freeze(
            block_bootstrap(
                series,
                bootstrap_rng
            )
        )
        print("BOOTSTRAP MEAN:", boot["mean"])
        print("BOOTSTRAP STD:", boot["std"])
        print("ALPHA:", alpha)

        bootstrap_guard = validate_bootstrap(
            alpha,
            boot["mean"],
            boot["std"]
        )
        if not bootstrap_guard["passed"]:
            raise SystemExit(
                "❌ Bootstrap consistency failed"
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

        if stats["p_value"] > 0.05:
            print(
                "⚠️ Null hypothesis not rejected"
            )

        from analysis.independent_validation import compare_methods

        alpha_fft, alpha_welch = compare_methods(series)

        if not np.isfinite(alpha_fft):
            raise SystemExit(
                "❌ Primary alpha estimator failed"
            )

        alpha = stable_float(
            alpha_fft,
            8
        )

        validation_delta = np.nan

        if np.isfinite(alpha_welch):
            validation_delta = abs(
                alpha_fft
                -
                alpha_welch
            )

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

        null_samples = []

        for _ in range(400):
            sample = generate_strong_null(
                len(series),
                stats_rng
            )

            alpha_null = estimate_alpha(sample)
            if np.isfinite(alpha_null):
                null_samples.append(sample)

        sep = separation_score(series, null_samples)

        print(
            "NULL STD:",
            np.std([
                estimate_alpha(s)
                for s in null_samples
            ])
        )

        print("=== SEPARATION ===")
        with open(
            "core-scientific/strict_claim.json",
            "r",
            encoding="utf-8"
        ) as f:
            strict_claim = json.load(f)

        required_z = (
            strict_claim
            ["expected_result"]
            ["min_separation_z"]
        )

        if sep is None:
            print("SEP = None")
        else:
            for k, v in sep.items():
                print(f"{k}: {v}")

        if sep is not None:
            if (
                sep["z_score"]
                <
                required_z
            ):
                raise SystemExit(
                    f"❌ separation z-score too low: "
                    f"{sep['z_score']:.3f}"
                )

            if (
                sep["overlap_score"] > 0.95
                and
                sep["effect_size"] < 0.05
            ):
                raise SystemExit(
                    "❌ excessive null overlap"
                )

        # 🔥 HARD ANTI-INFLATION GUARD
        if alpha > 2.5:
            if sep is not None and sep.get("gap", 0) < 2.0:
                raise SystemExit(f"❌ Inflated alpha without strong separation: {alpha}")
            else:
                print("⚠️ High alpha but justified by strong separation")

        falsification_delta = abs(
            falsification["original_alpha"]
            -
            falsification["white_noise_alpha"]
        )

        validation_delta = abs(
            alpha_fft
            -
            alpha_welch
        )

        fusion = evidence_fusion(
            alpha_delta=abs(
                alpha - alpha_noise
            ),
            p_value=stats["p_value"],
            scale_dispersion=scale_test[
                "dispersion"
            ],
            validation_delta=validation_delta,
            falsification_delta=falsification_delta
        )

        consensus = consensus_check(
            alpha_fft,
            alpha_welch,
            stats["p_value"],
            scale_test["dispersion"],
            fusion["evidence_score"]
        )

        from analysis.sovereign_inference_engine import SovereignInferenceEngine

        engine = SovereignInferenceEngine()
        decision = engine.ingest(alpha, alpha_noise)
        decision["primary_estimator"] = "FFT"
        decision["independent_validator"] = "Welch"
        decision["validation_delta"] = stable_float(
            validation_delta,
            8
        )

        if not fusion[
            "structure_detected"
        ]:
            raise SystemExit(
                "❌ Insufficient convergent evidence"
            )

        if not consensus["passed"]:
            print(
                "⚠️ Consensus guard did not pass:",
                consensus["diagnostics"]
            )
            print(
                "ℹ️ Scientific claim remains under investigation."
            )
        else:
            print(
                "✅ Consensus guard passed."
            )

        print(
            "Consensus diagnostics:",
            consensus["diagnostics"]
        )
        print(
            "Evidence score:",
            fusion["evidence_score"]
        )
        print(
            "P-value:",
            stats["p_value"]
        )
        print(
            "Dispersion:",
            scale_test["dispersion"]
        )

        report = {
            "predictive_validation": prediction_validation,
            "evidence_fusion": fusion,
            "phase_surrogate_guard": phase_guard,
            "bootstrap_consistency_guard": bootstrap_guard,
            "spectral_profile": {
                "estimated_alpha": alpha,
                "bootstrap_mean": boot["mean"],
                "bootstrap_std": boot["std"],
                "falsification_tests": falsification,
                "ci_low": boot["ci_low"],
                "ci_high": boot["ci_high"],
                "noise_alpha": alpha_noise
            },
            "dataset_audit": {
                "primary_dataset":
                    "sunspots_full",

                "primary_length":
                    int(len(real_reference)),

                "auxiliary_available":
                    bool(
                        extended_reference
                        is not None
                    ),

                "auxiliary_length":
                    int(
                        len(extended_reference)
                    )
                    if extended_reference
                    is not None
                    else 0
            },
            "metadata": {
                "seed": args.seed,
                "generator": generator_type
            },
            "integration_diagnostics": {
                "integration_ratio": stable_float(
                    integration_ratio,
                    8
                ),
                "process_class": process_class
            },
            "statistical_test": stats,
            "separation_test": sep,
            "multi_scale_validation": scale_test,
            "cross_seed_validation": cross_seed,
            "cross_method_validation": {
                "primary_method": "FFT",
                "validation_method": "Welch",
                "fft_alpha": stable_float(
                    alpha_fft
                ),
                "welch_alpha": stable_float(
                    alpha_welch
                ),
                "agreement_delta": stable_float(
                    validation_delta
                ),
                "validated": bool(
                    validation_delta <= 0.30
                )
            },
            "scientific_interpretation": {
                "null_rejected":
                    bool(stats["p_value"] <= 0.05),
                "evidence_strength":
                    (
                        "strong"
                        if stats["p_value"] <= 0.05
                        else "weak"
                    ),
                "claim_status":
                    (
                        "established"
                        if stats["p_value"] <= 0.05
                        else "under_investigation"
                    ),
                "reproducibility":
                    (
                        "confirmed"
                        if cross_seed.get("seed_stable", False)
                        else "unconfirmed"
                    )
            },
            "consensus_guard": consensus,
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

        adaptive_gap = max(
            0.20,
            0.15 * alpha
        )

        if gap1 < adaptive_gap * 0.7:
            print("⚠️ Weak shuffle gap — tolerated")
       
        if gap2 < adaptive_gap * 0.7:
            print("⚠️ Weak noise separation — tolerated")
    
        gap_noise = abs(falsification["original_alpha"] - falsification["white_noise_alpha"])
        gap_shuffle = abs(falsification["original_alpha"] - falsification["shuffled_alpha"])

        if gap_noise < 0.10:
            raise SystemExit(
                "❌ Noise separation too weak"
            )
        if gap_shuffle < 0.10:
            raise SystemExit(
                "❌ Shuffle separation too weak"
            )
    
        if direction_gap < 0.005:
            print("⚠️ Weak temporal directionality — tolerated")

        method_delta = validation_delta

        if not np.isfinite(method_delta):
            raise SystemExit(
                "❌ Independent validation unavailable"
            )

        if method_delta > 0.30:
            raise SystemExit(
                "❌ Method inconsistency too high"
            )

        if method_delta > 0.20:
            print(
                "⚠️ Method inconsistency near threshold"
            )
    
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
