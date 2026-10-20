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


def generate_ar(phi: list[float], n: int, rng: np.random.Generator) -> np.ndarray:
    ar = np.asarray([1.0] + [-float(value) for value in phi], dtype=float)
    process = ArmaProcess(ar=ar, ma=np.asarray([1.0]))
    if not bool(process.isstationary):
        raise ValueError(f"Non-stationary declared pilot scenario: {phi}")
    full = process.generate_sample(nsample=n + BURN_IN, burnin=0, distrvs=rng.standard_normal)
    return np.asarray(full[BURN_IN:], dtype=np.float64)


def atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


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
            raise SystemExit(f"Output already exists; choose a new path or pass --resume: {args.output}")
        prior = json.loads(args.output.read_text(encoding="utf-8"))
        if prior.get("run_identity") != identity:
            raise SystemExit("RESUME BLOCKED: output identity differs from current arguments/files/commit.")
        records = {int(row["replicate_index"]): row for row in prior.get("attempt_records", [])}
        if any(index not in indices for index in records):
            raise SystemExit("RESUME BLOCKED: checkpoint contains records outside this shard range.")
    elif args.resume:
        raise SystemExit("RESUME BLOCKED: no existing checkpoint file was found.")

    started = time.monotonic()
    for index in indices:
        if index in records:
            continue
        attempt_start = time.monotonic()
        dgp_rng, null_rng = replicate_rngs(args.master_seed, args.scenario, index)
        record = {
            "replicate_index": index,
            "dgp_seed_identity": [args.master_seed, stable_scenario_key(args.scenario), index, 0],
            "null_seed_identity": [args.master_seed, stable_scenario_key(args.scenario), index, 1],
            "status": "INVALID",
            "reason": None,
        }
        try:
            series = generate_ar(scenario["phi"], PILOT_N, dgp_rng)
            observed_alpha = float(estimate_alpha(series))
            result = parametric_short_memory_null(series, observed_alpha, null_rng, trials=args.surrogates)
            record.update({
                "observed_alpha": observed_alpha,
                "null_valid": bool(result.get("valid") is True),
                "requested_surrogates": int(result.get("trials_requested", args.surrogates)),
                "valid_surrogates": int(result.get("null_samples", 0)),
                "exceedances": result.get("exceedances"),
                "p_value_mc_add_one": result.get("p_value_mc_add_one"),
                "selected_order": result.get("selected_order"),
                "order_selection_diagnostic": result.get("order_selection_diagnostic"),
            })
            if result.get("valid") is True and int(result.get("null_samples", 0)) == args.surrogates and result.get("p_value_mc_add_one") is not None:
                record.update({"status": "VALID", "reason": None})
            else:
                record["reason"] = result.get("reason", "invalid_or_short_surrogate_result")
        except Exception as exc:
            record["reason"] = f"{type(exc).__name__}: {exc}"
            record["traceback"] = traceback.format_exc(limit=8)
        record["elapsed_seconds"] = round(time.monotonic() - attempt_start, 6)
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
    final["status"] = "PILOT_COMPLETE_DIAGNOSTIC_ONLY" if final["shard_complete"] else "PILOT_INCOMPLETE_OR_DIAGNOSTIC_ONLY"
    final["formal_calibration_pass"] = False
    atomic_write(args.output, final)
    print(json.dumps({"status": final["status"], "scenario": args.scenario, "records": len(final.get("attempt_records", [])), "invalid_attempts": final.get("invalid_attempts"), "elapsed_seconds": final["elapsed_seconds_total_for_this_invocation"], "output": str(args.output)}, indent=2))
    return 0 if final["shard_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
