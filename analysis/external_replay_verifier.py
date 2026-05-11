import json
import subprocess
import tempfile
import shutil
from pathlib import Path

ARTIFACT = "artifacts/canonical_report.json"


def load(path):
    with open(path) as f:
        return json.load(f)


before = load(ARTIFACT)

print("Original alpha:")
print(before["spectral_profile"]["estimated_alpha"])

print("\nRe-running canonical pipeline...\n")

tmpdir = tempfile.mkdtemp()

try:

    subprocess.run(
        [
            "python",
            "scripts/generate_report.py",
            "--seed",
            "42",
            "--canonical",
            "--output-dir",
            tmpdir
        ],
        check=True
    )

    reproduced = load(
        Path(tmpdir) / "canonical_report.json"
    )

    a1 = before["spectral_profile"]["estimated_alpha"]
    a2 = reproduced["spectral_profile"]["estimated_alpha"]

    delta = abs(a1 - a2)

    print("Reproduced alpha:")
    print(a2)

    print("Delta:")
    print(delta)

    report = {
        "original_alpha": a1,
        "reproduced_alpha": a2,
        "delta": delta,
        "match": bool(delta < 1e-6)
    }

    with open(
        "artifacts/external_replay_verification.json",
        "w"
    ) as f:
        json.dump(report, f, indent=2)

    if delta >= 1e-6:
        raise SystemExit(
            "❌ External replay mismatch"
        )

    print("✅ EXTERNAL REPLAY VERIFIED")

finally:
    shutil.rmtree(tmpdir, ignore_errors=True)
