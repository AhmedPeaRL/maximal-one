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

    if not isinstance(history, list):
        history = []

    clean = []
    for x in history:
        try:
            v = float(x)
            if 0 <= v <= 1:
                clean.append(v)
        except:
            continue

    history = clean

    current_strength = float(current.get("strength", 0))
    history.append(current_strength)

    history = history[-25:]

    save_json(HISTORY_FILE, history)
    save_json("artifacts/universality_history.json", history)

    weights = [math.exp(-0.15 * i) for i in range(len(history))]
    weights.reverse()

    score = sum(w for w, x in zip(weights, history) if x > 0.75)

    strong_count = sum(1 for x in history if x > 0.75)
    strong_ratio = strong_count / len(history) if history else 0

    # 🔥 التعديل الذكي هنا
    min_runs = 4

    passed = (
        len(history) >= min_runs and
        strong_ratio >= 0.75 and
        score >= 2.75
    )

    progress = {
        "runs": len(history),
        "strong_ratio": strong_ratio,
        "score": score,
        "target_score": 2.6,
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
