import random
import math
import json
import cmath

def deterministic_sequence(seed, N):
    random.seed(seed)
    return [random.random() - 0.5 for _ in range(N)]

def dft_energy_spectrum(data):
    N = len(data)
    spectrum = []

    for k in range(N):
        s = 0
        for n in range(N):
            s += data[n] * cmath.exp(-2j * math.pi * k * n / N)
        spectrum.append(abs(s)**2)

    total_energy = sum(spectrum)
    normalized = [x / total_energy for x in spectrum]

    return normalized

def spectral_deviation(seed, N):
    data = deterministic_sequence(seed, N)
    spectrum = dft_energy_spectrum(data)

    expected = 1 / len(spectrum)
    deviation = max(abs(s - expected) for s in spectrum)

    return {
        "seed": seed,
        "max_spectral_deviation": deviation
    }

if __name__ == "__main__":
    result = spectral_deviation(seed=42, N=128)
    print(json.dumps(result, indent=2))
