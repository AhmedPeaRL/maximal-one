import hashlib
import json
from pathlib import Path

ARTIFACTS_DIR = Path("artifacts")

REQUIRED = [
    "canonical_report.json",
    "pipeline_sovereignty.json",
    "fingerprint.txt",
    "full_replay_consistency.json"
]

OPTIONAL = [
    "multi_report.json",
    "physical_interpretation.json"
]

missing = []

for f in REQUIRED:
    if not (ARTIFACTS_DIR / f).exists():
        missing.append(f)

if missing:
    raise SystemExit(
        f"❌ Missing required artifacts: {missing}"
    )

hashes = {}

EXCLUDED = {
    "artifact_closure.json",
    "temporal_sovereignty.json",
    "final_state_lock.json",
    "release_manifest.json"
}

for path in sorted(ARTIFACTS_DIR.glob("*")):

    if path.name in EXCLUDED:
        continue

    if path.is_file():

        content = path.read_bytes()

        sha = hashlib.sha256(content).hexdigest()

        hashes[path.name] = sha

closure = {
    "artifact_count": len(hashes),
    "hashes": hashes
}

out = ARTIFACTS_DIR / "artifact_closure.json"

with open(out, "w") as f:
    json.dump(closure, f, indent=2)

print(json.dumps(closure, indent=2))

print("✅ ARTIFACT CLOSURE HOLDS")
