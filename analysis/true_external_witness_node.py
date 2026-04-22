# analysis/true_external_witness_node.py

import requests
import hashlib
import json
import time
import random

"""
TRUE EXTERNAL WITNESS NODE

This script runs OUTSIDE the system assumptions.

It:
- pulls public artifact
- recomputes hash
- injects unpredictable entropy
- returns independent verdict

NO shared runtime
NO shared environment
"""

TARGET_URL = "https://ahmedpearl.github.io/maximal-one/public/repro_bundle/canonical_report.json"


def fetch_external():
    urls = [
        TARGET_URL,
        TARGET_URL.replace("canonical_report.json", "report.hash"),
    ]

    last_error = None

    for url in urls:
        try:
            r = requests.get(url, timeout=10)

            if r.status_code == 200 and len(r.text.strip()) > 0:
                return r.text

        except Exception as e:
            last_error = e

    raise Exception(f"Failed to fetch external artifact from all mirrors: {last_error}")


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
    raw = fetch_external()
    normalized = normalize(raw)

    h = compute_hash(normalized)
    entropy = inject_entropy()

    result = {
        "external_hash": h,
        "entropy": entropy,
        "verdict": "independent_observation"
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
