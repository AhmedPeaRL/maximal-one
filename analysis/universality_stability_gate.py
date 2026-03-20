import json
import os
import math

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

    # HARD GUARANTEE: always valid list
    if not isinstance(history, list):
        history = []

    # defensive: remove corrupt entries
    clean_history = []
    for x in history:
        try:
            v = float(x)
            if 0 <= v <= 1:
                clean_history.append(v)
        except:
            continue

    history = clean_history

    # append new strength
    history.append(float(current["strength"]))

    # prevent duplicate consecutive entries
    if len(history) >= 2 and abs(history[-1] - history[-2]) < 1e-9:
        history = history[:-1]

    # keep last 20 runs
    history = history[-20:]

    # persist
    save_json(HISTORY_FILE, history)
    save_json("artifacts/universality_history.json", history)

    # weights
    weights = [math.exp(-0.3 * i) for i in range(len(history))]
    weights.reverse()

    score = sum(w for w, x in zip(weights, history) if x > 0.75)

    min_runs = 5
    strong_ratio = sum(1 for x in history if x > 0.75) / len(history)

    passed = (
        len(history) >= min_runs and
        strong_ratio > 0.8 and
        score > 3.5
    )

    progress = {
        "runs": len(history),
        "strong_ratio": strong_ratio,
        "score": score,
        "target_score": 3.5,
        "target_runs": min_runs
    }

    result = {
        "weights": weights,
        "history": history,
        "score": score,
        "passed": passed,
        "progress": progress
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
