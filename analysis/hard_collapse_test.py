import json
import random
import numpy as np

def generate_noise_series(n=2000):
    return np.random.normal(0, 1, n)

def collapse_test(alpha, sigma):
    # simulate worst-case falsification pressure
    
    noise = generate_noise_series()
    noise_std = np.std(noise)

    # if system alpha cannot dominate noise structure → collapse
    if sigma > noise_std:
        return "collapse_sigma_dominant_noise"

    if abs(alpha) < 0.5:
        return "collapse_alpha_vanish"

    return "resilient"

def run():
    with open("artifacts/canonical_report.json") as f:
        report = json.load(f)

    alpha = report["spectral_profile"]["estimated_alpha"]
    sigma = report["spectral_profile"]["bootstrap_std"]

    verdict = collapse_test(alpha, sigma)

    result = {
        "alpha": alpha,
        "sigma": sigma,
        "collapse_test": verdict
    }

    with open("artifacts/collapse_test.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Collapse test:", verdict)

if __name__ == "__main__":
    run()
