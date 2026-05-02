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


def extract_alphas(alphas_dict):
    values = []

    for domain_name, domain in alphas_dict.items():
        if isinstance(domain, dict):
            for k, v in domain.items():
                if isinstance(v, (int, float)) and np.isfinite(v):
                    values.append(v)
                else:
                    print(f"⚠️ skipped invalid alpha in {domain_name}:{k} -> {v}")

    return values


if __name__ == "__main__":
    data = json.load(open("artifacts/multi_report.json"))

    if "alphas" not in data:
        raise SystemExit("❌ Invalid report format: missing 'alphas'")

    alphas_dict = data["alphas"]

    # ✅ FIX الحقيقي
    alphas = extract_alphas(alphas_dict)

    print(f"extracted_alphas: {alphas}")

    check_stability(alphas)
