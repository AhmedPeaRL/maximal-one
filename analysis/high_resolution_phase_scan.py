import numpy as np
import json
import os

def simulate(alpha_gamma):
    # Replace with real core call if needed
    x = np.cumsum(np.random.normal(0, 1, 5000))
    msd = np.mean((x - x.mean())**2)
    return np.log(msd) / np.log(len(x))

def main():
    np.random.seed(42)
    gammas = np.arange(0.90, 1.0001, 0.001)
    alphas = []

    for g in gammas:
        alpha = simulate(g)
        alphas.append(alpha)

    result = {
        "gamma_min": float(gammas.min()),
        "gamma_max": float(gammas.max()),
        "step": 0.001,
        "alphas": list(map(float, alphas))
    }

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/high_resolution_phase_scan.json","w") as f:
        json.dump(result,f,indent=2)

if __name__ == "__main__":
    main()
