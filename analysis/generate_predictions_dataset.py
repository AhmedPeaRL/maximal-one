import numpy as np
import pandas as pd

def lorenz(x, y, z, s=10, r=28, b=2.667):
    dx = s*(y - x)
    dy = r*x - y - x*z
    dz = x*y - b*z
    return dx, dy, dz

dt = 0.01
steps = 1000

xs = np.empty(steps)
ys = np.empty(steps)
zs = np.empty(steps)

xs[0], ys[0], zs[0] = (0., 1., 1.05)

for i in range(steps-1):
    dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
    xs[i+1] = xs[i] + dx*dt
    ys[i+1] = ys[i] + dy*dt
    zs[i+1] = zs[i] + dz*dt

df = pd.DataFrame({
    "x": xs,
    "y": ys,
    "z": zs
})

df.to_csv("real-data/predictions.csv", index=False)

print("Generated 1000-row Lorenz dataset.")
