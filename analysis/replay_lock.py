import json
import hashlib
from pathlib import Path

from analysis.canonical_json import canonicalize

SOURCE = Path("artifacts/canonical_report.json")
LOCK = Path("artifacts/canonical_report.lock")

if not SOURCE.exists():
    raise SystemExit("❌ canonical report missing")

content = json.loads(
    SOURCE.read_text(encoding="utf-8")
)

canonical = canonicalize(content)

sha = hashlib.sha256(
    canonical.encode()
).hexdigest()

payload = {
    "sha256": sha,
    "length": len(canonical),
    "locked": True
}

LOCK.write_text(
    canonicalize(payload),
    encoding="utf-8"
)

print("✅ CANONICAL REPLAY LOCK SEALED")
print(sha)
