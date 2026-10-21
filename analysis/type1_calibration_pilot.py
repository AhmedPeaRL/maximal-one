from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess

from analysis.appropriate_stochastic_null import parametric_short_memory_null
from analysis.numerical_spectral_verification import estimate_alpha

MATRIX_PATH = Path("protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json")
MATRIX = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
SCENARIOS = {row["scenario_id"]: row for row in MATRIX["scenarios"]}
PILOT_SEED = int(MATRIX["runtime_plan"]["pilot_seed"])
PILOT_N = int(MATRIX["primary_design_candidate"]["sample_size"])
BURN_IN = int(MATRIX["primary_design_candidate"]["dgp_burn_in"])
MANIFEST_SUFFIX = ".manifest.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_scenario_key(scenario_id: str) -> int:
    """Stable 32-bit key derived from the scenario ID, not list position."""
    return int.from_bytes(hashlib.sha256(scenario_id.encode("utf-8")).digest()[:4], "big")


def replicate_rngs(master_seed: int, scenario_id: str, replicate_index: int):
    if min(master_seed, replicate_index) < 0:
        raise ValueError("Seed components must be non-negative")
    scenario_key = stable_scenario_key(scenario_id)
    dgp = np.random.default_rng(np.random.SeedSequence([master_seed, scenario_key, replicate_index, 0]))
    null = np.random.default_rng(np.random.SeedSequence([master_seed, scenario_key, replicate_index, 1]))
    return dgp, null


def shard_indices(start: int, stop: int, total: int) -> list[int]:
    if total < 1 or start < 0 or stop > total or start >= stop:
        raise ValueError("Require 0 <= start < stop <= total")
    return list(range(start, stop))


def generate_ar(
    phi: list[float],
    n: int,
    rng: np.random.Generator,
    burn_in: int = BURN_IN,
) -> np.ndarray:
    ar = np.asarray(
        [1.0] + [-float(value) for value in phi],
        dtype=float,
    )
    process = ArmaProcess(ar=ar, ma=np.asarray([1.0]))

    if not bool(process.isstationary):
        raise ValueError(
            f"Non-stationary declared pilot scenario: {phi}"
        )

    full = process.generate_sample(
        nsample=n + burn_in,
        burnin=0,
        distrvs=rng.standard_normal,
    )
    return np.asarray(full[burn_in:], dtype=np.float64)


def execute_attempt(
    index: int,
    scenario: dict,
    master_seed: int,
    surrogates: int,
    n: int = PILOT_N,
    burn_in: int = BURN_IN,
) -> dict:
    """Execute one replicate through the pilot's endpoint and null path."""
    dgp_rng, null_rng = replicate_rngs(
        master_seed,
        scenario["scenario_id"],
        index,
    )

    record = {
        "replicate_index": index,
        "dgp_seed_identity": [
            master_seed,
            stable_scenario_key(scenario["scenario_id"]),
            index,
            0,
        ],
        "null_seed_identity": [
            master_seed,
            stable_scenario_key(scenario["scenario_id"]),
            index,
            1,
        ],
        "status": "INVALID",
        "reason": None,
    }

    try:
        series = generate_ar(
            scenario["phi"],
            n,
            dgp_rng,
            burn_in=burn_in,
        )

        record["generated_series_sha256"] = hashlib.sha256(
            np.asarray(series, dtype="<f8").tobytes()
        ).hexdigest()

        observed_alpha = float(estimate_alpha(series))
        result = parametric_short_memory_null(
            series,
            observed_alpha,
            null_rng,
            trials=surrogates,
        )

        record.update({
            "observed_alpha": observed_alpha,
            "null_valid": bool(result.get("valid") is True),
            "requested_surrogates": int(
                result.get("trials_requested", surrogates)
            ),
            "valid_surrogates": int(result.get("null_samples", 0)),
            "exceedances": result.get("exceedances"),
            "p_value_mc_add_one": result.get("p_value_mc_add_one"),
            "selected_order": result.get("selected_order"),
            "order_selection_diagnostic": result.get(
                "order_selection_diagnostic"
            ),
        })

        if (
            result.get("valid") is True
            and int(result.get("null_samples", 0)) == surrogates
            and result.get("p_value_mc_add_one") is not None
        ):
            record.update({"status": "VALID", "reason": None})
        else:
            record["reason"] = result.get(
                "reason",
                "invalid_or_short_surrogate_result",
            )

    except Exception as exc:
        record["reason"] = f"{type(exc).__name__}: {exc}"
        record["traceback"] = traceback.format_exc(limit=8)

    return record


