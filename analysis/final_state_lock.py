import hashlib
import json
from pathlib import Path

ARTIFACTS = [
    "canonical_report.json",
    "pipeline_sovereignty.json",
    "provenance_chain.json",
    "environment_fingerprint.json",
    "external_replay_verification.json",
    "adversarial_control.json",
    "witness_lock.json",
    "release_manifest.json",
    "reproducibility_stamp.json",
    "temporal_sovereignty.json"
]

base = Path("artifacts")

combined = hashlib.sha256()

for name in sorted(ARTIFACTS):
    path = base / name

    if not path.exists():
        raise SystemExit(
            f"Missing required artifact: {name}"
        )

    combined.update(
        path.read_bytes()
    )

final_hash = combined.hexdigest()

lock = {
    "final_state_hash": final_hash,
    "sealed": True,
    "artifact_count": len(ARTIFACTS),
    "artifacts": sorted(ARTIFACTS)
}

out = base / "final_state_lock.json"

with open(out, "w") as f:
    json.dump(
        lock,
        f,
        indent=2,
        sort_keys=True
    )

print(
    json.dumps(
        lock,
        indent=2
    )
)

print(
    "✅ FINAL STATE LOCK SEALED"
)
