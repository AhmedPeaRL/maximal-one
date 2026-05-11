import json
import hashlib
from pathlib import Path
import subprocess

from analysis.canonical_json import canonicalize

REPORT = Path("artifacts/canonical_report.json")

def sha(obj):

    return hashlib.sha256(      
        canonicalize(obj).encode()      
    ).hexdigest()

if not REPORT.exists():
    
    raise SystemExit(     
        "❌ canonical report missing"     
    )

before = canonicalize(
    json.loads(
        REPORT.read_text(
            encoding="utf-8"
        )
    )
)

before_hash = hashlib.sha256(
    before.encode()
).hexdigest()

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

after = canonicalize(
    json.loads(
        REPORT.read_text(
            encoding="utf-8"
        )
    )
)

after_hash = hashlib.sha256(
    after.encode()
).hexdigest()

print("Reproduced report hash:")
print(after_hash)

match = before_hash == after_hash

result = {
    "before_hash": before_hash,
    "after_hash": after_hash,
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
