from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess

from analysis.appropriate_stochastic_null import parametric_short_memory_null
from analysis.numerical_spectral_verification import estimate_alpha

OUTPUT = Path("artifacts/null_type1_calibration_v1.json")
NOMINAL_ALPHA = 0.05
MIN_CONFIRMATORY_REPETITIONS = 1000
MAX_ACCEPTABLE_WILSON_UPPER = 0.075

# Fixed, declared synthetic null scenarios. These are not fitted to the
# observed sunspot result and do not alter the production AR order limit.
SCENARIOS = {
    "gaussian_ar1_phi_0_4": [0.40],
    "gaussian_ar2_phi_0_45_minus_0_10": [0.45, -0.10],
    "gaussian_ar5_low_order_coefficients": [0.20, 0.10, 0.05, 0.025, 0.0125],
    "gaussian_ar10_low_order_coefficients": [0.15, 0.08, 0.05, 0.03, 0.02, 0.015, 0.01, 0.008, 0.006, 0.004],
}


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if trials <= 0:
        return (float("nan"), float("nan"))
    p = successes / trials
    denom = 1.0 + z * z / trials
    center = (p + z * z / (2.0 * trials)) / denom
    half = z * np.sqrt((p * (1.0 - p) / trials) + (z * z / (4.0 * trials * trials))) / denom
    return max(0.0, float(center - half)), min(1.0, float(center + half))


def generate_ar(phi: list[float], n: int, rng: np.random.Generator) -> np.ndarray:
    ar = np.asarray([1.0] + [-float(value) for value in phi], dtype=float)
    process = ArmaProcess(ar=ar, ma=np.asarray([1.0]))
    if not bool(process.isstationary):
        raise RuntimeError(f"Declared synthetic AR coefficients are not stationary: {phi}")
    # Fixed burn-in rule; use a deterministic RNG stream per replicate.
    values = process.generate_sample(
        nsample=n + 2000,
        burnin=0,
        distrvs=rng.standard_normal,
    )
    return np.asarray(values[2000:], dtype=np.float64)


