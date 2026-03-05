import numpy as np

def spectral_entropy(x):
    fft = np.abs(np.fft.fft(x))**2
    p = fft / np.sum(fft)
    return -np.sum(p * np.log(p + 1e-12))

def adaptive_attractor_strength(x):
    return np.std(x) / (np.mean(np.abs(x)) + 1e-9)

def psi(x):
    return spectral_entropy(x) * adaptive_attractor_strength(x)

def test_invariance():
    x = np.random.RandomState(42).normal(size=2048)
    y = np.roll(x, 50)  # phase shift

    psi_x = psi(x)
    psi_y = psi(y)

    assert abs(psi_x - psi_y) < 1e-6, "Observable not phase invariant"

if __name__ == "__main__":
    test_invariance()
    print("Observable invariant ✓")