def manifest_path_for(path: Path) -> Path:
    return Path(str(path) + MANIFEST_SUFFIX)


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temp.replace(path)


def atomic_write(path: Path, payload: dict) -> None:
    """Write the artifact, then bind its exact bytes to a sidecar manifest."""
    atomic_write_json(path, payload)
    manifest = {
        "manifest_schema": "HCM_TYPE1_PILOT_ARTIFACT_MANIFEST_V1",
        "artifact_file": path.name,
        "artifact_sha256": sha256_file(path),
        "run_identity": payload.get("run_identity"),
    }
    atomic_write_json(manifest_path_for(path), manifest)


def load_verified_checkpoint(path: Path, expected_identity: dict) -> dict:
    """Fail closed unless artifact bytes, manifest, and run identity agree."""
    sidecar = manifest_path_for(path)

    if not path.is_file():
        raise ValueError(f"Missing checkpoint artifact: {path}")
    if not sidecar.is_file():
        raise ValueError(f"Missing checkpoint manifest: {sidecar}")

    try:
        manifest = json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(
            f"Unreadable checkpoint manifest: {sidecar}: {exc}"
        ) from exc

    if manifest.get("manifest_schema") != "HCM_TYPE1_PILOT_ARTIFACT_MANIFEST_V1":
        raise ValueError(f"Unsupported checkpoint manifest schema: {sidecar}")

    if manifest.get("artifact_file") != path.name:
        raise ValueError(f"Checkpoint manifest filename mismatch: {sidecar}")

    expected_hash = manifest.get("artifact_sha256")
    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise ValueError(f"Missing or malformed artifact_sha256: {sidecar}")

    actual_hash = sha256_file(path)
    if actual_hash.lower() != expected_hash.lower():
        raise ValueError(f"Checkpoint SHA-256 mismatch: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(
            f"Unreadable checkpoint artifact: {path}: {exc}"
        ) from exc

    if payload.get("run_identity") != manifest.get("run_identity"):
        raise ValueError(f"Checkpoint manifest/run identity mismatch: {path}")

    if payload.get("run_identity") != expected_identity:
        raise ValueError(
            "RESUME BLOCKED: output identity differs from current "
            "arguments/files/commit."
        )

    if not isinstance(payload.get("attempt_records"), list):
        raise ValueError(f"Malformed checkpoint attempt_records: {path}")

    return payload


def git_head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return os.environ.get("GITHUB_SHA", "UNAVAILABLE")


