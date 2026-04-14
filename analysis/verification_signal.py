import json
import os

signal = {
    "fast_layer": os.getenv("FAST_OK", "unknown"),
    "core_layer": os.getenv("CORE_OK", "unknown"),
    "deep_layer": os.getenv("DEEP_OK", "unknown"),
}

score = 0

if signal["fast_layer"] == "true":
    score += 0.4

if signal["core_layer"] == "true":
    score += 0.4

if signal["deep_layer"] == "true":
    score += 0.2

result = {
    "verification_score": score,
    "status": "emerging" if score >= 0.5 else "unstable"
}

os.makedirs("artifacts", exist_ok=True)

with open("artifacts/verification_signal.json", "w") as f:
    json.dump(result, f, indent=2)

print("Verification score:", score)
