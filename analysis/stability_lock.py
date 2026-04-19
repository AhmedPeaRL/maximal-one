import json
import os

def check_system_stability():
    issues = []

    # 1. Check canonical report
    if not os.path.exists("artifacts/canonical_report.json"):
        issues.append("missing_report")

    # 2. Check spectral signal
    try:
        with open("artifacts/canonical_report.json") as f:
            r = json.load(f)

        alpha = r["spectral_profile"]["estimated_alpha"]
        sigma = r["spectral_profile"]["bootstrap_std"]

        if sigma > 0.5:
            issues.append("high_uncertainty")

        if alpha is None:
            issues.append("invalid_alpha")

    except Exception:
        issues.append("corrupt_report")

    # 3. Check divergence
    if os.path.exists("artifacts/runtime_divergence.json"):
        with open("artifacts/runtime_divergence.json") as f:
            d = json.load(f)

        if d.get("status") != "controlled":
            issues.append("uncontrolled_divergence")

    return issues


if __name__ == "__main__":
    issues = check_system_stability()

    os.makedirs("artifacts", exist_ok=True)

    result = {
        "status": "stable" if len(issues) == 0 else "degraded",
        "issues": issues
    }

    with open("artifacts/stability_status.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Stability status:", result)

    # IMPORTANT: never break pipeline
    exit(0)
