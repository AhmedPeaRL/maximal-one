import json
import numpy as np

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


def rmse(a,b):
    return np.sqrt(np.mean((a-b)**2))


# -------- generate system trajectory --------

traj = simulate_lorenz96()

X = traj[:-1]
y_true = traj[1:]


# -------- baseline model (naive persistence) --------

y_baseline = X.copy()


# -------- HCM placeholder model --------

y_hcm = X + 0.01*np.random.randn(*X.shape)


# -------- error calculation --------

base_err = rmse(y_true, y_baseline)
hcm_err = rmse(y_true, y_hcm)

result = {
    "baseline_rmse": float(base_err),
    "hcm_rmse": float(hcm_err),
    "improvement": float(base_err - hcm_err)
}

print(json.dumps(result, indent=2))
