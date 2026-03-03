import numpy as np
from scipy.integrate import solve_ivp
from sklearn.linear_model import LinearRegression
import json

def lorenz(t, xyz, sigma=10, rho=28, beta=8/3):
    x, y, z = xyz
    return [
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z
    ]

def generate_lorenz(n=5000, dt=0.01):
    sol = solve_ivp(lorenz, [0, n*dt], [1,1,1],
                    t_eval=np.linspace(0,n*dt,n))
    return sol.y[0]

def naive_predict(x):
    return np.roll(x,1)

def hcm_predict(x):
    X = x[:-1].reshape(-1,1)
    y = x[1:]
    model = LinearRegression().fit(X,y)
    pred = model.predict(X)
    return np.concatenate([[x[0]], pred])

def mse(a,b):
    return np.mean((a-b)**2)

if __name__ == "__main__":

    x = generate_lorenz()

    naive = naive_predict(x)
    hcm = hcm_predict(x)

    mse_naive = mse(x,naive)
    mse_hcm = mse(x,hcm)

    result = {
        "mse_naive": float(mse_naive),
        "mse_hcm": float(mse_hcm),
        "hcm_superior": bool(mse_hcm < mse_naive)
    }

    print(json.dumps(result,indent=2))
