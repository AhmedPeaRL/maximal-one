import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Namespace-package import; repository root must be the working directory.
from analysis.safe_payload import normalize_payload, write_payload


class PayloadBoundaryTests(unittest.TestCase):
    def test_shell_metacharacters_are_preserved_as_data(self):
        hostile_values = [
            "$(touch SHOULD_NOT_EXIST)",
            "`touch SHOULD_NOT_EXIST`",
            "; touch SHOULD_NOT_EXIST",
            "x && touch SHOULD_NOT_EXIST",
            "$(id); `whoami`",
            "${IFS}; echo PWNED",
            "line one\nline two\n; touch SHOULD_NOT_EXIST",
            "quotes ' \" ; $HOME",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "SHOULD_NOT_EXIST"
            for value in hostile_values:
                payload = {"input": value}
                normalized = normalize_payload(json.dumps(payload))
                self.assertEqual(normalized["input"], value)
                self.assertFalse(marker.exists())

    def test_empty_and_null_behavior(self):
        self.assertEqual(normalize_payload(None), {"_empty": True})
        self.assertEqual(normalize_payload(""), {"_empty": True})
        self.assertEqual(normalize_payload("null"), {"_empty": True})
        with self.assertRaises(ValueError):
            normalize_payload("null ")

    def test_empty_object_rejected(self):
        with self.assertRaises(ValueError):
            normalize_payload("{}")

    def test_oversized_payload_rejected(self):
        with self.assertRaises(ValueError):
            normalize_payload(json.dumps({"x": "a" * 6000}))

    def test_cli_writes_json_without_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "payload.json"
            marker = Path(tmp) / "PWNED"
            hostile = {"input": f"$(touch {marker})"}
            env = os.environ.copy()
            env["CLIENT_PAYLOAD_JSON"] = json.dumps(hostile)
            subprocess.run(
                [
                    sys.executable,
                    "analysis/safe_payload.py",
                    "--output",
                    str(output),
                ],
                env=env,
                check=True,
                shell=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(json.loads(output.read_text())["input"], hostile["input"])
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
