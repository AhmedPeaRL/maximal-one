from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from analysis.type1_execution_artifacts import (
    load_verified_artifact,
    write_artifact_with_manifest,
)


def identity_fixture() -> dict:
    """Valid synthetic identity for rejection tests; not a scientific run."""
    return {
        "protocol": "HCM_TYPE1_CALIBRATION_V4_CANDIDATE",
        "scenario_id": "synthetic_identity_test",
        "scenario_coefficients": [0.45, -0.1],
        "sample_size": 3328,
        "dgp_burn_in": 2000,
        "surrogates_requested": 1000,
        "total_repetitions": 6,
        "master_seed": 20261021,
        "seed_schedule_id": (
            "NumPy SeedSequence([master_seed, stable_scenario_key, "
            "replicate_index, stream_id]); stream 0=DGP, 1=null"
        ),
        "start_index": 0,
        "stop_index": 6,
        "commit_sha": "a" * 40,
        "matrix_sha256": "1" * 64,
        "runner_sha256": "2" * 64,
        "endpoint_identity": (
            "analysis.numerical_spectral_verification.estimate_alpha"
        ),
        "null_implementation_identity": (
            "analysis.appropriate_stochastic_null."
            "parametric_short_memory_null"
        ),
        "requirements_lock_sha256": "3" * 64,
        "python_version": "3.11.15 test fixture",
        "platform_identity": "synthetic-test-platform",
    }


class ResumeIdentityRejectionTests(unittest.TestCase):
    def test_exact_identity_is_accepted(self):
        identity = identity_fixture()

        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "checkpoint.json"
            write_artifact_with_manifest(
                artifact,
                {"status": "ENGINEERING_INCOMPLETE",
                 "attempt_records": []},
                identity,
            )

            loaded = load_verified_artifact(
                artifact, expected_identity=identity
            )
            self.assertEqual(loaded["run_identity"], identity)

    def test_each_identity_mismatch_is_rejected(self):
        identity = identity_fixture()

        mismatches = {
            "commit_sha": "b" * 40,
            "matrix_sha256": "4" * 64,
            "runner_sha256": "5" * 64,
            "scenario_id": "different_scenario",
            "seed_schedule_id": "different_seed_schedule",
            "sample_size": 4096,
            "dgp_burn_in": 2500,
            "surrogates_requested": 999,
            "total_repetitions": 7,
            "master_seed": 20261022,
            "start_index": 1,
            "stop_index": 5,
            "endpoint_identity": "different.endpoint",
            "null_implementation_identity": "different.null",
            "requirements_lock_sha256": "6" * 64,
            "python_version": "different-python",
            "platform_identity": "different-platform",
        }

        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "checkpoint.json"
            write_artifact_with_manifest(
                artifact,
                {"status": "ENGINEERING_INCOMPLETE",
                 "attempt_records": []},
                identity,
            )

            for field, replacement in mismatches.items():
                with self.subTest(field=field):
                    requested = dict(identity)
                    requested[field] = replacement

                    with self.assertRaises(ValueError):
                        load_verified_artifact(
                            artifact, expected_identity=requested
                        )

    def test_corrupt_artifact_is_rejected(self):
        identity = identity_fixture()

        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "checkpoint.json"
            write_artifact_with_manifest(
                artifact,
                {"status": "ENGINEERING_INCOMPLETE",
                 "attempt_records": []},
                identity,
            )

            artifact.write_text(
                artifact.read_text(encoding="utf-8") + " ",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError, "SHA-256 mismatch"
            ):
                load_verified_artifact(
                    artifact, expected_identity=identity
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
