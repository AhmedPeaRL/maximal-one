import json
import pathlib
import time

ART = pathlib.Path("artifacts")

def wait_for_file(name, timeout=20):
    path = ART / name
    start = time.time()
    while time.time() - start < timeout:
        if path.exists():
            return json.loads(path.read_text())
        time.sleep(1)
    return None


def main():
    verdict = wait_for_file("global_verdict.json")
    universality = wait_for_file("universality_stability.json")

    if not verdict or not universality:
        result = {
            "passed": False,
            "reason": "missing core signals (timeout)"
        }
        print(json.dumps(result))
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
    if ratio > 0.65 and stable:
        confidence = "high"
    elif ratio > 0.55:
        confidence = "moderate"

    result = {
        "passed": irreversible,
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
