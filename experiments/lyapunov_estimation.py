import numpy as np

def generate_hcm_series(seed, n=2000):
    np.random.seed(seed)
    x = np.zeros(n)
    noise = np.random.normal(0, 1, n)

    for t in range(1, n):
        x[t] = 0.8 * x[t-1] + 0.15 * np.tanh(x[t-1]) + 0.5 * noise[t]

    return x

def safe_mean(arr):
    if arr is None or len(arr) == 0:
        return None
    return float(np.mean(arr))

def estimate_lyapunov(seed, epsilon=1e-8, n=2000):
    x1 = generate_hcm_series(seed, n)
    x2 = generate_hcm_series(seed, n)
    x2[0] += epsilon

    divergence = []

    for i in range(1, n):
        delta = abs(x1[i] - x2[i])
        if delta > 0:
            divergence.append(np.log(delta / epsilon))

    return safe_mean(divergence)

if __name__ == "__main__":
    seeds = range(100)
    exponents = [estimate_lyapunov(s) for s in seeds]
    mean_lyap = safe_mean(exponents)
    
if result is None:
    print("LYAPUNOV_FAILURE: empty trajectory")

    print("=== Lyapunov Analysis ===")
    print(f"Mean Lyapunov exponent: {mean_lyap}")
