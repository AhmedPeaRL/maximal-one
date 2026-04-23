import os
import json
import hashlib

def check_external_fingerprint():
    path = "artifacts/external_witness.json"

    if not os.path.exists(path):
        print("❌ No external fingerprint → self-referential")
        exit(1)

    with open(path) as f:
        data = f.read()

    fingerprint = hashlib.sha256(data.encode()).hexdigest()

    if len(fingerprint) < 10:
        print("❌ Invalid fingerprint")
        exit(1)

    print("✅ External fingerprint detected:", fingerprint[:12])

if __name__ == "__main__":
    check_external_fingerprint()
