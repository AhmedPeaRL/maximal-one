import numpy as np

class HCMCrossScalePredictor:

    def predict(self, history):
        if len(history) < 20:
            return history[-1]

        h = np.array(history)

        # multi-scale smoothing
        scales = [2, 4, 8]

        preds = []

        for s in scales:
            if len(h) < s + 2:
                continue

            smoothed = np.convolve(h, np.ones(s)/s, mode='valid')

            if len(smoothed) < 2:
                continue

            # local trend
            delta = smoothed[-1] - smoothed[-2]

            preds.append(smoothed[-1] + delta)

        if not preds:
            return history[-1]

        return float(np.mean(preds))
