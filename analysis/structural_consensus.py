import numpy as np

def structural_consensus(preds, history, tolerance=1e-6):
    """
    Deterministic consensus over supplied predictions.

    No random value is manufactured when all predictions collapse to
    the current observation. In that case the function returns the
    current observation and explicitly exposes that no non-trivial
    consensus existed.
    """

    preds = np.asarray(preds, dtype=np.float64)
    history = np.asarray(history, dtype=np.float64)

    if len(history) == 0:
        raise ValueError("history must not be empty")

    last = float(history[-1])

    finite = np.isfinite(preds)

    if not np.any(finite):
        return {
            "prediction": last,
            "consensus_available": False,
            "reason": "no_finite_predictions",
        }

    preds = preds[finite]

    deviations = preds - last

    nontrivial = np.abs(deviations) > tolerance

    if not np.any(nontrivial):
        return {
            "prediction": last,
            "consensus_available": False,
            "reason": "all_predictions_trivial",
        }

    preds = preds[nontrivial]
    deviations = deviations[nontrivial]

    # Deterministic magnitude weighting.
    weights = np.abs(deviations) + 1e-12
    weights /= np.sum(weights)

    prediction = float(
        np.sum(preds * weights)
    )

    if not np.isfinite(prediction):
        return {
            "prediction": last,
            "consensus_available": False,
            "reason": "nonfinite_consensus",
        }

    return {
        "prediction": prediction,
        "consensus_available": True,
        "reason": "nontrivial_consensus",
        "contributors": int(len(preds)),
    }
