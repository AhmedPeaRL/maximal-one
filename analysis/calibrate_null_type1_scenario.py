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
    MATRIX,
    MATRIX_PATH,
    DESIGN,
    V4_APPROVED,
    MASTER_SEED,
    NOMINAL_ALPHA,
    DGP_BURN_IN,
    REQUIRED_OUTER_REPETITIONS,
    REQUIRED_SAMPLE_SIZE,
    REQUIRED_SURROGATES,
    SCENARIO_ORDER,
    SCENARIOS,
    ACCEPTANCE_RULE,
    MAX_ACCEPTABLE_WILSON_UPPER,
    generate_ar,
    replicate_rngs,
    stable_scenario_key,
    acceptance_decision,
    wilson_interval,
    wilson_upper_one_sided,
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


def formal_main() -> int:
    if not V4_APPROVED:
        raise SystemExit(
            "BLOCKED: V4 matrix is not approved, frozen, and separately "
            "authorized. No formal calibration was started."
        )
    
    parser = argparse.ArgumentParser(
        description=(
            "V4 candidate Type-I calibration runner. "
            "Formal execution remains blocked until separately reviewed, "
            "frozen, and explicitly authorized."
        )
    )

    parser.add_argument("--scenario", required=True, choices=SCENARIO_ORDER)
    parser.add_argument("--repetitions", type=int, default=REQUIRED_OUTER_REPETITIONS)
    parser.add_argument("--surrogates", type=int, default=REQUIRED_SURROGATES)
    parser.add_argument("--n", type=int, default=REQUIRED_SAMPLE_SIZE)
    parser.add_argument("--master-seed", type=int, default=MASTER_SEED)
    parser.add_argument("--checkpoint-every", type=int, default=25)
    args = parser.parse_args()
    if args.checkpoint_every < 1:
        raise SystemExit(
            "BLOCKED: --checkpoint-every must be a positive integer."
        )

    if MATRIX.get("status") != "APPROVED_FROZEN" or MATRIX.get("freeze_state") != "FROZEN" or MATRIX.get("confirmatory_execution_authorized") is not True:
        raise SystemExit("BLOCKED: protocol is not independently reviewed and frozen. No simulation was started.")
    
    if (
        args.repetitions != REQUIRED_OUTER_REPETITIONS
        or args.surrogates != REQUIRED_SURROGATES
        or args.n != REQUIRED_SAMPLE_SIZE
        or args.master_seed != MASTER_SEED
    ):
        raise SystemExit(
            "BLOCKED: parameters must exactly match the V4 candidate "
            "dimensions. Candidate values do not authorize execution."
        )

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
        
        passed, decision_reason = acceptance_decision(
            requested=args.repetitions,
            completed=completed,
            invalid=invalid,
            upper=upper,
        )

        if status != "FINAL" or not all_completed:
            final_status = "INCOMPLETE_NOT_A_PASS"
        elif invalid:
            final_status = "TYPE1_CALIBRATION_FAILED_INVALID_ATTEMPTS"
        elif upper is None:
            final_status = "TYPE1_CALIBRATION_FAILED_NO_VALID_BOUND"
        elif decision_reason == "BLOCKED_ACCEPTANCE_RULE_UNRESOLVED":
            final_status = "BLOCKED_ACCEPTANCE_RULE_UNRESOLVED"
        elif not passed:
            final_status = decision_reason
        else:
            final_status = (
                "TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE"
            )

        return {
            "protocol": MATRIX["protocol"],
            "protocol_status": MATRIX["status"],
            "created_at_utc": utc_now(),
            "status": final_status,
            "scenario": args.scenario,
            "scenario_index": scenario_index,
            "ar_coefficients": phi,
            "dgp_burn_in": DGP_BURN_IN,
            "master_seed": args.master_seed,
            "seed_schedule": MATRIX.get("seed_schedule_candidate"),
            "repetitions_requested": args.repetitions,
            "completed_repetitions": completed,
            "valid_repetitions": valid,
            "invalid_repetitions": invalid,
            "surrogates_requested_per_test": args.surrogates,
            "nominal_alpha": NOMINAL_ALPHA,
            "rejections_at_nominal_alpha": int(rejections),
            "rejection_rate_requested_denominator": rate_requested,
            "rejection_rate_requested_denominator_N": args.repetitions,
            "empirical_type1_rate_among_valid_attempts_descriptive_only": rate_valid_only,
            "wilson_95_percent_two_sided_valid_attempts_report_only": two_sided,
            "wilson_95_percent_one_sided_upper_bound_valid_attempts_descriptive_only": upper_valid_only,
            "acceptance_bound_eligible": acceptance_eligible,
            "wilson_95_percent_one_sided_upper_bound_acceptance": upper,
            "acceptance_upper_bound_maximum": MAX_ACCEPTABLE_WILSON_UPPER,
            "scenario_calibration_passed": passed,
            "acceptance_decision_reason": decision_reason,
            "attempt_records": attempt_records,
            "mean_surrogate_boundary_fraction": float(np.mean(boundary_fractions)) if boundary_fractions else None,
            "code_sha256": {str(p): sha256(p) for p in [Path("analysis/calibrate_null_type1.py"), Path("analysis/calibrate_null_type1_scenario.py"), Path("analysis/appropriate_stochastic_null.py"), Path("analysis/numerical_spectral_verification.py")]},
            "matrix_sha256": sha256(MATRIX_PATH),
            "acceptance_rule": ACCEPTANCE_RULE,
            "formal_calibration_pass": False,
            "python_version": sys.version,
            "platform": platform.platform(),
            "claim_support": False,
            "promotion_authority": False,
            "confirmatory_execution_authorized": False,
            "confirmatory_null_frozen": False,
            "interpretation": "Candidate-only synthetic operating-characteristic diagnostic. This artifact cannot establish production-null adequacy, real-domain replication, or HCM claim support. Any invalid attempt blocks scenario pass.",
        }

    for replicate_index in range(args.repetitions):
        # The formal runner and bounded engineering mode share this exact
        # scientific attempt function. Governance gates remain separate.
        record = execute_attempt(
            args.scenario,
            replicate_index,
            args.master_seed,
            args.n,
            args.surrogates,
        )
        if record["status"] == "VALID":
            p_values.append(float(record["p_value_mc_add_one"]))
            boundary_fraction = record.get("surrogate_boundary_fraction")
            if boundary_fraction is not None and np.isfinite(float(boundary_fraction)):
                boundary_fractions.append(float(boundary_fraction))
        else:
            invalid += 1
        attempt_records.append(record)
        completed = replicate_index + 1
        if completed % args.checkpoint_every == 0 or completed == args.repetitions:
            output.write_text(
                json.dumps(
                    report("CHECKPOINT" if completed < args.repetitions else "FINAL", completed),
                    indent=2,
                    sort_keys=True,
                ) + "\n",
                encoding="utf-8",
            )
            print(
                f"{args.scenario}: completed={completed}/{args.repetitions}; "
                f"valid={len(p_values)}; invalid={invalid}",
                flush=True,
            )

    final = report("FINAL", args.repetitions)
    output.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"scenario": args.scenario, "status": final["status"], "valid_repetitions": final["valid_repetitions"], "invalid_repetitions": final["invalid_repetitions"], "one_sided_upper_bound": final["wilson_95_percent_one_sided_upper_bound_acceptance"], "output": str(output)}, indent=2))
    return 0 if final["scenario_calibration_passed"] else 1


