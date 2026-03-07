import numpy as np
import pandas as pd

def generate_lorenz(n=2000, dt=0.01):
    sigma = 10
    beta = 8/3
    rho = 28

    x, y, z = 1.0, 1.0, 1.0

    xs = []

    for _ in range(n):
        dx = sigma*(y-x)
        dy = x*(rho-z)-y
        dz = x*y-beta*z

        x += dx*dt
        y += dy*dt
        z += dz*dt

        xs.append(x)

    return np.array(xs)

series = generate_lorenz()

df = pd.DataFrame({"value": series})

import os
os.makedirs("real-data", exist_ok=True)

df.to_csv("real-data/sample.csv", index=False)

print("Dataset generated:", len(df))
