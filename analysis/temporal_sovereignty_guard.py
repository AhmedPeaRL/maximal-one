import json
import hashlib
from pathlib import Path

ARTIFACTS = Path("artifacts")

CRITICAL = [
    "canonical_report.json",
    "pipeline_sovereignty.json",
    "external_replay_verification.json"
]

BOOTSTRAP_ALLOWED = True

def sha(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

snapshot = {}

missing = []

for name in CRITICAL:

    p = ARTIFACTS / name

    if not p.exists():
        missing.append(name)
        continue

    snapshot[name] = sha(p)

if missing:
    raise SystemExit(
        f"❌ Missing critical temporal artifacts: {missing}"
    )

temporal_file = ARTIFACTS / "temporal_sovereignty.json"

# FIRST CREATION → bootstrap allowed
if not temporal_file.exists():

    report = {
        "hashes": snapshot,
        "artifact_count": len(snapshot),
        "status": "BOOTSTRAP_TEMPORAL_SOVEREIGNTY"
    }

    with open(temporal_file, "w") as f:
        json.dump(report, f, indent=2)

    print("✅ TEMPORAL SOVEREIGNTY BOOTSTRAPPED")
    raise SystemExit(0)

previous = json.loads(
    temporal_file.read_text()
)

previous_hashes = previous.get(
    "hashes",
    {}
)

drift = []

for k, v in snapshot.items():

    old = previous_hashes.get(k)

    if old and old != v:
        drift.append({
            "artifact": k,
            "before": old,
            "after": v
        })

if drift:

    print(json.dumps(
        drift,
        indent=2
    ))

    raise SystemExit(
        "❌ TEMPORAL DRIFT DETECTED"
    )

report = {
    "hashes": snapshot,
    "artifact_count": len(snapshot),
    "status": "TEMPORAL_SOVEREIGNTY_HOLDS"
}

with open(temporal_file, "w") as f:
    json.dump(report, f, indent=2)

print("✅ TEMPORAL SOVEREIGNTY HOLDS")
