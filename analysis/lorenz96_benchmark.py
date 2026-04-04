import json
import numpy as np

# -----------------------------
# Lorenz96 system
# -----------------------------

def simulate_lorenz96(F=8.0, dim=5, steps=500, dt=0.01):
    x = F * np.ones(dim)
    x[0] += 0.01
    trajectory = []

    for _ in range(steps):
        dx = np.zeros(dim)
        for i in range(dim):
            dx[i] = (x[(i+1)%dim] - x[i-2]) * x[i-1] - x[i] + F
        x = x + dt * dx
        trajectory.append(x.copy())

    return np.array(trajectory)


def rmse(a, b):
    return np.sqrt(np.mean((a - b) ** 2))


# -----------------------------
# HCM predictor (REAL)
# -----------------------------

from analysis.hcm_phase_space_predictor import HCMPhaseSpacePredictor
from analysis.hcm_meta_predictor import HCMMetaPredictor

meta_model = HCMMetaPredictor()


def hcm_predict(history):
    return meta_model.predict(history)


# -----------------------------
# Rolling prediction
# -----------------------------

def rollout_predict(X, predictor):
    preds = []
    history = list(X[0])

    for i in range(len(X)):
        try:
            p = predictor(history)
            if not np.isfinite(p):
                p = history[-1]
        except:
            p = history[-1]

        preds.append(p)
        history.append(X[i][-1])

    return np.array(preds)


# -----------------------------
# MAIN
# -----------------------------

traj = simulate_lorenz96()

X = traj[:-1]
y_true = traj[1:, -1]  # predict last dimension only


# -------- baseline --------
y_baseline = X[:, -1]


# -------- HCM --------
y_hcm = rollout_predict(X, hcm_predict)


# -------- metrics --------
base_err = rmse(y_true, y_baseline)
hcm_err = rmse(y_true, y_hcm)


result = {
    "baseline_rmse": float(base_err),
    "hcm_rmse": float(hcm_err),
    "improvement": float(base_err - hcm_err),
    "hcm_superior": hcm_err < base_err
}

print(json.dumps(result, indent=2))
