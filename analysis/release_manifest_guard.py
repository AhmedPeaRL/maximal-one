import json
import hashlib
from pathlib import Path
import subprocess

ARTIFACTS_DIR = Path("artifacts")


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


manifest = {}

EXCLUDED = {
    "release_manifest.json"
}

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

old_content = None

if manifest_path.exists():
    old_content = manifest_path.read_text()

new_content = json.dumps(
    output,
    indent=2,
    sort_keys=True
)

if old_content != new_content:

    manifest_path.write_text(
        new_content
    )

    print("Manifest updated deterministically")

print("✅ RELEASE MANIFEST SEALED")

result = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True,
    text=True
)

changes = []

for line in result.stdout.splitlines():

    path = line[3:]

    if (
        path.startswith("artifacts/")
        and path != "artifacts/release_manifest.json"
    ):
        changes.append(line)

if changes:

    print("\n".join(changes))

    raise SystemExit(
        "❌ Post-seal mutation detected"
    )

print("✅ No post-seal mutation detected")
