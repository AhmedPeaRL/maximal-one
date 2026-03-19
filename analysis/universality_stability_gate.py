import json
import os

HISTORY_FILE = "artifacts/universality_history.json"

CURRENT_FILE = "artifacts/universality_gate.json"


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    current = load_json(CURRENT_FILE)

    if current is None:
        print(json.dumps({"passed": False, "reason": "missing current universality"}))
        return

    history = load_json(HISTORY_FILE)

    if history is None:
        history = []

    history.append(current["strength"])

    # keep last 10 runs
    history = history[-10:]

    save_json(HISTORY_FILE, history)

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
