import numpy as np
import pandas as pd
import os

np.random.seed(42)

OUT = "real-data"
os.makedirs(OUT, exist_ok=True)

def logistic_map(r=3.9, n=5000):
    x = 0.5
    data = []
    for _ in range(n):
        x = r * x * (1 - x)
        data.append(x)
    return np.array(data)

def henon_map(a=1.4, b=0.3, n=5000):
    x = 0.1
    y = 0.1
    xs = []

    for _ in range(n):
        x_new = 1 - a * x * x + y
        y = b * x
        x = x_new
        xs.append(x)

    return np.array(xs)

def rossler(n=5000, dt=0.01):

    a = 0.2
    b = 0.2
    c = 5.7

    x, y, z = 1, 1, 1
    xs = []

    for _ in range(n):

        dx = -y - z
        dy = x + a * y
        dz = b + z * (x - c)

        x += dx * dt
        y += dy * dt
        z += dz * dt

        xs.append(x)

    return np.array(xs)


datasets = {
    "logistic_map.csv": logistic_map(),
    "henon_map.csv": henon_map(),
    "rossler.csv": rossler()
}

for name, data in datasets.items():

    path = os.path.join(OUT, name)

    df = pd.DataFrame({"x": data})

    df.to_csv(path, index=False)

print("Chaotic datasets generated:", list(datasets.keys()))
