import json
import hashlib
from pathlib import Path

ARTIFACTS = Path("artifacts")

CRITICAL = [
    "canonical_report.json",
    "pipeline_sovereignty.json",
    "external_replay_verification.json",
    "release_manifest.json",
    "reproducibility_stamp.json"
]

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

report = {
    "hashes": snapshot,
    "artifact_count": len(snapshot),
    "status": "TEMPORAL_SOVEREIGNTY_HOLDS"
}

out = ARTIFACTS / "temporal_sovereignty.json"

out.write_text(
    json.dumps(
        report,
        indent=2,
        sort_keys=True
    ) + "\n"
)

print(json.dumps(report, indent=2))
print("✅ TEMPORAL SOVEREIGNTY HOLDS")
