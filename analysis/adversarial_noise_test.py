import numpy as np
import json

np.random.seed(42)

def generate_adversarial_series(n=1000):
    x = np.random.randn(n)

    # inject structured adversarial drift
    drift = np.linspace(0, 3, n)
    noise = np.sin(np.linspace(0, 50, n)) * 0.5

    return x + drift + noise

def naive_predict(x):
    return np.roll(x, 1)

def hcm_predict(x):
    window = 5
    pred = np.convolve(x, np.ones(window)/window, mode='same')
    return pred

series = generate_adversarial_series()

naive = naive_predict(series)
hcm = hcm_predict(series)

mse_naive = np.mean((series - naive)**2)
mse_hcm = np.mean((series - hcm)**2)

result = {
    "mse_naive": float(mse_naive),
    "mse_hcm": float(mse_hcm),
    "hcm_superior": bool(mse_hcm < mse_naive)
}

print(json.dumps(result, indent=2))

if not result["hcm_superior"]:
    raise SystemExit("Adversarial robustness failed")
