from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from analysis.compare_type1_cross_runner import main
from analysis.type1_execution_artifacts import (
    validate_run_identity,
    write_artifact_with_manifest,
)


def identity(start, stop, runner_id, job_id):
    return {
        "protocol": "HCM_TYPE1_CALIBRATION_V4_CANDIDATE",
        "scenario_id": "synthetic_cross_runner_test",
        "scenario_coefficients": [0.45, -0.1],
        "sample_size": 3328,
        "dgp_burn_in": 2000,
        "surrogates_requested": 1000,
        "total_repetitions": 2,
        "master_seed": 20261021,
        "seed_schedule_id": "test-seed-schedule-v1",
        "start_index": start,
        "stop_index": stop,
        "commit_sha": "engineering-test-only",
        "matrix_sha256": "a" * 64,
        "runner_sha256": "b" * 64,
        "workflow_run_id": 41904649393,
        "workflow_run_attempt": 1,
        "workflow_job_id": job_id,
        "runner_instance_id": runner_id,
        "endpoint_identity": "canonical_primary_alpha",
        "null_implementation_identity": "existing-null-implementation",
        "requirements_lock_sha256": "c" * 64,
        "python_version": "test-runtime",
        "platform_identity": "same-platform-is-not-independence-proof",
    }


def row(index):
    return {
        "replicate_index": index,
        "dgp_seed_identity": [20261021, 1, index, 0],
        "null_seed_identity": [20261021, 1, index, 1],
        "generated_series_sha256": f"{index:064x}",
        "observed_alpha": 0.5,
        "requested_surrogates": 1000,
        "valid_surrogates": 1000,
        "exceedances": 500,
        "p_value_mc_add_one": 0.5,
        "selected_order": 2,
        "surrogate_boundary_fraction": 0.0,
        "refit_failures": 0,
        "alpha_estimation_failures": 0,
        "status": "VALID",
        "reason": None,
    }


class CrossRunnerIdentityTests(unittest.TestCase):
    def run_comparison(self, root, ref_id, worker_ids):
        ref = root / "reference.json"
        write_artifact_with_manifest(ref, {
            "artifact_kind": "V4_OFFICIAL_RUNNER_ENGINEERING_ONLY",
            "formal_calibration_pass": False,
            "attempt_records": [row(0), row(1)],
        }, ref_id)
        workers = []
        for index, worker_id in enumerate(worker_ids):
            path = root / f"worker-{index}.json"
            write_artifact_with_manifest(path, {
                "artifact_kind": "V4_OFFICIAL_RUNNER_ENGINEERING_ONLY",
                "formal_calibration_pass": False,
                "attempt_records": [row(index)],
            }, worker_id)
            workers.append(path)
        output = root / "comparison.json"
        argv = ["compare", "--reference", str(ref), "--total-repetitions", "2", "--output", str(output)]
        for worker in workers:
            argv.extend(["--worker", str(worker)])
        with patch("sys.argv", argv):
            code = main()
        return code, json.loads(output.read_text(encoding="utf-8"))

    def test_distinct_runner_instances_pass_and_retain_each_replicate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ref = identity(0, 2, "1" * 64, "connected-reference")
            workers = [
                identity(0, 1, "2" * 64, "independent-workers"),
                identity(1, 2, "3" * 64, "independent-workers"),
            ]
            code, report = self.run_comparison(root, ref, workers)
            self.assertEqual(code, 0)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(set(report["replicate_records"]), {"0", "1"})
            self.assertEqual(len(report["runner_identity_records"]), 3)

    def test_same_runner_as_reference_fails_even_if_platform_differs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ref = identity(0, 2, "1" * 64, "connected-reference")
            workers = [
                identity(0, 1, "1" * 64, "independent-workers"),
                identity(1, 2, "3" * 64, "independent-workers"),
            ]
            workers[0]["platform_identity"] = "different-platform-string"
            code, report = self.run_comparison(root, ref, workers)
            self.assertEqual(code, 1)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any("runner instance is not independent" in item for item in report["failures"]))

    def test_missing_runner_instance_identity_is_rejected(self):
        value = identity(0, 1, "2" * 64, "independent-workers")
        value.pop("runner_instance_id")
        with self.assertRaisesRegex(ValueError, "runner_instance_id"):
            validate_run_identity(value)

    def test_missing_runner_environment_identity_is_rejected(self):
        from unittest.mock import patch
        from analysis.calibrate_null_type1_scenario import _runner_instance_identity
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "Missing GitHub runner identity fields"):
                _runner_instance_identity()

    def test_invalid_workflow_run_identity_is_rejected(self):
        value = identity(0, 1, "2" * 64, "independent-workers")
        value["workflow_run_attempt"] = 0
        with self.assertRaisesRegex(ValueError, "workflow_run_attempt"):
            validate_run_identity(value)

    def test_worker_run_identity_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ref = identity(0, 2, "1" * 64, "connected-reference")
            workers = [
                identity(0, 1, "2" * 64, "independent-workers"),
                identity(1, 2, "3" * 64, "independent-workers"),
            ]
            workers[1]["workflow_run_id"] += 1
            code, report = self.run_comparison(root, ref, workers)
            self.assertEqual(code, 1)
            self.assertTrue(any("workflow_run_id differs" in item for item in report["failures"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
