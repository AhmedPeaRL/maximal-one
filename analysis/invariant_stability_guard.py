import numpy as np
import json

def check_stability(alphas):
    alphas = np.array(alphas)
    
    mean = np.mean(alphas)
    std = np.std(alphas)
    spread = np.max(alphas) - np.min(alphas)

    print(f"mean_alpha: {mean}")
    print(f"std_alpha: {std}")
    print(f"spread: {spread}")

    if std > 0.5:
        raise SystemExit("❌ Invariant unstable (std too high)")

    if spread > 1.5:
        raise SystemExit("❌ Invariant broken (spread too large)")

    print("✅ INVARIANT STABLE")

if __name__ == "__main__":
    data = json.load(open("artifacts/multi_report.json"))
    alphas = [x["alpha"] for x in data["results"] if "alpha" in x]
    check_stability(alphas)
