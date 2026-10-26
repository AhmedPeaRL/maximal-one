from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from analysis.merge_type1_execution_shards import merge_shards
from analysis.type1_execution_artifacts import write_artifact_with_manifest


def identity(start: int, stop: int, total: int = 4, **overrides) -> dict:
    value = {
        "protocol": "HCM_TYPE1_CALIBRATION_V4_CANDIDATE",
        "scenario_id": "synthetic_merge_test",
        "scenario_coefficients": [0.4, -0.1],
        "sample_size": 3328,
        "dgp_burn_in": 2000,
        "surrogates_requested": 1000,
        "total_repetitions": total,
        "master_seed": 20261021,
        "seed_schedule_id": "test-seed-schedule-v1",
        "start_index": start,
        "stop_index": stop,
        "commit_sha": "engineering-test-only",
        "matrix_sha256": "a" * 64,
        "runner_sha256": "b" * 64,
        "endpoint_identity": "canonical_primary_alpha",
        "null_implementation_identity": "existing-null-implementation",
        "requirements_lock_sha256": "c" * 64,
        "python_version": "test-runtime",
        "platform_identity": "test-platform",
    }
    value.update(overrides)
    return value


def row(index: int, status: str = "VALID") -> dict:
    return {
        "replicate_index": index,
        "status": status,
        "reason": None if status == "VALID" else "synthetic-invalid-attempt",
        "requested_surrogates": 1000,
        "valid_surrogates": 1000 if status == "VALID" else 0,
        "p_value_mc_add_one": 0.5 if status == "VALID" else None,
    }


class ExecutionMergeRejectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.output = self.root / "merged.json"

    def tearDown(self):
        self.temp.cleanup()

    def shard(self, name: str, start: int, stop: int, rows: list[dict], **identity_overrides) -> Path:
        path = self.root / name
        write_artifact_with_manifest(
            path,
            {
                "artifact_kind": "V4_OFFICIAL_RUNNER_ENGINEERING_ONLY",
                "attempt_records": rows,
            },
            identity(start, stop, **identity_overrides),
        )
        return path

    def test_valid_shards_merge_and_invalid_attempt_remains_failure(self):
        first = self.shard("a.json", 0, 2, [row(0), row(1, "INVALID")])
        second = self.shard("b.json", 2, 4, [row(2), row(3)])
        result = merge_shards([first, second], 4, self.output)
        self.assertEqual(result["status"], "ENGINEERING_FAILED_INVALID_ATTEMPTS")
        self.assertEqual(result["invalid_attempts"], 1)
        self.assertFalse(result["formal_calibration_pass"])

    def test_tampered_shard_hash_is_rejected(self):
        first = self.shard("a.json", 0, 2, [row(0), row(1)])
        second = self.shard("b.json", 2, 4, [row(2), row(3)])
        first.write_text(first.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            merge_shards([first, second], 4, self.output)

    def test_overlapping_shard_ranges_are_rejected(self):
        first = self.shard("a.json", 0, 3, [row(0), row(1), row(2)])
        second = self.shard("b.json", 2, 4, [row(2), row(3)])
        with self.assertRaisesRegex(ValueError, "Duplicate/overlapping|gap or overlap"):
            merge_shards([first, second], 4, self.output)

    def test_missing_replicate_is_rejected(self):
        first = self.shard("a.json", 0, 2, [row(0)])
        second = self.shard("b.json", 2, 4, [row(2), row(3)])
        with self.assertRaisesRegex(ValueError, "Shard is incomplete"):
            merge_shards([first, second], 4, self.output)

    def test_common_identity_mismatch_is_rejected(self):
        first = self.shard("a.json", 0, 2, [row(0), row(1)])
        second = self.shard("b.json", 2, 4, [row(2), row(3)], master_seed=20261022)
        with self.assertRaisesRegex(ValueError, "common run identity mismatch"):
            merge_shards([first, second], 4, self.output)

    def test_record_outside_declared_range_is_rejected(self):
        first = self.shard("a.json", 0, 2, [row(0), row(2)])
        second = self.shard("b.json", 2, 4, [row(2), row(3)])
        with self.assertRaisesRegex(ValueError, "outside requested range"):
            merge_shards([first, second], 4, self.output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
