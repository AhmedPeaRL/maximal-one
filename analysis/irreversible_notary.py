import hashlib
import json
import time
import os
import subprocess

ARTIFACT = "artifacts/canonical_report.json"
OUTPUT = "data/irreversible_notary.json"

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def opentimestamp(hash_value):
    try:
        # create temp file
        with open("temp.hash", "w") as f:
            f.write(hash_value)

        # try ots (if available)
        subprocess.run(["ots", "stamp", "temp.hash"], check=True)

        return True
    except Exception:
        return False

def multi_anchor(hash_value):
    anchors = []

    # GitHub anchor (implicit)
    anchors.append({
        "type": "github_commit",
        "status": "pending"
    })

    # Local redundancy
    anchors.append({
        "type": "local_record",
        "timestamp": time.time()
    })

    return anchors

def store(data):
    os.makedirs("data", exist_ok=True)

    if os.path.exists(OUTPUT):
        with open(OUTPUT) as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append(data)

    with open(OUTPUT, "w") as f:
        json.dump(existing, f, indent=2)

def main():
    if not os.path.exists(ARTIFACT):
        print("No artifact")
        return

    h = sha256_file(ARTIFACT)

    ots_ok = opentimestamp(h)

    anchors = multi_anchor(h)

    entry = {
        "hash": h,
        "timestamp": time.time(),
        "opentimestamped": ots_ok,
        "anchors": anchors,
        "source": "maximal-one"
    }

    store(entry)

    print("NOTARIZED:", h)
    print("OTS:", ots_ok)

if __name__ == "__main__":
    main()