# ---------------------------------------------------------------------------
# Bounded engineering entry point. This path is intentionally separate from
# formal calibration and cannot set formal_calibration_pass=True.
# ---------------------------------------------------------------------------
def _engineering_file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _engineering_identity(scenario_id, start, stop, repetitions, surrogates, n, master_seed):
    import subprocess
    root = Path(__file__).resolve().parents[1]
    try:
        commit_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        import os
        commit_sha = os.environ.get("GITHUB_SHA", "LOCAL_COMMIT_UNAVAILABLE")
    return {
        "protocol": MATRIX["protocol"],
        "scenario_id": scenario_id,
        "scenario_coefficients": SCENARIOS[scenario_id],
        "sample_size": n,
        "dgp_burn_in": DGP_BURN_IN,
        "surrogates_requested": surrogates,
        "total_repetitions": repetitions,
        "master_seed": master_seed,
        "seed_schedule_id": "NumPy SeedSequence([master_seed, stable_scenario_key, replicate_index, stream_id]); stream 0=DGP, 1=null",
        "start_index": start,
        "stop_index": stop,
        "commit_sha": commit_sha,
        "matrix_sha256": _engineering_file_hash(Path(MATRIX_PATH)),
        "runner_sha256": _engineering_file_hash(Path(__file__)),
        "endpoint_identity": "analysis.numerical_spectral_verification.estimate_alpha",
        "null_implementation_identity": "analysis.appropriate_stochastic_null.parametric_short_memory_null",
        "requirements_lock_sha256": _engineering_file_hash(root / "requirements-lock.txt"),
        "python_version": sys.version,
        "platform_identity": platform.platform(),
    }


