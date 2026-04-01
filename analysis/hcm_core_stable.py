import numpy as np

def stable_structure_signal(history):
    recent = np.array(history[-20:])
    
    drift = np.mean(np.diff(recent))
    volatility = np.std(recent)
    curvature = np.mean(np.abs(np.gradient(np.gradient(recent))))
    
    return drift, volatility, curvature


def invariant_anchor(history):
    return float(history[-1])


def stable_predict(history):

    base = invariant_anchor(history)

    drift, vol, curv = stable_structure_signal(history)

    # 🔥 stability score
    stability = vol / (abs(base) + 1e-8)

    # 🔥 deterministic regime selection
    if stability < 0.05:
        # stable regime → follow drift
        return float(base + drift)

    elif stability < 0.2:
        # semi-chaotic → damped response
        return float(base + 0.5 * drift + 0.2 * curv)

    else:
        # chaotic regime → anchor-preserving correction
        return float(base + 0.3 * drift + 0.3 * curv)
