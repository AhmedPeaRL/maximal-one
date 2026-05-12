import json
import hashlib
from pathlib import Path

REPORT = Path("artifacts/canonical_report.json")
OUT = Path("artifacts/reproducibility_stamp.json")

if not REPORT.exists():
    raise SystemExit("❌ canonical report missing")

content = REPORT.read_bytes()

stamp = hashlib.sha256(content).hexdigest()

payload = {
    "artifact": REPORT.name,
    "sha256": stamp,
    "sealed": True
}

OUT.write_text(
    json.dumps(
        payload,
        indent=2,
        sort_keys=True
    ) + "\n",
    encoding="utf-8"
)

print("✅ REPRODUCIBILITY STAMP SEALED")
print(stamp)
