import json
import hashlib
import time

INPUT_FILE = "external_input.json"
OUTPUT_FILE = "artifacts/external_attack_result.json"

def load_input():
    with open(INPUT_FILE) as f:
        return json.load(f)

def evaluate(data):
    # مثال بسيط — تقدر تربطه لاحقاً بالـ spectral core
    signal = data.get("values", [])

    if not signal or len(signal) < 10:
        return {
            "status": "invalid",
            "reason": "insufficient data"
        }

    variance = sum((x - sum(signal)/len(signal))**2 for x in signal) / len(signal)

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
    data = load_input()
    result = evaluate(data)
    final = build_result(result)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(final, f, indent=2)

    print("External model evaluated.")

if __name__ == "__main__":
    main()
