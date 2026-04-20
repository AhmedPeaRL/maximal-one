import hashlib
import json
import time
import os
import requests

ARTIFACT_PATH = "artifacts/canonical_report.json"
OUTPUT_PATH = "data/external_anchor_log.json"

def compute_hash():
    if not os.path.exists(ARTIFACT_PATH):
        return None

    with open(ARTIFACT_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def publish_anchor(hash_value):
    
    try:
        response = requests.post(
            "https://api.github.com/gists",
            headers={"Authorization": f"token {os.getenv('GH_TOKEN', '')}"},
            json={
                "public": True,
                "files": {
                    "anchor.txt": {
                        "content": f"{hash_value} @ {time.time()}"
                    }
                }
            },
            timeout=10
        )

        return response.status_code == 200

    except Exception:
        return False

def store_local(hash_value, published):
    os.makedirs("data", exist_ok=True)

    entry = {
        "timestamp": time.time(),
        "hash": hash_value,
        "published": published
    }

    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH) as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

def main():
    h = compute_hash()

    if not h:
        print("No artifact found")
        return

    published = publish_anchor(h)

    store_local(h, published)

    print("External anchor:", h, "| published:", published)

if __name__ == "__main__":
    main()
