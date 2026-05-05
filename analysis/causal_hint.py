import numpy as np

def spectral_energy_distribution(series):
    series = np.asarray(series, dtype=np.float64)
    series = series - np.mean(series)

    fft_vals = np.fft.rfft(series)
    power = np.abs(fft_vals) ** 2

    total_energy = np.sum(power)
    low_freq_energy = np.sum(power[:len(power)//4])
    high_freq_energy = np.sum(power[len(power)//4:])

    return {
        "low_freq_ratio": float(low_freq_energy / total_energy),
        "high_freq_ratio": float(high_freq_energy / total_energy)
    }


def interpret_structure(ratios):
    if ratios["low_freq_ratio"] > 0.7:
        return "long_range_dominance"
    elif ratios["high_freq_ratio"] > 0.7:
        return "noise_like"
    else:
        return "mixed_structure"
