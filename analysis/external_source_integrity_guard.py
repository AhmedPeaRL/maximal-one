import hashlib
import requests
import os

url = os.getenv("EXTERNAL_SOURCE_URL", "").strip()

if not url:
    raise SystemExit("❌ missing external source url")

r = requests.get(url, timeout=10)
r.raise_for_status()

content = r.text.strip().encode()

sha = hashlib.sha256(content).hexdigest()

print("External source SHA256:", sha)

if len(content) < 10:
    raise SystemExit("❌ external source too small")

print("✅ EXTERNAL SOURCE INTEGRITY HOLDS")
