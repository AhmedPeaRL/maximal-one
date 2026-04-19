import json
import hashlib
import time
import os

INPUT_FILE = "external_input.json"
OUTPUT_FILE = "artifacts/external_attack_result.json"


def load_input():
    if not os.path.exists(INPUT_FILE):
        return {
            "status": "no_input",
            "values": []
        }

    with open(INPUT_FILE) as f:
        return json.load(f)


def evaluate(data):
    signal = data.get("values", [])

    if not signal or len(signal) < 10:
        return {
            "status": "invalid",
            "reason": "insufficient data",
            "input_detected": False
        }

    mean = sum(signal) / len(signal)
    variance = sum((x - mean) ** 2 for x in signal) / len(signal)

    return {
        "status": "evaluated",
        "variance": variance,
        "stability": "unstable" if variance > 100 else "stable",
        "input_detected": True
    }


def build_result(eval_result):
    raw = json.dumps(eval_result, sort_keys=True).encode()

    return {
        "timestamp": time.time(),
        "result": eval_result,
        "hash": hashlib.sha256(raw).hexdigest()
    }


def main():
    data = load_input()
    result = evaluate(data)
    final = build_result(result)

    os.makedirs("artifacts", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(final, f, indent=2)

    print("External model evaluated safely.")


if __name__ == "__main__":
    main()
