import numpy as np
from numerical_spectral_verification import estimate_alpha

def generate_white_noise(n):
    return np.random.normal(0, 1, n)

def monte_carlo_alpha(trials=2000, n=5000):
    alphas = []
    for _ in range(trials):
        series = generate_white_noise(n)
        alpha = estimate_alpha(series)
        alphas.append(alpha)
    return np.array(alphas)

if __name__ == "__main__":

    np.random.seed(0)

    null_alphas = monte_carlo_alpha()

    mean_null = np.mean(null_alphas)
    std_null = np.std(null_alphas)

    observed_alpha = estimate_alpha(generate_white_noise(5000))

    print("min_null:", float(np.min(null_alphas)))
    print("max_null:", float(np.max(null_alphas)))

    z_score = (observed_alpha - mean_null) / std_null

    print("==== NULL MONTE CARLO SPECTRAL TEST ====")
    print("mean_null:", float(mean_null))
    print("std_null:", float(std_null))
    print("observed_alpha:", float(observed_alpha))
    print("z_score:", float(z_score))
