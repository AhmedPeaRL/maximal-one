import json
import hashlib
from pathlib import Path

ARTIFACTS_DIR = Path("artifacts")


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


manifest = {}

for file in sorted(ARTIFACTS_DIR.glob("*")):

    if file.is_file():

        manifest[file.name] = {
            "sha256": sha256(file),
            "size": file.stat().st_size
        }

output = {
    "artifact_count": len(manifest),
    "manifest": manifest
}

Path("artifacts").mkdir(exist_ok=True)

with open(
    "artifacts/release_manifest.json",
    "w"
) as f:

    json.dump(
        output,
        f,
        indent=2,
        sort_keys=True
    )

print("✅ RELEASE MANIFEST SEALED")
