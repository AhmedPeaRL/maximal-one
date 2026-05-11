import hashlib
import json
from pathlib import Path

ARTIFACTS = [
    "artifact_closure.json",
    "release_manifest.json",
    "provenance_chain.json",
    "witness_lock.json",
    "temporal_sovereignty.json"
]

base = Path("artifacts")

combined = hashlib.sha256()

for name in sorted(ARTIFACTS):

    path = base / name

    if not path.exists():
        raise SystemExit(f"Missing required artifact: {name}")

    combined.update(path.read_bytes())

final_hash = combined.hexdigest()

lock = {
    "final_state_hash": final_hash,
    "sealed": True
}

out = base / "final_state.lock"

with open(out, "w") as f:
    json.dump(lock, f, indent=2)

print(json.dumps(lock, indent=2))
print("✅ FINAL STATE LOCK SEALED")