def execute_attempt(scenario_id, replicate_index, master_seed, n, surrogates):
    """One replicate through the runner's canonical endpoint and null implementation."""
    phi = SCENARIOS[scenario_id]
    dgp_rng, null_rng = replicate_rngs(master_seed, scenario_id, replicate_index)
    scenario_key = stable_scenario_key(scenario_id)
    row = {
        "replicate_index": replicate_index,
        "scenario_id": scenario_id,
        "scenario_key": scenario_key,
        "dgp_seed_identity": [master_seed, scenario_key, replicate_index, 0],
        "null_seed_identity": [master_seed, scenario_key, replicate_index, 1],
        "requested_surrogates": surrogates,
        "status": "INVALID",
        "reason": None,
    }
    try:
        series = generate_ar(phi, n, dgp_rng)
        row["generated_series_sha256"] = hashlib.sha256(
            np.asarray(series, dtype="<f8").tobytes()
        ).hexdigest()
        observed_alpha = float(estimate_alpha(series))
        result = parametric_short_memory_null(
            series, observed_alpha, null_rng, trials=surrogates
        )
        diagnostic = result.get("order_selection_diagnostic") or {}
        p_value = result.get("p_value_mc_add_one")
        row.update({
            "observed_alpha": observed_alpha,
            "null_valid": result.get("valid") is True,
            "requested_surrogates": int(result.get("trials_requested", surrogates)),
            "valid_surrogates": int(result.get("null_samples", 0)),
            "exceedances": result.get("exceedances"),
            "p_value_mc_add_one": (
                float(p_value) if p_value is not None and np.isfinite(float(p_value)) else None
            ),
            "selected_order": result.get("selected_order"),
            "surrogate_boundary_fraction": diagnostic.get("surrogate_boundary_fraction"),
            "refit_failures": diagnostic.get("refit_failures"),
            "alpha_estimation_failures": diagnostic.get("alpha_estimation_failures"),
        })
        if result.get("valid") is not True:
            row["reason"] = result.get("reason", "invalid_null_result")
        elif int(result.get("null_samples", 0)) != surrogates:
            row["reason"] = "requested_surrogate_count_not_fully_valid"
        elif row["p_value_mc_add_one"] is None:
            row["reason"] = "missing_or_nonfinite_p_value"
        else:
            row.update({
                "status": "VALID", "reason": None,
                "rejected": bool(row["p_value_mc_add_one"] <= NOMINAL_ALPHA),
            })
    except Exception as exc:
        row["reason"] = f"{type(exc).__name__}:{exc}"
    return row


