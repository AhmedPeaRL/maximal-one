import json
import hashlib
from pathlib import Path
import subprocess
import os

from analysis.canonical_json import canonicalize

REPORT = Path("artifacts/canonical_report.json")


def sha(obj):

    return hashlib.sha256(
        canonicalize(obj).encode("utf-8")
    ).hexdigest()


if not REPORT.exists():

    raise SystemExit(
        "❌ canonical report missing"
    )


before_obj = json.loads(
    REPORT.read_text(
        encoding="utf-8"
    )
)

before = canonicalize(before_obj)

before_hash = hashlib.sha256(
    before.encode("utf-8")
).hexdigest()

print("Original report hash:")
print(before_hash)

print("\nRe-running canonical pipeline...\n")

env = os.environ.copy()

env["PYTHONHASHSEED"] = "42"
env["OMP_NUM_THREADS"] = "1"
env["MKL_NUM_THREADS"] = "1"
env["OPENBLAS_NUM_THREADS"] = "1"
env["NUMEXPR_NUM_THREADS"] = "1"

subprocess.run(
    [
        "python",
        "scripts/generate_report.py",
        "--seed",
        "42",
        "--canonical",
        "--output-dir",
        "artifacts/replay_check"
    ],
    check=True,
    env=env
)

after_obj = json.loads(
    Path(
        "artifacts/replay_check/canonical_report.json"
    ).read_text(
        encoding="utf-8"
    )
)

after = canonicalize(after_obj)

after_hash = hashlib.sha256(
    after.encode("utf-8")
).hexdigest()

print("Reproduced report hash:")
print(after_hash)

match = before_hash == after_hash

delta_report = {
    "before_hash": before_hash,
    "after_hash": after_hash,
    "match": bool(match)
}

Path(
    "artifacts/full_replay_consistency.json"
).write_text(
    canonicalize(delta_report),
    encoding="utf-8"
)

if not match:

    print(json.dumps({
        "before": before_obj,
        "after": after_obj
    }, indent=2))

    raise SystemExit(
        "❌ Full replay inconsistency detected"
    )

print("✅ FULL REPLAY CONSISTENCY VERIFIED")
