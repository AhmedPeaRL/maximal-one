# analysis/lorenz96_benchmark.py

import numpy as np
import json
from sklearn.metrics import mean_squared_error

def lorenz96(x, F=8):
    d = len(x)
    dxdt = np.zeros(d)
    for i in range(d):
        dxdt[i] = (x[(i+1)%d] - x[i-2]) * x[i-1] - x[i] + F
    return dxdt

def simulate(d=10, steps=2000, dt=0.01):
    x = np.random.rand(d)
    trajectory = []
    for _ in range(steps):
        x = x + dt * lorenz96(x)
        trajectory.append(x.copy())
    return np.array(trajectory)

def naive_predict(series):
    return series[:-1]

def hcm_predict(series):
    # placeholder – replace with HCM core predictor
    return series[:-1]  # currently same as naive

def run():
    np.random.seed(42)
    data = simulate()
    true = data[1:]
    
    naive = naive_predict(data)
    hcm = hcm_predict(data)

    mse_naive = mean_squared_error(true, naive)
    mse_hcm = mean_squared_error(true, hcm)

    result = {
        "mse_naive": float(mse_naive),
        "mse_hcm": float(mse_hcm),
        "hcm_superior": mse_hcm < mse_naive
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    run()
