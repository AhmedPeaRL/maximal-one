import json
import hashlib
from pathlib import Path

REPORT = Path("artifacts/canonical_report.json")


def canonical(obj):

    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":")
    ).encode()


report = json.loads(
    REPORT.read_text()
)

digest = hashlib.sha256(
    canonical(report)
).hexdigest()

manifest = {
    "canonical_sha256": digest
}

Path("artifacts/report_hash_manifest.json").write_text(
    json.dumps(
        manifest,
        indent=2,
        sort_keys=True
    )
)

print("✅ REPORT HASH MANIFEST SEALED")
print(digest)
