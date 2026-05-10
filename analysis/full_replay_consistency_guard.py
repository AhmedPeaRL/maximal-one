import json
import hashlib
from pathlib import Path
import subprocess

REPORT = Path("artifacts/canonical_report.json")


def canonical_json(obj):
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":")
    ).encode()


def sha(obj):
    return hashlib.sha256(
        canonical_json(obj)
    ).hexdigest()


if not REPORT.exists():
    raise SystemExit(
        "❌ canonical report missing"
    )

before = json.loads(
    REPORT.read_text()
)

before_hash = sha(before)

print("Original report hash:")
print(before_hash)

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

after = json.loads(
    REPORT.read_text()
)

after_hash = sha(after)

print("Reproduced report hash:")
print(after_hash)

match = before_hash == after_hash

result = {
    "before_hash": before_hash,
    "after_hash": after_hash,
    "match": bool(match)
}

with open(
    "artifacts/full_replay_consistency.json",
    "w"
) as f:
    json.dump(result, f, indent=2)

if not match:
    raise SystemExit(
        "❌ Full replay inconsistency detected"
    )

print("✅ FULL REPLAY CONSISTENCY VERIFIED")
