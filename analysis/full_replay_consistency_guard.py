import json
import hashlib
from pathlib import Path
import subprocess
import os

from analysis.canonical_json import canonicalize

REPORT = Path("artifacts/canonical_report.json")


IMMUTABLE_KEYS = [
    "spectral_profile",
    "statistical_test",
    "cross_method_validation",
    "sovereign_layer"
]


def stable_projection(obj):

    return {
        k: obj[k]
        for k in IMMUTABLE_KEYS
        if k in obj
    }


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

before_projection = stable_projection(
    before_obj
)

before_hash = sha(
    before_projection
)

print("Original immutable hash:")
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

after_projection = stable_projection(
    after_obj
)

after_hash = sha(
    after_projection
)

print("Reproduced immutable hash:")
print(after_hash)

match = before_hash == after_hash

delta_report = {
    "before_hash": before_hash,
    "after_hash": after_hash,
    "match": bool(match),
    "verified_keys": IMMUTABLE_KEYS
}

Path(
    "artifacts/full_replay_consistency.json"
).write_text(
    canonicalize(delta_report),
    encoding="utf-8"
)

if not match:

    print(json.dumps({
        "before": before_projection,
        "after": after_projection
    }, indent=2))

    raise SystemExit(
        "❌ Full replay inconsistency detected"
    )

print("✅ FULL REPLAY CONSISTENCY VERIFIED")
