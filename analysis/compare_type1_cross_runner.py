from __future__ import annotations

import argparse
import json
from pathlib import Path

from analysis.type1_execution_artifacts import load_verified_artifact

COMPARE_FIELDS = (
    "replicate_index",
    "dgp_seed_identity",
    "null_seed_identity",
    "generated_series_sha256",
    "observed_alpha",
    "requested_surrogates",
    "valid_surrogates",
    "exceedances",
    "p_value_mc_add_one",
    "selected_order",
    "surrogate_boundary_fraction",
    "refit_failures",
    "alpha_estimation_failures",
    "status",
    "reason",
)

# The range must differ for each shard. Runtime platform identity is
# retained and reported, but may legitimately differ between hosted runners.
ALLOWED_IDENTITY_DIFFERENCES = {
    "start_index",
    "stop_index",
    "platform_identity",  # descriptive only; never evidence of independence
    "workflow_job_id",
    "runner_instance_id",
}


def projection(row: dict) -> dict:
    return {key: row.get(key) for key in COMPARE_FIELDS}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--worker", type=Path, action="append", required=True)
    parser.add_argument("--total-repetitions", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    failures = []
    compared = {}
    platform_identities = []
    runner_identity_records = []
    replicate_records = {}
    reference = None

    try:
        reference = load_verified_artifact(args.reference)
        reference_identity = reference["run_identity"]
        reference_rows = reference["attempt_records"]

        if reference.get("artifact_kind") != "V4_OFFICIAL_RUNNER_ENGINEERING_ONLY":
            failures.append("Reference is not an official engineering artifact")

        if reference.get("formal_calibration_pass") is not False:
            failures.append("Reference must keep formal_calibration_pass=false")

        if reference_identity.get("total_repetitions") != args.total_repetitions:
            failures.append("Reference denominator differs from requested N")

        if (
            reference_identity.get("start_index") != 0
            or reference_identity.get("stop_index") != args.total_repetitions
        ):
            failures.append("Reference does not cover the full requested range")

        expected_indices = list(range(args.total_repetitions))
        reference_map = {
            row.get("replicate_index"): row for row in reference_rows
        }
        if sorted(reference_map) != expected_indices:
            failures.append("Reference has missing or duplicate replicate indices")

        reference_runner_id = reference_identity.get("runner_instance_id")
        if not reference_runner_id:
            failures.append("Connected reference is missing runner_instance_id")
        runner_ids = {reference_runner_id} if reference_runner_id else set()
        reference_run_id = reference_identity.get("workflow_run_id")
        reference_run_attempt = reference_identity.get("workflow_run_attempt")
        reference_job_id = reference_identity.get("workflow_job_id")
        runner_identity_records.append({
            "role": "connected_reference",
            "workflow_run_id": reference_run_id,
            "workflow_run_attempt": reference_run_attempt,
            "workflow_job_id": reference_job_id,
            "runner_instance_id": reference_runner_id,
            "platform_identity": reference_identity.get("platform_identity"),
        })
        platform_identities.append({
            "role": "connected_reference",
            "platform_identity": reference_identity.get("platform_identity"),
        })

        worker_map = {}

        for worker_path in args.worker:
            payload = load_verified_artifact(worker_path)
            identity = payload["run_identity"]

            if payload.get("artifact_kind") != "V4_OFFICIAL_RUNNER_ENGINEERING_ONLY":
                failures.append(f"Not an official engineering artifact: {worker_path}")

            if payload.get("formal_calibration_pass") is not False:
                failures.append(f"Formal flag is not false: {worker_path}")

            worker_runner_id = identity.get("runner_instance_id")
            if not worker_runner_id:
                failures.append(f"{worker_path}: missing runner_instance_id")
            elif worker_runner_id in runner_ids:
                failures.append(f"{worker_path}: runner instance is not independent")
            else:
                runner_ids.add(worker_runner_id)

            if identity.get("workflow_run_id") != reference_run_id:
                failures.append(f"{worker_path}: workflow_run_id differs from reference")
            if identity.get("workflow_run_attempt") != reference_run_attempt:
                failures.append(f"{worker_path}: workflow_run_attempt differs from reference")
            if not identity.get("workflow_job_id"):
                failures.append(f"{worker_path}: missing workflow_job_id")
            if identity.get("workflow_job_id") == reference_job_id:
                failures.append(f"{worker_path}: worker job identity matches connected reference")

            runner_identity_records.append({
                "role": f"worker_{identity.get('start_index')}",
                "workflow_run_id": identity.get("workflow_run_id"),
                "workflow_run_attempt": identity.get("workflow_run_attempt"),
                "workflow_job_id": identity.get("workflow_job_id"),
                "runner_instance_id": worker_runner_id,
                "platform_identity": identity.get("platform_identity"),
            })

            # Match scientific/protocol identity fields except the declared
            # shard range and per-job/instance metadata. Platform identity is
            # descriptive only and cannot substitute for runner_instance_id.
            for key, expected_value in reference_identity.items():
                if key in ALLOWED_IDENTITY_DIFFERENCES:
                    continue
                if identity.get(key) != expected_value:
                    failures.append(
                        f"{worker_path}: identity mismatch in {key}"
                    )

            start = identity.get("start_index")
            stop = identity.get("stop_index")
            if (
                not isinstance(start, int)
                or not isinstance(stop, int)
                or stop != start + 1
                or not 0 <= start < args.total_repetitions
            ):
                failures.append(
                    f"{worker_path}: expected exactly one assigned replicate"
                )
                continue

            rows = payload.get("attempt_records")
            if not isinstance(rows, list) or len(rows) != 1:
                failures.append(
                    f"{worker_path}: expected exactly one attempt record"
                )
                continue

            row = rows[0]
            index = row.get("replicate_index")
            if index != start:
                failures.append(
                    f"{worker_path}: attempt index does not match assigned range"
                )
                continue

            if index in worker_map:
                failures.append(f"Duplicate worker result for index {index}")
                continue

            worker_map[index] = row
            platform_identities.append({
                "role": f"worker_{index}",
                "platform_identity": identity.get("platform_identity"),
            })

        expected_indices = list(range(args.total_repetitions))
        if sorted(worker_map) != expected_indices:
            failures.append(
                "Worker artifacts do not cover each requested index exactly once"
            )

        for index in expected_indices:
            if index not in reference_map or index not in worker_map:
                continue

            expected = projection(reference_map[index])
            actual = projection(worker_map[index])
            if actual != expected:
                failures.append(
                    f"Replicate {index} differs from connected reference"
                )
                comparison_status = "MISMATCH"
            else:
                compared[str(index)] = "MATCH"
                comparison_status = "MATCH"
            replicate_records[str(index)] = {
                "comparison": comparison_status,
                "reference_record": reference_map[index],
                "worker_record": worker_map[index],
            }

        invalid = [
            index for index, row in sorted(worker_map.items())
            if row.get("status") != "VALID"
        ]
        if invalid:
            failures.append(
                f"Invalid worker attempts must remain failures: {invalid}"
            )

    except Exception as exc:
        failures.append(f"{type(exc).__name__}: {exc}")

    report = {
        "test": "TYPE1_CROSS_RUNNER_WORKER_EQUIVALENCE_V1",
        "status": "PASS" if not failures else "FAIL",
        "total_repetitions_requested": args.total_repetitions,
        "replicate_comparisons": compared,
        "replicate_records": replicate_records,
        "runner_identity_records": runner_identity_records,
        "platform_identities": platform_identities,
        "failures": failures,
        "formal_calibration_pass": False,
        "claim_support": False,
        "promotion_authority": False,
        "confirmatory_execution_authorized": False,
        "interpretation": (
            "Cross-runner engineering comparison only; "
            "not formal Type-I calibration."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
