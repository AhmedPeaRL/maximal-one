import numpy as np
from analysis.invariant_core_v2 import extract_strong_invariants

class InvariantLatentPredictor:

    def __init__(self, window=30):
        self.window = window

    def build_latent_trajectory(self, history):
        h = np.array(history)

        traj = []

        for i in range(len(h) - self.window):
            seg = h[i:i+self.window]
            inv = extract_strong_invariants(seg)

            if inv is not None:
                traj.append(inv)

        if len(traj) < 5:
            return None

        return np.array(traj)

    def predict(self, history):

        if len(history) < self.window + 10:
            return history[-1]

        traj = self.build_latent_trajectory(history)

        if traj is None:
            return history[-1]

        current = traj[-1]

        # nearest neighbors in invariant space
        dists = np.linalg.norm(traj[:-1] - current, axis=1)

        k = min(5, len(dists))
        idx = np.argsort(dists)[:k]

        # future invariant drift
        deltas = []

        for i in idx:
            if i+1 < len(traj):
                deltas.append(traj[i+1] - traj[i])

        if not deltas:
            return history[-1]

        delta = np.mean(deltas, axis=0)

        next_inv = current + delta

        # 🔥 project back to signal space
        h = np.array(history[-self.window:])
        scale = np.std(h)

        projection = (
            0.3 * next_inv[1] +  # entropy
            0.3 * next_inv[2] +  # rank
            0.2 * next_inv[3] +  # curvature
            0.2 * next_inv[4]    # zero-cross
        )

        return float(h[-1] + projection * scale)
