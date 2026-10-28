from __future__ import annotations

import concurrent.futures
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from analysis.type1_execution_artifacts import load_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = "gaussian_ar2_phi_0_45_minus_0_10_n3328"
MASTER_SEED = 20261021
TOTAL = 6
SURROGATES = 1000
SAMPLE_SIZE = 3328
EVIDENCE = ROOT / "artifacts" / "type1_worker_assignment_matrices"

# Same six replicate indices; different worker-to-index assignments.
MATRIX_A = {
    "worker-0": [0, 3],
    "worker-1": [1, 4],
    "worker-2": [2, 5],
}
MATRIX_B = {
    "worker-0": [4, 1],
    "worker-1": [5, 2],
    "worker-2": [0, 3],
}

FIELDS = (
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_rows(payload: dict) -> list[dict]:
    rows = payload.get("attempt_records")
    if not isinstance(rows, list):
        raise AssertionError("Missing attempt_records")
    return sorted(rows, key=lambda row: row["replicate_index"])


def scientific_row(row: dict) -> dict:
    return {field: row.get(field) for field in FIELDS}


class WorkerAssignmentMatrixTests(unittest.TestCase):
    """Engineering-only comparison; never a formal calibration."""

    @classmethod
    def setUpClass(cls):
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        cls.run_dir = Path(
            tempfile.mkdtemp(prefix="run-", dir=EVIDENCE)
        )
        cls.logs = []

    def run_replicate(self, label: str, index: int) -> dict:
        output = self.run_dir / f"{label}-replicate-{index}.json"
        command = [
            sys.executable,
            "-m", "analysis.calibrate_null_type1_scenario",
            "--engineering-test",
            "--scenario", SCENARIO,
            "--repetitions", str(TOTAL),
            "--surrogates", str(SURROGATES),
            "--n", str(SAMPLE_SIZE),
            "--master-seed", str(MASTER_SEED),
            "--start-index", str(index),
            "--stop-index", str(index + 1),
            "--output", str(output),
        ]

        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

        log = self.run_dir / f"{label}-replicate-{index}.log"
        log.write_text(result.stdout, encoding="utf-8")
        self.logs.append({
            "label": label,
            "index": index,
            "command": command,
            "exit_code": result.returncode,
            "log": str(log.relative_to(ROOT)),
        })

        # Preserve exit 1 as a possible recorded invalid attempt.
        # Any other exit code is an execution failure.
        self.assertIn(
            result.returncode, (0, 1),
            f"Unexpected CLI exit for {label}/{index}: {log}",
        )
        self.assertTrue(output.is_file(), f"Missing output: {output}")
        self.assertTrue(
            Path(str(output) + ".manifest.json").is_file(),
            f"Missing manifest: {output}",
        )

        payload = load_verified_artifact(output)
        for field in (
            "formal_calibration_pass",
            "claim_support",
            "promotion_authority",
            "confirmatory_execution_authorized",
        ):
            self.assertIs(
                payload.get(field), False,
                f"{field} must remain false in engineering mode",
            )

        rows = canonical_rows(payload)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["replicate_index"], index)
        self.assertEqual(rows[0].get("requested_surrogates"), SURROGATES)
        return rows[0]

    def run_assignment_matrix(self, name: str, matrix: dict) -> dict:
        assigned = [
            index
            for indices in matrix.values()
            for index in indices
        ]

        # The requested denominator is fixed before any worker starts.
        self.assertEqual(sorted(assigned), list(range(TOTAL)))
        self.assertEqual(len(assigned), TOTAL)
        self.assertEqual(len(set(assigned)), TOTAL)

        observed = {}

        def worker(worker_name: str, indices: list[int]):
            local = {}
            for index in indices:
                if index in local:
                    raise AssertionError(
                        f"Duplicate index {index} within {worker_name}"
                    )
                local[index] = self.run_replicate(
                    f"{name}-{worker_name}", index
                )
            return worker_name, local

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=len(matrix)
        ) as executor:
            futures = [
                executor.submit(worker, worker_name, indices)
                for worker_name, indices in matrix.items()
            ]
            for future in concurrent.futures.as_completed(futures):
                worker_name, local = future.result()
                for index, row in local.items():
                    if index in observed:
                        raise AssertionError(
                            f"Duplicate result for index {index}"
                        )
                    observed[index] = row

        self.assertEqual(set(observed), set(range(TOTAL)))
        self.assertEqual(len(observed), TOTAL)
        return observed

    def test_two_assignment_matrices_match_connected_reference(self):
        connected_output = self.run_dir / "connected-reference.json"
        command = [
            sys.executable,
            "-m", "analysis.calibrate_null_type1_scenario",
            "--engineering-test",
            "--scenario", SCENARIO,
            "--repetitions", str(TOTAL),
            "--surrogates", str(SURROGATES),
            "--n", str(SAMPLE_SIZE),
            "--master-seed", str(MASTER_SEED),
            "--start-index", "0",
            "--stop-index", str(TOTAL),
            "--output", str(connected_output),
        ]

        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        reference_log = self.run_dir / "connected-reference.log"
        reference_log.write_text(result.stdout, encoding="utf-8")
        self.logs.append({
            "label": "connected-reference",
            "exit_code": result.returncode,
            "command": command,
            "log": str(reference_log.relative_to(ROOT)),
        })

        self.assertIn(result.returncode, (0, 1), result.stdout)
        self.assertTrue(connected_output.is_file())
        self.assertTrue(
            Path(str(connected_output) + ".manifest.json").is_file()
        )

        reference_payload = load_verified_artifact(connected_output)
        self.assertIs(
            reference_payload.get("formal_calibration_pass"), False
        )
        reference_rows = canonical_rows(reference_payload)
        self.assertEqual(
            [r["replicate_index"] for r in reference_rows],
            list(range(TOTAL)),
        )

        reference = {
            row["replicate_index"]: row for row in reference_rows
        }

        matrix_a = self.run_assignment_matrix("matrix-a", MATRIX_A)
        matrix_b = self.run_assignment_matrix("matrix-b", MATRIX_B)

        mismatches = []
        invalid_attempts = []

        for index in range(TOTAL):
            expected = scientific_row(reference[index])

            for label, actual_rows in (
                ("matrix-a", matrix_a),
                ("matrix-b", matrix_b),
            ):
                actual = scientific_row(actual_rows[index])
                if actual != expected:
                    mismatches.append({
                        "matrix": label,
                        "replicate_index": index,
                        "reference": expected,
                        "actual": actual,
                    })

            # Invalid attempts remain failures; never silently replace.
            for label, actual_rows in (
                ("reference", reference),
                ("matrix-a", matrix_a),
                ("matrix-b", matrix_b),
            ):
                row = actual_rows[index]
                if row.get("status") != "VALID":
                    invalid_attempts.append({
                        "source": label,
                        "replicate_index": index,
                        "status": row.get("status"),
                        "reason": row.get("reason"),
                    })

        report = {
            "test": "TYPE1_WORKER_ASSIGNMENT_MATRIX_INVARIANCE_V1",
            "scenario": SCENARIO,
            "master_seed": MASTER_SEED,
            "requested_repetitions": TOTAL,
            "requested_surrogates_per_replicate": SURROGATES,
            "sample_size": SAMPLE_SIZE,
            "matrix_a": MATRIX_A,
            "matrix_b": MATRIX_B,
            "fields_compared": list(FIELDS),
            "connected_artifact_sha256": sha256_file(connected_output),
            "matrix_a_indices": sorted(matrix_a),
            "matrix_b_indices": sorted(matrix_b),
            "mismatches": mismatches,
            "invalid_attempts": invalid_attempts,
            "logs": self.logs,
            "status": (
                "PASS_ENGINEERING_ONLY"
                if not mismatches and not invalid_attempts
                else "FAIL_ENGINEERING"
            ),
            "formal_calibration_pass": False,
            "claim_support": False,
            "promotion_authority": False,
            "confirmatory_execution_authorized": False,
        }

        report_path = EVIDENCE / "assignment_matrix_report.json"
        report_path.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        self.assertEqual(
            mismatches, [],
            f"Assignment mismatch; inspect {report_path}",
        )
        self.assertEqual(
            invalid_attempts, [],
            f"Invalid attempts block this engineering comparison: {report_path}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
