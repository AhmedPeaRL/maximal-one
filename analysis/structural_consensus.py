import numpy as np

def structural_consensus(
    preds,
    history,
    tolerance=1e-6,
):
    """
    Deterministic descriptive consensus.

    Consensus is descriptive only.
    No prediction is favored because it is
    farther from the current observation.
    """

    preds = np.asarray(
        preds,
        dtype=np.float64,
    )

    history = np.asarray(
        history,
        dtype=np.float64,
    )

    if len(history) == 0:
        raise ValueError(
            "history must not be empty"
        )

    last = float(history[-1])

    finite = preds[
        np.isfinite(preds)
    ]

    if len(finite) == 0:
        return {
            "prediction": last,
            "consensus_available": False,
            "reason": "no_finite_predictions",
            "contributors": 0,
        }

    deviations = finite - last

    nontrivial = (
        np.abs(deviations)
        > tolerance
    )

    if not np.any(nontrivial):
        return {
            "prediction": last,
            "consensus_available": False,
            "reason": "all_predictions_trivial",
            "contributors": int(len(finite)),
        }

    # Median is deterministic and does not reward
    # extreme predictions.
    prediction = float(
        np.median(finite)
    )

    if not np.isfinite(prediction):
        return {
            "prediction": last,
            "consensus_available": False,
            "reason": "nonfinite_consensus",
            "contributors": int(len(finite)),
        }

    return {
        "prediction": prediction,
        "consensus_available": True,
        "reason": "median_consensus",
        "contributors": int(len(finite)),
        "nontrivial_contributors": int(
            np.sum(nontrivial)
        ),
    }
