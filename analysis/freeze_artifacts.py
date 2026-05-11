import json
import hashlib
from pathlib import Path

ARTIFACTS = Path("artifacts")

EXCLUDED = {
    "artifact_closure.json",
    "temporal_sovereignty.json",
    "final_state_lock.json",
    "release_manifest.json"
}

hashes = {}

for path in sorted(ARTIFACTS.glob("*")):

    if not path.is_file():
        continue

    if path.name in EXCLUDED:
        continue

    content = path.read_bytes()

    hashes[path.name] = hashlib.sha256(
        content
    ).hexdigest()

report = {
    "artifact_count": len(hashes),
    "hashes": hashes,
    "frozen": True
}

out = ARTIFACTS / "artifact_closure.json"

with open(out, "w") as f:
    json.dump(
        report,
        f,
        indent=2,
        sort_keys=True
    )

print("✅ ARTIFACT FREEZE COMPLETE")