def main() -> int:
    parser = argparse.ArgumentParser(description="Exploratory Type-I runtime/reproducibility pilot only; never a formal calibration.")
    parser.add_argument("--scenario", required=True, choices=sorted(SCENARIOS))
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--stop-index", type=int, default=2)
    parser.add_argument("--total-repetitions", type=int, default=2)
    parser.add_argument("--surrogates", type=int, default=200)
    parser.add_argument("--master-seed", type=int, default=PILOT_SEED)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if MATRIX.get("status") != "DRAFT_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW":
        raise SystemExit("BLOCKED: pilot script requires the V4 draft status; it cannot run formal calibration.")
    if args.total_repetitions < 1 or args.total_repetitions > 20:
        raise SystemExit("PILOT SAFETY BLOCK: total repetitions must be between 1 and 20.")
    if args.surrogates != 200:
        raise SystemExit("PILOT SAFETY BLOCK: use exactly 200 surrogates per test for this runtime pilot.")
    indices = shard_indices(args.start_index, args.stop_index, args.total_repetitions)
    scenario = SCENARIOS[args.scenario]
    identity = {
        "protocol": MATRIX["protocol"],
        "scenario": args.scenario,
        "phi": scenario["phi"],
        "n": PILOT_N,
        "dgp_burn_in": BURN_IN,
        "surrogates": args.surrogates,
        "total_repetitions": args.total_repetitions,
        "start_index": args.start_index,
        "stop_index": args.stop_index,
        "master_seed": args.master_seed,
        "scenario_key": stable_scenario_key(args.scenario),
        "matrix_sha256": sha256_file(MATRIX_PATH),
        "script_sha256": sha256_file(Path(__file__)),
        "commit_sha": git_head(),
    }
    
    records: dict[int, dict] = {}

    if args.output.exists():
        if not args.resume:
            raise SystemExit(
                f"Output already exists; choose a new path or pass --resume: "
                f"{args.output}"
            )

        try:
            prior = load_verified_checkpoint(args.output, identity)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc

        prior_records = prior["attempt_records"]
        records = {
            int(row["replicate_index"]): row
            for row in prior_records
        }

        if len(records) != len(prior_records):
            raise SystemExit(
                "RESUME BLOCKED: duplicate replicate indices in checkpoint."
            )

        if any(index not in indices for index in records):
            raise SystemExit(
                "RESUME BLOCKED: checkpoint contains records outside this shard range."
            )

    elif args.resume:
        raise SystemExit(
            "RESUME BLOCKED: no existing checkpoint file was found."
        )

    started = time.monotonic()
    for index in indices:
        if index in records:
            continue

        attempt_start = time.monotonic()

        record = execute_attempt(
            index=index,
            scenario={"scenario_id": args.scenario, **scenario},
            master_seed=args.master_seed,
            surrogates=args.surrogates,
        )

        record["elapsed_seconds"] = round(
            time.monotonic() - attempt_start,
            6,
        )
        records[index] = record
        payload = {
            "artifact_kind": "EXPLORATORY_PILOT_ONLY_NOT_FORMAL_CALIBRATION",
            "status": "PILOT_INCOMPLETE_OR_DIAGNOSTIC_ONLY",
            "run_identity": identity,
            "environment": {"python_version": sys.version, "platform": platform.platform(), "workflow_run_id": os.environ.get("GITHUB_RUN_ID"), "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT")},
            "elapsed_seconds_so_far": round(time.monotonic() - started, 6),
            "attempt_records": [records[k] for k in sorted(records)],
            "invalid_attempts": sum(row["status"] != "VALID" for row in records.values()),
            "formal_calibration_pass": False,
            "claim_support": False,
            "promotion_authority": False,
            "confirmatory_null_frozen": False,
            "interpretation": "Runtime, determinism, and engineering pilot only. These 200-surrogate runs are not production calibration and cannot pass or fail the formal Type-I protocol.",
        }
        atomic_write(args.output, payload)
        print(f"scenario={args.scenario} replicate={index} status={record['status']} elapsed_seconds={record['elapsed_seconds']}", flush=True)

    final = json.loads(args.output.read_text(encoding="utf-8")) if args.output.exists() else {}
    final["elapsed_seconds_total_for_this_invocation"] = round(time.monotonic() - started, 6)
    final["completed_indices_in_this_shard"] = sorted(records)
    final["shard_complete"] = all(index in records for index in indices)
    final["invalid_attempts"] = sum(
        row.get("status") != "VALID"
        for row in final.get("attempt_records", [])
    )
    if not final["shard_complete"]:
        final["status"] = "PILOT_INCOMPLETE_OR_DIAGNOSTIC_ONLY"
    elif final["invalid_attempts"] > 0:
        final["status"] = "PILOT_FAILED_DIAGNOSTIC_ONLY"
    else:
        final["status"] = "PILOT_COMPLETE_DIAGNOSTIC_ONLY"
    final["formal_calibration_pass"] = False
    atomic_write(args.output, final)
    print(json.dumps({"status": final["status"], "scenario": args.scenario, "records": len(final.get("attempt_records", [])), "invalid_attempts": final.get("invalid_attempts"), "elapsed_seconds": final["elapsed_seconds_total_for_this_invocation"], "output": str(args.output)}, indent=2))
    
    return (
        0
        if (
            final["shard_complete"]
            and final["invalid_attempts"] == 0
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
