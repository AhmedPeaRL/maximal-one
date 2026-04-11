import requests
import hashlib
import time
import json

"""
External Irreducible Anchor V2

هدفه:
إدخال "عدم قابلية السيطرة" الحقيقية في النظام.

مش مجرد API...
لكن مصدر لا يمكن إعادة إنتاجه deterministic داخل نفس البيئة.

"""

ANCHORS = [
    "https://worldtimeapi.org/api/timezone/Etc/UTC",
    "https://api.coindesk.com/v1/bpi/currentprice.json",
    "https://random-data-api.com/api/number/random_number"
]


def fetch_anchor(url):
    try:
        r = requests.get(url, timeout=5)
        return r.text
    except:
        return "FAIL"


def build_anchor_fingerprint():
    raw = {}

    for src in ANCHORS:
        raw[src] = fetch_anchor(src)

    combined = json.dumps(raw, sort_keys=True)

    fingerprint = hashlib.sha256(combined.encode()).hexdigest()

    return {
        "timestamp": time.time(),
        "sources": list(raw.keys()),
        "fingerprint": fingerprint,
        "raw_entropy_size": len(combined),
        "status": "external_irreducible"
    }


if __name__ == "__main__":
    anchor = build_anchor_fingerprint()

    with open("artifacts/external_anchor_v2.json", "w") as f:
        json.dump(anchor, f, indent=2)

    print("External anchor generated:")
    print(json.dumps(anchor, indent=2))
