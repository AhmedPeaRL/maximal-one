import numpy as np

# -----------------------------
# TRUE FORWARD SCORING (CRITICAL)
# -----------------------------

def forward_projection_score(history, candidate):

    history = np.array(history)

    # simulate forward consistency
    trend = np.mean(np.diff(history[-10:]))
    curvature = np.mean(np.gradient(np.gradient(history[-10:])))

    expected = history[-1] + trend + 0.5 * curvature

    # deviation from expected forward dynamic
    deviation = abs(candidate - expected)

    # stability penalty
    noise = np.std(history[-20:])
    stability_penalty = abs(candidate - history[-1]) / (noise + 1e-8)

    return deviation + 0.3 * stability_penalty


# -----------------------------
# TRUE SELECTION CORE
# -----------------------------

def select_prediction(history, candidates):

    if not candidates:
        return float(history[-1])

    scores = []

    for c in candidates:
        if not np.isfinite(c):
            continue

        s = forward_projection_score(history, c)
        scores.append((s, c))

    if not scores:
        return float(history[-1])

    # 🔥 pick MOST forward-consistent (NOT closest to past)
    best = min(scores, key=lambda x: x[0])[1]

    return float(best)
