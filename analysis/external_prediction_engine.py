import json
import pandas as pd
import numpy as np

def load_data(path):
    return pd.read_csv(path)

def compute_signal(alpha):
    return 1 if alpha > 0.5 else -1

def evaluate_prediction(series):
    correct = 0
    total = 0

    for i in range(len(series) - 1):
        alpha = np.random.normal(0.5, 0.05)  # placeholder
        pred = compute_signal(alpha)

        real = np.sign(series[i+1] - series[i])

        if pred == real:
            correct += 1
        total += 1

    return correct / total if total > 0 else 0

def run():
    with open("core-scientific/external_prediction_bridge.json") as f:
        cfg = json.load(f)

    results = {}

    for target in cfg["prediction_targets"]:
        data = load_data(target["source"])

        acc = evaluate_prediction(data["value"].values)

        results[target["id"]] = {
            "accuracy": acc
        }

    with open("artifacts/external_prediction.json", "w") as f:
        json.dump(results, f, indent=2)

    print("External prediction evaluation complete:", results)

if __name__ == "__main__":
    run()
