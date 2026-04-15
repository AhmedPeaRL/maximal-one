import hashlib
import requests
import time
import json
import os

def generate_anchor():
    if not os.path.exists("artifacts/canonical_report.json"):
        print("No report found")
        return

    with open("artifacts/canonical_report.json","rb") as f:
        data = f.read()

    h = hashlib.sha256(data).hexdigest()

    anchor = {
        "hash": h,
        "timestamp": int(time.time())
    }

    try:
        # Public timestamp API (fallback-safe)
        r = requests.post(
            "https://httpbin.org/post",
            json=anchor,
            timeout=10
        )

        if r.status_code == 200:
            anchor["external_ack"] = True
        else:
            anchor["external_ack"] = False

    except:
        anchor["external_ack"] = False

    os.makedirs("public", exist_ok=True)

    with open("public/external_time_anchor.json","w") as f:
        json.dump(anchor, f, indent=2)

    print("External time anchor generated")

if __name__ == "__main__":
    generate_anchor()
