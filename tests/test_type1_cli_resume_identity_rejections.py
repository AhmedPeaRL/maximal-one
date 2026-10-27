from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = "gaussian_ar2_phi_0_45_minus_0_10_n3328"
MASTER_SEED = 20261021
SAMPLE_SIZE = 3328
SURROGATES = 1000
TOTAL = 6

IDENTITY_FIELDS = (
    "protocol",
    "scenario_id",
    "scenario_coefficients",
    "sample_size",
    "dgp_burn_in",
    "surrogates_requested",
    "total_repetitions",
    "master_seed",
    "seed_schedule_id",
    "start_index",
    "stop_index",
    "commit_sha",
    "matrix_sha256",
    "runner_sha256",
    "endpoint_identity",
    "null_implementation_identity",
    "requirements_lock_sha256",
    "python_version",
    "platform_identity",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cli_command(
    checkpoint: Path,
    *,
    resume: bool,
    mismatch_field: str | None = None,
) -> list[str]:
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

    if mismatch_field is not None:
        command.extend([
            "--test-identity-mismatch-field",
            mismatch_field,
        ])

    return command


class OfficialCliResumeIdentityTests(unittest.TestCase):
    def setUp(self):
        self.evidence_dir = (
            ROOT / "artifacts" / "type1_cli_resume_identity"
        )
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def run_cli(self, label, command):
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        (self.evidence_dir / f"{label}.log").write_text(
            result.stdout,
            encoding="utf-8",
        )
        return result

    def test_cli_rejects_each_identity_mismatch_without_mutation(self):
        summary = []

        with tempfile.TemporaryDirectory(
            prefix="cli-resume-",
            dir=self.evidence_dir,
        ) as temporary:
            checkpoint = Path(temporary) / "checkpoint.json"
            manifest = Path(str(checkpoint) + ".manifest.json")

            created = self.run_cli(
                "create-valid-checkpoint",
                cli_command(checkpoint, resume=False),
            )

            self.assertEqual(
                created.returncode, 0, created.stdout
            )
            self.assertTrue(checkpoint.is_file())
            self.assertTrue(manifest.is_file())

            # Freeze the exact original bytes once.
            original_checkpoint = checkpoint.read_bytes()
            original_manifest = manifest.read_bytes()
            original_checkpoint_sha = sha256_bytes(
                original_checkpoint
            )
            original_manifest_sha = sha256_bytes(
                original_manifest
            )

            payload = json.loads(original_checkpoint)
            manifest_payload = json.loads(original_manifest)

            identity = payload["run_identity"]
            self.assertEqual(
                identity, manifest_payload["run_identity"]
            )
            self.assertEqual(
                set(identity), set(IDENTITY_FIELDS),
                "Update this test when the identity schema changes.",
            )

            for field in IDENTITY_FIELDS:
                with self.subTest(field=field):
                    # The checkpoint and manifest are never edited here.
                    result = self.run_cli(
                        f"resume-reject-{field}",
                        cli_command(
                            checkpoint,
                            resume=True,
                            mismatch_field=field,
                        ),
                    )

                    self.assertEqual(
                        result.returncode,
                        1,
                        f"Wrong exit code for {field}:\n{result.stdout}",
                    )
                    self.assertIn(
                        "Artifact run identity differs from requested execution",
                        result.stdout,
                        f"Wrong rejection reason for {field}:\n{result.stdout}",
                    )

                    # Exact byte-for-byte preservation of the original files.
                    self.assertEqual(
                        checkpoint.read_bytes(),
                        original_checkpoint,
                        f"Checkpoint bytes changed for {field}",
                    )
                    self.assertEqual(
                        manifest.read_bytes(),
                        original_manifest,
                        f"Manifest bytes changed for {field}",
                    )

                    self.assertEqual(
                        sha256_bytes(checkpoint.read_bytes()),
                        original_checkpoint_sha,
                    )
                    self.assertEqual(
                        sha256_bytes(manifest.read_bytes()),
                        original_manifest_sha,
                    )

                    summary.append({
                        "field": field,
                        "exit_code": result.returncode,
                        "expected_diagnostic_observed": True,
                        "checkpoint_sha256_before": original_checkpoint_sha,
                        "checkpoint_sha256_after": sha256_bytes(
                            checkpoint.read_bytes()
                        ),
                        "manifest_sha256_before": original_manifest_sha,
                        "manifest_sha256_after": sha256_bytes(
                            manifest.read_bytes()
                        ),
                        "log": f"resume-reject-{field}.log",
                    })

            report = {
                "test": "OFFICIAL_CLI_RESUME_IDENTITY_REJECTIONS_V2",
                "status": "PASS",
                "identity_fields_tested": len(summary),
                "results": summary,
                "formal_calibration_pass": False,
                "claim_support": False,
                "promotion_authority": False,
                "confirmatory_execution_authorized": False,
                "interpretation": (
                    "Engineering rejection test only. "
                    "The original checkpoint and manifest remain "
                    "byte-identical after every rejected resume. "
                    "This is not Type-I calibration."
                ),
            }

            (self.evidence_dir / "summary.json").write_text(
                json.dumps(report, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
