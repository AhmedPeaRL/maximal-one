# analysis/external_pressure_oracle.py

import json
import hashlib
import time
import os
import random

"""
External Pressure Oracle

This module introduces non-controlled external-like pressure
to challenge internal system stability.

It simulates:
- adversarial randomness
- unpredictable perturbations
- environment-independent stress

Goal:
Break internal self-consistency illusions.
"""

OUTPUT_PATH = "artifacts/external_pressure.json"


def generate_pressure():
    try:
        with open("artifacts/external_witness.json") as f:
            external = json.load(f)

        return {
            "timestamp": time.time(),
            "external_hash": external.get("external_hash"),
            "entropy": external.get("entropy", {}),
            "shock": "external_real"
        }

    except Exception:
        return {
            "timestamp": time.time(),
            "entropy": random.random(),
            "noise_vector": [random.uniform(-1, 1) for _ in range(10)],
            "shock": "fallback_internal"
        }


def compute_fingerprint(data):
    raw = json.dumps(data, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def evaluate_pressure(pressure):
    instability_score = sum(abs(x) for x in pressure["noise_vector"]) / 10

    return {
        "instability_score": instability_score,
        "shock_level": pressure["shock"],
        "status": (
            "stable" if instability_score < 0.3
            else "strained" if instability_score < 0.7
            else "critical"
        )
    }


def main():
    os.makedirs("artifacts", exist_ok=True)

    pressure = generate_pressure()
    fingerprint = compute_fingerprint(pressure)
    evaluation = evaluate_pressure(pressure)

    output = {
        "pressure": pressure,
        "fingerprint": fingerprint,
        "evaluation": evaluation
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print("External pressure injected.")
    print("Status:", evaluation["status"])


if __name__ == "__main__":
    main()
