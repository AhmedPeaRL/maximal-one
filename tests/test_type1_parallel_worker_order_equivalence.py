from __future__ import annotations

import concurrent.futures
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
WORKER_ORDER = [4, 1, 5, 0, 3, 2]
MAX_WORKERS = 3

EVIDENCE_ROOT = ROOT / "artifacts" / "type1_parallel_worker_order"


def canonical_records(payload: dict) -> list[dict]:
    rows = payload.get("attempt_records")
    if not isinstance(rows, list):
        raise AssertionError("Missing attempt_records")
    return sorted(rows, key=lambda row: row["replicate_index"])


def scientific_record(row: dict) -> dict:
    # Fields that must match the connected reference per replicate.
    keys = (
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
    return {key: row.get(key) for key in keys}


class ParallelWorkerOrderEquivalenceTests(unittest.TestCase):
    """Compare concurrent CLI workers with the connected reference."""

    def setUp(self):
        EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)

    def run_cli(
        self,
        label: str,
        output: Path,
        start: int,
        stop: int,
    ) -> dict:
        output.parent.mkdir(parents=True, exist_ok=True)

        command = [
            sys.executable,
            "-m",
            "analysis.calibrate_null_type1_scenario",
            "--engineering-test",
            "--scenario", SCENARIO,
            "--repetitions", str(TOTAL),
            "--surrogates", str(SURROGATES),
            "--n", str(SAMPLE_SIZE),
            "--master-seed", str(MASTER_SEED),
            "--start-index", str(start),
            "--stop-index", str(stop),
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

        log_path = EVIDENCE_ROOT / f"{label}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(result.stdout, encoding="utf-8")

        # Exit 1 can represent preserved invalid attempts. Do not discard
        # the artifact or silently retry/replace an attempt.
        self.assertIn(
            result.returncode,
            (0, 1),
            f"Unexpected CLI execution error; inspect {log_path}",
        )
        self.assertTrue(output.is_file(), f"Missing artifact: {output}")
        self.assertTrue(
            Path(str(output) + ".manifest.json").is_file(),
            f"Missing manifest: {output}",
        )

        payload = load_verified_artifact(output)
        self.assertIs(payload.get("formal_calibration_pass"), False)
        self.assertIs(payload.get("claim_support"), False)
        self.assertIs(payload.get("promotion_authority"), False)
        self.assertIs(
            payload.get("confirmatory_execution_authorized"), False
        )
        return payload

    def test_parallel_worker_order_matches_connected_reference(self):
        with tempfile.TemporaryDirectory(
            prefix="parallel-worker-order-",
            dir=EVIDENCE_ROOT,
        ) as temporary:
            run_dir = Path(temporary)

            # Reference: one connected CLI invocation for indices 0..5.
            connected_path = run_dir / "connected.json"
            connected = self.run_cli(
                "connected-reference",
                connected_path,
                0,
                TOTAL,
            )
            reference_rows = canonical_records(connected)

            self.assertEqual(
                [r["replicate_index"] for r in reference_rows],
                list(range(TOTAL)),
            )

            # Actual concurrency: independent CLI subprocesses execute
            # concurrently, with a deliberately permuted assignment order.
            def execute_worker(index: int):
                path = run_dir / f"worker-{index}.json"
                payload = self.run_cli(
                    f"parallel-worker-{index}",
                    path,
                    index,
                    index + 1,
                )
                rows = canonical_records(payload)
                if len(rows) != 1:
                    raise AssertionError(
                        f"Worker {index} must preserve exactly one attempt"
                    )
                if rows[0]["replicate_index"] != index:
                    raise AssertionError(
                        f"Worker {index} returned the wrong replicate"
                    )
                return index, rows[0]

            worker_rows = {}
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=MAX_WORKERS
            ) as executor:
                futures = [
                    executor.submit(execute_worker, index)
                    for index in WORKER_ORDER
                ]
                for future in concurrent.futures.as_completed(futures):
                    index, row = future.result()
                    if index in worker_rows:
                        raise AssertionError(
                            f"Duplicate worker result for index {index}"
                        )
                    worker_rows[index] = row

            self.assertEqual(set(worker_rows), set(range(TOTAL)))
            self.assertEqual(len(worker_rows), TOTAL)

            # Compare every requested scientific field against the connected
            # reference, indexed by the original replicate index.
            mismatches = []
            for reference_row in reference_rows:
                index = reference_row["replicate_index"]
                actual = scientific_record(worker_rows[index])
                expected = scientific_record(reference_row)
                if actual != expected:
                    mismatches.append({
                        "replicate_index": index,
                        "reference": expected,
                        "parallel_worker": actual,
                    })

            report = {
                "test": "TYPE1_PARALLEL_WORKER_ORDER_EQUIVALENCE_V1",
                "scenario": SCENARIO,
                "master_seed": MASTER_SEED,
                "total_repetitions_requested": TOTAL,
                "surrogates_requested_per_replicate": SURROGATES,
                "worker_order": WORKER_ORDER,
                "max_concurrent_workers": MAX_WORKERS,
                "replicate_indices_observed": sorted(worker_rows),
                "comparison_fields": list(
                    scientific_record(reference_rows[0]).keys()
                ),
                "mismatches": mismatches,
                "status": "PASS" if not mismatches else "FAIL",
                "formal_calibration_pass": False,
                "claim_support": False,
                "promotion_authority": False,
                "confirmatory_execution_authorized": False,
                "interpretation": (
                    "Concurrent CLI path equivalence only; "
                    "not Type-I calibration."
                ),
            }

            report_path = EVIDENCE_ROOT / "parallel_equivalence_report.json"
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(
                json.dumps(report, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            self.assertEqual(
                mismatches,
                [],
                f"Parallel worker mismatch; inspect {report_path}",
            )

            # Equivalence does not turn an invalid attempt into a valid one.
            invalid = [
                row["replicate_index"]
                for row in reference_rows
                if row.get("status") != "VALID"
            ]
            self.assertEqual(
                invalid,
                [],
                f"Invalid attempts remain failures: {invalid}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
