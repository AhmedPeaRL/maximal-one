import numpy as np

def topology_error(x, y):
    return np.abs(np.corrcoef(x, y)[0,1] - 1)

if __name__ == "__main__":
    rng = np.random.RandomState(42)
    x = rng.normal(size=2000)
    y = x + 0.01*rng.normal(size=2000)

    error = topology_error(x,y)

    print("Topology error:", error)

    if error > 0.05:
        raise SystemExit("Topology not preserved")
