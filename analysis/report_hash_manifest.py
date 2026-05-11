import json
import hashlib
from pathlib import Path

from analysis.canonical_json import canonicalize

REPORT = Path("artifacts/canonical_report.json")

report = json.loads(
    REPORT.read_text(encoding="utf-8")
)

digest = hashlib.sha256(
    canonicalize(report).encode()
).hexdigest()

manifest = {
    "canonical_sha256": digest
}

Path(
    "artifacts/report_hash_manifest.json"
).write_text(
    canonicalize(manifest),
    encoding="utf-8"
)

print("✅ REPORT HASH MANIFEST SEALED")
print(digest)
