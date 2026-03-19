import json
import os

# ⚠️ IMPORTANT: persistent history inside repo
HISTORY_FILE = "data/universality_history.json"

CURRENT_FILE = "artifacts/universality_gate.json"


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    current = load_json(CURRENT_FILE)

    if current is None:
        print(json.dumps({
            "passed": False,
            "reason": "missing current universality"
        }))
        return

    history = load_json(HISTORY_FILE)

    if history is None:
        history = []

    # append new strength
    history.append(current["strength"])

    # keep last 10 runs فقط
    history = history[-10:]

    save_json(HISTORY_FILE, history)

    # حساب الاستقرار الحقيقي
    stable_runs = sum(1 for x in history if x > 0.75)

    passed = stable_runs >= 5

    result = {
        "stable_runs": stable_runs,
        "history": history,
        "passed": passed
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
