import json
import os

HISTORY_PATH = "data/decision_history.json"
OUTPUT_PATH = "artifacts/temporal_intelligence.json"


def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    with open(HISTORY_PATH) as f:
        return json.load(f)


def analyze_trend(history):
    if len(history) < 10:
        return "insufficient_data"

    recent = history[-10:]
    z_values = [h["z"] for h in recent]

    avg = sum(z_values) / len(z_values)

    if avg > 4:
        return "strong_field"
    elif avg > 2:
        return "emerging_field"
    else:
        return "weak_field"


def run():
    history = load_history()
    trend = analyze_trend(history)

    result = {
        "trend": trend,
        "history_length": len(history)
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print("Temporal intelligence built:", trend)


if __name__ == "__main__":
    run()
