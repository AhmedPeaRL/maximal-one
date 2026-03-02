import numpy as np

def simulate(dtype):
    np.random.seed(42)
    x = np.cumsum(np.random.normal(0,1,5000).astype(dtype))
    msd = np.mean((x - x.mean())**2)
    return np.log(msd) / np.log(len(x))

a64 = simulate(np.float64)
a32 = simulate(np.float32)

print("float64:", a64)
print("float32:", a32)

if abs(a64 - a32) > 0.01:
    raise RuntimeError("Precision instability detected")
