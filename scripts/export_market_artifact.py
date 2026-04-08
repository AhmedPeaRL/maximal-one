import json
import os
import hashlib
from datetime import datetime

INPUT = "artifacts/canonical_report.json"
OUTPUT_DIR = "market"
os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.exists(INPUT):
    raise Exception("Missing canonical report")

with open(INPUT) as f:
    data = json.load(f)

# Extract only meaningful layer (no noise)
artifact = {
    "timestamp": datetime.utcnow().isoformat(),
    "spectral_alpha": data.get("spectral_profile", {}).get("estimated_alpha"),
    "stability": data.get("stability", {}),
    "invariants": data.get("invariants", {}),
    "verdict": data.get("global_verdict"),
}

raw = json.dumps(artifact, sort_keys=True)

hash_val = hashlib.sha256(raw.encode()).hexdigest()

artifact["_proof"] = {
    "sha256": hash_val
}

filename = f"{OUTPUT_DIR}/artifact_{hash_val[:12]}.json"

with open(filename, "w") as f:
    json.dump(artifact, f, indent=2)

print("Market artifact created:", filename)
