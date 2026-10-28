from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "artifacts" / "type1_resume_cli_identity"
SCENARIO = "gaussian_ar2_phi_0_45_minus_0_10_n3328"

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


class OfficialCliResumeIdentityTests(unittest.TestCase):
    """Real CLI rejection test; engineering-only, never calibration."""

    @classmethod
    def setUpClass(cls):
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        cls.logs_dir = EVIDENCE / "logs"
        cls.logs_dir.mkdir(parents=True, exist_ok=True)
        cls.report = {
            "test": "OFFICIAL_CLI_RESUME_IDENTITY_REJECTIONS_V1",
            "classification": "ENGINEERING_ONLY",
            "scenario": SCENARIO,
            "identity_fields": list(IDENTITY_FIELDS),
            "baseline_exit_code": None,
            "baseline_checkpoint_sha256": None,
            "baseline_manifest_sha256": None,
            "cases": [],
            "formal_calibration_pass": False,
            "claim_support": False,
            "promotion_authority": False,
            "confirmatory_execution_authorized": False,
        }

    def command(self, output: Path, *extra: str) -> list[str]:
        return [
            sys.executable,
            "-m",
            "analysis.calibrate_null_type1_scenario",
            "--engineering-test",
            "--scenario", SCENARIO,
            "--repetitions", "2",
            "--surrogates", "1000",
            "--n", "3328",
            "--master-seed", "20261021",
            "--start-index", "0",
            "--stop-index", "2",
            "--output", str(output),
            *extra,
        ]

    def run_cli(self, label: str, command: list[str]) -> subprocess.CompletedProcess:
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        log_path = self.logs_dir / f"{label}.log"
        log_path.write_text(
            "COMMAND:\n"
            + json.dumps(command, indent=2)
            + f"\nEXIT_CODE: {result.returncode}\n\n"
            + result.stdout,
            encoding="utf-8",
        )
        return result

    def test_every_supported_identity_mismatch_rejects_resume_immutably(self):
        with tempfile.TemporaryDirectory(
            prefix="cli-resume-identity-"
        ) as temporary:
            output = Path(temporary) / "checkpoint.json"
            manifest = Path(str(output) + ".manifest.json")

            # Create a real, valid, bounded engineering checkpoint.
            baseline = self.run_cli(
                "baseline_checkpoint",
                self.command(output, "--stop-after", "1"),
            )
            self.report["baseline_exit_code"] = baseline.returncode

            self.assertEqual(
                baseline.returncode, 0,
                "Checkpoint creation failed; inspect baseline_checkpoint.log",
            )
            self.assertTrue(output.is_file(), "Checkpoint was not created")
            self.assertTrue(manifest.is_file(), "Manifest was not created")

            original_checkpoint = output.read_bytes()
            original_manifest = manifest.read_bytes()
            checkpoint_hash = sha256_bytes(original_checkpoint)
            manifest_hash = sha256_bytes(original_manifest)

            self.report["baseline_checkpoint_sha256"] = checkpoint_hash
            self.report["baseline_manifest_sha256"] = manifest_hash

            for field in IDENTITY_FIELDS:
                with self.subTest(identity_field=field):
                    result = self.run_cli(
                        f"resume_mismatch_{field}",
                        self.command(
                            output,
                            "--resume",
                            "--test-identity-mismatch-field",
                            field,
                        ),
                    )

                    checkpoint_unchanged = (
                        output.is_file()
                        and output.read_bytes() == original_checkpoint
                    )
                    manifest_unchanged = (
                        manifest.is_file()
                        and manifest.read_bytes() == original_manifest
                    )

                    case = {
                        "field": field,
                        "exit_code": result.returncode,
                        "rejected": result.returncode != 0,
                        "checkpoint_unchanged": checkpoint_unchanged,
                        "manifest_unchanged": manifest_unchanged,
                        "log": f"logs/resume_mismatch_{field}.log",
                    }
                    self.report["cases"].append(case)

                    self.assertNotEqual(
                        result.returncode, 0,
                        f"Changed identity field was accepted: {field}",
                    )
                    self.assertTrue(
                        checkpoint_unchanged,
                        f"Checkpoint bytes changed after rejecting {field}",
                    )
                    self.assertTrue(
                        manifest_unchanged,
                        f"Manifest bytes changed after rejecting {field}",
                    )
                    self.assertTrue(
                        result.stdout.strip(),
                        f"Missing failure log for field {field}",
                    )

            self.assertEqual(
                len(self.report["cases"]), len(IDENTITY_FIELDS)
            )
            self.assertTrue(
                all(case["rejected"] for case in self.report["cases"])
            )
            self.assertTrue(
                all(case["checkpoint_unchanged"]
                    for case in self.report["cases"])
            )
            self.assertTrue(
                all(case["manifest_unchanged"]
                    for case in self.report["cases"])
            )

        (EVIDENCE / "resume_identity_report.json").write_text(
            json.dumps(self.report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
