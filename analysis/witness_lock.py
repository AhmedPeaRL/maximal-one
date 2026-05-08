import json
import hashlib
import os

ARTIFACTS = [
    "artifacts/canonical_report.json",
    "artifacts/pipeline_sovereignty.json",
    "artifacts/provenance_chain.json",
    "artifacts/environment_fingerprint.json",
    "artifacts/external_replay_verification.json"
]

payload = {}

for path in ARTIFACTS:

    with open(path, "rb") as f:
        payload[path] = hashlib.sha256(
            f.read()
        ).hexdigest()

payload["commit"] = os.getenv(
    "GITHUB_SHA",
    "unknown"
)

final_hash = hashlib.sha256(
    json.dumps(
        payload,
        sort_keys=True
    ).encode()
).hexdigest()

payload["witness_lock"] = final_hash

with open(
    "artifacts/witness_lock.json",
    "w"
) as f:

    json.dump(
        payload,
        f,
        indent=2
    )

print(
    "✅ WITNESS LOCK SEALED"
)
