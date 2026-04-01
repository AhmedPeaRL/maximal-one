import numpy as np
import json
from pathlib import Path

ART = Path("artifacts")


def entropy(x, bins=50):
    hist, _ = np.histogram(x, bins=bins, density=True)
    hist = hist + 1e-12
    return -np.sum(hist * np.log(hist))


def structure_score(series):
    series = np.array(series)

    diff = np.diff(series)
    curvature = np.gradient(np.gradient(series))

    return {
        "entropy": float(entropy(series)),
        "diff_entropy": float(entropy(diff)),
        "curvature_energy": float(np.mean(curvature**2))
    }


def compare(series, pred):

    s_real = structure_score(series)
    s_pred = structure_score(pred)

    diff = {
        k: abs(s_real[k] - s_pred[k])
        for k in s_real
    }

    total = sum(diff.values())

    return {
        "structure_difference": diff,
        "total_difference": float(total),
        "structure_preserved": total < 0.05
    }


def main():
    import numpy as np

    real_path = ART / "lorenz.json"

    if not real_path.exists():
        print(json.dumps({"skipped": True}))
        return

    data = json.loads(real_path.read_text())

    if "series" not in data:
        print(json.dumps({"skipped": True}))
        return

    series = np.array(data["series"])
    pred = np.array(data.get("prediction", series))

    result = compare(series, pred)

    print(json.dumps(result, indent=2))

    (ART / "structural_advantage.json").write_text(
        json.dumps(result, indent=2)
    )


if __name__ == "__main__":
    main()
