import json
import hashlib
from pathlib import Path

ARTIFACTS_DIR = Path("artifacts")

EXCLUDED = {
    "release_manifest.json"
}


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


manifest = {}

for file in sorted(ARTIFACTS_DIR.glob("*")):

    if (
        file.is_file()
        and file.name not in EXCLUDED
    ):

        manifest[file.name] = {
            "sha256": sha256(file),
            "size": file.stat().st_size
        }

output = {
    "artifact_count": len(manifest),
    "manifest": manifest
}

manifest_path = (
    ARTIFACTS_DIR
    / "release_manifest.json"
)

manifest_path.write_text(
    json.dumps(
        output,
        indent=2,
        sort_keys=True
    )
)

print("✅ RELEASE MANIFEST BUILT")
