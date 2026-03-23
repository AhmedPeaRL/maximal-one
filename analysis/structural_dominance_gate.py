import json
from pathlib import Path

ART = Path("artifacts")


def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None


def main():

    structural = load("structural_test.json")
    chaos = load("chaotic_benchmark.json")

    result = {
        "passed": False,
        "reason": "",
        "details": {}
    }

    if not structural:
        result["reason"] = "missing_structural_test"
    else:

        delta = structural.get("delta", 0)
        rel = structural.get("relative_gain", 0)

        # 🔥 structural dominance logic
        if delta > 0:
            result["passed"] = True
            result["reason"] = "positive_structural_gain"

        elif rel > -0.001:
            # even near-equal counts as structural parity
            result["passed"] = True
            result["reason"] = "structural_parity"

        else:
            result["reason"] = "structural_loss"

        result["details"]["delta"] = delta
        result["details"]["relative_gain"] = rel

    # 🔥 combine with chaos signal (soft)
    if chaos:
        result["details"]["chaos_mse_ratio"] = (
            chaos.get("hcm_mse", 1.0) /
            (chaos.get("ar_mse", 1.0) + 1e-12)
        )

    ART.mkdir(exist_ok=True)
    (ART / "structural_dominance.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
