import json
import pathlib

ART = pathlib.Path("artifacts")

def load(name):
    p = ART / name
    if p.exists():
        return json.loads(p.read_text())
    return None


def main():
    verdict = load("global_verdict.json")
    universality = load("universality_stability.json")

    if not verdict or not universality:
        print(json.dumps({
            "passed": False,
            "reason": "missing core signals"
        }))
        return

    score = verdict.get("final_score", 0)
    ratio = verdict.get("score_ratio", 0)
    stable = universality.get("passed", False)

    # -----------------------------
    # Irreversibility logic
    # -----------------------------
    irreversible = (
    ratio > 0.6 and
    score > 0.55 and
    stable
    )

    confidence = "low"
    if ratio > 0.7 and stable:
        confidence = "high"
    elif ratio > 0.6:
        confidence = "moderate"

    result = {
        "irreversible": irreversible,
        "confidence": confidence,
        "score_ratio": ratio,
        "final_score": score,
        "universality_stable": stable
    }

    ART.mkdir(exist_ok=True)
    (ART / "irreversibility.json").write_text(json.dumps(result, indent=2))

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
