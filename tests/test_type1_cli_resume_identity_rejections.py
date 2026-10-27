from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from analysis.type1_execution_artifacts import (
    atomic_write_bytes,
    canonical_json_bytes,
    sha256_bytes,
)

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = "gaussian_ar2_phi_0_45_minus_0_10_n3328"
MASTER_SEED = 20261021
SAMPLE_SIZE = 3328
SURROGATES = 1000
TOTAL = 6


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cli_command(checkpoint: Path, *, resume: bool) -> list[str]:
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
        "--start-index", "0",
        "--stop-index", "2",
        "--output", str(checkpoint),
    ]
    if resume:
        command.append("--resume")
    return command


def changed_identity_fields() -> dict:
    return {
        "protocol": "HCM_TYPE1_CALIBRATION_V4_TEST_MUTATION",
        "scenario_id": "gaussian_ar1_phi_0_4_n3328",
        "scenario_coefficients": [0.41],
        "sample_size": SAMPLE_SIZE + 1,
        "dgp_burn_in": 2001,
        "surrogates_requested": SURROGATES - 1,
        "total_repetitions": TOTAL + 1,
        "master_seed": MASTER_SEED + 1,
        "seed_schedule_id": "mutated-seed-schedule",
        "start_index": 1,
        "stop_index": 1,
        "commit_sha": "b" * 40,
        "matrix_sha256": "4" * 64,
        "runner_sha256": "5" * 64,
        "endpoint_identity": "mutated.endpoint",
        "null_implementation_identity": "mutated.null",
        "requirements_lock_sha256": "6" * 64,
        "python_version": "mutated-python",
        "platform_identity": "mutated-platform",
    }


class OfficialCliResumeIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence_dir = (
            ROOT / "artifacts" / "type1_cli_resume_identity"
        )
        cls.evidence_dir.mkdir(parents=True, exist_ok=True)

    def run_cli(self, label: str, command: list[str]) -> subprocess.CompletedProcess:
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        log = self.evidence_dir / f"{label}.log"
        log.write_text(result.stdout, encoding="utf-8")
        return result

    def test_cli_rejects_each_identity_mismatch_without_mutation(self):
        with tempfile.TemporaryDirectory(
            prefix="cli-resume-",
            dir=self.evidence_dir,
        ) as temporary:
            checkpoint = Path(temporary) / "checkpoint.json"
            manifest = Path(str(checkpoint) + ".manifest.json")

            # Create a real checkpoint through the official CLI.
            created = self.run_cli(
                "create-valid-checkpoint",
                cli_command(checkpoint, resume=False),
            )
            baseline_checkpoint_copy = Path(temporary) / "baseline-checkpoint.json"
            baseline_manifest_copy = Path(temporary) / "baseline-manifest.json"

            baseline_checkpoint_copy.write_bytes(checkpoint.read_bytes())
            baseline_manifest_copy.write_bytes(manifest.read_bytes())

            baseline_checkpoint_sha256 = sha256_file(baseline_checkpoint_copy)
            baseline_manifest_sha256 = sha256_file(baseline_manifest_copy)
            self.assertEqual(
                created.returncode, 0, created.stdout
            )
            self.assertTrue(checkpoint.is_file())
            self.assertTrue(manifest.is_file())

            baseline_payload = json.loads(
                checkpoint.read_text(encoding="utf-8")
            )
            baseline_manifest = json.loads(
                manifest.read_text(encoding="utf-8")
            )
            baseline_identity = baseline_payload["run_identity"]

            self.assertEqual(
                baseline_identity,
                baseline_manifest["run_identity"],
            )

            mismatches = changed_identity_fields()
            self.assertEqual(
                set(mismatches),
                set(baseline_identity),
                "Update this test whenever the identity schema changes.",
            )

            summary = []

            for field, replacement in mismatches.items():
                with self.subTest(field=field):
                    payload = json.loads(
                        json.dumps(baseline_payload)
                    )
                    current_manifest = json.loads(
                        json.dumps(baseline_manifest)
                    )

                    mutated_identity = dict(baseline_identity)
                    mutated_identity[field] = replacement

                    payload["run_identity"] = mutated_identity
                    current_manifest["run_identity"] = mutated_identity

                    artifact_bytes = canonical_json_bytes(payload)
                    current_manifest["artifact_sha256"] = (
                        sha256_bytes(artifact_bytes)
                    )
                    manifest_bytes = canonical_json_bytes(
                        current_manifest
                    )

                    # Install a self-consistent checkpoint whose recorded
                    # identity differs from the actual CLI environment.
                    atomic_write_bytes(checkpoint, artifact_bytes)
                    atomic_write_bytes(manifest, manifest_bytes)

                    before_checkpoint = checkpoint.read_bytes()
                    before_manifest = manifest.read_bytes()

                    immutable_baseline_checkpoint = bytes(before_checkpoint)
                    immutable_baseline_manifest = bytes(before_manifest)

                    result = self.run_cli(
                        f"resume-reject-{field}",
                        cli_command(checkpoint, resume=True),
                    )

                    after_checkpoint = checkpoint.read_bytes()
                    after_manifest = manifest.read_bytes()

                    self.assertEqual(
                        result.returncode,
                        1,
                        f"Unexpected exit code for identity mismatch {field}: "
                        f"{result.returncode}\n{result.stdout}",
                    )
                    self.assertIn(
                        "Artifact run identity differs from requested execution",
                        result.stdout,
                        f"Expected identity-rejection diagnostic missing for {field}:\n"
                        f"{result.stdout}",
                    )
                    self.assertEqual(
                        after_checkpoint, before_checkpoint,
                        f"Rejected resume changed checkpoint for {field}",
                    )
                    self.assertEqual(
                        after_manifest, before_manifest,
                        f"Rejected resume changed manifest for {field}",
                    )
                    self.assertEqual(
                        sha256_file(baseline_checkpoint_copy),
                        baseline_checkpoint_sha256,
                    )
                    self.assertEqual(
                        sha256_file(baseline_manifest_copy),
                        baseline_manifest_sha256,
                    )

                    summary.append({
                        "field": field,
                        "exit_code": result.returncode,
                        "checkpoint_sha256_before": sha256_bytes(
                            before_checkpoint
                        ),
                        "checkpoint_sha256_after": sha256_bytes(
                            after_checkpoint
                        ),
                        "manifest_sha256_before": sha256_bytes(
                            before_manifest
                        ),
                        "manifest_sha256_after": sha256_bytes(
                            after_manifest
                        ),
                        "log": f"resume-reject-{field}.log",
                    })

            report = {
                "test": "OFFICIAL_CLI_RESUME_IDENTITY_REJECTIONS",
                "status": "PASS",
                "identity_fields_tested": len(summary),
                "results": summary,
                "formal_calibration_pass": False,
                "claim_support": False,
                "promotion_authority": False,
                "confirmatory_execution_authorized": False,
                "interpretation": (
                    "Engineering rejection test only. "
                    "Not Type-I calibration or scientific claim support."
                ),
            }
            (self.evidence_dir / "summary.json").write_text(
                json.dumps(report, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
