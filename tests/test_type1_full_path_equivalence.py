from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = "gaussian_ar2_phi_0_45_minus_0_10_n3328"
MASTER_SEED = 20261021
TOTAL = 6
SURROGATES = 1000
SAMPLE_SIZE = 3328
ARTIFACT_ROOT = ROOT / "artifacts" / "type1_official_runner_equivalence"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_records(payload: dict) -> list[dict]:
    rows = payload.get("attempt_records")
    if not isinstance(rows, list):
        raise AssertionError("Missing attempt_records list")
    return sorted(rows, key=lambda row: row["replicate_index"])


class OfficialRunnerEquivalenceTests(unittest.TestCase):
    """Engineering equivalence through the official runner entry point only.

    Six outer replicates and 1000 requested surrogates per replicate. This is
    not a formal Type-I calibration and cannot authorize a scientific claim.
    """

    @classmethod
    def setUpClass(cls):
        ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
        cls.run_dir = Path(tempfile.mkdtemp(prefix="run-", dir=ARTIFACT_ROOT))
        cls.summary_path = cls.run_dir / "evidence_summary.json"
        cls.summary = {
            "test": "TYPE1_OFFICIAL_RUNNER_EQUIVALENCE_V1",
            "scenario": SCENARIO,
            "master_seed": MASTER_SEED,
            "total_repetitions": TOTAL,
            "surrogates_per_attempt": SURROGATES,
            "repository_commit": os.environ.get("GITHUB_SHA", "LOCAL_OR_UNAVAILABLE"),
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
        cls.summary_path.write_text(json.dumps(cls.summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def run_runner(self, label: str, start: int, stop: int, output: Path, resume: bool = False, stop_after: int | None = None):
        args = [
            sys.executable, "-m", "analysis.calibrate_null_type1_scenario",
            "--engineering-test", "--scenario", SCENARIO,
            "--repetitions", str(TOTAL), "--surrogates", str(SURROGATES),
            "--n", str(SAMPLE_SIZE), "--master-seed", str(MASTER_SEED),
            "--start-index", str(start), "--stop-index", str(stop),
            "--output", str(output),
        ]
        if resume:
            args.append("--resume")
        if stop_after is not None:
            args.extend(["--stop-after", str(stop_after)])
        result = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        log_path = self.run_dir / f"{label}.log"
        log_path.write_text(result.stdout, encoding="utf-8")
        self.summary["paths"][label] = {"command": args, "returncode": result.returncode, "log": str(log_path.relative_to(ROOT))}
        self.save_summary()
        self.assertIn(result.returncode, (0, 1), msg=f"{label} had an execution error; inspect {log_path}")
        self.assertTrue(output.is_file(), f"{label} did not write an artifact")
        self.assertTrue(Path(str(output) + ".manifest.json").is_file(), f"{label} did not write a manifest")
        payload = read_json(output)
        self.assertFalse(payload.get("formal_calibration_pass", True))
        return payload

    def run_merge(self, label: str, output: Path, shards: list[Path]) -> dict:
        args = [sys.executable, "-m", "analysis.merge_type1_execution_shards", "--total-repetitions", str(TOTAL), "--output", str(output), *[str(p) for p in shards]]
        result = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        log_path = self.run_dir / f"{label}.log"
        log_path.write_text(result.stdout, encoding="utf-8")
        self.summary["paths"][label] = {"command": args, "returncode": result.returncode, "log": str(log_path.relative_to(ROOT))}
        self.save_summary()
        self.assertEqual(result.returncode, 0, msg=f"{label} failed; inspect {log_path}")
        self.assertTrue(output.is_file())
        self.assertTrue(Path(str(output) + ".manifest.json").is_file())
        payload = read_json(output)
        self.assertFalse(payload.get("formal_calibration_pass", True))
        return payload

    def assert_records_preserved(self, payload: dict):
        rows = canonical_records(payload)
        self.assertEqual([row["replicate_index"] for row in rows], list(range(TOTAL)))
        for row in rows:
            self.assertEqual(row.get("requested_surrogates"), SURROGATES)
            self.assertIn(row.get("status"), {"VALID", "INVALID"})
            if row["status"] == "INVALID":
                self.assertTrue(row.get("reason"), "Invalid attempt must preserve a reason")
            else:
                self.assertEqual(row.get("valid_surrogates"), SURROGATES)
                self.assertIsNotNone(row.get("p_value_mc_add_one"))

    def test_official_runner_connected_sharded_merge_and_resume_equivalence(self):
        connected_path = self.run_dir / "connected.json"
        connected = self.run_runner("connected", 0, TOTAL, connected_path)
        self.assert_records_preserved(connected)

        shard_a_path = self.run_dir / "shard-a.json"
        shard_b_path = self.run_dir / "shard-b.json"
        shard_a = self.run_runner("shard_a", 0, 3, shard_a_path)
        shard_b = self.run_runner("shard_b", 3, TOTAL, shard_b_path)
        self.assertEqual([r["replicate_index"] for r in canonical_records(shard_a)], [0, 1, 2])
        self.assertEqual([r["replicate_index"] for r in canonical_records(shard_b)], [3, 4, 5])

        normal = self.run_merge("merge_normal", self.run_dir / "merged-normal.json", [shard_a_path, shard_b_path])
        reverse = self.run_merge("merge_reverse", self.run_dir / "merged-reverse.json", [shard_b_path, shard_a_path])
        self.assertEqual(canonical_records(connected), canonical_records(normal))
        self.assertEqual(canonical_records(connected), canonical_records(reverse))

        resume_path = self.run_dir / "resume.json"
        interrupted = self.run_runner("resume_interrupted", 0, TOTAL, resume_path, stop_after=2)
        self.assertEqual(interrupted["status"], "ENGINEERING_INCOMPLETE")
        self.assertEqual(interrupted["missing_indices"], [2, 3, 4, 5])
        resumed = self.run_runner("resume_completed", 0, TOTAL, resume_path, resume=True)
        self.assertEqual(canonical_records(connected), canonical_records(resumed))

        self.summary["status"] = "ENGINEERING_EQUIVALENCE_PASS"
        self.summary["invalid_attempts_observed"] = sum(r["status"] == "INVALID" for r in canonical_records(connected))
        self.summary["scientific_interpretation"] = "Path equivalence only. Invalid attempts remain invalid; this does not pass Type-I calibration."
        self.save_summary()


if __name__ == "__main__":
    unittest.main(verbosity=2)
