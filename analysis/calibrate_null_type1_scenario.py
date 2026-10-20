from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from analysis.appropriate_stochastic_null import parametric_short_memory_null
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.calibrate_null_type1 import (
    MATRIX, MASTER_SEED, NOMINAL_ALPHA, REQUIRED_OUTER_REPETITIONS,
    REQUIRED_SAMPLE_SIZE, REQUIRED_SURROGATES, SCENARIO_ORDER, SCENARIOS,
    generate_ar, replicate_rngs, wilson_interval, wilson_upper_one_sided,
)

ARTIFACT_DIR = Path("artifacts")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="V3 candidate Type-I calibration; do not run until independently reviewed and frozen.")
    parser.add_argument("--scenario", required=True, choices=SCENARIO_ORDER)
    parser.add_argument("--repetitions", type=int, default=REQUIRED_OUTER_REPETITIONS)
    parser.add_argument("--surrogates", type=int, default=REQUIRED_SURROGATES)
    parser.add_argument("--n", type=int, default=REQUIRED_SAMPLE_SIZE)
    parser.add_argument("--master-seed", type=int, default=MASTER_SEED)
    parser.add_argument("--checkpoint-every", type=int, default=25)
    args = parser.parse_args()

    if MATRIX.get("status") != "APPROVED_FROZEN" or MATRIX.get("freeze_state") != "FROZEN" or MATRIX.get("confirmatory_execution_authorized") is not True:
        raise SystemExit("BLOCKED: protocol is not independently reviewed and frozen. No simulation was started.")
    if args.repetitions != REQUIRED_OUTER_REPETITIONS or args.surrogates != REQUIRED_SURROGATES or args.n != REQUIRED_SAMPLE_SIZE or args.master_seed != MASTER_SEED:
        raise SystemExit("BLOCKED: parameters must exactly match the machine-readable V3 candidate matrix; do not run a partial configuration as formal calibration.")

    scenario_index = SCENARIO_ORDER.index(args.scenario)
    phi = SCENARIOS[args.scenario]
    p_values: list[float] = []
    boundary_fractions: list[float] = []
    attempt_records: list[dict] = []
    invalid = 0
    output = ARTIFACT_DIR / f"null_type1_calibration_{args.scenario}.json"
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    def report(status: str, completed: int) -> dict:
        valid = len(p_values)
        rejections = sum(p <= NOMINAL_ALPHA for p in p_values)
        all_completed = completed == args.repetitions

        # Descriptive rates use the requested denominator N.
        # Invalid attempts remain visible and are never treated as non-rejections.
        rate_requested = (
            rejections / args.repetitions
            if args.repetitions > 0
            else None
        )
        rate_valid_only = rejections / valid if valid else None

        two_sided = (
            list(wilson_interval(rejections, valid))
            if valid
            else None
        )
        upper_valid_only = (
            wilson_upper_one_sided(rejections, valid)
            if valid
            else None
        )

        # The acceptance bound is eligible only when every requested
        # attempt is complete and valid. Do not change the threshold.
        acceptance_eligible = bool(
            all_completed
            and invalid == 0
            and valid == args.repetitions
        )

        upper = (
            upper_valid_only
            if acceptance_eligible
            else None
        )

        passed = bool(
            acceptance_eligible
            and upper is not None
            and upper
            <= MATRIX["primary_design"]["one_sided_upper_bound_maximum"]
        )
        if status != "FINAL":
            final_status = "INCOMPLETE_NOT_A_PASS"
        elif not all_completed:
            final_status = "INCOMPLETE_NOT_A_PASS"
        elif invalid:
            final_status = "TYPE1_CALIBRATION_FAILED_INVALID_ATTEMPTS"
        elif upper is None:
            final_status = "TYPE1_CALIBRATION_FAILED_NO_VALID_BOUND"
        elif upper > MATRIX["primary_design"]["one_sided_upper_bound_maximum"]:
            final_status = "TYPE1_CALIBRATION_FAILED_UPPER_BOUND"
        else:
            final_status = "TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE"
        return {
            "protocol": MATRIX["protocol"], "protocol_status": MATRIX["status"],
            "created_at_utc": utc_now(), "status": final_status,
            "scenario": args.scenario, "scenario_index": scenario_index, "ar_coefficients": phi,
            "sample_size": args.n, "dgp_burn_in": MATRIX["primary_design"]["dgp_burn_in"],
            "master_seed": args.master_seed, "seed_schedule": MATRIX["primary_design"]["seed_schedule"],
            "repetitions_requested": args.repetitions, "completed_repetitions": completed,
            "valid_repetitions": valid, "invalid_repetitions": invalid,
            "surrogates_requested_per_test": args.surrogates,
            "nominal_alpha": NOMINAL_ALPHA, "rejections_at_nominal_alpha": int(rejections),
            "rejection_rate_requested_denominator": rate_requested,
            "rejection_rate_requested_denominator_N": args.repetitions,
            "empirical_type1_rate_among_valid_attempts_descriptive_only": rate_valid_only,
            "wilson_95_percent_two_sided_valid_attempts_report_only": two_sided,
            "wilson_95_percent_one_sided_upper_bound_valid_attempts_descriptive_only": upper_valid_only,
            "acceptance_bound_eligible": acceptance_eligible,
            "wilson_95_percent_one_sided_upper_bound_acceptance": upper,
            "acceptance_upper_bound_maximum": MATRIX["primary_design"]["one_sided_upper_bound_maximum"],
            "scenario_calibration_passed": passed,
            "attempt_records": attempt_records,
            "mean_surrogate_boundary_fraction": float(np.mean(boundary_fractions)) if boundary_fractions else None,
            "code_sha256": {str(p): sha256(p) for p in [Path("analysis/calibrate_null_type1.py"), Path("analysis/calibrate_null_type1_scenario.py"), Path("analysis/appropriate_stochastic_null.py"), Path("analysis/numerical_spectral_verification.py")]},
            "matrix_sha256": sha256(Path("protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json")),
            "python_version": sys.version, "platform": platform.platform(),
            "claim_support": False, "promotion_authority": False,
            "confirmatory_null_frozen": False,
            "interpretation": "Candidate-only synthetic operating-characteristic diagnostic. This artifact cannot establish production-null adequacy, real-domain replication, or HCM claim support. Any invalid attempt blocks scenario pass.",
        }

    for replicate_index in range(args.repetitions):
        dgp_rng, null_rng = replicate_rngs(args.master_seed, scenario_index, replicate_index)
        record = {"replicate_index": replicate_index, "dgp_seed_entropy": [args.master_seed, scenario_index, replicate_index, 0], "null_seed_entropy": [args.master_seed, scenario_index, replicate_index, 1], "status": "INVALID", "reason": None}
        try:
            x = generate_ar(phi, args.n, dgp_rng)
            observed_alpha = float(estimate_alpha(x))
            result = parametric_short_memory_null(x, observed_alpha, null_rng, trials=args.surrogates)
            diagnostics = result.get("order_selection_diagnostic") or {}
            record.update({
                "observed_alpha": observed_alpha,
                "null_valid": bool(result.get("valid") is True),
                "requested_surrogates": int(result.get("trials_requested", args.surrogates)),
                "valid_surrogates": int(result.get("null_samples", 0)),
                "selected_order": result.get("selected_order"),
                "surrogate_boundary_fraction": diagnostics.get("surrogate_boundary_fraction"),
                "refit_failures": diagnostics.get("refit_failures"),
                "alpha_estimation_failures": diagnostics.get("alpha_estimation_failures"),
            })
            p_value = result.get("p_value_mc_add_one")
            if result.get("valid") is not True:
                record["reason"] = result.get("reason", "invalid_null_result")
            elif int(result.get("null_samples", 0)) != args.surrogates:
                record["reason"] = "requested_surrogate_count_not_fully_valid"
            elif p_value is None or not np.isfinite(float(p_value)):
                record["reason"] = "missing_or_nonfinite_p_value"
            else:
                record.update({"status": "VALID", "reason": None, "p_value": float(p_value), "rejected": bool(float(p_value) <= NOMINAL_ALPHA)})
                p_values.append(float(p_value))
                bf = diagnostics.get("surrogate_boundary_fraction")
                if bf is not None and np.isfinite(float(bf)):
                    boundary_fractions.append(float(bf))
        except Exception as exc:
            record["reason"] = f"{type(exc).__name__}:{exc}"
        if record["status"] != "VALID":
            invalid += 1
        attempt_records.append(record)
        completed = replicate_index + 1
        if completed % args.checkpoint_every == 0 or completed == args.repetitions:
            output.write_text(json.dumps(report("CHECKPOINT" if completed < args.repetitions else "FINAL", completed), indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(f"{args.scenario}: completed={completed}/{args.repetitions}; valid={len(p_values)}; invalid={invalid}", flush=True)

    final = report("FINAL", args.repetitions)
    output.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"scenario": args.scenario, "status": final["status"], "valid_repetitions": final["valid_repetitions"], "invalid_repetitions": final["invalid_repetitions"], "one_sided_upper_bound": final["wilson_95_percent_one_sided_upper_bound_acceptance"], "output": str(output)}, indent=2))
    return 0 if final["scenario_calibration_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