def engineering_main() -> int:
    import argparse
    from analysis.type1_execution_artifacts import (
        load_verified_artifact, validate_attempt_records,
        write_artifact_with_manifest,
    )
    parser = argparse.ArgumentParser(description="Bounded V4 engineering-only execution; never formal calibration.")
    parser.add_argument("--engineering-test", action="store_true")
    parser.add_argument("--scenario", required=True, choices=SCENARIO_ORDER)
    parser.add_argument("--repetitions", type=int, default=6)
    parser.add_argument("--surrogates", type=int, default=1000)
    parser.add_argument("--n", type=int, default=REQUIRED_SAMPLE_SIZE)
    parser.add_argument("--master-seed", type=int, default=MASTER_SEED)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--stop-index", type=int)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--stop-after", type=int, help="Inject an interruption after this many new attempts.")
    args = parser.parse_args()
    if not args.engineering_test:
        raise SystemExit("BLOCKED: pass --engineering-test explicitly.")
    if args.scenario != "gaussian_ar2_phi_0_45_minus_0_10_n3328":
        raise SystemExit("BLOCKED: engineering mode is restricted to the declared stationary AR(2) baseline.")
    if not 1 <= args.repetitions <= 6:
        raise SystemExit("BLOCKED: at most six outer replicates are allowed in engineering mode.")
    if args.surrogates != 1000:
        raise SystemExit("BLOCKED: engineering equivalence requires exactly 1000 surrogates per replicate.")
    if args.n != REQUIRED_SAMPLE_SIZE or args.master_seed != MASTER_SEED:
        raise SystemExit("BLOCKED: engineering dimensions must match the candidate sample size and seed.")
    stop = args.repetitions if args.stop_index is None else args.stop_index
    if not 0 <= args.start_index < stop <= args.repetitions:
        raise SystemExit("BLOCKED: require 0 <= start-index < stop-index <= repetitions.")
    if args.stop_after is not None and args.stop_after < 1:
        raise SystemExit("BLOCKED: --stop-after must be positive.")
    identity = _engineering_identity(args.scenario, args.start_index, stop, args.repetitions, args.surrogates, args.n, args.master_seed)
    output = args.output
    records = []
    if output.exists():
        if not args.resume:
            raise SystemExit("BLOCKED: output exists; use --resume with identical identity or choose another path.")
        payload = load_verified_artifact(output, expected_identity=identity)
        records = payload.get("attempt_records")
        if not isinstance(records, list):
            raise SystemExit("BLOCKED: malformed checkpoint records.")
        validate_attempt_records(records, args.start_index, stop)
    elif args.resume:
        raise SystemExit("BLOCKED: checkpoint requested for resume does not exist.")
    present = {row["replicate_index"] for row in records}
    pending = [i for i in range(args.start_index, stop) if i not in present]
    executed = 0

    def save():
        validation = validate_attempt_records(records, args.start_index, stop)
        status = "ENGINEERING_INCOMPLETE"
        if validation["complete"]:
            status = "ENGINEERING_FAILED_INVALID_ATTEMPTS" if validation["invalid_count"] else "ENGINEERING_COMPLETE"
        artifact = {
            "artifact_kind": "V4_OFFICIAL_RUNNER_ENGINEERING_ONLY",
            "status": status,
            "scenario_id": args.scenario,
            "requested_surrogates_per_replicate": args.surrogates,
            "requested_repetitions": args.repetitions,
            "range_start_index": args.start_index,
            "range_stop_index": stop,
            "completed_indices": sorted(row["replicate_index"] for row in records),
            "missing_indices": validation["missing_indices"],
            "invalid_attempts": validation["invalid_count"],
            "attempt_records": sorted(records, key=lambda row: row["replicate_index"]),
            "formal_calibration_pass": False,
            "claim_support": False,
            "promotion_authority": False,
            "confirmatory_execution_authorized": False,
            "confirmatory_null_frozen": False,
            "interpretation": "Engineering-only execution of the runner's endpoint/null path; not a formal calibration result.",
        }
        write_artifact_with_manifest(output, artifact, identity)
        return artifact

    save()
    for index in pending:
        row = execute_attempt(args.scenario, index, args.master_seed, args.n, args.surrogates)
        records.append(row)
        executed += 1
        current = save()
        print(json.dumps({"replicate_index": index, "attempt_status": row["status"], "reason": row["reason"], "checkpoint_status": current["status"], "missing_indices": current["missing_indices"]}), flush=True)
        if args.stop_after is not None and executed >= args.stop_after:
            print("ENGINEERING INTERRUPTION INJECTED; checkpoint retained.")
            return 0
    final = save()
    print(json.dumps({"status": final["status"], "completed_indices": final["completed_indices"], "missing_indices": final["missing_indices"], "invalid_attempts": final["invalid_attempts"], "artifact": str(output), "manifest": str(output) + ".manifest.json", "formal_calibration_pass": False}, indent=2))
    return 0 if final["status"] in {"ENGINEERING_COMPLETE", "ENGINEERING_INCOMPLETE"} else 1


def main() -> int:
    import sys as _sys
    if "--engineering-test" in _sys.argv:
        return engineering_main()
    return formal_main()


if __name__ == "__main__":
    raise SystemExit(main())
