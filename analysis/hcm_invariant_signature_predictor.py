import numpy as np

class HCMInvariantSignaturePredictor:
    """
    True invariant extractor:
    - ignores time order
    - learns distributional signature
    """

    def predict(self, history):

        if len(history) < 50:
            return history[-1]

        x = np.array(history[-200:])

        # --- invariant features ---
        mean = np.mean(x)
        std = np.std(x)
        skew = np.mean((x - mean)**3) / (std**3 + 1e-8)

        # --- spectral signature ---
        fft = np.fft.rfft(x)
        power = np.abs(fft)

        dominant_freq = np.argmax(power[1:]) + 1

        # --- prediction ---
        # NOT time dependent
        pred = mean + 0.3 * std * np.sign(skew)

        return float(pred)