def run_scenario(name: str, phi: list[float], repetitions: int, surrogates: int, n: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    p_values: list[float] = []
    boundary_fractions: list[float] = []
    invalid = 0
    failures: list[str] = []

    for replicate in range(repetitions):
        x = generate_ar(phi, n, rng)
        try:
            observed_alpha = float(estimate_alpha(x))
            result = parametric_short_memory_null(
                x,
                observed_alpha,
                rng,
                trials=surrogates,
            )
            p_value = result.get("p_value_mc_add_one")
            diagnostics = result.get("order_selection_diagnostic") or {}
            boundary_fraction = diagnostics.get("surrogate_boundary_fraction")
            if result.get("valid") is not True or p_value is None or not np.isfinite(float(p_value)):
                invalid += 1
                failures.append(f"replicate_{replicate + 1}:invalid_null_result")
                continue
            p_values.append(float(p_value))
            if boundary_fraction is not None and np.isfinite(float(boundary_fraction)):
                boundary_fractions.append(float(boundary_fraction))
        except Exception as exc:
            invalid += 1
            failures.append(f"replicate_{replicate + 1}:{type(exc).__name__}:{exc}")

    valid = len(p_values)
    rejections = sum(p <= NOMINAL_ALPHA for p in p_values)
    rate = (rejections / valid) if valid else None
    lower, upper = wilson_interval(rejections, valid) if valid else (None, None)
    enough = valid >= MIN_CONFIRMATORY_REPETITIONS
    calibrated = bool(
        enough
        and lower is not None
        and lower <= NOMINAL_ALPHA <= upper
        and upper <= MAX_ACCEPTABLE_WILSON_UPPER
    )

    return {
        "scenario": name,
        "ar_coefficients": phi,
        "sample_size": n,
        "repetitions_requested": repetitions,
        "valid_repetitions": valid,
        "invalid_repetitions": invalid,
        "surrogates_per_test": surrogates,
        "nominal_type1_rate": NOMINAL_ALPHA,
        "rejections_at_nominal_alpha": int(rejections),
        "empirical_type1_rate": rate,
        "wilson_95_percent_interval": [lower, upper] if valid else None,
        "mean_surrogate_boundary_fraction": float(np.mean(boundary_fractions)) if boundary_fractions else None,
        "confirmatory_replication_count_requirement_met": enough,
        "scenario_calibration_passed": calibrated,
        "failure_examples_first_20": failures[:20],
        "interpretation": "Synthetic calibration of the current implemented test under this declared Gaussian AR scenario only; not proof of general null adequacy or scientific claim support.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Monte Carlo Type-I calibration of the current HCM AR(p) null test")
    parser.add_argument("--repetitions", type=int, default=10, help="Pilot default is 10. Use at least 1000 per scenario for a confirmatory calibration assessment.")
    parser.add_argument("--surrogates", type=int, default=200, help="Surrogate draws per synthetic test; minimum production function requirement is 200.")
    parser.add_argument("--n", type=int, default=1024, help="Synthetic series length; must match or exceed the canonical 1024 sample requirement.")
    parser.add_argument("--seed", type=int, default=20261009)
    args = parser.parse_args()

    if args.repetitions < 1:
        raise SystemExit("--repetitions must be >= 1")
    if args.surrogates < 200:
        raise SystemExit("--surrogates must be >= 200")
    if args.n < 1024:
        raise SystemExit("--n must be >= 1024 for this calibration protocol")

    scenarios = []
    for index, (name, phi) in enumerate(SCENARIOS.items()):
        print(f"Running {name}: repetitions={args.repetitions}, surrogates={args.surrogates}, n={args.n}", flush=True)
        scenarios.append(run_scenario(name, phi, args.repetitions, args.surrogates, args.n, args.seed + index * 1000003))
        # Checkpoint after each scenario so a timeout still leaves an auditable artifact.
        checkpoint = {
            "protocol": "NULL_TYPE1_CALIBRATION_V1",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "status": "INCOMPLETE_RUN_CHECKPOINT",
            "production_null_protocol": "stationary_gaussian_ar_p_aic_v2_exploratory",
            "nominal_alpha": NOMINAL_ALPHA,
            "minimum_valid_repetitions_per_scenario": MIN_CONFIRMATORY_REPETITIONS,
            "maximum_acceptable_95pct_wilson_upper_bound": MAX_ACCEPTABLE_WILSON_UPPER,
            "repetitions_requested": args.repetitions,
            "surrogates_per_test": args.surrogates,
            "sample_size": args.n,
            "seed": args.seed,
            "scenarios_completed": len(scenarios),
            "scenarios_expected": len(SCENARIOS),
            "scenarios": scenarios,
            "confirmatory_null_frozen": False,
            "promotion_authority": False,
            "claim_support": False,
            "interpretation": "Partial checkpoint only. A timeout or incomplete run cannot be interpreted as calibration success.",
        }
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    full_run = all(item["valid_repetitions"] >= MIN_CONFIRMATORY_REPETITIONS for item in scenarios)
    all_pass = full_run and all(item["scenario_calibration_passed"] for item in scenarios)
    report = {
        "protocol": "NULL_TYPE1_CALIBRATION_V1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE" if all_pass else "PILOT_OR_CALIBRATION_NOT_PASSED",
        "production_null_protocol": "stationary_gaussian_ar_p_aic_v2_exploratory",
        "nominal_alpha": NOMINAL_ALPHA,
        "minimum_valid_repetitions_per_scenario": MIN_CONFIRMATORY_REPETITIONS,
        "maximum_acceptable_95pct_wilson_upper_bound": MAX_ACCEPTABLE_WILSON_UPPER,
        "repetitions_requested": args.repetitions,
        "surrogates_per_test": args.surrogates,
        "sample_size": args.n,
        "seed": args.seed,
        "scenarios": scenarios,
        "confirmatory_null_frozen": False,
        "promotion_authority": False,
        "claim_support": False,
        "interpretation": "This report never freezes or approves the null automatically. Even a pass is limited to the tested synthetic Gaussian AR scenarios and must be combined with residual, stationarity, parameter-stability, surrogate-validity, boundary-saturation, effective-sample-size, and nuisance-preservation reviews. A pilot run cannot support confirmatory inference.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "output": str(OUTPUT), "valid_repetitions": [x["valid_repetitions"] for x in scenarios]}, indent=2))
    return 0 if full_run and all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
