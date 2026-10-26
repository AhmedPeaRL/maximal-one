from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from analysis.type1_execution_artifacts import (
    REQUIRED_IDENTITY_FIELDS,
    canonical_json_bytes,
    sha256_bytes,
)

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = "gaussian_ar2_phi_0_45_minus_0_10_n3328"
MASTER_SEED = 20261021
TOTAL = 6
SURROGATES = 1000
SAMPLE_SIZE = 3328

EVIDENCE_ROOT = (
    ROOT / "artifacts" / "type1_cli_resume_identity_rejections"
)


def file_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identity_mutations() -> dict:
    """One validly encoded, deliberately different value per identity field."""
    return {
        "protocol": "HCM_TYPE1_CALIBRATION_V4_IDENTITY_TEST",
        "scenario_id": "gaussian_ar1_phi_0_4_n3328",
        "scenario_coefficients": [0.46, -0.10],
        "sample_size": SAMPLE_SIZE + 1,
        "dgp_burn_in": 2001,
        "surrogates_requested": SURROGATES - 1,
        "total_repetitions": TOTAL + 1,
        "master_seed": MASTER_SEED + 1,
        "seed_schedule_id": "DELIBERATELY_CHANGED_SEED_SCHEDULE",
        "start_index": 1,
        "stop_index": TOTAL - 1,
        "commit_sha": "b" * 40,
        "matrix_sha256": "4" * 64,
        "runner_sha256": "5" * 64,
        "endpoint_identity": "deliberately.changed.endpoint",
        "null_implementation_identity": "deliberately.changed.null",
        "requirements_lock_sha256": "6" * 64,
        "python_version": "DELIBERATELY_CHANGED_PYTHON",
        "platform_identity": "DELIBERATELY_CHANGED_PLATFORM",
    }


class ActualCliResumeIdentityRejectionTests(unittest.TestCase):
    """Exercise the real CLI resume path, not just its identity helper."""

    @classmethod
    def setUpClass(cls):
        EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
        cls.run_dir = Path(
            tempfile.mkdtemp(
                prefix="cli-resume-identity-",
                dir=EVIDENCE_ROOT,
            )
        )

    def command(self, checkpoint: Path, *, resume: bool) -> list[str]:
        args = [
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
            "--stop-index", str(TOTAL),
            "--output", str(checkpoint),
        ]
        if resume:
            args.append("--resume")
        return args

    def test_real_cli_rejects_each_identity_mismatch_without_writing(self):
        checkpoint = self.run_dir / "checkpoint.json"
        manifest_path = Path(str(checkpoint) + ".manifest.json")

        # Create a real checkpoint through the official bounded CLI.
        created = subprocess.run(
            self.command(checkpoint, resume=False)
            + ["--stop-after", "1"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        (self.run_dir / "checkpoint_creation.log").write_text(
            created.stdout, encoding="utf-8"
        )

        self.assertEqual(created.returncode, 0, created.stdout)
        self.assertTrue(checkpoint.is_file())
        self.assertTrue(manifest_path.is_file())

        base_artifact = checkpoint.read_bytes()
        base_manifest = manifest_path.read_bytes()

        base_payload = json.loads(base_artifact)
        base_manifest_obj = json.loads(base_manifest)
        original_identity = base_payload["run_identity"]

        self.assertEqual(
            set(original_identity),
            REQUIRED_IDENTITY_FIELDS,
            "Update this test if the required identity schema changes.",
        )

        mutations = identity_mutations()
        self.assertEqual(set(mutations), REQUIRED_IDENTITY_FIELDS)

        evidence = []

        for field in sorted(REQUIRED_IDENTITY_FIELDS):
            with self.subTest(identity_field=field):
                # Start each case from the exact same valid checkpoint.
                payload = copy.deepcopy(base_payload)
                manifest = copy.deepcopy(base_manifest_obj)

                changed_identity = dict(payload["run_identity"])
                changed_identity[field] = mutations[field]

                payload["run_identity"] = changed_identity
                manifest["run_identity"] = changed_identity

                # Keep the artifact internally hash-consistent so the
                # rejection is specifically an identity mismatch, not
                # merely an artifact-tampering rejection.
                artifact_bytes = canonical_json_bytes(payload)
                manifest["artifact_sha256"] = sha256_bytes(artifact_bytes)
                manifest_bytes = canonical_json_bytes(manifest)

                checkpoint.write_bytes(artifact_bytes)
                manifest_path.write_bytes(manifest_bytes)

                before_artifact = checkpoint.read_bytes()
                before_manifest = manifest_path.read_bytes()

                result = subprocess.run(
                    self.command(checkpoint, resume=True),
                    cwd=ROOT,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=False,
                )

                log_path = self.run_dir / f"reject_{field}.log"
                log_path.write_text(result.stdout, encoding="utf-8")

                after_artifact = checkpoint.read_bytes()
                after_manifest = manifest_path.read_bytes()

                artifact_unchanged = (
                    before_artifact == after_artifact
                )
                manifest_unchanged = (
                    before_manifest == after_manifest
                )

                evidence.append({
                    "field": field,
                    "exit_code": result.returncode,
                    "expected_rejection_message_present": (
                        "Artifact run identity differs"
                        in result.stdout
                    ),
                    "artifact_sha256_before": file_sha256(
                        before_artifact
                    ),
                    "artifact_sha256_after": file_sha256(
                        after_artifact
                    ),
                    "manifest_sha256_before": file_sha256(
                        before_manifest
                    ),
                    "manifest_sha256_after": file_sha256(
                        after_manifest
                    ),
                    "artifact_byte_identical": artifact_unchanged,
                    "manifest_byte_identical": manifest_unchanged,
                    "log": log_path.name,
                })

                self.assertNotEqual(
                    result.returncode,
                    0,
                    f"Changed identity field was accepted: {field}",
                )
                self.assertIn(
                    "Artifact run identity differs",
                    result.stdout,
                    f"Unexpected failure mode for {field}; inspect {log_path}",
                )
                self.assertTrue(
                    artifact_unchanged,
                    f"Rejected resume changed checkpoint bytes: {field}",
                )
                self.assertTrue(
                    manifest_unchanged,
                    f"Rejected resume changed manifest bytes: {field}",
                )

                # Restore the original checkpoint before the next case.
                checkpoint.write_bytes(base_artifact)
                manifest_path.write_bytes(base_manifest)

        summary = {
            "test": "ACTUAL_CLI_RESUME_IDENTITY_REJECTION_V1",
            "classification": (
                "ENGINEERING_EVIDENCE_ONLY_NOT_FORMAL_CALIBRATION"
            ),
            "scenario": SCENARIO,
            "requested_repetitions": TOTAL,
            "surrogates_per_attempt": SURROGATES,
            "identity_fields_tested": len(evidence),
            "all_rejections_nonzero_exit": all(
                item["exit_code"] != 0 for item in evidence
            ),
            "all_artifact_bytes_unchanged": all(
                item["artifact_byte_identical"] for item in evidence
            ),
            "all_manifest_bytes_unchanged": all(
                item["manifest_byte_identical"] for item in evidence
            ),
            "cases": evidence,
            "formal_calibration_pass": False,
            "claim_support": False,
            "promotion_authority": False,
            "confirmatory_execution_authorized": False,
        }

        (self.run_dir / "identity_rejection_summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        # Leave the original valid checkpoint in the evidence directory.
        checkpoint.write_bytes(base_artifact)
        manifest_path.write_bytes(base_manifest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
