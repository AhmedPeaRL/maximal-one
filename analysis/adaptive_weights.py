import json

def load():
    try:
        with open("artifacts/history.json") as f:
            return json.load(f)
    except:
        return []

def update_weights(history):
    if not history:
        return {
            "predictive": 0.5,
            "structure": 0.25,
            "universality": 0.15
        }

    success = sum(1 for h in history if h.get("passed"))
    total = len(history)

    ratio = success / total if total else 0.5

    return {
        "predictive": 0.4 + 0.2 * ratio,
        "structure": 0.2,
        "universality": 0.2
    }

def main():
    h = load()
    w = update_weights(h)

    with open("artifacts/adaptive_weights.json", "w") as f:
        json.dump(w, f, indent=2)

    print(w)

if __name__ == "__main__":
    main()
