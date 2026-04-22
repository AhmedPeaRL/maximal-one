import requests
import hashlib
import json
import time
import random

TARGET_URLS = [
    "https://ahmedpearl.github.io/maximal-one/public/repro_bundle/canonical_report.json",
    "https://raw.githubusercontent.com/ahmedpearl/maximal-one/main/public/repro_bundle/canonical_report.json",
    "https://cdn.jsdelivr.net/gh/ahmedpearl/maximal-one@main/public/repro_bundle/canonical_report.json"
]

def fetch_external():
    errors = []

    for url in TARGET_URLS:
        try:
            r = requests.get(url, timeout=15)

            if r.status_code == 200 and len(r.text.strip()) > 0:
                return r.text, url

            else:
                errors.append(f"{url} -> bad response")

        except Exception as e:
            errors.append(f"{url} -> {str(e)}")

    return None, errors

def normalize(raw):
    data = json.loads(raw)

    def clean(obj):
        if isinstance(obj, dict):
            return {
                k: clean(v)
                for k, v in obj.items()
                if k not in ["timestamp", "_environment", "_sealed"]
            }
        if isinstance(obj, list):
            return [clean(x) for x in obj]
        if isinstance(obj, float):
            return round(obj, 8)
        return obj

    return json.dumps(clean(data), sort_keys=True)

def compute_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def inject_entropy():
    return {
        "noise": random.random(),
        "time": time.time()
    }

def main():
    raw, meta = fetch_external()

    if raw is None:
        result = {
            "status": "external_unavailable",
            "errors": meta,
            "entropy": inject_entropy(),
            "verdict": "degraded_but_recorded"
        }
        print(json.dumps(result, indent=2))
        return

    normalized = normalize(raw)
    h = compute_hash(normalized)

    result = {
        "status": "external_verified",
        "source": meta,
        "external_hash": h,
        "entropy": inject_entropy(),
        "verdict": "independent_observation"
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
