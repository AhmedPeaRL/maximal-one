import numpy as np

def extract_strong_invariants(series):

    x = np.array(series)

    if len(x) < 50:
        return None

    # normalize
    x = (x - np.mean(x)) / (np.std(x) + 1e-8)

    # derivatives
    dx = np.gradient(x)
    ddx = np.gradient(dx)

    # -------------------------
    # 1. Spectral invariants (🔥 مقاومة للـ phase)
    # -------------------------
    fft = np.fft.rfft(x)
    power = np.abs(fft)**2

    spectral_energy = np.sum(power)
    spectral_entropy = -np.sum((power/np.sum(power)+1e-8) * np.log(power/np.sum(power)+1e-8))

    # -------------------------
    # 2. Rank-order invariants (🔥 مقاومة للـ shuffle)
    # -------------------------
    ranks = np.argsort(np.argsort(x))
    rank_entropy = -np.sum((ranks/np.sum(ranks)+1e-8) * np.log(ranks/np.sum(ranks)+1e-8))

    # -------------------------
    # 3. curvature invariant
    # -------------------------
    curvature = np.mean(np.abs(ddx))

    # -------------------------
    # 4. zero-crossing rate (structure invariant)
    # -------------------------
    zero_cross = np.mean(np.diff(np.sign(x)) != 0)

    return np.array([
        spectral_energy,
        spectral_entropy,
        rank_entropy,
        curvature,
        zero_cross
    ])
