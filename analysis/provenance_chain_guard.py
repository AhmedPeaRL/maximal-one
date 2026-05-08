import json
import hashlib
import os
from datetime import datetime, timezone

ARTIFACT = "artifacts/canonical_report.json"
FINGERPRINT = "artifacts/fingerprint.txt"

if not os.path.exists(ARTIFACT):
    raise SystemExit("Missing canonical artifact")

if not os.path.exists(FINGERPRINT):
    raise SystemExit("Missing fingerprint")

artifact_bytes = open(
    ARTIFACT,
    "rb"
).read()

fingerprint = open(
    FINGERPRINT,
    "r"
).read().strip()

artifact_sha = hashlib.sha256(
    artifact_bytes
).hexdigest()

utc_now = datetime.now(
    timezone.utc
).isoformat()

record = {
    "artifact_sha256": artifact_sha,
    "fingerprint": fingerprint,
    "timestamp_utc": utc_now,
    "github_sha": os.getenv(
        "GITHUB_SHA",
        "unknown"
    )
}

serialized = json.dumps(
    record,
    sort_keys=True
).encode()

chain_hash = hashlib.sha256(
    serialized
).hexdigest()

record["chain_hash"] = chain_hash

with open(
    "artifacts/provenance_chain.json",
    "w"
) as f:
    json.dump(
        record,
        f,
        indent=2
    )

print(json.dumps(
    record,
    indent=2
))

print(
    "✅ PROVENANCE CHAIN SEALED"
)
