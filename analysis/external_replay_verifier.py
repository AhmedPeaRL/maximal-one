import json
import hashlib
import subprocess
from pathlib import Path

ARTIFACT = "artifacts/canonical_report.json"


def sha256_file(path):

    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:

            chunk = f.read(8192)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


before = sha256_file(ARTIFACT)

print("Original artifact hash:")
print(before)

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

after = sha256_file(ARTIFACT)

print("Reproduced artifact hash:")
print(after)

report = {
    "original_hash": before,
    "reproduced_hash": after,
    "match": before == after
}

Path("artifacts").mkdir(exist_ok=True)

with open(
    "artifacts/external_replay_verification.json",
    "w"
) as f:

    json.dump(report, f, indent=2)

if before != after:
    raise SystemExit(
        "❌ External replay mismatch"
    )

print("✅ EXTERNAL REPLAY VERIFIED")
