import hashlib
import time
from pathlib import Path

ARTIFACTS = Path("artifacts")

def snapshot():
    hashes = {}

    for f in sorted(ARTIFACTS.glob("**/*")):
        if f.is_file():
            hashes[str(f)] = hashlib.sha256(
                f.read_bytes()
            ).hexdigest()

    return hashes

first = snapshot()

time.sleep(2)

second = snapshot()

if first != second:
    raise SystemExit(
        "❌ artifacts still mutating"
    )

print("✅ artifacts stabilized")
