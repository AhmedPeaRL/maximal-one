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
    universality = load("universality_gate.json")
    stability = load("universality_stability.json")
    existential = load("existential_signal.json")

    reasons = []
    score = 0.0

    # -------------------------
    # 1. Strong predictive base
    # -------------------------
    if verdict and verdict.get("score_ratio", 0) > 0.65:
        score += 0.3
    else:
        reasons.append("weak_predictive_core")

    # -------------------------
    # 2. Universality strength
    # -------------------------
    if universality and universality.get("strength", 0) > 0.7:
        score += 0.25
    else:
        reasons.append("weak_universality")

    # -------------------------
    # 3. Stability over time
    # -------------------------
    if stability and stability.get("passed"):
        score += 0.2
    else:
        reasons.append("unstable_universality")

    # -------------------------
    # 4. Existential anchoring
    # -------------------------
    if existential and existential.get("strong_count", 0) >= 3:
        score += 0.15
    else:
        reasons.append("weak_signal_anchor")

    # -------------------------
    # 5. Structural redundancy (anti-fragility)
    # -------------------------
    redundancy = 0

    if verdict and verdict.get("tests_run", 0) >= 3:
        redundancy += 1

    if existential and existential.get("strong_count", 0) >= 3:
        redundancy += 1

    if universality and universality.get("passed"):
        redundancy += 1

    if redundancy >= 3:
        score += 0.1
    else:
        reasons.append("low_redundancy")

    # -------------------------
    # Final irreversibility decision
    # -------------------------
    irreversible = score >= 0.85

    result = {
        "irreversibility_score": score,
        "irreversible": irreversible,
        "confidence": (
            "absolute" if score >= 0.9 else
            "high" if score >= 0.85 else
            "emerging" if score >= 0.7 else
            "weak"
        ),
        "failure_modes": reasons
    }

    (ART / "irreversibility_enforced.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
