import json, os
import numpy as np
from scipy import stats


def rmse(a, b):
    n = min(len(a), len(b))
    a = a[:n]
    b = b[:n]
    return np.sqrt(np.mean((a - b) ** 2))


def generate_lorenz96(T=2000, F=8.0, N=40, dt=0.01):
    x = F * np.ones(N)
    x[0] += 0.01

    def step(x):
        dx = np.zeros_like(x)
        for i in range(N):
            dx[i] = (x[(i + 1) % N] - x[i - 2]) * x[i - 1] - x[i] + F
        return dx

    traj = []
    for _ in range(T):
        x = x + dt * step(x)
        traj.append(x.copy())

    return np.array(traj)


def persistence_predict(x):
    return x[:-1]


def hcm_predict(x):
    dx = x[1:] - x[:-1]
    pred = x[1:] + 0.05 * dx
    return pred

assert y_true is not None
assert y_baseline is not None
assert y_hcm is not None

# Generate Lorenz96 trajectory
trajectory = simulate_lorenz96(F=8.0, dim=5, steps=500)

# split sequence
X = trajectory[:-1]
y_true = trajectory[1:]

y_baseline = baseline_model(X)
y_hcm = hcm_model(X)

target = traj[2:]
baseline_pred = persistence_predict(traj[1:])
hcm_pred = hcm_predict(traj)

baseline_err = rmse(target, baseline_pred)
min_len = min(len(target), len(hcm_pred))
hcm_err = rmse(y_true, y_hcm)
base_err = rmse(y_true, y_baseline)

improvement = base_err - hcm_err

# bootstrap significance
boot = []
rng = np.random.default_rng(42)

for _ in range(500):
    idx = rng.integers(0, len(target), len(target))
    b = rmse(target[idx], baseline_pred[idx])
    h = rmse(target[idx], hcm_pred[idx])
    boot.append(b - h)

boot = np.array(boot)

p_value = np.mean(boot <= 0)

hcm_superior = (improvement > 0) and (p_value < 0.05)

os.makedirs("artifacts", exist_ok=True)

result = {
    "hcm_rmse": float(hcm_err),
    "baseline_rmse": float(base_err),
    "improvement": float(base_err - hcm_err),
    "p_value": float(p)
}

with open("artifacts/lorenz96.json","w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result))
