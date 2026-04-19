import json
import hashlib
import time
import os

INPUT_FILE = "external_input.json"
OUTPUT_FILE = "artifacts/external_attack_result.json"


def load_input():
    # لو الملف مش موجود → نولّد input افتراضي
    if not os.path.exists(INPUT_FILE):
        print("No external input found. Generating fallback signal...")

        return {
            "values": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        }

    with open(INPUT_FILE) as f:
        return json.load(f)


def evaluate(data):
    signal = data.get("values", [])

    if not signal or len(signal) < 10:
        return {
            "status": "invalid",
            "reason": "insufficient data"
        }

    mean = sum(signal) / len(signal)
    variance = sum((x - mean) ** 2 for x in signal) / len(signal)

    return {
        "status": "evaluated",
        "variance": variance,
        "stability": "unstable" if variance > 100 else "stable"
    }


def build_result(eval_result):
    raw = json.dumps(eval_result, sort_keys=True).encode()

    return {
        "timestamp": time.time(),
        "result": eval_result,
        "hash": hashlib.sha256(raw).hexdigest()
    }


def main():
    os.makedirs("artifacts", exist_ok=True)

    data = load_input()
    result = evaluate(data)
    final = build_result(result)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(final, f, indent=2)

    print("External model evaluated successfully.")


if __name__ == "__main__":
    main()
