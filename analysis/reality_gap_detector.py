import json
from pathlib import Path

ART = Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None


def main():
    verdict = load("global_verdict.json")
    blind = load("external_validation.json")
    irr = load("irreversibility_enforced.json")

    gaps = []

    # 1. Predictive strength gap
    if verdict and verdict.get("final_score", 0) < 0.75:
        gaps.append("predictive_power_not_dominant")

    # 2. Blind validation weakness
    if blind and abs(blind.get("blind_mean", 0.5) - 0.5) < 0.01:
        gaps.append("no_signal_beyond_randomness")

    # 3. Irreversibility inflation
    if irr and irr.get("confidence") == "absolute":
        if verdict and verdict.get("final_score", 0) < 0.7:
            gaps.append("irreversibility_overstated")

    result = {
        "reality_check_passed": len(gaps) == 0,
        "gaps": gaps,
        "severity": (
            "none" if len(gaps) == 0 else
            "moderate" if len(gaps) == 1 else
            "critical"
        )
    }

    (ART / "reality_gap.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
