import hashlib
import unittest
from unittest.mock import patch

import scripts.audit_type1_governance_refs as scanner


class BinarySafeGovernanceInventoryTests(unittest.TestCase):
    def test_non_utf8_and_nul_blobs_are_recorded_and_text_scan_continues(self):
        binary_invalid_utf8 = b"\xff\xfe\x89PNG"
        binary_with_nul = b"PDF\x00V4\x00content"
        text_blob = b"V4 candidate reference\n"

        with patch.object(
            scanner,
            "git",
            side_effect=[
                "commit-sha",
                "binary-invalid.bin\nbinary-nul.bin\nnotes.md",
                "blob-invalid",
                "blob-nul",
            ],
        ), patch.object(
            scanner,
            "git_bytes",
            side_effect=[binary_invalid_utf8, binary_with_nul, text_blob],
        ):
            report = scanner.inspect_ref("refs/audit/target")

        excluded = {row["path"]: row for row in report["excluded_paths"]}
        self.assertEqual(set(excluded), {"binary-invalid.bin", "binary-nul.bin"})
        self.assertEqual(
            excluded["binary-invalid.bin"]["content_sha256"],
            hashlib.sha256(binary_invalid_utf8).hexdigest(),
        )
        self.assertEqual(
            excluded["binary-nul.bin"]["content_sha256"],
            hashlib.sha256(binary_with_nul).hexdigest(),
        )
        self.assertEqual(excluded["binary-invalid.bin"]["blob_object"], "blob-invalid")
        self.assertEqual(excluded["binary-nul.bin"]["blob_object"], "blob-nul")
        self.assertEqual(report["files_with_matches"], 1)
        self.assertEqual(report["entries"][0]["path"], "notes.md")
        self.assertEqual(report["entries"][0]["matches"][0]["text"], "V4 candidate reference")

    def test_binary_blobs_are_not_silently_classified_as_zero_occurrences(self):
        binary_blob = b"\x00\xffV4"
        with patch.object(
            scanner,
            "git",
            side_effect=["commit-sha", "binary.dat", "blob-id"],
        ), patch.object(scanner, "git_bytes", return_value=binary_blob):
            report = scanner.inspect_ref("refs/audit/target")

        self.assertEqual(report["files_with_matches"], 0)
        self.assertEqual(len(report["excluded_paths"]), 1)
        self.assertEqual(
            report["excluded_paths"][0]["classification"],
            "NON_TEXT_BLOB_NOT_LINE_SCANNED",
        )
        self.assertIn("not eligible for line-based", report["excluded_paths"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
