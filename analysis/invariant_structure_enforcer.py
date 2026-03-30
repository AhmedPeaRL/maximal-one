import numpy as np

def extract_invariant_structure(series):

    if len(series) < 20:
        return series[-1]

    # 🔥 remove direct temporal bias
    centered = series - np.mean(series)

    # 🔥 spectral signature
    fft = np.fft.rfft(centered)
    magnitude = np.abs(fft)

    # 🔥 normalize
    magnitude = magnitude / (np.sum(magnitude) + 1e-8)

    # 🔥 entropy of spectrum (structure richness)
    entropy = -np.sum(magnitude * np.log(magnitude + 1e-12))

    # 🔥 dominant frequency index
    dominant_idx = np.argmax(magnitude[1:]) + 1

    return {
        "entropy": entropy,
        "dominant_freq": dominant_idx,
        "energy": np.sum(centered**2)
    }


def invariant_prediction(history):

    features = extract_invariant_structure(history)

    base = history[-1]

    # 🔥 structure-driven modulation
    modulation = (
        0.2 * features["entropy"] +
        0.1 * features["dominant_freq"] / len(history) +
        0.1 * np.sqrt(features["energy"])
    )

    return float(base + modulation)
