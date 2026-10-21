from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from analysis.type1_calibration_pilot import atomic_write

ROOT = Path(__file__).resolve().parents[1]

SCENARIO = "gaussian_ar2_inband_f_0_02_radius_0_90_n3328"
MASTER_SEED = 20261021
TOTAL = 2
SURROGATES = 200

ARTIFACT_ROOT = ROOT / "artifacts" / "type1_full_path_equivalence"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_record(record: dict) -> dict:
    """Exclude timing/traceback metadata; preserve scientific fields."""
    return {
        key: value
        for key, value in record.items()
        if key not in {"elapsed_seconds", "traceback"}
    }


def canonical_records(payload: dict) -> list[dict]:
    rows = payload.get("attempt_records")
    if not isinstance(rows, list):
        raise AssertionError("Missing attempt_records list")

    ordered = sorted(rows, key=lambda row: row["replicate_index"])
    return [canonical_record(row) for row in ordered]


def canonical_merge(payload: dict) -> dict:
    """Normalize only input-order-dependent provenance ordering."""
    result = copy.deepcopy(payload)
    result["verified_shard_hashes"] = sorted(
        result.get("verified_shard_hashes", []),
        key=lambda row: (
            row.get("sha256") or "",
            row.get("manifest") or "",
        ),
    )
    return result


