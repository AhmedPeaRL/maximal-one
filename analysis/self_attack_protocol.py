import json
import random
import hashlib
import time

ATTACK_TYPES = [
    "noise_injection",
    "payload_mutation",
    "timing_distortion",
    "structure_break",
    "entropy_overload"
]

def generate_attack(payload):
    attack = random.choice(ATTACK_TYPES)

    if attack == "noise_injection":
        payload["noise"] = random.random()

    elif attack == "payload_mutation":
        payload["mutated"] = str(payload)[:50]

    elif attack == "timing_distortion":
        time.sleep(random.uniform(0, 0.2))

    elif attack == "structure_break":
        payload = {"corrupted": True}

    elif attack == "entropy_overload":
        payload["entropy"] = hashlib.sha256(str(time.time()).encode()).hexdigest()

    return payload, attack

def run_self_attack(input_payload):
    attacked, attack_type = generate_attack(input_payload)

    return {
        "original": input_payload,
        "attacked": attacked,
        "attack_type": attack_type,
        "timestamp": time.time()
    }

if __name__ == "__main__":
    sample = {"signal": "test"}
    result = run_self_attack(sample)
    print(json.dumps(result, indent=2))
