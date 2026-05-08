import json
import numpy as np

REPORT_PATH = "artifacts/canonical_report.json"


def main():

    report = json.load(
        open(REPORT_PATH)
    )

    alpha = (
        report["spectral_profile"]
        ["estimated_alpha"]
    )

    print(
        f"Observed alpha: {alpha}"
    )

    if not np.isfinite(alpha):
        raise SystemExit(
            "❌ alpha is not finite"
        )

    # detect estimator saturation
    if alpha >= 4.95:
        raise SystemExit(
            "❌ alpha saturation detected"
        )

    if alpha <= 0.05:
        raise SystemExit(
            "❌ alpha floor saturation detected"
        )

    print(
        "✅ Saturation guard passed"
    )


if __name__ == "__main__":
    main()
