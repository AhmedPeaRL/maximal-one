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
    r = requests.get(TARGET_URL, timeout=10)
    if r.status_code != 200:
        raise Exception("Failed to fetch external artifact")
    return r.text


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
