import json
import hashlib
from pathlib import Path

from analysis.canonical_json import canonicalize

REPORT = Path("artifacts/canonical_report.json")
LOCK = Path("artifacts/canonical_report.lock")


def sha(obj):

    return hashlib.sha256(
        canonicalize(obj).encode()
    ).hexdigest()


if not REPORT.exists():

    raise SystemExit(
        "❌ canonical report missing"
    )

if not LOCK.exists():

    raise SystemExit(
        "❌ replay lock missing"
    )

report = json.loads(
    REPORT.read_text(encoding="utf-8")
)

lock = json.loads(
    LOCK.read_text(encoding="utf-8")
)

current_hash = sha(report)

expected_hash = lock["sha256"]

print("Expected hash:")
print(expected_hash)

print("\nCurrent hash:")
print(current_hash)

match = (
    current_hash == expected_hash
)

result = {
    "expected_hash": expected_hash,
    "current_hash": current_hash,
    "match": bool(match)
}

Path(
    "artifacts/full_replay_consistency.json"
).write_text(
    canonicalize(result),
    encoding="utf-8"
)

if not match:

    raise SystemExit(
        "❌ Full replay inconsistency detected"
    )

print("✅ FULL REPLAY CONSISTENCY VERIFIED")
