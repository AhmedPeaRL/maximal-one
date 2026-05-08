import json
import subprocess
import numpy as np
from pathlib import Path

ARTIFACT = "artifacts/canonical_report.json"


def load():
    with open(ARTIFACT) as f:
        return json.load(f)


before = load()

print("Original alpha:")
print(before["spectral_profile"]["estimated_alpha"])

print("\nRe-running canonical pipeline...\n")

subprocess.run(
    [
        "python",
        "scripts/generate_report.py",
        "--seed",
        "42",
        "--canonical"
    ],
    check=True
)

after = load()

a1 = before["spectral_profile"]["estimated_alpha"]
a2 = after["spectral_profile"]["estimated_alpha"]

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

Path("artifacts").mkdir(exist_ok=True)

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
