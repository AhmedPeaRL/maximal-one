import numpy as np
import json

def check_stability(alphas):
    alphas = np.array(alphas)

    if len(alphas) < 3:
        raise SystemExit(f"❌ Not enough VALID alpha values: {alphas}")

    real = alphas[0]
    synthetic = alphas[1]
    noise = alphas[2]

    print(f"real: {real}")
    print(f"synthetic: {synthetic}")
    print(f"noise: {noise}")

    # guard ضد NaN
    if not (np.isfinite(real) and np.isfinite(synthetic) and np.isfinite(noise)):
        raise SystemExit("❌ Non-finite values detected after filtering")

    cond1 = abs(real - noise) > 0.25
    cond2 = abs(real - synthetic) > 0.25
    cond3 = abs(synthetic - noise) > 0.15

    if not (cond1 and cond2 and cond3):
        raise SystemExit("❌ Structural separation failed")

    print("✅ RELATIONAL INVARIANT HOLDS")


def extract_structured_alphas(alphas_dict):
    try:
        real = alphas_dict["real"]["sunspots"]
        synthetic = alphas_dict["synthetic"]["mean"]
        noise = alphas_dict["noise"]["white"]
    except KeyError as e:
        raise SystemExit(f"❌ Missing required alpha key: {e}")

    values = [real, synthetic, noise]

    for name, v in zip(["real", "synthetic", "noise"], values):
        if not isinstance(v, (int, float)) or not np.isfinite(v):
            raise SystemExit(f"❌ Invalid {name} alpha: {v}")

    return values


if __name__ == "__main__":
    data = json.load(open("artifacts/multi_report.json"))

    if "alphas" not in data:
        raise SystemExit("❌ Invalid report format: missing 'alphas'")

    alphas_dict = data["alphas"]

    # ✅ FIX الحقيقي
    alphas = extract_structured_alphas(alphas_dict)

    print(f"extracted_alphas: {alphas}")

    check_stability(alphas)
