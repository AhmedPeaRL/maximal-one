from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from analysis.appropriate_stochastic_null import parametric_short_memory_null
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.calibrate_null_type1 import (
    MAX_ACCEPTABLE_WILSON_UPPER,
    MIN_CONFIRMATORY_REPETITIONS,
    NOMINAL_ALPHA,
    SCENARIOS,
    generate_ar,
    wilson_interval,
)

ARTIFACT_DIR = Path("artifacts")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scenario-specific Type-I calibration; diagnostic only."
    )
    parser.add_argument("--scenario", required=True, choices=sorted(SCENARIOS))
    parser.add_argument("--repetitions", type=int, default=1000)
    parser.add_argument("--surrogates", type=int, default=200)
    parser.add_argument("--n", type=int, default=1024)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--checkpoint-every", type=int, default=25)
    args = parser.parse_args()

    if args.repetitions < 1:
        raise SystemExit("--repetitions must be >= 1")
    if args.surrogates < 200:
        raise SystemExit("--surrogates must be >= 200")
    if args.n < 1024:
        raise SystemExit("--n must be >= 1024")
    if args.checkpoint_every < 1:
        raise SystemExit("--checkpoint-every must be >= 1")

    phi = SCENARIOS[args.scenario]
    rng = np.random.default_rng(args.seed)
    p_values: list[float] = []
    boundary_fractions: list[float] = []
    failures: list[str] = []
    invalid = 0
    output = ARTIFACT_DIR / f"null_type1_calibration_{args.scenario}.json"
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    def report(status: str) -> dict:
        valid = len(p_values)
        rejections = sum(p <= NOMINAL_ALPHA for p in p_values)
        rate = rejections / valid if valid else None
        lower, upper = wilson_interval(rejections, valid) if valid else (None, None)
        enough = valid >= MIN_CONFIRMATORY_REPETITIONS
        calibrated = bool(
            enough
            and lower is not None
            and upper is not None
            and lower <= NOMINAL_ALPHA <= upper
            and upper <= MAX_ACCEPTABLE_WILSON_UPPER
        )
        if status != "FINAL":
            final_status = "INCOMPLETE_RUN_CHECKPOINT"
        elif calibrated:
            final_status = "TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE"
        elif args.repetitions < MIN_CONFIRMATORY_REPETITIONS and valid == args.repetitions and invalid == 0:
            final_status = "PILOT_COMPLETED_NOT_CONFIRMATORY"
        else:
            final_status = "CALIBRATION_NOT_PASSED_OR_INCOMPLETE"
        return {
            "protocol": "NULL_TYPE1_CALIBRATION_SCENARIO_V1",
            "created_at_utc": utc_now(),
            "status": final_status,
            "scenario": args.scenario,
            "ar_coefficients": phi,
            "production_null_protocol": "stationary_gaussian_ar_p_aic_v2_exploratory",
            "nominal_alpha": NOMINAL_ALPHA,
            "minimum_valid_repetitions_per_scenario": MIN_CONFIRMATORY_REPETITIONS,
            "maximum_acceptable_95pct_wilson_upper_bound": MAX_ACCEPTABLE_WILSON_UPPER,
            "repetitions_requested": args.repetitions,
            "valid_repetitions": valid,
            "invalid_repetitions": invalid,
            "completed_repetitions": valid + invalid,
            "surrogates_per_test": args.surrogates,
            "sample_size": args.n,
            "seed": args.seed,
            "rejections_at_nominal_alpha": int(rejections),
            "empirical_type1_rate": rate,
            "wilson_95_percent_interval": [lower, upper] if valid else None,
            "mean_surrogate_boundary_fraction": float(np.mean(boundary_fractions)) if boundary_fractions else None,
            "scenario_calibration_passed": calibrated if status == "FINAL" else False,
            "failure_examples_first_20": failures[:20],
            "confirmatory_null_frozen": False,
            "promotion_authority": False,
            "claim_support": False,
            "interpretation": (
                "Synthetic calibration under this one declared Gaussian AR scenario only. "
                "Even a pass does not establish general null adequacy, freeze the null, "
                "support the scientific claim, or authorize promotion."
            ),
        }

    for replicate in range(args.repetitions):
        x = generate_ar(phi, args.n, rng)
        try:
            observed_alpha = float(estimate_alpha(x))
            result = parametric_short_memory_null(
                x, observed_alpha, rng, trials=args.surrogates
            )
            p_value = result.get("p_value_mc_add_one")
            diagnostics = result.get("order_selection_diagnostic") or {}
            boundary_fraction = diagnostics.get("surrogate_boundary_fraction")
            if result.get("valid") is not True or p_value is None or not np.isfinite(float(p_value)):
                invalid += 1
                failures.append(f"replicate_{replicate + 1}:invalid_null_result")
            else:
                p_values.append(float(p_value))
                if boundary_fraction is not None and np.isfinite(float(boundary_fraction)):
                    boundary_fractions.append(float(boundary_fraction))
        except Exception as exc:
            invalid += 1
            failures.append(f"replicate_{replicate + 1}:{type(exc).__name__}:{exc}")

        completed = replicate + 1
        if completed % args.checkpoint_every == 0 or completed == args.repetitions:
            checkpoint = report("CHECKPOINT" if completed < args.repetitions else "FINAL")
            checkpoint["completed_repetitions"] = completed
            output.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(
                f"{args.scenario}: completed={completed}/{args.repetitions}, "
                f"valid={len(p_values)}, invalid={invalid}, status={checkpoint['status']}",
                flush=True,
            )

    final = report("FINAL")
    output.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "scenario": args.scenario,
        "status": final["status"],
        "valid_repetitions": final["valid_repetitions"],
        "empirical_type1_rate": final["empirical_type1_rate"],
        "wilson_95_percent_interval": final["wilson_95_percent_interval"],
        "output": str(output),
    }, indent=2))
    # A completed pilot is a successful diagnostic run, not a calibration pass.
    # Full assessments still exit nonzero unless all declared pass criteria hold.
    if final["status"] == "TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE":
        return 0
    if final["status"] == "PILOT_COMPLETED_NOT_CONFIRMATORY":
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
