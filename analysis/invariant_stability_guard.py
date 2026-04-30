import numpy as np
import json

def check_stability(alphas):
    alphas = np.array(alphas)

    if len(alphas) < 2:
        raise SystemExit("❌ Not enough alpha values for stability check")

    mean = np.mean(alphas)
    std = np.std(alphas)
    spread = np.max(alphas) - np.min(alphas)

    print(f"mean_alpha: {mean}")
    print(f"std_alpha: {std}")
    print(f"spread: {spread}")

    # 🔥 NEW LOGIC: relative stability instead of absolute
    cv = std / abs(mean) if mean != 0 else float("inf")

    print(f"coefficient_of_variation: {cv}")

    if cv > 0.4:
        raise SystemExit("❌ Invariant unstable (relative variation too high)")

    print("✅ RELATIVE INVARIANT STABLE")


if __name__ == "__main__":
    data = json.load(open("artifacts/multi_report.json"))

    # ✅ FIX: read from "alphas" instead of "results"
    if "alphas" not in data:
        raise SystemExit("❌ Invalid report format: missing 'alphas'")

    alphas_dict = data["alphas"]

    # convert dict → list
    alphas = [v for v in alphas_dict.values() if isinstance(v, (int, float))]

    check_stability(alphas)
