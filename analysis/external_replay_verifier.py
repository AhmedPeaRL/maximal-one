from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

ARTIFACT = Path(
    "artifacts/canonical_report.json"
)

OUTPUT = Path(
    "artifacts/internal_replay_verification.json"
)

def load(path: Path):
    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()

def main():
    if not ARTIFACT.exists():
        raise SystemExit(
            "❌ canonical_report.json missing"
        )

    before = load(ARTIFACT)

    original_alpha = float(
        before["spectral_profile"]["estimated_alpha"]
    )

    tmpdir = Path(
        tempfile.mkdtemp(
            prefix="hcm_internal_replay_"
        )
    )

    try:
        subprocess.run(
            [
                sys.executable,
                "scripts/generate_report.py",
                "--seed",
                "42",
                "--canonical",
                "--output-dir",
                str(tmpdir),
            ],
            check=True,
        )

        reproduced_path = (
            tmpdir / "canonical_report.json"
        )

        if not reproduced_path.exists():
            raise SystemExit(
                "❌ Internal replay did not produce canonical_report.json"
            )

        reproduced = load(
            reproduced_path
        )

        reproduced_alpha = float(
            reproduced["spectral_profile"]["estimated_alpha"]
        )

        delta = abs(
            original_alpha - reproduced_alpha
        )

        original_hash = sha256_file(
            ARTIFACT
        )

        reproduced_hash = sha256_file(
            reproduced_path
        )

        report = {
            "replay_type":
                "internal_same_environment_rerun",

            "independent_replay_verified":
                False,

            "fingerprint_match":
                False,

            "structure_match":
                False,

            "original_alpha":
                original_alpha,

            "reproduced_alpha":
                reproduced_alpha,

            "delta":
                delta,

            "original_report_sha256":
                original_hash,

            "reproduced_report_sha256":
                reproduced_hash,

            "environment": {
                "python":
                    platform.python_version(),

                "platform":
                    platform.platform(),
            },

            "verification_method":
                "same_environment_internal_rerun",

            "scientific_role":
                "diagnostic_only",

            "status":
                "verified"
                if delta <= 1e-8
                else "failed",

            "interpretation":
                (
                    "This artifact verifies repeatability "
                    "within the current execution environment. "
                    "It is not an independent clean-checkout "
                    "reproduction and is not external replication."
                ),
        }

        OUTPUT.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with OUTPUT.open(
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                report,
                f,
                indent=2,
                sort_keys=True,
            )

        if delta > 1e-8:
            raise SystemExit(
                "❌ Internal deterministic replay mismatch"
            )

        print(
            "✅ INTERNAL DETERMINISTIC REPLAY VERIFIED"
        )

        print(
            "ℹ️ Diagnostic only: "
            "not an independent clean-checkout reproduction."
        )

    finally:
        shutil.rmtree(
            tmpdir,
            ignore_errors=True,
        )

if __name__ == "__main__":
    main()
