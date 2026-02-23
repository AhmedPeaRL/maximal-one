import numpy as np
from .core_experiment import run_periodicity_test
from .synthetic_control import generate_noise, inject_periodic
from .statistics_utils import bonferroni_correction, fdr_correction

def randomized_seed_sweep(n=10**6, seeds=100):
    results = []
    for seed in range(seeds):
        signal = generate_noise(n, seed=seed)
        result = run_periodicity_test(signal)
        results.append(result["max_zscore"])
    return np.array(results)

def sample_size_ladder(sizes):
    ladder_results = {}
    for n in sizes:
        signal = generate_noise(n, seed=42)
        result = run_periodicity_test(signal)
        ladder_results[n] = result["max_zscore"]
    return ladder_results

def synthetic_amplitude_sweep(n=10**6, amplitudes=None):
    if amplitudes is None:
        amplitudes = np.linspace(0.0, 0.5, 10)

    sweep_results = {}
    base_noise = generate_noise(n, seed=123)

    for amp in amplitudes:
        signal = inject_periodic(base_noise.copy(), amplitude=amp)
        result = run_periodicity_test(signal)
        sweep_results[amp] = result["max_zscore"]

    return sweep_results

def apply_multiple_testing(p_values, method="bonferroni", alpha=0.05):
    if method == "bonferroni":
        return bonferroni_correction(p_values, alpha)
    elif method == "fdr":
        return fdr_correction(p_values, alpha)
    else:
        raise ValueError("Unknown correction method")
