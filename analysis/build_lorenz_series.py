import json
import numpy as np
from scipy.integrate import odeint
import pathlib

ART = pathlib.Path("artifacts")

def lorenz(state, t, sigma=10, beta=8/3, rho=28):
    x, y, z = state
    return [
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z
    ]

t = np.linspace(0, 50, 5000)
init = [1.0, 1.0, 1.0]

sol = odeint(lorenz, init, t)

real = sol[:, 0]

# model = shuffled version (baseline)
model = np.random.permutation(real)

ART.mkdir(exist_ok=True)

(ART / "lorenz_real.json").write_text(json.dumps(real.tolist()))
(ART / "lorenz_model.json").write_text(json.dumps(model.tolist()))

print("Lorenz series generated:", len(real))
