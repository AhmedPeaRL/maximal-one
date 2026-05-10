import json
import hashlib
from pathlib import Path

ARTIFACTS = Path("artifacts")

manifest = json.loads(
    Path(
        "artifacts/release_manifest.json"
    ).read_text()
)

expected = manifest["manifest"]

mutations = []

for name, meta in expected.items():

    path = ARTIFACTS / name

    if not path.exists():
        mutations.append(f"missing: {name}")
        continue

    current = hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

    if current != meta["sha256"]:
        mutations.append(
            f"modified: {name}"
        )

if mutations:

    print("\n".join(mutations))

    raise SystemExit(
        "❌ Post-seal mutation detected"
    )

print("✅ RELEASE MANIFEST SEALED")
print("✅ No post-seal mutation detected")
