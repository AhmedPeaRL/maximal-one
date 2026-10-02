from __future__ import annotations

import hashlib
import json
from pathlib import Path

from analysis.canonical_json import canonicalize
from analysis.external_reproduction_guard import compute_fingerprint


REPORT = Path("artifacts/canonical_report.json")
RAW_HASH = Path("artifacts/report.hash")
CANONICAL_HASH = Path("artifacts/report_hash_manifest.json")
FINGERPRINT = Path("artifacts/fingerprint.txt")
RELEASE = Path("artifacts/release_manifest.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main():
    if not REPORT.exists():
        raise SystemExit("Missing canonical_report.json")

    report_bytes = REPORT.read_bytes()
    report = json.loads(
        report_bytes.decode("utf-8")
    )

    raw_hash = sha256_bytes(
        report_bytes
    )

    canonical_hash = sha256_bytes(
        canonicalize(report).encode("utf-8")
    )

    semantic_fingerprint = compute_fingerprint(
        report
    )

    if RAW_HASH.exists():
        stored_raw = RAW_HASH.read_text(
            encoding="utf-8"
        ).strip()

        if stored_raw != raw_hash:
            raise SystemExit(
                "RAW REPORT HASH MISMATCH"
            )

    if CANONICAL_HASH.exists():
        manifest = json.loads(
            CANONICAL_HASH.read_text(
                encoding="utf-8"
            )
        )

        if manifest.get("canonical_sha256") != canonical_hash:
            raise SystemExit(
                "CANONICAL REPORT HASH MISMATCH"
            )

    if FINGERPRINT.exists():
        stored_fp = FINGERPRINT.read_text(
            encoding="utf-8"
        ).strip()

        if stored_fp != semantic_fingerprint:
            raise SystemExit(
                "SEMANTIC FINGERPRINT MISMATCH"
            )

    if RELEASE.exists():
        release = json.loads(
            RELEASE.read_text(
                encoding="utf-8"
            )
        )

        entry = (
            release
            .get("manifest", {})
            .get("canonical_report.json")
        )

        if entry is not None:
            if entry.get("sha256") != raw_hash:
                raise SystemExit(
                    "RELEASE MANIFEST CANONICAL REPORT HASH MISMATCH"
                )

    print("RAW_REPORT_SHA256 =", raw_hash)
    print(
        "CANONICAL_REPORT_SHA256 =",
        canonical_hash
    )
    print(
        "SEMANTIC_FINGERPRINT =",
        semantic_fingerprint
    )
    print("REPORT IDENTITY VERIFIED")


if __name__ == "__main__":
    main()