class Type1FullPathEquivalenceTests(unittest.TestCase):
    """
    Integration test over the real pilot runner, merger, endpoint,
    stochastic-null implementation, and checkpoint verification.

    This is still an exploratory engineering test, not formal
    Type-I calibration and not an independent scientific review.
    """

    @classmethod
    def setUpClass(cls):
        ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
        cls.run_dir = Path(
            tempfile.mkdtemp(
                prefix="run-",
                dir=str(ARTIFACT_ROOT),
            )
        )
        cls.summary_path = cls.run_dir / "evidence_summary.json"
        cls.summary = {
            "test": "TYPE1_FULL_PATH_EQUIVALENCE_V1",
            "scenario": SCENARIO,
            "master_seed": MASTER_SEED,
            "total_repetitions": TOTAL,
            "surrogates_per_attempt": SURROGATES,
            "repository_commit": os.environ.get(
                "GITHUB_SHA", "LOCAL_OR_UNAVAILABLE"
            ),
            "status": "IN_PROGRESS",
            "formal_calibration_pass": False,
            "claim_support": False,
            "promotion_authority": False,
            "confirmatory_execution_authorized": False,
            "paths": {},
        }
        cls.save_summary()

    @classmethod
    def save_summary(cls):
        write_json(cls.summary_path, cls.summary)

    def run_command(self, label: str, args: list[str]) -> subprocess.CompletedProcess:
        log_path = self.run_dir / f"{label}.log"
        result = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        log_path.write_text(result.stdout, encoding="utf-8")
        self.summary["paths"][label] = {
            "command": args,
            "returncode": result.returncode,
            "log": str(log_path.relative_to(ROOT)),
        }
        self.save_summary()
        return result

    def run_pilot(
        self,
        label: str,
        start: int,
        stop: int,
        output: Path,
        resume: bool = False,
    ) -> dict:
        args = [
            sys.executable,
            "-m",
            "analysis.type1_calibration_pilot",
            "--scenario",
            SCENARIO,
            "--start-index",
            str(start),
            "--stop-index",
            str(stop),
            "--total-repetitions",
            str(TOTAL),
            "--surrogates",
            str(SURROGATES),
            "--master-seed",
            str(MASTER_SEED),
            "--output",
            str(output),
        ]
        if resume:
            args.append("--resume")

        result = self.run_command(label, args)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"{label} failed. Inspect {label}.log in {self.run_dir}",
        )
        self.assertTrue(output.is_file(), f"{label} did not create its artifact")
        self.assertTrue(
            Path(str(output) + ".manifest.json").is_file(),
            f"{label} did not create its manifest",
        )
        return read_json(output)

    def run_merge(
        self,
        label: str,
        output: Path,
        shard_paths: list[Path],
        expected_returncode: int = 0,
    ) -> dict:
        args = [
            sys.executable,
            "-m",
            "analysis.merge_type1_calibration_pilot_shards",
            "--total-repetitions",
            str(TOTAL),
            "--output",
            str(output),
            *[str(path) for path in shard_paths],
        ]
        result = self.run_command(label, args)
        self.assertEqual(
            result.returncode,
            expected_returncode,
            msg=f"Unexpected return code for {label}; inspect its log",
        )
        self.assertTrue(output.is_file(), f"{label} did not write its output")
        return read_json(output)

    def assert_all_attempts_valid(self, payload: dict):
        rows = canonical_records(payload)
        self.assertEqual(len(rows), TOTAL)
        self.assertEqual(
            [row["replicate_index"] for row in rows],
            list(range(TOTAL)),
        )

        for row in rows:
            self.assertEqual(row.get("status"), "VALID")
            self.assertEqual(row.get("requested_surrogates"), SURROGATES)
            self.assertEqual(row.get("valid_surrogates"), SURROGATES)
            self.assertIsNotNone(row.get("p_value_mc_add_one"))
            self.assertEqual(
                row["p_value_mc_add_one"],
                (row["exceedances"] + 1) / (SURROGATES + 1),
            )

    def test_real_runner_merger_reverse_merge_and_resume(self):
        # 1. Fresh uninterrupted run through the real CLI runner.
        connected_path = self.run_dir / "connected.json"
        connected = self.run_pilot(
            "connected_runner",
            0,
            TOTAL,
            connected_path,
        )
        self.assert_all_attempts_valid(connected)

        # 2. Execute separate shards through the real CLI runner.
        shard0_path = self.run_dir / "shard_0.json"
        shard1_path = self.run_dir / "shard_1.json"

        shard0 = self.run_pilot("runner_shard_0", 0, 1, shard0_path)
        shard1 = self.run_pilot("runner_shard_1", 1, 2, shard1_path)

        self.assertEqual(len(canonical_records(shard0)), 1)
        self.assertEqual(len(canonical_records(shard1)), 1)

        # 3. Merge the real shard artifacts in normal order.
        merged_path = self.run_dir / "merged_normal.json"
        merged = self.run_merge(
            "merge_normal_order",
            merged_path,
            [shard0_path, shard1_path],
        )
        self.assertEqual(merged["status"], "PILOT_COMPLETE_DIAGNOSTIC_ONLY")
        self.assertEqual(merged["missing_indices"], [])
        self.assertEqual(merged["invalid_attempts"], 0)
        self.assertEqual(
            canonical_records(connected),
            canonical_records(merged),
        )

        # 4. Merge the same verified shard artifacts in reverse order.
        reverse_path = self.run_dir / "merged_reverse.json"
        reverse = self.run_merge(
            "merge_reverse_order",
            reverse_path,
            [shard1_path, shard0_path],
        )
        self.assertEqual(reverse["status"], "PILOT_COMPLETE_DIAGNOSTIC_ONLY")
        self.assertEqual(
            canonical_merge(merged),
            canonical_merge(reverse),
        )

        # 5. Create a verified partial checkpoint from the connected run.
        # The checkpoint identity stays exactly the same as the intended
        # 0..TOTAL run; only the retained attempt records are partial.
        checkpoint_path = self.run_dir / "resume_checkpoint.json"
        checkpoint = copy.deepcopy(connected)
        checkpoint["attempt_records"] = [
            row
            for row in connected["attempt_records"]
            if row["replicate_index"] == 0
        ]
        checkpoint["status"] = "PILOT_INCOMPLETE_OR_DIAGNOSTIC_ONLY"
        checkpoint["invalid_attempts"] = 0
        checkpoint["formal_calibration_pass"] = False
        atomic_write(checkpoint_path, checkpoint)

        # Verify the checkpoint is readable and bound to its manifest.
        from analysis.type1_calibration_pilot import load_verified_checkpoint

        restored = load_verified_checkpoint(
            checkpoint_path,
            connected["run_identity"],
        )
        self.assertEqual(
            [row["replicate_index"] for row in restored["attempt_records"]],
            [0],
        )

        # 6. Resume through the real CLI runner. Index 0 must not be rerun;
        # index 1 must be executed and retained in the final artifact.
        resumed = self.run_pilot(
            "runner_resume",
            0,
            TOTAL,
            checkpoint_path,
            resume=True,
        )
        self.assert_all_attempts_valid(resumed)
        self.assertEqual(
            canonical_records(connected),
            canonical_records(resumed),
        )

        # 7. Corrupt a shard's bytes and verify the real merger rejects it.
        original_bytes = shard0_path.read_bytes()
        try:
            shard0_path.write_bytes(original_bytes + b"\nCORRUPTED\n")
            corrupt_output = self.run_dir / "corrupt_merge.json"
            args = [
                sys.executable,
                "-m",
                "analysis.merge_type1_calibration_pilot_shards",
                "--total-repetitions",
                str(TOTAL),
                "--output",
                str(corrupt_output),
                str(shard0_path),
                str(shard1_path),
            ]
            result = self.run_command("merge_corrupted_shard", args)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("SHA-256 mismatch", result.stdout)
        finally:
            shard0_path.write_bytes(original_bytes)

        # Retain canonical expected/observed records and artifact hashes.
        self.summary["status"] = "PASS_ENGINEERING_EQUIVALENCE_ONLY"
        self.summary["formal_calibration_pass"] = False
        self.summary["claim_support"] = False
        self.summary["promotion_authority"] = False
        self.summary["confirmatory_execution_authorized"] = False
        self.summary["observed"] = {
            "connected": canonical_records(connected),
            "merged_normal": canonical_records(merged),
            "merged_reverse": canonical_records(reverse),
            "resumed": canonical_records(resumed),
            "normal_merge_status": merged["status"],
            "reverse_merge_status": reverse["status"],
            "corrupted_shard_rejected": True,
        }
        self.summary["artifact_sha256"] = {
            path.name: sha256_file(path)
            for path in [
                connected_path,
                shard0_path,
                shard1_path,
                merged_path,
                reverse_path,
                checkpoint_path,
            ]
        }
        self.save_summary()

        print(f"Evidence retained at: {self.run_dir}", flush=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
