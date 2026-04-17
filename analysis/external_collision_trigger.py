import requests
import json
import time
import hashlib
import os

GITHUB_TOKEN = os.getenv("GH_TOKEN")
REPO = os.getenv("GH_REPO")

def build_payload():
    payload = {
        "timestamp": time.time(),
        "source": "external_collision",
        "entropy": os.urandom(32).hex(),
        "signal": "forced_external_reality_probe"
    }

    payload["hash"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()

    return payload


def dispatch(payload):
    url = f"https://api.github.com/repos/{REPO}/dispatches"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    body = {
        "event_type": "external_witness",
        "client_payload": payload
    }

    r = requests.post(url, headers=headers, json=body)

    return r.status_code, r.text


if __name__ == "__main__":
    payload = build_payload()

    code, res = dispatch(payload)

    print("Status:", code)
    print("Response:", res)
